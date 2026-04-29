from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class SourceType(str, Enum):
    AUTO = "auto"
    CSV = "csv"
    PCAP = "pcap"


class ValueType(str, Enum):
    INTEGER = "integer"
    REAL = "real"
    CATEGORICAL = "categorical"
    BOOLEAN = "boolean"
    STRING = "string"


class FieldRole(str, Enum):
    SRC = "src"
    DST = "dst"
    PROTO = "proto"
    TIME = "time"
    SEQUENCE = "sequence"
    MEASUREMENT = "measurement"
    IDENTIFIER = "identifier"
    WINDOW = "window"
    COUNT = "count"
    SIZE = "size"
    FLAG = "flag"
    DERIVED = "derived"


class Comparator(str, Enum):
    EQ = "="
    NE = "!="
    GT = ">"
    GE = ">="
    LT = "<"
    LE = "<="


class ConstantKind(str, Enum):
    ASSIGNMENT = "assignment"
    SCALAR = "scalar"
    LIMIT = "limit"
    ADDITION = "addition"


class Aggregator(str, Enum):
    MIN = "min"
    MAX = "max"
    SUM = "sum"
    AVG = "avg"
    COUNT_NONZERO = "count_nonzero"
    EXISTS = "exists"
    FORALL = "forall"


class PreprocessKind(str, Enum):
    RENAME = "rename"
    DROP = "drop"
    CAST = "cast"
    PARSE_HEX = "parse_hex"
    FILLNA = "fillna"
    MAP_VALUES = "map_values"
    MAP_RULES = "map_rules"
    FILTER_EQUALS = "filter_equals"
    FILTER_IN = "filter_in"
    FILTER_PRESENT = "filter_present"
    SORT = "sort"


class DerivedOperation(str, Enum):
    COPY = "copy"
    SUM = "sum"
    MIN = "min"
    MAX = "max"
    AVG = "avg"
    STD = "std"
    DIFF = "diff"
    RATIO = "ratio"
    COUNT_NONZERO = "count_nonzero"
    EXISTS = "exists"
    FORALL = "forall"


class LearnerKind(str, Enum):
    HITTING_SET = "hitting-set"
    TREE = "tree"


class HittingSetBackend(str, Enum):
    AUTO = "auto"
    NATIVE = "native"
    PYTHON = "python"


class SourceSpec(StrictModel):
    type: SourceType
    path: str | None = None
    csv_read_options: dict[str, Any] = Field(default_factory=dict)


class BoundsSpec(StrictModel):
    lower: float | int | None = None
    upper: float | int | None = None


class FieldConstantSpec(StrictModel):
    kind: ConstantKind
    values: list[Any] = Field(default_factory=list)
    description: str = ""


class FieldSpec(StrictModel):
    name: str
    source_name: str | None = None
    value_type: ValueType | None = None
    roles: list[FieldRole] = Field(default_factory=list)
    bounds: BoundsSpec | None = None
    domain: list[Any] | None = None
    constants: list[FieldConstantSpec] = Field(default_factory=list)
    enum_labels: dict[str, str] = Field(default_factory=dict)
    context_family: str | None = None
    context_index: int | None = None


class ContextWindowSpec(StrictModel):
    size: int
    stride: int = 1
    partition_by: list[str] = Field(default_factory=list)
    order_by: list[str] = Field(default_factory=list)
    column_template: str = "{name}_ctx{index}"


class MappingRuleMode(str, Enum):
    EQUALS = "equals"
    IN = "in"
    RANGE = "range"
    PREFIX = "prefix"
    REGEX = "regex"
    DEFAULT = "default"


class MappingRuleSpec(StrictModel):
    mode: MappingRuleMode
    output: Any
    value: Any | None = None
    values: list[Any] = Field(default_factory=list)
    lower: float | int | None = None
    upper: float | int | None = None
    inclusive_lower: bool = True
    inclusive_upper: bool = True


class PreprocessStepSpec(StrictModel):
    kind: PreprocessKind
    columns: list[str] = Field(default_factory=list)
    target_column: str | None = None
    mapping: dict[str, Any] = Field(default_factory=dict)
    rules: list[MappingRuleSpec] = Field(default_factory=list)
    value: Any | None = None
    dtype: str | None = None
    by: list[str] = Field(default_factory=list)


class DerivedVariableSpec(StrictModel):
    name: str
    operation: DerivedOperation
    inputs: list[str] = Field(default_factory=list)
    value_type: ValueType
    roles: list[FieldRole] = Field(default_factory=lambda: [FieldRole.DERIVED])
    literal: Any | None = None
    numerator: str | None = None
    denominator: str | None = None
    description: str | None = None


