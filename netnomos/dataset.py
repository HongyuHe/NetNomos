from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import numpy as np
import pandas as pd

from netnomos.logging_utils import get_logger
from netnomos.specs import (
    DatasetSpec,
    DerivedOperation,
    DerivedVariableSpec,
    FieldRole,
    FieldSpec,
    MappingRuleMode,
    PreprocessKind,
    SourceType,
    ValueType,
)


CTX_PATTERNS = [
    re.compile(r"^(?P<base>.+)_ctx(?P<index>\d+)$"),
    re.compile(r"^(?P<base>.+)Ctx(?P<index>\d+)$"),
]
log = get_logger("dataset")


@dataclass(slots=True)
class PreparedDataset:
    spec: DatasetSpec
    source_type: SourceType
    dataframe: pd.DataFrame
    field_specs: dict[str, FieldSpec]
    value_catalog: dict[str, list[Any]]
    derived_provenance: dict[str, dict[str, Any]]
    context_families: dict[str, list[str]]
    configured_exclude_fields: list[str]
    excluded_fields: dict[str, str]

    @property
    def effective_excluded_fields(self) -> list[str]:
        seen = set(self.configured_exclude_fields)
        return [
            *self.configured_exclude_fields,
            *(name for name in self.excluded_fields if name not in seen),
        ]


def prepare_dataset(spec: DatasetSpec, input_path: str | Path | None = None, limit: int | None = None) -> PreparedDataset:
    source_type, path = resolve_source(spec, input_path)
    log.info("Loading dataset '%s' from %s as %s", spec.name, path, source_type.value)
    if source_type == SourceType.CSV:
        read_options = dict(spec.source.csv_read_options)
        if limit is not None:
            read_options["nrows"] = limit
        frame = pd.read_csv(path, **read_options)
    else:
        frame = read_pcap(path, limit=limit)

    frame = apply_source_renames(frame, spec)
    frame = apply_preprocessing(frame, spec)
    frame, configured_exclude_fields = apply_field_selection(frame, spec)
    frame, excluded_fields = drop_incomplete_columns(frame)
    validate_required_columns(frame, spec, excluded_fields)

    field_specs = initial_field_specs(spec, frame)
    if spec.context_window is not None:
        frame, field_specs = apply_context_windows(frame, field_specs, spec)

    frame, derived_provenance, field_specs = apply_derived_variables(frame, field_specs, spec.derived_variables)
    field_specs = enrich_context_families(field_specs, frame.columns)
    value_catalog = build_value_catalog(frame, field_specs)
    field_specs = attach_domains(field_specs, value_catalog)
    context_families = build_context_families(field_specs)
    return PreparedDataset(
        spec=spec,
        source_type=source_type,
        dataframe=frame,
        field_specs=field_specs,
        value_catalog=value_catalog,
        derived_provenance=derived_provenance,
        context_families=context_families,
        configured_exclude_fields=configured_exclude_fields,
        excluded_fields=excluded_fields,
    )


def resolve_source(spec: DatasetSpec, input_path: str | Path | None = None) -> tuple[SourceType, Path]:
    path = Path(input_path or spec.source.path or "")
    if spec.source.type == SourceType.AUTO:
        source_type = infer_source_type(path)
        if source_type is None:
            raise ValueError(
                "Dataset source.type='auto' requires a path ending in .csv, .pcap, .pcapng, or .cap."
            )
        return source_type, path
    return spec.source.type, path


def infer_source_type(path: Path) -> SourceType | None:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return SourceType.CSV
    if suffix in {".pcap", ".pcapng", ".cap"}:
        return SourceType.PCAP
    return None


def apply_source_renames(frame: pd.DataFrame, spec: DatasetSpec) -> pd.DataFrame:
    rename_map = {
        field.source_name: field.name
        for field in spec.fields
        if field.source_name and field.source_name in frame.columns and field.source_name != field.name
    }
    if rename_map:
        frame = frame.rename(columns=rename_map)
    return frame


