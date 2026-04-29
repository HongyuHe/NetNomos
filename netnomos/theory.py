from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
import z3

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
    formula_to_string,
)
from netnomos.dataset import PreparedDataset
from netnomos.specs import FieldSpec, ValueType


@dataclass(slots=True)
class Theory:
    formulas: list[Formula]
    fields: dict[str, FieldSpec]
    context_families: dict[str, list[str]]

    def entails(self, query: Formula) -> bool:
        solver = z3.Solver()
        for formula in self.formulas:
            solver.add(lower_formula(formula, self.fields, self.context_families))
        solver.add(z3.Not(lower_formula(query, self.fields, self.context_families)))
        return solver.check() == z3.unsat

    def is_consistent(self) -> bool:
        solver = z3.Solver()
        for formula in self.formulas:
            solver.add(lower_formula(formula, self.fields, self.context_families))
        return solver.check() == z3.sat

    def validate(self, prepared: PreparedDataset) -> dict[str, Any]:
        sats = [float(evaluate_formula_df(formula, prepared).mean()) for formula in self.formulas]
        return {
            "rule_count": len(self.formulas),
            "all_rows_satisfied": all(rate == 1.0 for rate in sats),
            "mean_satisfaction": float(np.mean(sats)) if sats else 1.0,
            "per_rule_satisfaction": sats,
        }


def evaluate_formula_df(formula: Formula, prepared: PreparedDataset) -> pd.Series:
    try:
        return _evaluate_formula_vectorized(formula, prepared)
    except Exception:
        return prepared.dataframe.apply(
            lambda row: bool(evaluate_formula_row(formula, row.to_dict(), prepared.context_families)),
            axis=1,
        )


def evaluate_formula_row(formula: Formula, row: dict[str, Any], context_families: dict[str, list[str]], env: dict[str, Any] | None = None) -> bool:
    env = env or {}
    if isinstance(formula, BoolConst):
        return formula.value
    if isinstance(formula, Compare):
        left = evaluate_term_row(formula.left, row, context_families, env)
        right = evaluate_term_row(formula.right, row, context_families, env)
        return compare_values(formula.op, left, right)
    if isinstance(formula, BoolNot):
        return not evaluate_formula_row(formula.value, row, context_families, env)
    if isinstance(formula, BoolAnd):
        return all(evaluate_formula_row(v, row, context_families, env) for v in formula.values)
    if isinstance(formula, BoolOr):
        return any(evaluate_formula_row(v, row, context_families, env) for v in formula.values)
    if isinstance(formula, Implies):
        return (not evaluate_formula_row(formula.left, row, context_families, env)) or evaluate_formula_row(formula.right, row, context_families, env)
    if isinstance(formula, ForAll):
        return all(evaluate_formula_row(formula.body, row, context_families, {**env, formula.variable: value}) for value in formula.domain)
    if isinstance(formula, Exists):
        return any(evaluate_formula_row(formula.body, row, context_families, {**env, formula.variable: value}) for value in formula.domain)
    raise TypeError(f"Unsupported formula node: {type(formula)!r}")


def evaluate_term_row(term: Term, row: dict[str, Any], context_families: dict[str, list[str]], env: dict[str, Any]) -> Any:
    if isinstance(term, Constant):
        return term.value
    if isinstance(term, SymbolRef):
        return row[term.name]
    if isinstance(term, IndexedRef):
        return row[resolve_indexed_name(term, env, context_families)]
    if isinstance(term, BinaryTerm):
        left = evaluate_term_row(term.left, row, context_families, env)
        right = evaluate_term_row(term.right, row, context_families, env)
        if term.op == "+":
            return left + right
        if term.op == "-":
            return left - right
        if term.op == "*":
            return left * right
        if term.op == "/":
            return left / right
        raise ValueError(f"Unsupported term op: {term.op}")
    if isinstance(term, FuncCall):
        args = [evaluate_term_row(arg, row, context_families, env) for arg in term.args]
        name = term.name.lower()
        if name == "min":
            return min(args)
        if name == "max":
            return max(args)
        if name == "sum":
            return sum(args)
        if name == "avg":
            return sum(args) / len(args)
        if name == "mod":
            if len(args) != 2:
                raise ValueError("MOD requires exactly two arguments")
            return args[0] % args[1]
        raise ValueError(f"Unsupported function: {term.name}")
    raise TypeError(f"Unsupported term node: {type(term)!r}")


