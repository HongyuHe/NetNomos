from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

import pandas as pd
from tqdm.auto import tqdm

from netnomos.ast import BinaryTerm, BoolAnd, BoolOr, Compare, Constant, Formula, FuncCall, SymbolRef, formula_to_string
from netnomos.dataset import PreparedDataset
from netnomos.semantic_values import quantile_label
from netnomos.specs import (
    Comparator,
    ConstantKind,
    ConstantSelectorSpec,
    FieldRole,
    FieldSpec,
    GrammarSpec,
    PredicateTermKind,
    QuantifierTemplateSpec,
    TermTemplateSpec,
    ValueType,
    VariableSelectorSpec,
)
from netnomos.theory import evaluate_formula_df


@dataclass(slots=True)
class GroundedPredicate:
    predicate_id: str
    formula: Formula
    display: str
    support: float
    source: dict[str, Any]


@dataclass(slots=True)
class GeneratedTerm:
    expr: Any
    display: str
    field_names: tuple[str, ...]
    has_field_reference: bool
    ordered_numeric: bool
    comparison_group: str | None
    value_type: ValueType
    source: dict[str, Any]


@dataclass(slots=True)
class SelectedConstant:
    value: Any
    label: str | None


def generate_predicates(prepared: PreparedDataset, grammar: GrammarSpec) -> list[GroundedPredicate]:
    candidates: dict[str, tuple[Formula, str, dict[str, Any]]] = {}
    for template in grammar.predicate_templates:
        if template.lhs_term is not None or template.rhs_term is not None:
            lhs_terms = generate_terms(prepared, template.lhs_term or TermTemplateSpec(kind=PredicateTermKind.FIELD, field=template.lhs))
            rhs_terms = generate_terms(
                prepared,
                template.rhs_term or build_legacy_rhs_term(template),
            )
            for lhs_term in lhs_terms:
                for rhs_term in rhs_terms:
                    if (not template.allow_same_field) and set(lhs_term.field_names) & set(rhs_term.field_names):
                        continue
                    if not compatible_terms(lhs_term, rhs_term, template.operators):
                        continue
                    for op in template.operators:
                        formula = Compare(op.value, lhs_term.expr, rhs_term.expr)
                        append_candidate(candidates, formula, {
                            "kind": "term-comparison",
                            "template": template.name,
                            "lhs_term": lhs_term.source,
                            "rhs_term": rhs_term.source,
                            "semantic_constants": [
                                *lhs_term.source.get("semantic_constants", []),
                                *rhs_term.source.get("semantic_constants", []),
                            ],
                        })
            continue
        lhs_fields = select_fields(prepared, template.lhs)
        if template.rhs_field is not None:
            rhs_fields = select_fields(prepared, template.rhs_field)
            for lhs in lhs_fields:
                for rhs in rhs_fields:
                    if lhs == rhs and not template.allow_same_field:
                        continue
                    if not compatible_fields(prepared.field_specs[lhs], prepared.field_specs[rhs], template.operators):
                        continue
                    for op in template.operators:
                        formula = Compare(op.value, SymbolRef(lhs), SymbolRef(rhs))
                        append_candidate(candidates, formula, {
                            "kind": "field-field",
                            "template": template.name,
                            "lhs": lhs,
                            "rhs": rhs,
                            "semantic_constants": [],
                        })
        if template.rhs_constant is not None:
            for lhs in lhs_fields:
                field = prepared.field_specs[lhs]
                for constant in select_constants(prepared, lhs, field, template.rhs_constant):
                    if not compatible_constant(field, constant.value, template.operators):
                        continue
                    for op in template.operators:
                        formula = Compare(op.value, SymbolRef(lhs), Constant(constant.value))
                        append_candidate(candidates, formula, {
                            "kind": "field-constant",
                            "template": template.name,
                            "lhs": lhs,
                            "constant": constant.value,
                            "semantic_constants": build_semantic_entries("field", lhs, constant),
                        })
    for template in grammar.quantifier_templates:
        families = select_context_families(prepared, template)
        for family_name, family_fields in families.items():
            constants = select_quantifier_constants(prepared, family_fields, template.constant)
            for constant in constants:
                for op in template.operators:
                    formula, display = project_quantified_family(family_name, family_fields, template, op, constant)
                    append_candidate(candidates, formula, {
                        "kind": "quantifier",
                        "template": template.name,
                        "family": family_name,
                        "fields": family_fields,
                        "constant": constant.value,
                        "quantifier": template.quantifier,
                        "semantic_constants": build_semantic_entries("family", family_name, constant),
                    }, display=display)
    predicates: list[GroundedPredicate] = []
    ordered_candidates = sorted(candidates.values(), key=lambda item: item[1])
    for formula, display, source in tqdm(
        ordered_candidates,
        desc="Evaluating predicate support",
        unit=" predicate",
        disable=None,
    ):
        support = float(evaluate_formula_df(formula, prepared).mean())
        predicates.append(GroundedPredicate(
            predicate_id=f"p{len(predicates):05d}",
            formula=formula,
            display=display,
            support=support,
            source=source,
        ))
    return predicates