def apply_preprocessing(frame: pd.DataFrame, spec: DatasetSpec) -> pd.DataFrame:
    for step in spec.preprocessing:
        if step.kind == PreprocessKind.RENAME:
            frame = frame.rename(columns=step.mapping)
        elif step.kind == PreprocessKind.DROP:
            frame = frame.drop(columns=[c for c in step.columns if c in frame.columns], errors="ignore")
        elif step.kind == PreprocessKind.CAST:
            for column in step.columns:
                if column in frame.columns:
                    frame[column] = frame[column].astype(step.dtype)
        elif step.kind == PreprocessKind.PARSE_HEX:
            for column in step.columns:
                if column in frame.columns:
                    frame[column] = frame[column].apply(parse_hex_value)
        elif step.kind == PreprocessKind.FILLNA:
            for column in step.columns:
                if column in frame.columns:
                    frame[column] = frame[column].fillna(step.value)
        elif step.kind == PreprocessKind.MAP_VALUES:
            for column in step.columns:
                if column in frame.columns:
                    mapped = frame[column].map(step.mapping).fillna(frame[column])
                    frame[resolve_preprocess_target(step, column)] = mapped
        elif step.kind == PreprocessKind.MAP_RULES:
            for column in step.columns:
                if column in frame.columns:
                    mapped = frame[column].apply(lambda value: apply_mapping_rules(value, step.rules))
                    frame[resolve_preprocess_target(step, column)] = mapped
        elif step.kind == PreprocessKind.FILTER_EQUALS:
            for column in step.columns:
                if column in frame.columns:
                    frame = frame.loc[frame[column] == step.value].copy()
        elif step.kind == PreprocessKind.FILTER_IN:
            for column in step.columns:
                if column in frame.columns:
                    frame = frame.loc[frame[column].isin(step.value)].copy()
        elif step.kind == PreprocessKind.FILTER_PRESENT:
            for column in step.columns:
                if column in frame.columns:
                    frame = frame.loc[is_present_value_series(frame[column])].copy()
        elif step.kind == PreprocessKind.SORT:
            by = step.by or step.columns
            if by:
                frame = frame.sort_values(by=by)
        else:
            raise ValueError(f"Unsupported preprocessing step: {step.kind}")
    return frame.reset_index(drop=True)


def apply_field_selection(frame: pd.DataFrame, spec: DatasetSpec) -> tuple[pd.DataFrame, list[str]]:
    selected = list(frame.columns)
    if spec.include_fields:
        missing = [name for name in spec.include_fields if name not in frame.columns]
        if missing:
            raise ValueError(f"Included fields not found after preprocessing: {missing}")
        selected = [name for name in spec.include_fields if name in frame.columns]
    configured_exclude_fields: list[str] = []
    if spec.exclude_fields:
        exclude_set = set(spec.exclude_fields)
        configured_exclude_fields = [name for name in frame.columns if name in exclude_set]
        selected = [name for name in selected if name not in exclude_set]
    return frame[selected].copy(), configured_exclude_fields


def initial_field_specs(spec: DatasetSpec, frame: pd.DataFrame) -> dict[str, FieldSpec]:
    resolved = {field.name: field for field in spec.fields if field.name in frame.columns}
    for column in frame.columns:
        if column not in resolved:
            resolved[column] = FieldSpec(name=column, value_type=infer_value_type(frame[column]))
    return resolved


def infer_value_type(series: pd.Series) -> ValueType:
    if pd.api.types.is_bool_dtype(series):
        return ValueType.BOOLEAN
    if pd.api.types.is_integer_dtype(series):
        return ValueType.INTEGER
    if pd.api.types.is_float_dtype(series):
        return ValueType.REAL
    nunique = series.nunique(dropna=True)
    if nunique <= 32:
        return ValueType.CATEGORICAL
    return ValueType.STRING