def compare_values(op: str, left: Any, right: Any) -> bool:
    if op == "=":
        return left == right
    if op == "!=":
        return left != right
    if op == ">":
        return left > right
    if op == ">=":
        return left >= right
    if op == "<":
        return left < right
    if op == "<=":
        return left <= right
    raise ValueError(f"Unsupported comparator: {op}")


def lower_formula(formula: Formula, fields: dict[str, FieldSpec], context_families: dict[str, list[str]], env: dict[str, Any] | None = None) -> z3.ExprRef:
    env = env or {}
    if isinstance(formula, BoolConst):
        return z3.BoolVal(formula.value)
    if isinstance(formula, Compare):
        left = lower_term(formula.left, fields, context_families, env)
        right = lower_term(formula.right, fields, context_families, env)
        if formula.op == "=":
            return left == right
        if formula.op == "!=":
            return left != right
        if formula.op == ">":
            return left > right
        if formula.op == ">=":
            return left >= right
        if formula.op == "<":
            return left < right
        if formula.op == "<=":
            return left <= right
        raise ValueError(f"Unsupported comparator: {formula.op}")
    if isinstance(formula, BoolNot):
        return z3.Not(lower_formula(formula.value, fields, context_families, env))
    if isinstance(formula, BoolAnd):
        return z3.And(*[lower_formula(v, fields, context_families, env) for v in formula.values])
    if isinstance(formula, BoolOr):
        return z3.Or(*[lower_formula(v, fields, context_families, env) for v in formula.values])
    if isinstance(formula, Implies):
        return z3.Implies(lower_formula(formula.left, fields, context_families, env), lower_formula(formula.right, fields, context_families, env))
    if isinstance(formula, ForAll):
        return z3.And(*[lower_formula(formula.body, fields, context_families, {**env, formula.variable: value}) for value in formula.domain])
    if isinstance(formula, Exists):
        return z3.Or(*[lower_formula(formula.body, fields, context_families, {**env, formula.variable: value}) for value in formula.domain])
    raise TypeError(f"Unsupported formula node: {type(formula)!r}")


def lower_term(term: Term, fields: dict[str, FieldSpec], context_families: dict[str, list[str]], env: dict[str, Any]) -> z3.ExprRef:
    if isinstance(term, Constant):
        if isinstance(term.value, bool):
            return z3.BoolVal(term.value)
        if isinstance(term.value, int):
            return z3.IntVal(term.value)
        if isinstance(term.value, float):
            return z3.RealVal(term.value)
        return z3.StringVal(str(term.value))
    if isinstance(term, SymbolRef):
        return symbol_for_field(term.name, fields[term.name])
    if isinstance(term, IndexedRef):
        name = resolve_indexed_name(term, env, context_families)
        return symbol_for_field(name, fields[name])
    if isinstance(term, BinaryTerm):
        left = lower_term(term.left, fields, context_families, env)
        right = lower_term(term.right, fields, context_families, env)
        if term.op == "+":
            return left + right
        if term.op == "-":
            return left - right
        if term.op == "*":
            return left * right
        if term.op == "/":
            return left / right
        raise ValueError(f"Unsupported term op: {term.op}")
    if isinstance(term, FuncCall):
        args = [lower_term(arg, fields, context_families, env) for arg in term.args]
        name = term.name.lower()
        if name == "min":
            return fold_if_min(args)
        if name == "max":
            return fold_if_max(args)
        if name == "sum":
            result = args[0]
            for arg in args[1:]:
                result = result + arg
            return result
        if name == "avg":
            total = lower_term(FuncCall("sum", term.args), fields, context_families, env)
            return total / z3.RealVal(len(args))
        if name == "mod":
            if len(args) != 2:
                raise ValueError("MOD requires exactly two arguments")
            return args[0] % args[1]
        raise ValueError(f"Unsupported function: {term.name}")
    raise TypeError(f"Unsupported term node: {type(term)!r}")


def symbol_for_field(name: str, field: FieldSpec) -> z3.ExprRef:
    if field.value_type == ValueType.INTEGER:
        return z3.Int(name)
    if field.value_type == ValueType.REAL:
        return z3.Real(name)
    if field.value_type == ValueType.BOOLEAN:
        return z3.Bool(name)
    if field.domain:
        if all(isinstance(value, bool) for value in field.domain):
            return z3.Bool(name)
        if all(isinstance(value, int) and not isinstance(value, bool) for value in field.domain):
            return z3.Int(name)
        if all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in field.domain):
            return z3.Real(name)
    return z3.String(name)