def append_candidate(
    candidates: dict[str, tuple[Formula, str, dict[str, Any]]],
    formula: Formula,
    source: dict[str, Any],
    display: str | None = None,
) -> None:
    key = formula_to_string(formula)
    if key in candidates:
        return
    candidates[key] = (formula, display or key, source)


def build_legacy_rhs_term(template: Any) -> TermTemplateSpec:
    if template.rhs_field is not None:
        return TermTemplateSpec(kind=PredicateTermKind.FIELD, field=template.rhs_field)
    if template.rhs_constant is not None:
        return TermTemplateSpec(kind=PredicateTermKind.CONSTANT, constant=template.rhs_constant)
    raise ValueError(f"Predicate template {template.name} must define a right-hand side")


def generate_terms(prepared: PreparedDataset, template: TermTemplateSpec) -> list[GeneratedTerm]:
    if template.kind == PredicateTermKind.FIELD:
        selector = template.field or VariableSelectorSpec()
        return [
            GeneratedTerm(
                expr=SymbolRef(name),
                display=name,
                field_names=(name,),
                has_field_reference=True,
                ordered_numeric=is_ordered_numeric_field(prepared.field_specs[name]),
                comparison_group=numeric_comparison_group(prepared.field_specs[name]),
                value_type=prepared.field_specs[name].value_type or ValueType.STRING,
                source={"kind": "field", "field": name, "semantic_constants": []},
            )
            for name in select_fields(prepared, selector)
        ]
    if template.kind == PredicateTermKind.CONSTANT:
        selector = template.constant or ConstantSelectorSpec(mode="explicit")
        if selector.mode != "explicit":
            raise ValueError("Constant term templates currently require mode='explicit'")
        terms: list[GeneratedTerm] = []
        for value in selector.values:
            terms.append(GeneratedTerm(
                expr=Constant(value),
                display=str(value),
                field_names=(),
                has_field_reference=False,
                ordered_numeric=False,
                comparison_group=None,
                value_type=infer_constant_value_type(value),
                source={"kind": "constant", "value": value, "semantic_constants": []},
            ))
        return terms
    if template.kind == PredicateTermKind.SCALAR:
        if template.field is None or template.constant is None:
            raise ValueError("Scalar term templates require both `field` and `constant`")
        terms: list[GeneratedTerm] = []
        for field_name in select_fields(prepared, template.field):
            field = prepared.field_specs[field_name]
            if not is_ordered_numeric_field(field):
                continue
            comparison_group = numeric_comparison_group(field)
            for value in select_constants(prepared, field_name, field, template.constant):
                if isinstance(value.value, str):
                    continue
                value_type = combine_numeric_types(field.value_type, infer_constant_value_type(value.value))
                terms.append(GeneratedTerm(
                    expr=BinaryTerm("*", SymbolRef(field_name), Constant(value.value)),
                    display=f"{field_name} * {value.value}",
                    field_names=(field_name,),
                    has_field_reference=True,
                    ordered_numeric=True,
                    comparison_group=comparison_group,
                    value_type=value_type,
                    source={
                        "kind": "scalar",
                        "field": field_name,
                        "constant": value.value,
                        "semantic_constants": build_semantic_entries("field", field_name, value),
                    },
                ))
        return terms
    if template.kind == PredicateTermKind.ADDITION:
        if template.field is None:
            raise ValueError("Addition term templates require `field`")
        terms: list[GeneratedTerm] = []
        left_fields = select_fields(prepared, template.field)
        if template.other_field is not None:
            right_fields = select_fields(prepared, template.other_field)
            for left_name in left_fields:
                left_field = prepared.field_specs[left_name]
                if not is_ordered_numeric_field(left_field):
                    continue
                left_group = numeric_comparison_group(left_field)
                for right_name in right_fields:
                    if left_name == right_name and not template.allow_same_field:
                        continue
                    right_field = prepared.field_specs[right_name]
                    if not is_ordered_numeric_field(right_field):
                        continue
                    addition_group = addition_comparison_group(left_field, right_field)
                    if addition_group is None:
                        continue
                    terms.append(GeneratedTerm(
                        expr=BinaryTerm("+", SymbolRef(left_name), SymbolRef(right_name)),
                        display=f"{left_name} + {right_name}",
                        field_names=(left_name, right_name),
                        has_field_reference=True,
                        ordered_numeric=True,
                        comparison_group=addition_group,
                        value_type=combine_numeric_types(left_field.value_type, right_field.value_type),
                        source={
                            "kind": "addition",
                            "left_field": left_name,
                            "right_field": right_name,
                            "semantic_constants": [],
                        },
                    ))
        if template.constant is not None:
            for left_name in left_fields:
                left_field = prepared.field_specs[left_name]
                if not is_ordered_numeric_field(left_field):
                    continue
                comparison_group = numeric_comparison_group(left_field)
                for value in select_constants(prepared, left_name, left_field, template.constant):
                    if isinstance(value.value, str):
                        continue
                    terms.append(GeneratedTerm(
                        expr=BinaryTerm("+", SymbolRef(left_name), Constant(value.value)),
                        display=f"{left_name} + {value.value}",
                        field_names=(left_name,),
                        has_field_reference=True,
                        ordered_numeric=True,
                        comparison_group=comparison_group,
                        value_type=combine_numeric_types(left_field.value_type, infer_constant_value_type(value.value)),
                        source={
                            "kind": "addition",
                            "left_field": left_name,
                            "constant": value.value,
                            "semantic_constants": build_semantic_entries("field", left_name, value),
                        },
                    ))
        return terms
    raise ValueError(f"Unsupported term template kind: {template.kind}")