def apply_context_windows(
    frame: pd.DataFrame,
    field_specs: dict[str, FieldSpec],
    spec: DatasetSpec,
) -> tuple[pd.DataFrame, dict[str, FieldSpec]]:
    ctx = spec.context_window
    assert ctx is not None
    ordered = frame.sort_values(by=ctx.partition_by + ctx.order_by if ctx.order_by else ctx.partition_by or frame.columns[:1].tolist())
    groups = [(None, ordered)] if not ctx.partition_by else list(ordered.groupby(ctx.partition_by, sort=False))
    rows: list[dict[str, Any]] = []
    for _, group in groups:
        group = group.reset_index(drop=True)
        for start in range(0, len(group) - ctx.size + 1, ctx.stride):
            window = group.iloc[start:start + ctx.size]
            row: dict[str, Any] = {}
            for offset in range(ctx.size):
                entry = window.iloc[offset]
                for column, value in entry.items():
                    row[ctx.column_template.format(name=column, index=offset)] = value
            rows.append(row)
    new_specs: dict[str, FieldSpec] = {}
    for name, base_field in field_specs.items():
        for offset in range(ctx.size):
            new_name = ctx.column_template.format(name=name, index=offset)
            new_specs[new_name] = base_field.model_copy(
                update={
                    "name": new_name,
                    "context_family": name,
                    "context_index": offset,
                    "roles": list(dict.fromkeys([*base_field.roles, FieldRole.WINDOW])),
                }
            )
    windowed = pd.DataFrame(rows, columns=list(new_specs))
    return windowed, new_specs


def apply_derived_variables(
    frame: pd.DataFrame,
    field_specs: dict[str, FieldSpec],
    derived_specs: list[DerivedVariableSpec],
) -> tuple[pd.DataFrame, dict[str, dict[str, Any]], dict[str, FieldSpec]]:
    provenance: dict[str, dict[str, Any]] = {}
    for derived in derived_specs:
        missing = [
            name
            for name in [*derived.inputs, *( [derived.numerator] if derived.numerator else [] ), *( [derived.denominator] if derived.denominator else [] )]
            if name not in frame.columns
        ]
        if missing:
            raise ValueError(
                f"Derived variable '{derived.name}' references unavailable columns: {sorted(set(missing))}"
            )
        frame[derived.name] = compute_derived_column(frame, derived)
        field_specs[derived.name] = FieldSpec(
            name=derived.name,
            value_type=derived.value_type,
            roles=derived.roles,
        )
        provenance[derived.name] = derived.model_dump(mode="json")
    return frame, provenance, field_specs


def compute_derived_column(frame: pd.DataFrame, spec: DerivedVariableSpec) -> pd.Series:
    if spec.operation == DerivedOperation.COPY:
        return frame[spec.inputs[0]]
    if spec.operation == DerivedOperation.SUM:
        return frame[spec.inputs].sum(axis=1)
    if spec.operation == DerivedOperation.MIN:
        return frame[spec.inputs].min(axis=1)
    if spec.operation == DerivedOperation.MAX:
        return frame[spec.inputs].max(axis=1)
    if spec.operation == DerivedOperation.AVG:
        return frame[spec.inputs].mean(axis=1)
    if spec.operation == DerivedOperation.STD:
        return frame[spec.inputs].std(axis=1, ddof=0)
    if spec.operation == DerivedOperation.DIFF:
        return frame[spec.inputs[0]] - frame[spec.inputs[1]]
    if spec.operation == DerivedOperation.RATIO:
        denom = frame[spec.denominator or spec.inputs[1]].replace(0, np.nan)
        return frame[spec.numerator or spec.inputs[0]] / denom
    if spec.operation == DerivedOperation.COUNT_NONZERO:
        return (frame[spec.inputs] != 0).sum(axis=1)
    if spec.operation == DerivedOperation.EXISTS:
        return (frame[spec.inputs] != 0).any(axis=1).astype(int)
    if spec.operation == DerivedOperation.FORALL:
        return (frame[spec.inputs] != 0).all(axis=1).astype(int)
    raise ValueError(f"Unsupported derived operation: {spec.operation}")


def build_value_catalog(frame: pd.DataFrame, field_specs: dict[str, FieldSpec]) -> dict[str, list[Any]]:
    catalog: dict[str, list[Any]] = {}
    for name, field in field_specs.items():
        if name not in frame.columns:
            continue
        if field.domain is not None:
            catalog[name] = list(field.domain)
            continue
        series = frame[name].dropna()
        if field.value_type in {ValueType.CATEGORICAL, ValueType.STRING, ValueType.BOOLEAN}:
            catalog[name] = sorted(series.unique().tolist())
        else:
            catalog[name] = sorted(series.drop_duplicates().tolist())
    return catalog


