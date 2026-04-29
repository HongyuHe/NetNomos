from __future__ import annotations

import argparse
import ast as pyast
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from netnomos.ast import (
    BinaryTerm,
    BoolAnd,
    BoolConst,
    BoolNot,
    BoolOr,
    Compare,
    Constant,
    Formula,
    FuncCall,
    Implies,
    SymbolRef,
    Term,
    formula_to_dict,
    formula_to_string,
)


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OLD_RULES_DIR = Path("/Users/hongyu/Projects/Formal/anuta/rules")
DEFAULT_OUTPUT_ROOT = ROOT_DIR / "rules"


class CliFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


CIDDS_EQUALITY_LABELS = {
    "SrcIpAddr": {
        0: "private_p2p",
        1: "private_broadcast",
        2: "0.0.0.0",
        3: "public_p2p",
        4: "dns",
    },
    "DstIpAddr": {
        0: "private_p2p",
        1: "private_broadcast",
        2: "0.0.0.0",
        3: "public_p2p",
        4: "dns",
    },
    "Flags": {
        0: "noflags",
        1: "hasflags",
    },
    "Proto": {
        0: "TCP",
        1: "UDP",
        2: "ICMP",
        3: "IGMP",
    },
    "SrcPt": {
        60000: "unknown_port",
    },
    "DstPt": {
        60000: "unknown_port",
    },
}


PCAP_FIELD_NAMES = {
    "FrameLen": "frame.len",
    "IpVersion": "ip.version",
    "IpHdrLen": "ip.hdr_len",
    "IpLen": "ip.len",
    "IpTtl": "ip.ttl",
    "IpProto": "ip.proto",
    "IpSrc": "ip.src",
    "IpDst": "ip.dst",
    "TcpSrcport": "tcp.srcport",
    "TcpDstport": "tcp.dstport",
    "TcpHdrLen": "tcp.hdr_len",
    "TcpLen": "tcp.len",
    "TcpFlags": "tcp.flags",
    "TcpSeq": "tcp.seq",
    "TcpAck": "tcp.ack",
    "TcpUrgentPointer": "tcp.urgent_pointer",
    "TcpWindowSizeValue": "tcp.window_size_value",
    "TcpWindowSizeScalefactor": "tcp.window_size_scalefactor",
    "TcpWindowSize": "tcp.window_size",
    "Tsval": "tcp.options.timestamp.tsval",
    "Tsecr": "tcp.options.timestamp.tsecr",
    "Protocol": "_ws.col.protocol",
    "InterArrivalMicro": "interarrival_micro",
}


@dataclass(frozen=True, slots=True)
class ConversionSpec:
    name: str
    input_path: Path
    output_dir: Path
    field_mode: str
    label_mode: str


def flatten_bool(formula_type: type[BoolAnd] | type[BoolOr], values: list[Formula]) -> Formula:
    flattened: list[Formula] = []
    for value in values:
        if isinstance(value, formula_type):
            flattened.extend(value.values)
        else:
            flattened.append(value)
    if len(flattened) == 1:
        return flattened[0]
    return formula_type(tuple(flattened))


def fold_binary(op: str, args: list[Term]) -> Term:
    if not args:
        raise ValueError(f"{op} requires at least one argument")
    node = args[0]
    for arg in args[1:]:
        node = BinaryTerm(op, node, arg)
    return node


def remap_field_name(field_name: str, field_mode: str) -> str:
    if field_mode != "pcap":
        return field_name
    if "_" in field_name:
        base, _, suffix = field_name.rpartition("_")
        if suffix.isdigit() and base in PCAP_FIELD_NAMES:
            return f"{PCAP_FIELD_NAMES[base]}_ctx{int(suffix) - 1}"
        return field_name
    index_start = len(field_name)
    while index_start > 0 and field_name[index_start - 1].isdigit():
        index_start -= 1
    if index_start == len(field_name):
        return PCAP_FIELD_NAMES.get(field_name, field_name)
    base = field_name[:index_start]
    suffix = field_name[index_start:]
    if base not in PCAP_FIELD_NAMES or not suffix.isdigit():
        return field_name
    return f"{PCAP_FIELD_NAMES[base]}_ctx{int(suffix) - 1}"


def parse_number_arg(node: pyast.AST) -> int | float:
    if isinstance(node, pyast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, pyast.UnaryOp) and isinstance(node.op, pyast.USub):
        value = parse_number_arg(node.operand)
        return -value
    raise ValueError(f"Expected numeric literal, got: {pyast.dump(node)}")


