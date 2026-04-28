from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Constant:
    value: Any


@dataclass(frozen=True, slots=True)
class SymbolRef:
    name: str


@dataclass(frozen=True, slots=True)
class IndexedRef:
    base: str
    index: int | str


@dataclass(frozen=True, slots=True)
class BinaryTerm:
    op: str
    left: Term
    right: Term


@dataclass(frozen=True, slots=True)
class FuncCall:
    name: str
    args: tuple[Term, ...]


Term = Constant | SymbolRef | IndexedRef | BinaryTerm | FuncCall


@dataclass(frozen=True, slots=True)
class Compare:
    op: str
    left: Term
    right: Term


@dataclass(frozen=True, slots=True)
class BoolConst:
    value: bool


@dataclass(frozen=True, slots=True)
class BoolNot:
    value: Formula


@dataclass(frozen=True, slots=True)
class BoolAnd:
    values: tuple[Formula, ...]


@dataclass(frozen=True, slots=True)
class BoolOr:
    values: tuple[Formula, ...]


@dataclass(frozen=True, slots=True)
class Implies:
    left: Formula
    right: Formula


@dataclass(frozen=True, slots=True)
class ForAll:
    variable: str
    domain: tuple[Any, ...]
    body: Formula


@dataclass(frozen=True, slots=True)
class Exists:
    variable: str
    domain: tuple[Any, ...]
    body: Formula


Formula = Compare | BoolConst | BoolNot | BoolAnd | BoolOr | Implies | ForAll | Exists


def constant(value: Any) -> Constant:
    return Constant(value=value)


def formula_to_dict(node: Formula) -> dict[str, Any]:
    if isinstance(node, Compare):
        return {
            "kind": "compare",
            "op": node.op,
            "left": term_to_dict(node.left),
            "right": term_to_dict(node.right),
        }
    if isinstance(node, BoolConst):
        return {"kind": "bool", "value": node.value}
    if isinstance(node, BoolNot):
        return {"kind": "not", "value": formula_to_dict(node.value)}
    if isinstance(node, BoolAnd):
        return {"kind": "and", "values": [formula_to_dict(v) for v in node.values]}
    if isinstance(node, BoolOr):
        return {"kind": "or", "values": [formula_to_dict(v) for v in node.values]}
    if isinstance(node, Implies):
        return {
            "kind": "implies",
            "left": formula_to_dict(node.left),
            "right": formula_to_dict(node.right),
        }
    if isinstance(node, ForAll):
        return {
            "kind": "forall",
            "variable": node.variable,
            "domain": list(node.domain),
            "body": formula_to_dict(node.body),
        }
    if isinstance(node, Exists):
        return {
            "kind": "exists",
            "variable": node.variable,
            "domain": list(node.domain),
            "body": formula_to_dict(node.body),
        }
    raise TypeError(f"Unsupported formula node: {type(node)!r}")


def term_to_dict(node: Term) -> dict[str, Any]:
    if isinstance(node, Constant):
        return {"kind": "constant", "value": node.value}
    if isinstance(node, SymbolRef):
        return {"kind": "symbol", "name": node.name}
    if isinstance(node, IndexedRef):
        return {"kind": "indexed", "base": node.base, "index": node.index}
    if isinstance(node, BinaryTerm):
        return {
            "kind": "binary",
            "op": node.op,
            "left": term_to_dict(node.left),
            "right": term_to_dict(node.right),
        }
    if isinstance(node, FuncCall):
        return {"kind": "call", "name": node.name, "args": [term_to_dict(v) for v in node.args]}
    raise TypeError(f"Unsupported term node: {type(node)!r}")


def formula_from_dict(data: dict[str, Any]) -> Formula:
    kind = data["kind"]
    if kind == "compare":
        return Compare(data["op"], term_from_dict(data["left"]), term_from_dict(data["right"]))
    if kind == "bool":
        return BoolConst(bool(data["value"]))
    if kind == "not":
        return BoolNot(formula_from_dict(data["value"]))
    if kind == "and":
        return BoolAnd(tuple(formula_from_dict(v) for v in data["values"]))
    if kind == "or":
        return BoolOr(tuple(formula_from_dict(v) for v in data["values"]))
    if kind == "implies":
        return Implies(formula_from_dict(data["left"]), formula_from_dict(data["right"]))
    if kind == "forall":
        return ForAll(variable=data["variable"], domain=tuple(data["domain"]), body=formula_from_dict(data["body"]))
    if kind == "exists":
        return Exists(variable=data["variable"], domain=tuple(data["domain"]), body=formula_from_dict(data["body"]))
    raise ValueError(f"Unsupported formula kind: {kind}")


def term_from_dict(data: dict[str, Any]) -> Term:
    kind = data["kind"]
    if kind == "constant":
        return Constant(data["value"])
    if kind == "symbol":
        return SymbolRef(data["name"])
    if kind == "indexed":
        return IndexedRef(data["base"], data["index"])
    if kind == "binary":
        return BinaryTerm(data["op"], term_from_dict(data["left"]), term_from_dict(data["right"]))
    if kind == "call":
        return FuncCall(data["name"], tuple(term_from_dict(v) for v in data["args"]))
    raise ValueError(f"Unsupported term kind: {kind}")


def term_to_string(node: Term) -> str:
    if isinstance(node, Constant):
        return repr(node.value) if isinstance(node.value, str) else str(node.value)
    if isinstance(node, SymbolRef):
        return node.name
    if isinstance(node, IndexedRef):
        return f"{node.base}[{node.index}]"
    if isinstance(node, BinaryTerm):
        return f"({term_to_string(node.left)} {node.op} {term_to_string(node.right)})"
    if isinstance(node, FuncCall):
        return f"{node.name}({', '.join(term_to_string(v) for v in node.args)})"
    raise TypeError(f"Unsupported term node: {type(node)!r}")


def formula_to_string(node: Formula) -> str:
    if isinstance(node, Compare):
        return f"{term_to_string(node.left)} {node.op} {term_to_string(node.right)}"
    if isinstance(node, BoolConst):
        return "true" if node.value else "false"
    if isinstance(node, BoolNot):
        return f"not ({formula_to_string(node.value)})"
    if isinstance(node, BoolAnd):
        return " and ".join(f"({formula_to_string(v)})" for v in node.values)
    if isinstance(node, BoolOr):
        return " or ".join(f"({formula_to_string(v)})" for v in node.values)
    if isinstance(node, Implies):
        return f"({formula_to_string(node.left)}) -> ({formula_to_string(node.right)})"
    if isinstance(node, ForAll):
        return f"forall {node.variable} in {{{', '.join(map(str, node.domain))}}}: {formula_to_string(node.body)}"
    if isinstance(node, Exists):
        return f"exists {node.variable} in {{{', '.join(map(str, node.domain))}}}: {formula_to_string(node.body)}"
    raise TypeError(f"Unsupported formula node: {type(node)!r}")