def select_fields(prepared: PreparedDataset, selector: VariableSelectorSpec) -> list[str]:
    names = selector.names or list(prepared.field_specs)
    if selector.regex is not None:
        pattern = re.compile(selector.regex)
        names = [name for name in names if pattern.search(name)]
    names = [name for name in names if name in prepared.field_specs and name not in selector.exclude]
    selected: list[str] = []
    for name in names:
        field = prepared.field_specs[name]
        if selector.types and field.value_type not in selector.types:
            continue
        if selector.roles and not set(selector.roles).intersection(field.roles):
            continue
        if selector.derived_only is True and FieldRole.DERIVED not in field.roles:
            continue
        if selector.derived_only is False and FieldRole.DERIVED in field.roles:
            continue
        if selector.context_family is not None and field.context_family != selector.context_family:
            continue
        if selector.window_only is True and field.context_family is None:
            continue
        if selector.window_only is False and field.context_family is not None:
            continue
        selected.append(name)
    return selected


def compatible_fields(lhs: FieldSpec, rhs: FieldSpec, ops: list[Comparator]) -> bool:
    if any(op in {Comparator.GT, Comparator.GE, Comparator.LT, Comparator.LE} for op in ops):
        return are_numeric_fields_comparable(lhs, rhs)
    return lhs.value_type == rhs.value_type or {lhs.value_type, rhs.value_type} <= {ValueType.CATEGORICAL, ValueType.STRING}