def parse_term(node: pyast.AST, field_mode: str) -> Term:
    if isinstance(node, pyast.Name):
        return SymbolRef(remap_field_name(node.id, field_mode))
    if isinstance(node, pyast.Constant):
        return Constant(node.value)
    if isinstance(node, pyast.UnaryOp) and isinstance(node.op, pyast.USub):
        inner = parse_term(node.operand, field_mode)
        if not isinstance(inner, Constant) or not isinstance(inner.value, (int, float)):
            raise ValueError(f"Unsupported unary term: {pyast.dump(node)}")
        return Constant(-inner.value)
    if isinstance(node, pyast.BinOp):
        if isinstance(node.op, pyast.Add):
            return BinaryTerm("+", parse_term(node.left, field_mode), parse_term(node.right, field_mode))
        if isinstance(node.op, pyast.Sub):
            return BinaryTerm("-", parse_term(node.left, field_mode), parse_term(node.right, field_mode))
        if isinstance(node.op, pyast.Mult):
            return BinaryTerm("*", parse_term(node.left, field_mode), parse_term(node.right, field_mode))
        if isinstance(node.op, pyast.Div):
            return BinaryTerm("/", parse_term(node.left, field_mode), parse_term(node.right, field_mode))
        if isinstance(node.op, pyast.Mod):
            return FuncCall("mod", (parse_term(node.left, field_mode), parse_term(node.right, field_mode)))
    if isinstance(node, pyast.Call):
        func = getattr(node.func, "id", None)
        if func == "Symbol":
            arg = node.args[0]
            if isinstance(arg, pyast.Constant) and isinstance(arg.value, str):
                return SymbolRef(remap_field_name(arg.value, field_mode))
            raise ValueError(f"Symbol expects a string literal: {pyast.dump(node)}")
        if func == "Integer":
            return Constant(int(parse_number_arg(node.args[0])))
        if func == "Float":
            return Constant(float(parse_number_arg(node.args[0])))
        if func == "Rational":
            if len(node.args) != 2:
                raise ValueError("Rational requires exactly two arguments")
            numerator = parse_number_arg(node.args[0])
            denominator = parse_number_arg(node.args[1])
            return Constant(numerator / denominator)
        if func == "Add":
            return fold_binary("+", [parse_term(arg, field_mode) for arg in node.args])
        if func == "Mul":
            return fold_binary("*", [parse_term(arg, field_mode) for arg in node.args])
        if func == "Mod":
            if len(node.args) != 2:
                raise ValueError("Mod requires exactly two arguments")
            return FuncCall("mod", tuple(parse_term(arg, field_mode) for arg in node.args))
        if func in {"Min", "Max"}:
            return FuncCall(func.lower(), tuple(parse_term(arg, field_mode) for arg in node.args))
    raise ValueError(f"Unsupported term node: {pyast.dump(node)}")


def parse_compare(node: pyast.AST, field_mode: str) -> Formula:
    if isinstance(node, pyast.Call):
        func = getattr(node.func, "id", None)
        if func in {"Eq", "Equality"}:
            return Compare("=", parse_term(node.args[0], field_mode), parse_term(node.args[1], field_mode))
        if func in {"Ne", "Unequality"}:
            return Compare("!=", parse_term(node.args[0], field_mode), parse_term(node.args[1], field_mode))
        if func in {"Ge", "GreaterThan"}:
            return Compare(">=", parse_term(node.args[0], field_mode), parse_term(node.args[1], field_mode))
        if func in {"Le", "LessThan"}:
            return Compare("<=", parse_term(node.args[0], field_mode), parse_term(node.args[1], field_mode))
        if func in {"Gt", "StrictGreaterThan"}:
            return Compare(">", parse_term(node.args[0], field_mode), parse_term(node.args[1], field_mode))
        if func in {"Lt", "StrictLessThan"}:
            return Compare("<", parse_term(node.args[0], field_mode), parse_term(node.args[1], field_mode))
    if isinstance(node, pyast.Compare):
        if len(node.ops) != 1 or len(node.comparators) != 1:
            raise ValueError(f"Only single comparisons are supported: {pyast.dump(node)}")
        op = node.ops[0]
        if isinstance(op, pyast.Eq):
            token = "="
        elif isinstance(op, pyast.NotEq):
            token = "!="
        elif isinstance(op, pyast.Gt):
            token = ">"
        elif isinstance(op, pyast.GtE):
            token = ">="
        elif isinstance(op, pyast.Lt):
            token = "<"
        elif isinstance(op, pyast.LtE):
            token = "<="
        else:
            raise ValueError(f"Unsupported comparator: {pyast.dump(node)}")
        return Compare(token, parse_term(node.left, field_mode), parse_term(node.comparators[0], field_mode))
    raise ValueError(f"Unsupported comparison node: {pyast.dump(node)}")