def attach_domains(field_specs: dict[str, FieldSpec], value_catalog: dict[str, list[Any]]) -> dict[str, FieldSpec]:
    for name, field in list(field_specs.items()):
        if field.domain is not None or name not in value_catalog:
            continue
        if field.value_type in {ValueType.CATEGORICAL, ValueType.STRING, ValueType.BOOLEAN}:
            field_specs[name] = field.model_copy(update={"domain": value_catalog[name]})
    return field_specs


def apply_mapping_rules(value: Any, rules: list[Any]) -> Any:
    default_value = value
    for rule in rules:
        if rule.mode == MappingRuleMode.DEFAULT:
            default_value = rule.output
            continue
        if rule.mode == MappingRuleMode.EQUALS and value == rule.value:
            return rule.output
        if rule.mode == MappingRuleMode.IN and value in set(rule.values):
            return rule.output
        if rule.mode == MappingRuleMode.PREFIX and isinstance(value, str) and isinstance(rule.value, str):
            if value.startswith(rule.value):
                return rule.output
        if rule.mode == MappingRuleMode.REGEX and isinstance(rule.value, str):
            if re.search(rule.value, str(value)):
                return rule.output
        if rule.mode == MappingRuleMode.RANGE and value is not None:
            try:
                numeric = float(value)
            except (TypeError, ValueError):
                continue
            lower_ok = True
            upper_ok = True
            if rule.lower is not None:
                lower_ok = numeric >= rule.lower if rule.inclusive_lower else numeric > rule.lower
            if rule.upper is not None:
                upper_ok = numeric <= rule.upper if rule.inclusive_upper else numeric < rule.upper
            if lower_ok and upper_ok:
                return rule.output
    return default_value


def parse_hex_value(value: Any) -> Any:
    if value is None or pd.isna(value):
        return np.nan
    if isinstance(value, (int, np.integer)):
        return int(value)
    if isinstance(value, (float, np.floating)) and float(value).is_integer():
        return int(value)
    text = str(value).strip()
    if not text:
        return np.nan
    if text.lower() in {"nan", "none"}:
        return np.nan
    if text.lower().startswith("0x"):
        return int(text, 16)
    return int(text)


def is_present_value_series(series: pd.Series) -> pd.Series:
    mask = series.notna()
    if pd.api.types.is_string_dtype(series) or series.dtype == object:
        stripped = series.astype("string").str.strip()
        mask = mask & stripped.ne("")
    return mask


def drop_incomplete_columns(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, str]]:
    excluded_fields: dict[str, str] = {}
    for column in frame.columns:
        reasons: list[str] = []
        series = frame[column]
        if series.isna().any():
            reasons.append("contains NaN values")
        if (pd.api.types.is_string_dtype(series) or series.dtype == object) and series.astype("string").str.strip().eq("").any():
            reasons.append("contains empty values")
        if reasons:
            excluded_fields[column] = " and ".join(reasons)
    if excluded_fields:
        details = ", ".join(f"{name} ({reason})" for name, reason in sorted(excluded_fields.items()))
        log.warning("Excluding incomplete columns during dataset loading: %s", details)
        frame = frame.drop(columns=list(excluded_fields))
    return frame, excluded_fields


def validate_required_columns(frame: pd.DataFrame, spec: DatasetSpec, excluded_fields: dict[str, str]) -> None:
    required: set[str] = set()
    if spec.context_window is not None:
        required.update(spec.context_window.partition_by)
        required.update(spec.context_window.order_by)
    missing = sorted(name for name in required if name not in frame.columns)
    if not missing:
        return
    details = ", ".join(
        f"{name} ({excluded_fields[name]})" if name in excluded_fields else name
        for name in missing
    )
    raise ValueError(f"Required dataset columns are unavailable after loading: {details}")


def resolve_preprocess_target(step: Any, column: str) -> str:
    if step.target_column is None:
        return column
    if len(step.columns) != 1:
        raise ValueError("`target_column` requires exactly one source column in the preprocessing step.")
    return step.target_column


def build_context_families(field_specs: dict[str, FieldSpec]) -> dict[str, list[str]]:
    families: dict[str, list[tuple[int, str]]] = {}
    for field in field_specs.values():
        if field.context_family is None or field.context_index is None:
            continue
        families.setdefault(field.context_family, []).append((field.context_index, field.name))
    return {family: [name for _, name in sorted(entries)] for family, entries in families.items()}