def compatible_terms(lhs: GeneratedTerm, rhs: GeneratedTerm, ops: list[Comparator]) -> bool:
    if any(op in {Comparator.GT, Comparator.GE, Comparator.LT, Comparator.LE} for op in ops):
        if lhs.value_type not in {ValueType.INTEGER, ValueType.REAL} or rhs.value_type not in {ValueType.INTEGER, ValueType.REAL}:
            return False
        if lhs.has_field_reference and rhs.has_field_reference:
            if lhs.source.get("kind") == "scalar" or rhs.source.get("kind") == "scalar":
                return lhs.ordered_numeric and rhs.ordered_numeric
            return (
                lhs.ordered_numeric
                and rhs.ordered_numeric
                and lhs.comparison_group is not None
                and lhs.comparison_group == rhs.comparison_group
            )
        if lhs.has_field_reference:
            return lhs.ordered_numeric
        if rhs.has_field_reference:
            return rhs.ordered_numeric
        return True
    if lhs.value_type == rhs.value_type:
        if lhs.value_type in {ValueType.INTEGER, ValueType.REAL} and lhs.has_field_reference and rhs.has_field_reference:
            if lhs.ordered_numeric and rhs.ordered_numeric:
                if lhs.source.get("kind") == "scalar" or rhs.source.get("kind") == "scalar":
                    return True
                return lhs.comparison_group is not None and lhs.comparison_group == rhs.comparison_group
        return True
    if lhs.value_type in {ValueType.INTEGER, ValueType.REAL} and rhs.value_type in {ValueType.INTEGER, ValueType.REAL}:
        return True
    return {lhs.value_type, rhs.value_type} <= {ValueType.CATEGORICAL, ValueType.STRING}


def compatible_constant(field: FieldSpec, constant: Any, ops: list[Comparator]) -> bool:
    if any(op in {Comparator.GT, Comparator.GE, Comparator.LT, Comparator.LE} for op in ops):
        return is_ordered_numeric_field(field) and not isinstance(constant, str)
    return True


def select_constants(
    prepared: PreparedDataset,
    field_name: str,
    field: FieldSpec,
    selector: ConstantSelectorSpec,
) -> list[SelectedConstant]:
    if selector.mode == "explicit":
        return [SelectedConstant(value=value, label=None) for value in selector.values]
    if selector.mode == "field_constants":
        values: list[SelectedConstant] = []
        allowed_kinds = set(selector.kinds)
        for constant_spec in field.constants:
            if allowed_kinds and constant_spec.kind not in allowed_kinds:
                continue
            for value in constant_spec.values:
                values.append(SelectedConstant(value=value, label=None))
        return dedupe_selected_constants(values)
    if selector.mode == "domain":
        return [SelectedConstant(value=value, label=None) for value in list(field.domain or prepared.value_catalog.get(field_name, []))]
    series = prepared.dataframe[field_name].dropna()
    if field.value_type in {ValueType.INTEGER, ValueType.REAL}:
        values: list[SelectedConstant] = []
        for quantile in selector.quantiles:
            raw_value = series.quantile(quantile)
            value = int(round(raw_value)) if field.value_type == ValueType.INTEGER else raw_value
            values.append(SelectedConstant(value=value, label=quantile_label(quantile)))
        return dedupe_selected_constants(values)
    return [
        SelectedConstant(value=value, label=f"top{index}")
        for index, value in enumerate(series.value_counts().head(selector.top_k).index.tolist(), start=1)
    ]


def select_quantifier_constants(
    prepared: PreparedDataset,
    field_names: list[str],
    selector: ConstantSelectorSpec,
) -> list[SelectedConstant]:
    if selector.mode == "explicit":
        return [SelectedConstant(value=value, label=None) for value in selector.values]
    series = pd.concat([prepared.dataframe[field] for field in field_names], axis=0).dropna()
    if selector.mode == "domain":
        return [SelectedConstant(value=value, label=None) for value in sorted(series.drop_duplicates().tolist())]
    if pd.api.types.is_numeric_dtype(series):
        values: list[SelectedConstant] = []
        for quantile in selector.quantiles:
            raw_value = series.quantile(quantile)
            value = int(round(raw_value)) if pd.api.types.is_integer_dtype(series) else raw_value
            values.append(SelectedConstant(value=value, label=quantile_label(quantile)))
        return dedupe_selected_constants(values)
    return [
        SelectedConstant(value=value, label=f"top{index}")
        for index, value in enumerate(series.value_counts().head(selector.top_k).index.tolist(), start=1)
    ]


