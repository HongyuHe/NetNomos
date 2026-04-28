from __future__ import annotations

import json
from typing import Any

from netnomos.ast import BinaryTerm, FuncCall, IndexedRef, SymbolRef, Term
from netnomos.specs import FieldSpec


def make_value_key(value: Any) -> str:
    return json.dumps(value, sort_keys=True, default=str)


def quantile_label(quantile: float) -> str:
    percent = quantile * 100
    rounded = round(percent)
    if abs(percent - rounded) < 1e-9:
        return f"p{int(rounded)}"
    sanitized = str(round(percent, 3)).replace(".", "_")
    return f"p{sanitized}"


def build_semantic_value_catalog(predicates: list[Any]) -> dict[str, dict[str, dict[str, Any]]]:
    catalog: dict[str, dict[str, dict[str, Any]]] = {
        "fields": {},
        "families": {},
    }
    for predicate in predicates:
        for entry in iter_semantic_entries(getattr(predicate, "source", {})):
            label = entry.get("label")
            if not label:
                continue
            scope_kind = entry.get("scope_kind")
            scope_name = entry.get("scope_name")
            value = entry.get("value")
            catalog_key = f"{scope_kind}s"
            if catalog_key not in catalog or not scope_name:
                continue
            catalog[catalog_key].setdefault(scope_name, {})
            catalog[catalog_key][scope_name].setdefault(label, value)
    return catalog


def iter_semantic_entries(payload: Any) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    if isinstance(payload, dict):
        raw_entries = payload.get("semantic_constants", [])
        if isinstance(raw_entries, list):
            entries.extend(entry for entry in raw_entries if isinstance(entry, dict))
        for value in payload.values():
            entries.extend(iter_semantic_entries(value))
    elif isinstance(payload, list):
        for item in payload:
            entries.extend(iter_semantic_entries(item))
    return entries


def lookup_semantic_label(
    term: Term,
    value: Any,
    fields: dict[str, FieldSpec],
    catalog: dict[str, dict[str, dict[str, Any]]] | None,
) -> str | None:
    if not catalog:
        return None
    value_key = make_value_key(value)
    field_name = resolve_field_reference(term)
    if field_name is not None:
        label = lookup_scope_label(catalog.get("fields", {}), field_name, value_key)
        if label is not None:
            return label
    family_name = resolve_family_reference(term, fields)
    if family_name is not None:
        return lookup_scope_label(catalog.get("families", {}), family_name, value_key)
    return None


def lookup_scope_label(scope_catalog: dict[str, dict[str, Any]], scope_name: str, value_key: str) -> str | None:
    labels = scope_catalog.get(scope_name, {})
    for label, raw_value in labels.items():
        if make_value_key(raw_value) == value_key:
            return label
    return None


def resolve_field_reference(term: Term) -> str | None:
    symbols = collect_symbol_refs(term)
    if len(symbols) == 1:
        return symbols[0]
    return None


def resolve_family_reference(term: Term, fields: dict[str, FieldSpec]) -> str | None:
    symbols = collect_symbol_refs(term)
    families = {
        fields[name].context_family
        for name in symbols
        if name in fields and fields[name].context_family is not None
    }
    if len(families) == 1:
        return next(iter(families))
    return None


def collect_symbol_refs(term: Term) -> list[str]:
    if isinstance(term, SymbolRef):
        return [term.name]
    if isinstance(term, IndexedRef):
        return []
    if isinstance(term, BinaryTerm):
        return [*collect_symbol_refs(term.left), *collect_symbol_refs(term.right)]
    if isinstance(term, FuncCall):
        refs: list[str] = []
        for arg in term.args:
            refs.extend(collect_symbol_refs(arg))
        return refs
    return []
