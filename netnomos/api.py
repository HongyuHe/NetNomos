from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
from pathlib import Path
from typing import Any

from netnomos.artifacts import ArtifactStore
from netnomos.ast import Formula, formula_from_dict, formula_to_dict
from netnomos.dataset import PreparedDataset, prepare_dataset
from netnomos.dsl import parse_formula
from netnomos.interpreter import interpret_formula
from netnomos.learners import EntropyTreeLearner, HittingSetLearner, LearnedRule
from netnomos.logging_utils import get_logger
from netnomos.projection import GroundedPredicate, generate_predicates
from netnomos.semantic_values import build_semantic_value_catalog
from netnomos.specs import (
    DatasetSpec,
    GrammarSpec,
    HittingSetBackend,
    LearnerKind,
    load_dataset_spec,
    load_grammar_spec,
)
from netnomos.theory import Theory

log = get_logger("api")


@dataclass(slots=True)
class MiningResult:
    run_dir: Path
    prepared: PreparedDataset
    predicates: list[GroundedPredicate]
    interpreted_predicates: list[str]
    rules: list[LearnedRule]
    interpreted_rules: list[str]
    semantic_values: dict[str, dict[str, dict[str, Any]]]
    fit_metadata: dict[str, Any]


class NetNomosMiner:
    def __init__(self, dataset_spec: DatasetSpec, grammar_spec: GrammarSpec, runs_dir: str | Path = "runs"):
        self.dataset_spec = dataset_spec
        self.grammar_spec = grammar_spec
        self.runs_dir = Path(runs_dir)
        self.last_result: MiningResult | None = None

    @classmethod
    def from_files(
        cls,
        dataset_spec: str | Path,
        grammar_spec: str | Path,
        runs_dir: str | Path = "runs",
    ) -> "NetNomosMiner":
        return cls(
            dataset_spec=load_dataset_spec(dataset_spec),
            grammar_spec=load_grammar_spec(grammar_spec),
            runs_dir=runs_dir,
        )

    def prepare(self, input_path: str | Path | None = None, limit: int | None = None) -> PreparedDataset:
        return prepare_dataset(self.dataset_spec, input_path=input_path, limit=limit)

    def fit(
        self,
        input_path: str | Path | None = None,
        learner: LearnerKind | str = LearnerKind.HITTING_SET,
        limit: int | None = None,
        stall_timeout: float | None = None,
        hitting_set_backend: HittingSetBackend | str = HittingSetBackend.AUTO,
    ) -> MiningResult:
        prepared = self.prepare(input_path=input_path, limit=limit)
        predicates = generate_predicates(prepared, self.grammar_spec)
        learner_kind = LearnerKind(learner)
        if learner_kind == LearnerKind.HITTING_SET:
            evidence_cache_path = self._build_evidence_cache_path(input_path, limit, prepared, predicates)
            backend = HittingSetLearner(
                max_clause_size=self.grammar_spec.max_clause_size,
                max_rules=self.grammar_spec.max_rules,
                stall_timeout=stall_timeout,
                backend=hitting_set_backend,
            )
            rules = backend.fit(predicates, prepared, evidence_cache_path=evidence_cache_path)
        else:
            if stall_timeout is not None or HittingSetBackend(hitting_set_backend) != HittingSetBackend.AUTO:
                log.warning(
                    (
                        "Ignoring hitting-set specific options for learner '%s'; stall timeout and "
                        "hitting-set backend selection only apply to the hitting-set learner."
                    ),
                    learner_kind.value,
                )
            backend = EntropyTreeLearner(
                max_depth=self.grammar_spec.max_clause_size,
                max_rules=self.grammar_spec.max_rules,
            )
            rules = backend.fit(predicates, prepared)
        fit_metadata = getattr(backend, "last_fit_metadata", {})
        if learner_kind != LearnerKind.HITTING_SET and (
            stall_timeout is not None or HittingSetBackend(hitting_set_backend) != HittingSetBackend.AUTO
        ):
            fit_metadata = {
                **fit_metadata,
                "stall_timeout_seconds": stall_timeout,
                "stall_timeout_ignored": stall_timeout is not None,
                "hitting_set_backend_requested": HittingSetBackend(hitting_set_backend).value,
                "hitting_set_backend_ignored": True,
            }
        semantic_values = build_semantic_value_catalog(predicates)
        interpreted_predicates = [
            interpret_formula(predicate.formula, prepared.field_specs, semantic_values)
            for predicate in predicates
        ]
        interpreted_rules = [
            interpret_formula(rule.formula, prepared.field_specs, semantic_values)
            for rule in rules
        ]
        store = ArtifactStore.create(self.runs_dir, self.dataset_spec.name, self.grammar_spec.name)
        self._write_artifacts(
            store,
            prepared,
            predicates,
            interpreted_predicates,
            rules,
            interpreted_rules,
            semantic_values,
            learner_kind,
            fit_metadata,
        )
        result = MiningResult(
            run_dir=store.root,
            prepared=prepared,
            predicates=predicates,
            interpreted_predicates=interpreted_predicates,
            rules=rules,
            interpreted_rules=interpreted_rules,
            semantic_values=semantic_values,
            fit_metadata=fit_metadata,
        )
        self.last_result = result
        return result

    def entails(self, query: str | Formula, rules: list[LearnedRule] | None = None) -> bool:
        if isinstance(query, str):
            query = parse_formula(query)
        formulas = [rule.formula for rule in (rules or self._require_last_result().rules)]
        prepared = self._require_last_result().prepared
        theory = Theory(formulas=formulas, fields=prepared.field_specs, context_families=prepared.context_families)
        return theory.entails(query)

    def validate(self, rules: list[LearnedRule] | None = None) -> dict[str, Any]:
        result = self._require_last_result()
        formulas = [rule.formula for rule in (rules or result.rules)]
        theory = Theory(formulas=formulas, fields=result.prepared.field_specs, context_families=result.prepared.context_families)
        return theory.validate(result.prepared)

    def interpret(self, rules: list[LearnedRule] | None = None) -> list[str]:
        result = self._require_last_result()
        return [
            interpret_formula(rule.formula, result.prepared.field_specs, result.semantic_values)
            for rule in (rules or result.rules)
        ]

    def validate_rules(
        self,
        rules: list[LearnedRule],
        input_path: str | Path | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        prepared = self.prepare(input_path=input_path, limit=limit)
        theory = Theory(
            formulas=[rule.formula for rule in rules],
            fields=prepared.field_specs,
            context_families=prepared.context_families,
        )
        return theory.validate(prepared)

    def entails_with_rules(
        self,
        query: str | Formula,
        rules: list[LearnedRule],
        input_path: str | Path | None = None,
        limit: int | None = None,
    ) -> bool:
        if isinstance(query, str):
            query = parse_formula(query)
        prepared = self.prepare(input_path=input_path, limit=limit)
        theory = Theory(
            formulas=[rule.formula for rule in rules],
            fields=prepared.field_specs,
            context_families=prepared.context_families,
        )
        return theory.entails(query)

    def interpret_rules(
        self,
        rules: list[LearnedRule],
        input_path: str | Path | None = None,
        limit: int | None = None,
        semantic_values: dict[str, dict[str, dict[str, Any]]] | None = None,
    ) -> list[str]:
        prepared = self.prepare(input_path=input_path, limit=limit)
        return [interpret_formula(rule.formula, prepared.field_specs, semantic_values) for rule in rules]

    def load_semantic_values(self, path: str | Path) -> dict[str, dict[str, dict[str, Any]]]:
        return json.loads(Path(path).read_text())

    def load_semantic_values_for_rules(self, rules_path: str | Path) -> dict[str, dict[str, dict[str, Any]]]:
        candidate = Path(rules_path).with_name("semantic_values.json")
        if candidate.exists():
            return self.load_semantic_values(candidate)
        return {}

    def load_rules(self, path: str | Path) -> list[LearnedRule]:
        import json

        raw = json.loads(Path(path).read_text())
        rules: list[LearnedRule] = []
        for item in raw:
            rules.append(LearnedRule(
                rule_id=item["rule_id"],
                formula=formula_from_dict(item["formula"]),
                display=item.get("display", ""),
                support=float(item.get("support", 0.0)),
                source=item.get("source", {}),
            ))
        return rules

    def _write_artifacts(
        self,
        store: ArtifactStore,
        prepared: PreparedDataset,
        predicates: list[GroundedPredicate],
        interpreted_predicates: list[str],
        rules: list[LearnedRule],
        interpreted_rules: list[str],
        semantic_values: dict[str, dict[str, dict[str, Any]]],
        learner_kind: LearnerKind,
        fit_metadata: dict[str, Any],
    ) -> None:
        store.write_json("dataset_spec.json", self.dataset_spec.model_dump(mode="json"))
        store.write_json("grammar_spec.json", self.grammar_spec.model_dump(mode="json"))
        store.write_json("fields.json", {name: field.model_dump(mode="json") for name, field in prepared.field_specs.items()})
        store.write_json("derived_variables.json", prepared.derived_provenance)
        store.write_json("configured_exclude_fields.json", prepared.configured_exclude_fields)
        store.write_json("excluded_fields.json", prepared.excluded_fields)
        store.write_json("semantic_values.json", semantic_values)
        store.write_json("manifest.json", {
            "dataset": self.dataset_spec.name,
            "grammar": self.grammar_spec.name,
            "learner": learner_kind.value,
            "source_type": prepared.source_type.value,
            "row_count": len(prepared.dataframe),
            "configured_exclude_fields": prepared.configured_exclude_fields,
            "auto_excluded_fields": prepared.excluded_fields,
            "excluded_fields": prepared.effective_excluded_fields,
            "predicate_count": len(predicates),
            "rule_count": len(rules),
            "fit_metadata": fit_metadata,
        })
        store.write_jsonl("predicates.jsonl", [{
            "predicate_id": predicate.predicate_id,
            "display": predicate.display,
            "support": predicate.support,
            "formula": formula_to_dict(predicate.formula),
            "source": predicate.source,
        } for predicate in predicates])
        store.write_text("interpreted_predicates.clj", "\n".join(interpreted_predicates))
        store.write_json("rules.json", [rule.to_dict() for rule in rules])
        store.write_text("interpreted_rules.clj", "\n".join(interpreted_rules))

    def _require_last_result(self) -> MiningResult:
        if self.last_result is None:
            raise RuntimeError("No result available. Run fit() first.")
        return self.last_result

    def _build_evidence_cache_path(
        self,
        input_path: str | Path | None,
        limit: int | None,
        prepared: PreparedDataset,
        predicates: list[GroundedPredicate],
    ) -> Path:
        cache_key = self._build_evidence_cache_key(input_path, limit, prepared, predicates)
        cache_dir = self.runs_dir / ".cache" / "evidence"
        index_path = cache_dir / "index.json"
        index = self._load_evidence_cache_index(index_path)
        filename = index.get(cache_key)
        if filename is not None:
            cache_path = cache_dir / filename
            if cache_path.exists():
                return cache_path
            index.pop(cache_key, None)
        cache_path = self._allocate_evidence_cache_path(cache_dir)
        index[cache_key] = cache_path.name
        self._write_evidence_cache_index(index_path, index)
        return cache_path

    def _build_evidence_cache_key(
        self,
        input_path: str | Path | None,
        limit: int | None,
        prepared: PreparedDataset,
        predicates: list[GroundedPredicate],
    ) -> str:
        source_path = Path(input_path or self.dataset_spec.source.path or "")
        source_meta: dict[str, Any] = {
            "limit": limit,
        }
        if source_path.exists():
            stat = source_path.stat()
            source_meta |= {
                "path": str(source_path.resolve()),
                "size": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
            }
        payload = {
            "cache_version": 1,
            "source": source_meta,
            "prepared": {
                "row_count": len(prepared.dataframe),
                "columns": list(prepared.dataframe.columns),
                "field_specs": {
                    name: field.model_dump(mode="json")
                    for name, field in prepared.field_specs.items()
                },
                "derived_provenance": prepared.derived_provenance,
            },
            "predicates": [
                {
                    "display": predicate.display,
                    "formula": formula_to_dict(predicate.formula),
                }
                for predicate in predicates
            ],
        }
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
        ).hexdigest()

    def _allocate_evidence_cache_path(self, cache_dir: Path) -> Path:
        cache_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%y%m%d-%H%M%S")
        candidate = cache_dir / f"{self.dataset_spec.name}_{stamp}.pkl"
        if not candidate.exists():
            return candidate
        suffix = 2
        while True:
            candidate = cache_dir / f"{self.dataset_spec.name}_{stamp}_{suffix}.pkl"
            if not candidate.exists():
                return candidate
            suffix += 1

    def _load_evidence_cache_index(self, index_path: Path) -> dict[str, str]:
        if not index_path.exists():
            return {}
        payload = json.loads(index_path.read_text())
        entries = payload.get("entries", {})
        return {
            str(key): str(value)
            for key, value in entries.items()
        }

    def _write_evidence_cache_index(self, index_path: Path, entries: dict[str, str]) -> None:
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text(json.dumps({
            "version": 1,
            "entries": entries,
        }, indent=2, sort_keys=True))
