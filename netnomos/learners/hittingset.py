from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import pickle
from pathlib import Path
import time
from typing import Any

import numpy as np
from tqdm.auto import tqdm

from netnomos.ast import BoolOr, Compare, Constant, Formula, SymbolRef, formula_to_dict, formula_to_string
from netnomos.dataset import PreparedDataset
from netnomos.logging_utils import get_logger
from netnomos.projection import GroundedPredicate
from netnomos.theory import evaluate_formula_df

log = get_logger("hittingset")


@dataclass(slots=True)
class LearnedRule:
    rule_id: str
    formula: Formula
    display: str
    support: float
    source: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "formula": formula_to_dict(self.formula),
            "display": self.display,
            "support": self.support,
            "source": self.source,
        }


class HittingSetLearner:
    def __init__(
        self,
        max_clause_size: int = 4,
        max_rules: int = 250,
        stall_timeout: float | None = None,
        clock: Callable[[], float] | None = None,
    ):
        if stall_timeout is not None and stall_timeout < 0:
            raise ValueError("stall_timeout must be non-negative when provided")
        self.max_clause_size = max_clause_size
        self.max_rules = max_rules
        self.stall_timeout = stall_timeout
        self._clock = clock or time.monotonic
        self.last_fit_metadata: dict[str, Any] = {}

    def fit(
        self,
        predicates: list[GroundedPredicate],
        prepared: PreparedDataset,
        evidence_cache_path: str | Path | None = None,
    ) -> list[LearnedRule]:
        evidence_sets, cache_metadata = self._load_or_build_evidence_sets(
            predicates,
            prepared,
            evidence_cache_path=evidence_cache_path,
        )
        covers, search_metadata = self.enumerate_minimal_hitting_sets(evidence_sets)
        rules: list[LearnedRule] = []
        for index, cover in enumerate(covers):
            formulas = tuple(predicates[predicate_index].formula for predicate_index in sorted(cover))
            formula = BoolOr(formulas) if len(formulas) > 1 else formulas[0]
            display = " OR ".join(predicates[predicate_index].display for predicate_index in sorted(cover))
            support = float(evaluate_formula_df(formula, prepared).mean())
            rules.append(LearnedRule(
                rule_id=f"hs{index:05d}",
                formula=formula,
                display=display,
                support=support,
                source={
                    "learner": "hitting-set",
                    "predicate_ids": [predicates[predicate_index].predicate_id for predicate_index in sorted(cover)],
                },
            ))
        pruned_rules = self.prune_tautologies(rules)
        if search_metadata["search_stopped_early"]:
            log.warning(
                "Stopping hitting-set search after %.2fs without a new rule; returning %d partial rules.",
                search_metadata.get("stall_elapsed_seconds") or 0.0,
                len(pruned_rules),
            )
        self.last_fit_metadata = {
            **cache_metadata,
            **search_metadata,
            "rule_count_before_prune": len(rules),
            "rule_count_after_prune": len(pruned_rules),
            "evidence_set_count": len(evidence_sets),
        }
        return pruned_rules

    def enumerate_minimal_hitting_sets(self, evidence_sets: list[set[int]]) -> tuple[list[set[int]], dict[str, Any]]:
        if not evidence_sets:
            return [], {
                "search_stopped_early": False,
                "stop_reason": "complete",
                "stall_timeout_seconds": self.stall_timeout,
                "stall_elapsed_seconds": 0.0,
                "search_elapsed_seconds": 0.0,
            }
        idx_by_pred: dict[int, set[int]] = {}
        for evidence_index, evidence in enumerate(evidence_sets):
            for predicate_index in evidence:
                idx_by_pred.setdefault(predicate_index, set()).add(evidence_index)
        universe = set(range(len(evidence_sets)))
        solutions: list[set[int]] = []
        start_time = self._clock()
        last_solution_time = start_time
        stopped_early = False
        hit_max_rules = False
        progress = tqdm(
            total=self.max_rules,
            desc="Enumerating rules",
            unit=" rule",
            disable=None,
        )

        def has_subset(candidate: set[int]) -> bool:
            return any(solution <= candidate for solution in solutions)

        def is_stalled() -> bool:
            if self.stall_timeout is None:
                return False
            return (self._clock() - last_solution_time) >= self.stall_timeout

        def branch(chosen: set[int], covered: set[int]) -> None:
            nonlocal hit_max_rules, last_solution_time, stopped_early
            if hit_max_rules or stopped_early:
                return
            if is_stalled():
                stopped_early = True
                return
            if len(solutions) >= self.max_rules:
                hit_max_rules = True
                return
            if covered == universe:
                if not has_subset(chosen):
                    solutions[:] = [solution for solution in solutions if not chosen < solution]
                    solutions.append(set(chosen))
                    last_solution_time = self._clock()
                    progress.n = len(solutions)
                    progress.refresh()
                return
            if len(chosen) >= self.max_clause_size:
                return
            uncovered = universe - covered
            pivot = min(uncovered, key=lambda item: len(evidence_sets[item]))
            candidates = sorted(evidence_sets[pivot], key=lambda pred: len(idx_by_pred.get(pred, set()) & uncovered), reverse=True)
            for predicate_index in candidates:
                if hit_max_rules or stopped_early:
                    return
                if is_stalled():
                    stopped_early = True
                    return
                if predicate_index in chosen:
                    continue
                next_chosen = set(chosen)
                next_chosen.add(predicate_index)
                if has_subset(next_chosen):
                    continue
                branch(next_chosen, covered | idx_by_pred.get(predicate_index, set()))

        try:
            branch(set(), set())
        finally:
            progress.close()
        end_time = self._clock()
        if stopped_early:
            stop_reason = "stall-timeout"
        elif hit_max_rules:
            stop_reason = "max-rules"
        else:
            stop_reason = "complete"
        return solutions, {
            "search_stopped_early": stopped_early,
            "stop_reason": stop_reason,
            "stall_timeout_seconds": self.stall_timeout,
            "stall_elapsed_seconds": end_time - last_solution_time,
            "search_elapsed_seconds": end_time - start_time,
        }

    def _load_or_build_evidence_sets(
        self,
        predicates: list[GroundedPredicate],
        prepared: PreparedDataset,
        evidence_cache_path: str | Path | None = None,
    ) -> tuple[list[set[int]], dict[str, Any]]:
        cache_path = Path(evidence_cache_path) if evidence_cache_path is not None else None
        if cache_path is not None and cache_path.exists():
            with cache_path.open("rb") as handle:
                payload = pickle.load(handle)
            evidence_sets = [set(entry) for entry in payload["evidence_sets"]]
            return evidence_sets, {
                "evidence_cache_hit": True,
                "evidence_cache_path": str(cache_path),
            }

        evidence_sets: list[set[int]] = [set() for _ in range(len(prepared.dataframe))]
        for predicate_index, predicate in enumerate(tqdm(
            predicates,
            total=len(predicates),
            desc="Building evidence sets",
            unit=" predicate",
            disable=None,
        )):
            sat = evaluate_formula_df(predicate.formula, prepared)
            rows = np.flatnonzero(sat.to_numpy())
            for row_index in rows.tolist():
                evidence_sets[row_index].add(predicate_index)

        evidence_sets = [evidence for evidence in evidence_sets if evidence]
        if cache_path is not None:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            with cache_path.open("wb") as handle:
                pickle.dump({
                    "evidence_sets": [sorted(entry) for entry in evidence_sets],
                    "row_count": len(prepared.dataframe),
                    "predicate_count": len(predicates),
                }, handle)
        return evidence_sets, {
            "evidence_cache_hit": False,
            "evidence_cache_path": str(cache_path) if cache_path is not None else None,
        }

    def prune_tautologies(self, rules: list[LearnedRule]) -> list[LearnedRule]:
        pruned: list[LearnedRule] = []
        for rule in rules:
            if not isinstance(rule.formula, BoolOr):
                pruned.append(rule)
                continue
            signatures: dict[tuple[str, Any], set[str]] = {}
            tautology = False
            for literal in rule.formula.values:
                if not isinstance(literal, Compare):
                    continue
                if not isinstance(literal.left, SymbolRef) or not isinstance(literal.right, Constant):
                    continue
                key = (literal.left.name, literal.right.value)
                seen = signatures.setdefault(key, set())
                seen.add(literal.op)
                if {"=", "!="} <= seen or {">", "<="} <= seen or {">=", "<"} <= seen:
                    tautology = True
                    break
            if not tautology:
                pruned.append(rule)
        return pruned