class DatasetSpec(StrictModel):
    name: str
    description: str = ""
    source: SourceSpec
    fields: list[FieldSpec] = Field(default_factory=list)
    include_fields: list[str] = Field(default_factory=list)
    exclude_fields: list[str] = Field(default_factory=list)
    entity_keys: list[str] = Field(default_factory=list)
    grouping_keys: list[str] = Field(default_factory=list)
    ordering_keys: list[str] = Field(default_factory=list)
    preprocessing: list[PreprocessStepSpec] = Field(default_factory=list)
    context_window: ContextWindowSpec | None = None
    derived_variables: list[DerivedVariableSpec] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def normalize_legacy_keys(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        if "excluded_fields" in data:
            if "exclude_fields" in data:
                raise ValueError("Use only one of `exclude_fields` or legacy `excluded_fields`.")
            data = dict(data)
            data["exclude_fields"] = data.pop("excluded_fields")
        return data


class ConstantSelectorSpec(StrictModel):
    mode: Literal["explicit", "domain", "profile", "field_constants"] = "profile"
    values: list[Any] = Field(default_factory=list)
    kinds: list[ConstantKind] = Field(default_factory=list)
    top_k: int = 10
    quantiles: list[float] = Field(default_factory=lambda: [0.25, 0.5, 0.75, 0.9])


class VariableSelectorSpec(StrictModel):
    names: list[str] = Field(default_factory=list)
    regex: str | None = None
    types: list[ValueType] = Field(default_factory=list)
    roles: list[FieldRole] = Field(default_factory=list)
    derived_only: bool | None = None
    context_family: str | None = None
    window_only: bool | None = None
    exclude: list[str] = Field(default_factory=list)


class PredicateTermKind(str, Enum):
    FIELD = "field"
    CONSTANT = "constant"
    SCALAR = "scalar"
    ADDITION = "addition"


class TermTemplateSpec(StrictModel):
    kind: PredicateTermKind = PredicateTermKind.FIELD
    field: VariableSelectorSpec | None = None
    other_field: VariableSelectorSpec | None = None
    constant: ConstantSelectorSpec | None = None
    allow_same_field: bool = False
    description: str = ""


class PredicateTemplateSpec(StrictModel):
    name: str
    lhs: VariableSelectorSpec | None = None
    operators: list[Comparator]
    rhs_field: VariableSelectorSpec | None = None
    rhs_constant: ConstantSelectorSpec | None = None
    lhs_term: TermTemplateSpec | None = None
    rhs_term: TermTemplateSpec | None = None
    allow_same_field: bool = False
    description: str = ""

    @model_validator(mode="after")
    def validate_shape(self) -> "PredicateTemplateSpec":
        if self.lhs is None and self.lhs_term is None:
            raise ValueError("Predicate templates must define either `lhs` or `lhs_term`.")
        rhs_count = int(self.rhs_field is not None) + int(self.rhs_constant is not None) + int(self.rhs_term is not None)
        if rhs_count == 0:
            raise ValueError("Predicate templates must define one right-hand side selector or term.")
        if rhs_count > 1:
            raise ValueError("Predicate templates may define only one of `rhs_field`, `rhs_constant`, or `rhs_term`.")
        return self


class QuantifierTemplateSpec(StrictModel):
    name: str
    quantifier: Literal["forall", "exists"]
    selector: VariableSelectorSpec
    operators: list[Comparator]
    constant: ConstantSelectorSpec
    aggregator_projection: Aggregator | None = None
    description: str = ""


class GrammarSpec(StrictModel):
    name: str
    description: str = ""
    max_clause_size: int = 4
    max_rules: int = 250
    predicate_templates: list[PredicateTemplateSpec] = Field(default_factory=list)
    quantifier_templates: list[QuantifierTemplateSpec] = Field(default_factory=list)


def load_model(model_type: type[BaseModel], path: str | Path) -> BaseModel:
    return model_type.model_validate_json(Path(path).read_text())


def dump_model(model: BaseModel, path: str | Path) -> None:
    Path(path).write_text(model.model_dump_json(indent=2))


def load_dataset_spec(path: str | Path) -> DatasetSpec:
    return load_model(DatasetSpec, path)


def load_grammar_spec(path: str | Path) -> GrammarSpec:
    return load_model(GrammarSpec, path)


def json_dumps(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, default=str)