def infer_constant_value_type(value: Any) -> ValueType:
    if isinstance(value, bool):
        return ValueType.BOOLEAN
    if isinstance(value, int):
        return ValueType.INTEGER
    if isinstance(value, float):
        return ValueType.REAL
    return ValueType.STRING


def combine_numeric_types(lhs: ValueType | None, rhs: ValueType | None) -> ValueType:
    if ValueType.REAL in {lhs, rhs}:
        return ValueType.REAL
    return ValueType.INTEGER


def dedupe_selected_constants(values: list[SelectedConstant]) -> list[SelectedConstant]:
    seen: set[str] = set()
    deduped: list[SelectedConstant] = []
    for item in values:
        key = repr(item.value)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def build_semantic_entries(scope_kind: str, scope_name: str, constant: SelectedConstant) -> list[dict[str, Any]]:
    if not constant.label:
        return []
    return [{
        "scope_kind": scope_kind,
        "scope_name": scope_name,
        "label": constant.label,
        "value": constant.value,
    }]


def is_ordered_numeric_field(field: FieldSpec) -> bool:
    if field.value_type not in {ValueType.INTEGER, ValueType.REAL}:
        return False
    if field.enum_labels:
        return False
    return not any(constant.kind == ConstantKind.ASSIGNMENT for constant in field.constants)


def numeric_comparison_group(field: FieldSpec) -> str | None:
    if not is_ordered_numeric_field(field):
        return None
    for role in (FieldRole.SIZE, FieldRole.COUNT, FieldRole.TIME, FieldRole.SEQUENCE):
        if role in field.roles:
            return role.value
    return None


def are_numeric_fields_comparable(lhs: FieldSpec, rhs: FieldSpec) -> bool:
    if not is_ordered_numeric_field(lhs) or not is_ordered_numeric_field(rhs):
        return False
    lhs_group = numeric_comparison_group(lhs)
    rhs_group = numeric_comparison_group(rhs)
    return lhs_group is not None and lhs_group == rhs_group


def addition_comparison_group(lhs: FieldSpec, rhs: FieldSpec) -> str | None:
    if not is_ordered_numeric_field(lhs) or not is_ordered_numeric_field(rhs):
        return None
    lhs_group = numeric_comparison_group(lhs)
    rhs_group = numeric_comparison_group(rhs)
    if lhs_group is None or rhs_group is None:
        return None
    if lhs_group == rhs_group:
        return lhs_group
    if {lhs_group, rhs_group} == {FieldRole.SEQUENCE.value, FieldRole.SIZE.value}:
        return FieldRole.SEQUENCE.value
    return None


def select_context_families(prepared: PreparedDataset, template: QuantifierTemplateSpec) -> dict[str, list[str]]:
    families: dict[str, list[str]] = {}
    for family_name, field_names in prepared.context_families.items():
        sample = prepared.field_specs[field_names[0]]
        if template.selector.context_family is not None and family_name != template.selector.context_family:
            continue
        if template.selector.types and sample.value_type not in template.selector.types:
            continue
        if template.selector.roles and not set(template.selector.roles).intersection(sample.roles):
            continue
        families[family_name] = field_names
    return families


def project_quantified_family(
    family_name: str,
    family_fields: list[str],
    template: QuantifierTemplateSpec,
    op: Comparator,
    constant: SelectedConstant,
) -> tuple[Formula, str]:
    terms = tuple(SymbolRef(name) for name in family_fields)
    constant_term = Constant(constant.value)
    display = f"{template.quantifier} k in {{{', '.join(str(i) for i in range(len(family_fields)))}}}: {family_name}[k] {op.value} {constant.value}"
    if op in {Comparator.GT, Comparator.GE}:
        agg = "min" if template.quantifier == "forall" else "max"
        return Compare(op.value, FuncCall(agg, terms), constant_term), display
    if op in {Comparator.LT, Comparator.LE}:
        agg = "max" if template.quantifier == "forall" else "min"
        return Compare(op.value, FuncCall(agg, terms), constant_term), display
    grounded = tuple(Compare(op.value, SymbolRef(field), constant_term) for field in family_fields)
    if template.quantifier == "forall":
        return BoolAnd(grounded), display
    return BoolOr(grounded), display