def parse_formula(node: pyast.AST, field_mode: str) -> Formula:
    if isinstance(node, pyast.NameConstant):
        return BoolConst(bool(node.value))
    if isinstance(node, pyast.Constant) and isinstance(node.value, bool):
        return BoolConst(bool(node.value))
    if isinstance(node, pyast.BinOp):
        if isinstance(node.op, pyast.BitAnd):
            return flatten_bool(BoolAnd, [parse_formula(node.left, field_mode), parse_formula(node.right, field_mode)])
        if isinstance(node.op, pyast.BitOr):
            return flatten_bool(BoolOr, [parse_formula(node.left, field_mode), parse_formula(node.right, field_mode)])
        if isinstance(node.op, pyast.RShift):
            return Implies(parse_formula(node.left, field_mode), parse_formula(node.right, field_mode))
    if isinstance(node, pyast.BoolOp):
        if isinstance(node.op, pyast.And):
            return flatten_bool(BoolAnd, [parse_formula(value, field_mode) for value in node.values])
        if isinstance(node.op, pyast.Or):
            return flatten_bool(BoolOr, [parse_formula(value, field_mode) for value in node.values])
    if isinstance(node, pyast.UnaryOp) and isinstance(node.op, pyast.Invert):
        return BoolNot(parse_formula(node.operand, field_mode))
    if isinstance(node, pyast.Call):
        func = getattr(node.func, "id", None)
        if func in {"Eq", "Equality", "Ne", "Unequality", "Ge", "GreaterThan", "Le", "LessThan", "Gt", "StrictGreaterThan", "Lt", "StrictLessThan"}:
            return parse_compare(node, field_mode)
        if func == "And":
            return flatten_bool(BoolAnd, [parse_formula(arg, field_mode) for arg in node.args])
        if func == "Or":
            return flatten_bool(BoolOr, [parse_formula(arg, field_mode) for arg in node.args])
        if func == "Not":
            return BoolNot(parse_formula(node.args[0], field_mode))
        if func == "Implies":
            return Implies(parse_formula(node.args[0], field_mode), parse_formula(node.args[1], field_mode))
        if func in {"true", "True"}:
            return BoolConst(True)
        if func in {"false", "False"}:
            return BoolConst(False)
    if isinstance(node, pyast.Compare):
        return parse_compare(node, field_mode)
    raise ValueError(f"Unsupported formula node: {pyast.dump(node)}")


def normalize_name(path: Path) -> str:
    name = path.name
    for suffix in (".json", ".pl", ".rule"):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
    return name


def collect_rule_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        text = value.strip()
        if any(token in text for token in ("Implies(", "Equality(", "Unequality(", "Eq(", "Ne(", ">>", "Symbol(")):
            return [text]
        return []
    if isinstance(value, list):
        items: list[str] = []
        for item in value:
            items.extend(collect_rule_strings(item))
        return items
    if isinstance(value, dict):
        items: list[str] = []
        for item in value.values():
            items.extend(collect_rule_strings(item))
        return items
    return []


def load_expressions(path: Path) -> list[str]:
    if path.suffix.lower() != ".json":
        return [line.strip() for line in path.read_text().splitlines() if line.strip()]
    payload = json.loads(path.read_text())
    expressions = collect_rule_strings(payload)
    if not expressions:
        raise ValueError(f"No SymPy-style rule expressions found in {path}")
    return expressions


def render_term(term: Term) -> str:
    if isinstance(term, Constant):
        if isinstance(term.value, str):
            return term.value
        return str(term.value)
    if isinstance(term, SymbolRef):
        return term.name
    if isinstance(term, BinaryTerm):
        return f"({render_term(term.left)} {term.op} {render_term(term.right)})"
    if isinstance(term, FuncCall):
        return f"{term.name.upper()}({', '.join(render_term(arg) for arg in term.args)})"
    raise TypeError(f"Unsupported term type: {type(term)!r}")


def render_compare_right(formula: Compare, label_mode: str) -> str:
    if label_mode != "cidds":
        return render_term(formula.right)
    if formula.op not in {"=", "!="}:
        return render_term(formula.right)
    if not isinstance(formula.left, SymbolRef) or not isinstance(formula.right, Constant):
        return render_term(formula.right)
    if not isinstance(formula.right.value, int):
        return render_term(formula.right)
    label = CIDDS_EQUALITY_LABELS.get(formula.left.name, {}).get(formula.right.value)
    if label is None:
        return render_term(formula.right)
    return label


def render_formula(formula: Formula, label_mode: str) -> str:
    if isinstance(formula, Compare):
        return f"{render_term(formula.left)} {formula.op} {render_compare_right(formula, label_mode)}"
    if isinstance(formula, BoolConst):
        return "TRUE" if formula.value else "FALSE"
    if isinstance(formula, BoolNot):
        return f"NOT ({render_formula(formula.value, label_mode)})"
    if isinstance(formula, BoolAnd):
        return " AND ".join(f"({render_formula(value, label_mode)})" for value in formula.values)
    if isinstance(formula, BoolOr):
        return " OR ".join(f"({render_formula(value, label_mode)})" for value in formula.values)
    if isinstance(formula, Implies):
        return f"({render_formula(formula.left, label_mode)}) -> ({render_formula(formula.right, label_mode)})"
    return formula_to_string(formula)


