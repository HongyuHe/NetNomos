from __future__ import annotations

from typing import Any

from netnomos.ast import (
    BinaryTerm,
    BoolAnd,
    BoolConst,
    BoolNot,
    BoolOr,
    Compare,
    Constant,
    Exists,
    Formula,
    ForAll,
    FuncCall,
    Implies,
    IndexedRef,
    SymbolRef,
    Term,
    render_keyword,
)
from netnomos.semantic_values import lookup_semantic_label
from netnomos.specs import FieldSpec


def interpret_formula(
    formula: Formula,
    fields: dict[str, FieldSpec],
    semantic_values: dict[str, dict[str, dict[str, Any]]] | None = None,
) -> str:
    if isinstance(formula, BoolConst):
        return render_keyword("true") if formula.value else render_keyword("false")
    if isinstance(formula, Compare):
        return (
            f"{interpret_term(formula.left, fields)} {formula.op} "
            f"{interpret_constant(formula.left, formula.right, fields, semantic_values)}"
        )
    if isinstance(formula, BoolNot):
        return f"{render_keyword('not')} ({interpret_formula(formula.value, fields, semantic_values)})"
    if isinstance(formula, BoolAnd):
        return (
            f" {render_keyword('and')} ".join(
                f"({interpret_formula(v, fields, semantic_values)})"
                for v in formula.values
            )
        )
    if isinstance(formula, BoolOr):
        return (
            f" {render_keyword('or')} ".join(
                f"({interpret_formula(v, fields, semantic_values)})"
                for v in formula.values
            )
        )
    if isinstance(formula, Implies):
        return (
            f"({interpret_formula(formula.left, fields, semantic_values)}) -> "
            f"({interpret_formula(formula.right, fields, semantic_values)})"
        )
    if isinstance(formula, ForAll):
        return (
            f"{render_keyword('forall')} {formula.variable} {render_keyword('in')} "
            f"{{{', '.join(map(str, formula.domain))}}}: "
            f"{interpret_formula(formula.body, fields, semantic_values)}"
        )
    if isinstance(formula, Exists):
        return (
            f"{render_keyword('exists')} {formula.variable} {render_keyword('in')} "
            f"{{{', '.join(map(str, formula.domain))}}}: "
            f"{interpret_formula(formula.body, fields, semantic_values)}"
        )
    raise TypeError(f"Unsupported formula node: {type(formula)!r}")


def interpret_term(term: Term, fields: dict[str, FieldSpec]) -> str:
    if isinstance(term, Constant):
        return render_value(term.value)
    if isinstance(term, SymbolRef):
        return term.name
    if isinstance(term, IndexedRef):
        return f"{term.base}[{term.index}]"
    if isinstance(term, BinaryTerm):
        return f"({interpret_term(term.left, fields)} {term.op} {interpret_term(term.right, fields)})"
    if isinstance(term, FuncCall):
        return f"{render_keyword(term.name)}({', '.join(interpret_term(arg, fields) for arg in term.args)})"
    raise TypeError(f"Unsupported term node: {type(term)!r}")


def interpret_constant(
    left: Term,
    right: Term,
    fields: dict[str, FieldSpec],
    semantic_values: dict[str, dict[str, dict[str, Any]]] | None = None,
) -> str:
    if not isinstance(right, Constant):
        return interpret_term(right, fields)
    semantic_label = lookup_semantic_label(left, right.value, fields, semantic_values)
    if semantic_label is not None:
        return semantic_label
    if isinstance(left, SymbolRef) and left.name in fields:
        field = fields[left.name]
        lookup_key = str(right.value)
        if lookup_key in field.enum_labels:
            return field.enum_labels[lookup_key]
    return render_value(right.value)


def render_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    return str(value)