def enrich_context_families(field_specs: dict[str, FieldSpec], columns: Any) -> dict[str, FieldSpec]:
    for column in columns:
        if column not in field_specs:
            continue
        field = field_specs[column]
        if field.context_family is not None:
            continue
        for pattern in CTX_PATTERNS:
            match = pattern.match(column)
            if match is None:
                continue
            field_specs[column] = field.model_copy(
                update={
                    "context_family": match.group("base"),
                    "context_index": int(match.group("index")),
                    "roles": list(dict.fromkeys([*field.roles, FieldRole.WINDOW])),
                }
            )
            break
    return field_specs


def read_pcap(path: Path, limit: int | None = None) -> pd.DataFrame:
    from scapy.all import PcapReader
    from scapy.layers.inet import IP, TCP, UDP
    from scapy.layers.l2 import Ether

    rows: list[dict[str, Any]] = []
    with PcapReader(str(path)) as reader:
        for index, packet in enumerate(reader, start=1):
            if limit is not None and index > limit:
                break
            row: dict[str, Any] = {
                "frame.number": index,
                "frame.time_epoch": float(getattr(packet, "time", 0.0)),
                "frame.len": len(packet),
                "eth.src": None,
                "eth.dst": None,
                "ip.version": None,
                "ip.hdr_len": None,
                "ip.len": None,
                "ip.id": None,
                "ip.flags": None,
                "ip.frag_offset": None,
                "ip.ttl": None,
                "ip.proto": None,
                "ip.src": None,
                "ip.dst": None,
                "tcp.srcport": None,
                "tcp.dstport": None,
                "tcp.hdr_len": None,
                "tcp.flags": None,
                "tcp.len": None,
                "tcp.seq": None,
                "tcp.ack": None,
                "tcp.urgent_pointer": None,
                "tcp.window_size_value": None,
                "tcp.window_size": None,
                "tcp.options.timestamp.tsval": None,
                "tcp.options.timestamp.tsecr": None,
                "udp.srcport": None,
                "udp.dstport": None,
                "udp.length": None,
                "_ws.col.protocol": None,
            }
            if Ether in packet:
                row["eth.src"] = packet[Ether].src
                row["eth.dst"] = packet[Ether].dst
            if IP in packet:
                ip = packet[IP]
                row["ip.version"] = int(ip.version)
                row["ip.hdr_len"] = int(ip.ihl) * 4 if ip.ihl is not None else None
                row["ip.len"] = int(ip.len) if ip.len is not None else None
                row["ip.id"] = int(ip.id)
                row["ip.flags"] = int(ip.flags.value)
                row["ip.frag_offset"] = int(ip.frag)
                row["ip.ttl"] = int(ip.ttl)
                row["ip.proto"] = int(ip.proto)
                row["ip.src"] = ip.src
                row["ip.dst"] = ip.dst
                row["_ws.col.protocol"] = "IP"
            if TCP in packet:
                tcp = packet[TCP]
                row["tcp.srcport"] = int(tcp.sport)
                row["tcp.dstport"] = int(tcp.dport)
                row["tcp.hdr_len"] = int(tcp.dataofs) * 4 if tcp.dataofs is not None else None
                row["tcp.flags"] = int(tcp.flags.value)
                row["tcp.len"] = len(bytes(tcp.payload))
                row["tcp.seq"] = int(tcp.seq)
                row["tcp.ack"] = int(tcp.ack)
                row["tcp.urgent_pointer"] = int(tcp.urgptr)
                row["tcp.window_size_value"] = int(tcp.window)
                row["tcp.window_size"] = int(tcp.window)
                row["_ws.col.protocol"] = "TCP"
                for option_name, option_value in tcp.options or []:
                    if option_name != "Timestamp":
                        continue
                    if isinstance(option_value, tuple) and len(option_value) == 2:
                        row["tcp.options.timestamp.tsval"] = int(option_value[0])
                        row["tcp.options.timestamp.tsecr"] = int(option_value[1])
            if UDP in packet:
                udp = packet[UDP]
                row["udp.srcport"] = int(udp.sport)
                row["udp.dstport"] = int(udp.dport)
                row["udp.length"] = int(udp.len)
                row["_ws.col.protocol"] = "UDP"
            rows.append(row)
    return pd.DataFrame(rows)