def write_conversion(spec: ConversionSpec) -> dict[str, Any]:
    expressions = load_expressions(spec.input_path)
    spec.output_dir.mkdir(parents=True, exist_ok=True)
    rules: list[dict[str, Any]] = []
    interpreted: list[str] = []
    for index, expression in enumerate(expressions, start=1):
        formula = parse_formula(pyast.parse(expression, mode="eval").body, spec.field_mode)
        rules.append({
            "rule_id": f"{spec.name}_{index:05d}",
            "formula": formula_to_dict(formula),
            "display": formula_to_string(formula),
            "support": 0.0,
            "source": {
                "importer": "sympy-rule-converter",
                "original_file": str(spec.input_path),
                "original_line": index,
                "original_expression": expression,
                "field_mode": spec.field_mode,
                "label_mode": spec.label_mode,
            },
        })
        interpreted.append(render_formula(formula, spec.label_mode))
    (spec.output_dir / "rules.json").write_text(json.dumps(rules, indent=2))
    (spec.output_dir / "interpreted_rules.clj").write_text("\n".join(interpreted) + "\n")
    metadata = {
        "name": spec.name,
        "source_file": str(spec.input_path),
        "rule_count": len(rules),
        "field_mode": spec.field_mode,
        "label_mode": spec.label_mode,
    }
    (spec.output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))
    return {
        "name": spec.name,
        "input": str(spec.input_path),
        "output_dir": str(spec.output_dir),
        "rule_count": len(rules),
    }


def build_default_golden_specs(output_root: Path) -> list[ConversionSpec]:
    return [
        ConversionSpec(
            name="golden_cidds",
            input_path=DEFAULT_OLD_RULES_DIR / "golden_cidds.pl",
            output_dir=output_root / "golden_cidds",
            field_mode="generic",
            label_mode="cidds",
        ),
        ConversionSpec(
            name="golden_mawi",
            input_path=DEFAULT_OLD_RULES_DIR / "golden_mawi.pl",
            output_dir=output_root / "golden_mawi",
            field_mode="pcap",
            label_mode="none",
        ),
        ConversionSpec(
            name="golden_metadc",
            input_path=DEFAULT_OLD_RULES_DIR / "golden_metadc.pl",
            output_dir=output_root / "golden_metadc",
            field_mode="generic",
            label_mode="none",
        ),
        ConversionSpec(
            name="golden_netflix",
            input_path=DEFAULT_OLD_RULES_DIR / "golden_netflix.pl",
            output_dir=output_root / "golden_netflix",
            field_mode="pcap",
            label_mode="none",
        ),
        ConversionSpec(
            name="golden_netflix_full",
            input_path=DEFAULT_OLD_RULES_DIR / "golden_netflix_full.pl",
            output_dir=output_root / "golden_netflix_full",
            field_mode="pcap",
            label_mode="none",
        ),
    ]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Convert old anuta SymPy-style rule files (.pl or .json) into the current NetNomos "
            "rules.json format plus interpreted_rules.clj companions."
        ),
        formatter_class=CliFormatter,
    )
    parser.add_argument("--input", help="Path to a single source rule file in old SymPy syntax.")
    parser.add_argument(
        "--output-dir",
        help="Directory where rules.json, interpreted_rules.clj, and metadata.json will be written.",
    )
    parser.add_argument(
        "--name",
        help="Rule-set name used for rule ids and metadata. Defaults to a normalized input filename.",
    )
    parser.add_argument(
        "--field-mode",
        choices=["generic", "pcap"],
        default="generic",
        help="Optional field-name remapping mode.",
    )
    parser.add_argument(
        "--label-mode",
        choices=["none", "cidds"],
        default="none",
        help="Optional interpretation label mode.",
    )
    parser.add_argument(
        "--batch-golden",
        action="store_true",
        help="Regenerate the built-in golden_* conversions under the output root.",
    )
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_OUTPUT_ROOT),
        help="Base directory used by --batch-golden.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.batch_golden:
        results = [write_conversion(spec) for spec in build_default_golden_specs(Path(args.output_root))]
        print(json.dumps({"converted": results}, indent=2))
        return 0
    if not args.input or not args.output_dir:
        raise SystemExit("--input and --output-dir are required unless --batch-golden is used.")
    input_path = Path(args.input)
    name = args.name or normalize_name(input_path)
    result = write_conversion(ConversionSpec(
        name=name,
        input_path=input_path,
        output_dir=Path(args.output_dir),
        field_mode=args.field_mode,
        label_mode=args.label_mode,
    ))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