def fold_if_min(args: list[z3.ExprRef]) -> z3.ExprRef:
    result = args[0]
    for arg in args[1:]:
        result = z3.If(result <= arg, result, arg)
    return result


def fold_if_max(args: list[z3.ExprRef]) -> z3.ExprRef:
    result = args[0]
    for arg in args[1:]:
        result = z3.If(result >= arg, result, arg)
    return result


def resolve_indexed_name(term: IndexedRef, env: dict[str, Any], context_families: dict[str, list[str]]) -> str:
    index = env.get(term.index, term.index)
    if isinstance(index, str) and index.isdigit():
        index = int(index)
    if not isinstance(index, int):
        raise ValueError(f"Indexed reference {formula_to_string(Compare('=', term, Constant(0)))} requires an integer index")
    if term.base not in context_families:
        raise KeyError(f"Unknown context family: {term.base}")
    return context_families[term.base][index]


def _evaluate_formula_vectorized(formula: Formula, prepared: PreparedDataset) -> pd.Series:
    if isinstance(formula, BoolConst):
        return pd.Series([formula.value] * len(prepared.dataframe), index=prepared.dataframe.index)
    if isinstance(formula, Compare):
        left = _evaluate_term_vectorized(formula.left, prepared)
        right = _evaluate_term_vectorized(formula.right, prepared)
        if formula.op == "=":
            return left == right
        if formula.op == "!=":
            return left != right
        if formula.op == ">":
            return left > right
        if formula.op == ">=":
            return left >= right
        if formula.op == "<":
            return left < right
        if formula.op == "<=":
            return left <= right
    if isinstance(formula, BoolNot):
        return ~_evaluate_formula_vectorized(formula.value, prepared)
    if isinstance(formula, BoolAnd):
        result = _evaluate_formula_vectorized(formula.values[0], prepared)
        for child in formula.values[1:]:
            result = result & _evaluate_formula_vectorized(child, prepared)
        return result
    if isinstance(formula, BoolOr):
        result = _evaluate_formula_vectorized(formula.values[0], prepared)
        for child in formula.values[1:]:
            result = result | _evaluate_formula_vectorized(child, prepared)
        return result
    if isinstance(formula, Implies):
        left = _evaluate_formula_vectorized(formula.left, prepared)
        right = _evaluate_formula_vectorized(formula.right, prepared)
        return (~left) | right
    raise ValueError("Quantified formulas require row-wise evaluation")


def _evaluate_term_vectorized(term: Term, prepared: PreparedDataset) -> pd.Series | Any:
    frame = prepared.dataframe
    if isinstance(term, Constant):
        return term.value
    if isinstance(term, SymbolRef):
        return frame[term.name]
    if isinstance(term, IndexedRef):
        name = resolve_indexed_name(term, {}, prepared.context_families)
        return frame[name]
    if isinstance(term, BinaryTerm):
        left = _evaluate_term_vectorized(term.left, prepared)
        right = _evaluate_term_vectorized(term.right, prepared)
        if term.op == "+":
            return left + right
        if term.op == "-":
            return left - right
        if term.op == "*":
            return left * right
        if term.op == "/":
            return left / right
    if isinstance(term, FuncCall):
        columns = [_evaluate_term_vectorized(arg, prepared) for arg in term.args]
        name = term.name.lower()
        if all(isinstance(col, pd.Series) for col in columns):
            tmp = pd.concat(columns, axis=1)
            if name == "min":
                return tmp.min(axis=1)
            if name == "max":
                return tmp.max(axis=1)
            if name == "sum":
                return tmp.sum(axis=1)
            if name == "avg":
                return tmp.mean(axis=1)
            if name == "mod":
                if len(columns) != 2:
                    raise ValueError("MOD requires exactly two arguments")
                return columns[0] % columns[1]
        values = [col if not isinstance(col, pd.Series) else col.iloc[0] for col in columns]
        if name == "min":
            return min(values)
        if name == "max":
            return max(values)
        if name == "sum":
            return sum(values)
        if name == "avg":
            return sum(values) / len(values)
        if name == "mod":
            if len(values) != 2:
                raise ValueError("MOD requires exactly two arguments")
            return values[0] % values[1]
    raise TypeError(f"Unsupported vectorized term: {type(term)!r}")
