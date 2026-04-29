from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from netnomos.api import NetNomosMiner
from netnomos.ast import Compare, Constant, FuncCall, SymbolRef
from netnomos.dsl import parse_formula
from netnomos.learners import LearnedRule
from netnomos.specs import (
    ConstantSelectorSpec,
    DatasetSpec,
    FieldSpec,
    GrammarSpec,
    LearnerKind,
    PredicateTemplateSpec,
    SourceSpec,
    SourceType,
    ValueType,
    VariableSelectorSpec,
)


class EndToEndMiningTest(unittest.TestCase):
    def test_mining_and_entailment(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "toy.csv"
            runs_dir = Path(tmpdir) / "runs"
            pd.DataFrame([
                {"Bytes": 10, "Packets": 1, "Mtu": 5},
                {"Bytes": 11, "Packets": 2, "Mtu": 6},
                {"Bytes": 20, "Packets": 3, "Mtu": 7},
                {"Bytes": 21, "Packets": 4, "Mtu": 8},
            ]).to_csv(data_path, index=False)

            dataset = DatasetSpec(
                name="toy",
                source=SourceSpec(type=SourceType.CSV, path=str(data_path)),
                fields=[
                    FieldSpec(name="Bytes", value_type=ValueType.INTEGER, roles=["size"]),
                    FieldSpec(name="Packets", value_type=ValueType.INTEGER, roles=["count"]),
                    FieldSpec(name="Mtu", value_type=ValueType.INTEGER, roles=["size"]),
                ],
            )
            grammar = GrammarSpec(
                name="toy",
                max_clause_size=2,
                max_rules=16,
                predicate_templates=[
                    PredicateTemplateSpec(
                        name="numeric-pairs",
                        lhs=VariableSelectorSpec(names=["Bytes", "Packets", "Mtu"]),
                        operators=[">", ">="],
                        rhs_field=VariableSelectorSpec(names=["Bytes", "Packets", "Mtu"]),
                    ),
                    PredicateTemplateSpec(
                        name="numeric-constants",
                        lhs=VariableSelectorSpec(names=["Bytes", "Packets", "Mtu"]),
                        operators=[">"],
                        rhs_constant=ConstantSelectorSpec(mode="explicit", values=[0]),
                    ),
                ],
            )

            miner = NetNomosMiner(dataset, grammar, runs_dir=runs_dir)
            result1 = miner.fit(data_path, learner=LearnerKind.HITTING_SET)
            self.assertFalse(result1.fit_metadata["evidence_cache_hit"])
            cache_path = Path(result1.fit_metadata["evidence_cache_path"])
            self.assertTrue(cache_path.exists())
            self.assertRegex(cache_path.name, r"^toy_\d{6}-\d{6}(?:_\d+)?\.pkl$")
            interpreted_predicates_path = result1.run_dir / "interpreted_predicates.clj"
            self.assertTrue(interpreted_predicates_path.exists())
            interpreted_predicates = interpreted_predicates_path.read_text().splitlines()
            self.assertEqual(interpreted_predicates, result1.interpreted_predicates)
            self.assertIn("Bytes > Mtu", interpreted_predicates)

            result2 = miner.fit(data_path, learner=LearnerKind.HITTING_SET)
            self.assertTrue(result2.fit_metadata["evidence_cache_hit"])
            self.assertEqual(result2.fit_metadata["evidence_cache_path"], str(cache_path))
            index = json.loads((runs_dir / ".cache" / "evidence" / "index.json").read_text())
            self.assertTrue(index["entries"])

            displays = {rule.display for rule in result2.rules}
            self.assertIn("Bytes > Mtu", displays)
            self.assertTrue(miner.entails("Bytes > Mtu"))

    def test_semantic_value_artifacts_are_written(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "toy.csv"
            runs_dir = Path(tmpdir) / "runs"
            pd.DataFrame([
                {"Bytes": 10},
                {"Bytes": 20},
                {"Bytes": 30},
                {"Bytes": 40},
            ]).to_csv(data_path, index=False)

            dataset = DatasetSpec(
                name="toy",
                source=SourceSpec(type=SourceType.CSV, path=str(data_path)),
                fields=[
                    FieldSpec(name="Bytes", value_type=ValueType.INTEGER, roles=["size"]),
                ],
            )
            grammar = GrammarSpec(
                name="toy",
                max_clause_size=1,
                max_rules=8,
                predicate_templates=[
                    PredicateTemplateSpec(
                        name="numeric-constants",
                        lhs=VariableSelectorSpec(names=["Bytes"]),
                        operators=[">=", "<="],
                        rhs_constant=ConstantSelectorSpec(mode="profile", quantiles=[0.5, 0.9]),
                    ),
                ],
            )

            miner = NetNomosMiner(dataset, grammar, runs_dir=runs_dir)
            result = miner.fit(data_path, learner=LearnerKind.HITTING_SET)

            semantic_values_path = result.run_dir / "semantic_values.json"
            self.assertTrue(semantic_values_path.exists())
            semantic_values = json.loads(semantic_values_path.read_text())
            self.assertEqual(semantic_values["fields"]["Bytes"]["p50"], 25)
            self.assertEqual(semantic_values["fields"]["Bytes"]["p90"], 37)
            self.assertIn("Bytes <= p50", result.interpreted_predicates)

    def test_validate_and_entail_arithmetic_rules(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "toy.csv"
            pd.DataFrame([
                {"Packets": 1, "Bytes": 65535, "Header": 20, "MTU": 70000},
                {"Packets": 2, "Bytes": 200000, "Header": 40, "MTU": 250000},
            ]).to_csv(data_path, index=False)

            dataset = DatasetSpec(
                name="toy",
                source=SourceSpec(type=SourceType.CSV, path=str(data_path)),
                fields=[
                    FieldSpec(name="Packets", value_type=ValueType.INTEGER),
                    FieldSpec(name="Bytes", value_type=ValueType.INTEGER),
                    FieldSpec(name="Header", value_type=ValueType.INTEGER),
                    FieldSpec(name="MTU", value_type=ValueType.INTEGER),
                ],
            )
            miner = NetNomosMiner(dataset, GrammarSpec(name="toy"), runs_dir=Path(tmpdir) / "runs")
            rules = [
                LearnedRule(
                    rule_id="r0",
                    formula=parse_formula("Packets * 65535 <= Bytes"),
                    display="Packets * 65535 <= Bytes",
                    support=1.0,
                    source={},
                ),
                LearnedRule(
                    rule_id="r1",
                    formula=parse_formula("Bytes + Header <= MTU"),
                    display="Bytes + Header <= MTU",
                    support=1.0,
                    source={},
                ),
            ]

            validation = miner.validate_rules(rules, input_path=data_path)
            self.assertTrue(validation["all_rows_satisfied"])
            self.assertTrue(miner.entails_with_rules("Packets * 65535 <= Bytes", rules, input_path=data_path))
            self.assertTrue(miner.entails_with_rules("Bytes + Header <= MTU", rules, input_path=data_path))

    def test_validate_mod_rules(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "toy.csv"
            pd.DataFrame([
                {"TcpHdrLen": 20},
                {"TcpHdrLen": 24},
            ]).to_csv(data_path, index=False)

            dataset = DatasetSpec(
                name="toy",
                source=SourceSpec(type=SourceType.CSV, path=str(data_path)),
                fields=[
                    FieldSpec(name="TcpHdrLen", value_type=ValueType.INTEGER),
                ],
            )
            miner = NetNomosMiner(dataset, GrammarSpec(name="toy"), runs_dir=Path(tmpdir) / "runs")
            rules = [
                LearnedRule(
                    rule_id="r0",
                    formula=Compare("=", FuncCall("mod", (SymbolRef("TcpHdrLen"), Constant(4))), Constant(0)),
                    display="MOD(TcpHdrLen, 4) = 0",
                    support=1.0,
                    source={},
                ),
            ]

            validation = miner.validate_rules(rules, input_path=data_path)
            self.assertTrue(validation["all_rows_satisfied"])

    def test_manifest_separates_configured_and_auto_exclusions(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "toy.csv"
            runs_dir = Path(tmpdir) / "runs"
            pd.DataFrame([
                {"keep": 1, "drop_by_spec": 10, "drop_incomplete": 100},
                {"keep": 2, "drop_by_spec": 11, "drop_incomplete": None},
            ]).to_csv(data_path, index=False)

            dataset = DatasetSpec(
                name="toy",
                source=SourceSpec(type=SourceType.CSV, path=str(data_path)),
                fields=[
                    FieldSpec(name="keep", value_type=ValueType.INTEGER),
                    FieldSpec(name="drop_by_spec", value_type=ValueType.INTEGER),
                    FieldSpec(name="drop_incomplete", value_type=ValueType.INTEGER),
                ],
                include_fields=["keep", "drop_by_spec", "drop_incomplete"],
                exclude_fields=["drop_by_spec"],
            )
            grammar = GrammarSpec(
                name="toy",
                max_clause_size=1,
                max_rules=4,
                predicate_templates=[
                    PredicateTemplateSpec(
                        name="keep-threshold",
                        lhs=VariableSelectorSpec(names=["keep"]),
                        operators=[">="],
                        rhs_constant=ConstantSelectorSpec(mode="explicit", values=[0]),
                    ),
                ],
            )

            miner = NetNomosMiner(dataset, grammar, runs_dir=runs_dir)
            result = miner.fit(data_path, learner=LearnerKind.HITTING_SET)

            self.assertEqual(result.prepared.configured_exclude_fields, ["drop_by_spec"])
            self.assertIn("drop_incomplete", result.prepared.excluded_fields)
            self.assertEqual(
                result.prepared.effective_excluded_fields,
                ["drop_by_spec", "drop_incomplete"],
            )

            manifest = json.loads((result.run_dir / "manifest.json").read_text())
            self.assertEqual(manifest["configured_exclude_fields"], ["drop_by_spec"])
            self.assertEqual(manifest["excluded_fields"], ["drop_by_spec", "drop_incomplete"])
            self.assertIn("drop_incomplete", manifest["auto_excluded_fields"])

    def test_golden_rule_artifacts_exist(self) -> None:
        expected_counts = {
            "golden_cidds": 111,
            "golden_mawi": 942,
            "golden_metadc": 21,
            "golden_netflix": 111,
            "golden_netflix_full": 1006,
        }
        for name, count in expected_counts.items():
            rules_path = Path("rules") / name / "rules.json"
            interpreted_path = Path("rules") / name / "interpreted_rules.clj"
            metadata_path = Path("rules") / name / "metadata.json"
            self.assertTrue(rules_path.exists(), rules_path)
            self.assertTrue(interpreted_path.exists(), interpreted_path)
            self.assertTrue(metadata_path.exists(), metadata_path)
            rules = json.loads(rules_path.read_text())
            self.assertEqual(len(rules), count)
            interpreted = [line for line in interpreted_path.read_text().splitlines() if line.strip()]
            self.assertEqual(len(interpreted), count)


if __name__ == "__main__":
    unittest.main()
