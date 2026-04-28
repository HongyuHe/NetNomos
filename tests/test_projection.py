from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from netnomos.dataset import prepare_dataset
from netnomos.interpreter import interpret_formula
from netnomos.projection import generate_predicates
from netnomos.semantic_values import build_semantic_value_catalog
from netnomos.specs import (
    ConstantKind,
    ConstantSelectorSpec,
    DatasetSpec,
    FieldConstantSpec,
    FieldSpec,
    FieldRole,
    GrammarSpec,
    PredicateTemplateSpec,
    PredicateTermKind,
    SourceSpec,
    SourceType,
    TermTemplateSpec,
    ValueType,
    VariableSelectorSpec,
)


class ProjectionTest(unittest.TestCase):
    def test_generate_scalar_and_addition_predicates(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "toy.csv"
            pd.DataFrame([
                {"Packets": 1, "Bytes": 65535, "Header": 20, "MTU": 1500},
                {"Packets": 2, "Bytes": 150000, "Header": 40, "MTU": 200000},
            ]).to_csv(path, index=False)

            dataset = DatasetSpec(
                name="toy",
                source=SourceSpec(type=SourceType.CSV, path=str(path)),
                fields=[
                    FieldSpec(
                        name="Packets",
                        value_type=ValueType.INTEGER,
                        roles=[FieldRole.COUNT],
                        constants=[FieldConstantSpec(kind=ConstantKind.SCALAR, values=[65535])],
                    ),
                    FieldSpec(name="Bytes", value_type=ValueType.INTEGER, roles=[FieldRole.SIZE]),
                    FieldSpec(name="Header", value_type=ValueType.INTEGER, roles=[FieldRole.SIZE]),
                    FieldSpec(name="MTU", value_type=ValueType.INTEGER, roles=[FieldRole.SIZE]),
                ],
            )
            grammar = GrammarSpec(
                name="toy",
                predicate_templates=[
                    PredicateTemplateSpec(
                        name="scalar-bound",
                        lhs_term=TermTemplateSpec(
                            kind=PredicateTermKind.SCALAR,
                            field=VariableSelectorSpec(names=["Packets"]),
                            constant=ConstantSelectorSpec(mode="field_constants", kinds=[ConstantKind.SCALAR]),
                        ),
                        operators=["<="],
                        rhs_term=TermTemplateSpec(
                            kind=PredicateTermKind.FIELD,
                            field=VariableSelectorSpec(names=["Bytes"]),
                        ),
                    ),
                    PredicateTemplateSpec(
                        name="addition-bound",
                        lhs_term=TermTemplateSpec(
                            kind=PredicateTermKind.ADDITION,
                            field=VariableSelectorSpec(names=["Bytes"]),
                            other_field=VariableSelectorSpec(names=["Header"]),
                        ),
                        operators=["<="],
                        rhs_term=TermTemplateSpec(
                            kind=PredicateTermKind.FIELD,
                            field=VariableSelectorSpec(names=["MTU"]),
                        ),
                    ),
                ],
            )

            predicates = generate_predicates(prepare_dataset(dataset), grammar)
            displays = {predicate.display for predicate in predicates}
            self.assertIn("(Packets * 65535) <= Bytes", displays)
            self.assertIn("(Bytes + Header) <= MTU", displays)

    def test_reject_symbolic_numeric_thresholds_and_cross_role_additions(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "toy.csv"
            pd.DataFrame([
                {"Bytes": 64, "Duration": 0.01, "DstPortClass": 443},
                {"Bytes": 128, "Duration": 0.10, "DstPortClass": 71000},
                {"Bytes": 1500, "Duration": 1.20, "DstPortClass": 72000},
            ]).to_csv(path, index=False)

            dataset = DatasetSpec(
                name="toy",
                source=SourceSpec(type=SourceType.CSV, path=str(path)),
                fields=[
                    FieldSpec(
                        name="Bytes",
                        value_type=ValueType.INTEGER,
                        roles=[FieldRole.SIZE, FieldRole.MEASUREMENT],
                        constants=[FieldConstantSpec(kind=ConstantKind.ADDITION, values=[20, 40])],
                    ),
                    FieldSpec(
                        name="Duration",
                        value_type=ValueType.REAL,
                        roles=[FieldRole.TIME, FieldRole.MEASUREMENT],
                    ),
                    FieldSpec(
                        name="DstPortClass",
                        value_type=ValueType.INTEGER,
                        roles=[FieldRole.DST, FieldRole.IDENTIFIER],
                        constants=[FieldConstantSpec(kind=ConstantKind.ASSIGNMENT, values=[443, 71000, 72000])],
                        enum_labels={"443": "https", "71000": "registered", "72000": "dynamic"},
                    ),
                ],
            )
            grammar = GrammarSpec(
                name="toy",
                predicate_templates=[
                    PredicateTemplateSpec(
                        name="numeric-thresholds",
                        lhs=VariableSelectorSpec(types=[ValueType.INTEGER, ValueType.REAL]),
                        operators=[">=", "<="],
                        rhs_constant=ConstantSelectorSpec(mode="profile", quantiles=[0.5]),
                    ),
                    PredicateTemplateSpec(
                        name="numeric-offsets",
                        lhs_term=TermTemplateSpec(
                            kind=PredicateTermKind.ADDITION,
                            field=VariableSelectorSpec(types=[ValueType.INTEGER, ValueType.REAL]),
                            constant=ConstantSelectorSpec(mode="field_constants", kinds=[ConstantKind.ADDITION]),
                        ),
                        operators=["<=", ">="],
                        rhs_term=TermTemplateSpec(
                            kind=PredicateTermKind.FIELD,
                            field=VariableSelectorSpec(types=[ValueType.INTEGER, ValueType.REAL]),
                        ),
                    ),
                ],
            )

            predicates = generate_predicates(prepare_dataset(dataset), grammar)
            displays = {predicate.display for predicate in predicates}
            self.assertIn("Bytes <= 128", displays)
            self.assertIn("Duration <= 0.1", displays)
            self.assertNotIn("DstPortClass >= 71000", displays)
            self.assertNotIn("(Bytes + 20) <= Duration", displays)
            self.assertNotIn("(Bytes + 40) >= DstPortClass", displays)

    def test_semantic_labels_for_profiled_constants(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "toy.csv"
            pd.DataFrame([
                {"Bytes": 10, "Proto": "TCP"},
                {"Bytes": 20, "Proto": "TCP"},
                {"Bytes": 30, "Proto": "UDP"},
            ]).to_csv(path, index=False)

            dataset = DatasetSpec(
                name="toy",
                source=SourceSpec(type=SourceType.CSV, path=str(path)),
                fields=[
                    FieldSpec(name="Bytes", value_type=ValueType.INTEGER, roles=[FieldRole.SIZE]),
                    FieldSpec(name="Proto", value_type=ValueType.CATEGORICAL, roles=[FieldRole.PROTO]),
                ],
            )
            grammar = GrammarSpec(
                name="toy",
                predicate_templates=[
                    PredicateTemplateSpec(
                        name="numeric-thresholds",
                        lhs=VariableSelectorSpec(names=["Bytes"]),
                        operators=["<=", ">="],
                        rhs_constant=ConstantSelectorSpec(mode="profile", quantiles=[0.5]),
                    ),
                    PredicateTemplateSpec(
                        name="categorical-values",
                        lhs=VariableSelectorSpec(names=["Proto"]),
                        operators=["=", "!="],
                        rhs_constant=ConstantSelectorSpec(mode="profile", top_k=1),
                    ),
                ],
            )

            prepared = prepare_dataset(dataset)
            predicates = generate_predicates(prepared, grammar)
            semantic_values = build_semantic_value_catalog(predicates)
            interpreted = {
                interpret_formula(predicate.formula, prepared.field_specs, semantic_values)
                for predicate in predicates
            }

            self.assertEqual(semantic_values["fields"]["Bytes"]["p50"], 20)
            self.assertEqual(semantic_values["fields"]["Proto"]["top1"], "TCP")
            self.assertIn("Bytes <= p50", interpreted)
            self.assertIn("Proto = top1", interpreted)

    def test_generate_packet_sequencing_predicates(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "toy.csv"
            pd.DataFrame([
                {"tcp.seq_ctx0": 100, "tcp.ack_ctx0": 101, "frame.len_ctx0": 40},
                {"tcp.seq_ctx0": 200, "tcp.ack_ctx0": 260, "frame.len_ctx0": 60},
            ]).to_csv(path, index=False)

            dataset = DatasetSpec(
                name="toy",
                source=SourceSpec(type=SourceType.CSV, path=str(path)),
                fields=[
                    FieldSpec(
                        name="tcp.seq_ctx0",
                        value_type=ValueType.INTEGER,
                        roles=[FieldRole.SEQUENCE],
                        constants=[FieldConstantSpec(kind=ConstantKind.ADDITION, values=[1])],
                    ),
                    FieldSpec(
                        name="tcp.ack_ctx0",
                        value_type=ValueType.INTEGER,
                        roles=[FieldRole.SEQUENCE],
                    ),
                    FieldSpec(
                        name="frame.len_ctx0",
                        value_type=ValueType.INTEGER,
                        roles=[FieldRole.SIZE],
                    ),
                ],
            )
            grammar = GrammarSpec(
                name="toy",
                predicate_templates=[
                    PredicateTemplateSpec(
                        name="seq-ack-step",
                        lhs_term=TermTemplateSpec(
                            kind=PredicateTermKind.ADDITION,
                            field=VariableSelectorSpec(names=["tcp.seq_ctx0"]),
                            constant=ConstantSelectorSpec(mode="field_constants", kinds=[ConstantKind.ADDITION]),
                        ),
                        operators=["="],
                        rhs_term=TermTemplateSpec(
                            kind=PredicateTermKind.FIELD,
                            field=VariableSelectorSpec(names=["tcp.ack_ctx0"]),
                        ),
                    ),
                    PredicateTemplateSpec(
                        name="seq-frame-len-bound",
                        lhs_term=TermTemplateSpec(
                            kind=PredicateTermKind.ADDITION,
                            field=VariableSelectorSpec(names=["tcp.seq_ctx0"]),
                            other_field=VariableSelectorSpec(names=["frame.len_ctx0"]),
                        ),
                        operators=["<="],
                        rhs_term=TermTemplateSpec(
                            kind=PredicateTermKind.FIELD,
                            field=VariableSelectorSpec(names=["tcp.ack_ctx0"]),
                        ),
                    ),
                ],
            )

            predicates = generate_predicates(prepare_dataset(dataset), grammar)
            displays = {predicate.display for predicate in predicates}
            self.assertIn("(tcp.seq_ctx0 + 1) = tcp.ack_ctx0", displays)
            self.assertIn("(tcp.seq_ctx0 + frame.len_ctx0) <= tcp.ack_ctx0", displays)


if __name__ == "__main__":
    unittest.main()
