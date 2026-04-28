from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from netnomos.dataset import prepare_dataset
from netnomos.specs import (
    ContextWindowSpec,
    DatasetSpec,
    DerivedOperation,
    DerivedVariableSpec,
    FieldSpec,
    FieldRole,
    MappingRuleSpec,
    PreprocessKind,
    PreprocessStepSpec,
    SourceSpec,
    SourceType,
    ValueType,
)


class PrepareDatasetTest(unittest.TestCase):
    def test_dataset_spec_accepts_legacy_excluded_fields_key(self) -> None:
        spec = DatasetSpec.model_validate({
            "name": "toy",
            "source": {
                "type": "csv",
                "path": "toy.csv",
            },
            "fields": [],
            "excluded_fields": ["Noise"],
        })

        self.assertEqual(spec.exclude_fields, ["Noise"])

    def test_context_window_respects_partitions(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "toy.csv"
            pd.DataFrame([
                {"flow": "a", "t": 1, "x": 10},
                {"flow": "a", "t": 2, "x": 11},
                {"flow": "b", "t": 1, "x": 20},
                {"flow": "b", "t": 2, "x": 21},
            ]).to_csv(path, index=False)

            spec = DatasetSpec(
                name="toy",
                source=SourceSpec(type=SourceType.CSV, path=str(path)),
                fields=[
                    FieldSpec(name="flow", value_type=ValueType.CATEGORICAL, roles=[FieldRole.IDENTIFIER]),
                    FieldSpec(name="t", value_type=ValueType.INTEGER, roles=[FieldRole.TIME]),
                    FieldSpec(name="x", value_type=ValueType.INTEGER, roles=[FieldRole.MEASUREMENT]),
                ],
                context_window=ContextWindowSpec(
                    size=2,
                    stride=1,
                    partition_by=["flow"],
                    order_by=["t"],
                    column_template="{name}_ctx{index}",
                ),
            )
            prepared = prepare_dataset(spec)
            self.assertEqual(len(prepared.dataframe), 2)
            self.assertEqual(prepared.dataframe.iloc[0]["x_ctx0"], 10)
            self.assertEqual(prepared.dataframe.iloc[0]["x_ctx1"], 11)
            self.assertEqual(prepared.dataframe.iloc[1]["x_ctx0"], 20)
            self.assertEqual(prepared.dataframe.iloc[1]["x_ctx1"], 21)

    def test_mapping_rules_and_field_selection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "toy.csv"
            pd.DataFrame([
                {"SrcPt": 80, "SrcIpAddr": "192.168.100.10", "Noise": 1},
                {"SrcPt": 443, "SrcIpAddr": "DNS", "Noise": 2},
                {"SrcPt": 10000, "SrcIpAddr": "192.168.210.20", "Noise": 3},
                {"SrcPt": 55000, "SrcIpAddr": "8.8.8.8", "Noise": 4},
            ]).to_csv(path, index=False)

            spec = DatasetSpec(
                name="toy",
                source=SourceSpec(type=SourceType.CSV, path=str(path)),
                fields=[
                    FieldSpec(name="SrcPt", value_type=ValueType.INTEGER, roles=[FieldRole.SRC, FieldRole.IDENTIFIER]),
                    FieldSpec(name="SrcIpAddr", value_type=ValueType.CATEGORICAL, roles=[FieldRole.SRC, FieldRole.IDENTIFIER]),
                    FieldSpec(name="SrcPortClass", value_type=ValueType.INTEGER, roles=[FieldRole.SRC, FieldRole.IDENTIFIER]),
                    FieldSpec(name="SrcSubnet", value_type=ValueType.INTEGER, roles=[FieldRole.SRC, FieldRole.IDENTIFIER]),
                ],
                preprocessing=[
                    PreprocessStepSpec(
                        kind=PreprocessKind.MAP_RULES,
                        columns=["SrcPt"],
                        target_column="SrcPortClass",
                        rules=[
                            MappingRuleSpec(mode="equals", value=80, output=80),
                            MappingRuleSpec(mode="equals", value=443, output=443),
                            MappingRuleSpec(mode="range", lower=0, upper=1023, output=70000),
                            MappingRuleSpec(mode="range", lower=1024, upper=49151, output=71000),
                            MappingRuleSpec(mode="default", output=72000),
                        ],
                    ),
                    PreprocessStepSpec(
                        kind=PreprocessKind.MAP_RULES,
                        columns=["SrcIpAddr"],
                        target_column="SrcSubnet",
                        rules=[
                            MappingRuleSpec(mode="equals", value="DNS", output=888),
                            MappingRuleSpec(mode="prefix", value="192.168.100.", output=100),
                            MappingRuleSpec(mode="prefix", value="192.168.210.", output=210),
                            MappingRuleSpec(mode="default", output=666),
                        ],
                    ),
                ],
                include_fields=["SrcPt", "SrcPortClass", "SrcIpAddr", "SrcSubnet"],
                exclude_fields=["SrcIpAddr"],
            )

            prepared = prepare_dataset(spec)
            self.assertEqual(list(prepared.dataframe.columns), ["SrcPt", "SrcPortClass", "SrcSubnet"])
            self.assertEqual(prepared.configured_exclude_fields, ["SrcIpAddr"])
            self.assertEqual(prepared.effective_excluded_fields, ["SrcIpAddr"])
            self.assertEqual(prepared.dataframe["SrcPortClass"].tolist(), [80, 443, 71000, 72000])
            self.assertEqual(prepared.dataframe["SrcSubnet"].tolist(), [100, 888, 210, 666])

    def test_auto_source_type_uses_input_extension(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "toy.csv"
            pd.DataFrame([
                {"x": 1},
                {"x": 2},
            ]).to_csv(path, index=False)

            spec = DatasetSpec(
                name="toy",
                source=SourceSpec(type=SourceType.AUTO),
                fields=[FieldSpec(name="x", value_type=ValueType.INTEGER)],
            )

            prepared = prepare_dataset(spec, input_path=path)
            self.assertEqual(prepared.dataframe["x"].tolist(), [1, 2])

    def test_incomplete_selected_columns_are_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "toy.csv"
            pd.DataFrame([
                {"x": 1, "y": 10},
                {"x": 2, "y": None},
            ]).to_csv(path, index=False)

            spec = DatasetSpec(
                name="toy",
                source=SourceSpec(type=SourceType.CSV, path=str(path)),
                fields=[
                    FieldSpec(name="x", value_type=ValueType.INTEGER),
                    FieldSpec(name="y", value_type=ValueType.INTEGER),
                ],
                include_fields=["x", "y"],
            )

            prepared = prepare_dataset(spec)
            self.assertEqual(list(prepared.dataframe.columns), ["x"])
            self.assertEqual(prepared.configured_exclude_fields, [])
            self.assertIn("y", prepared.excluded_fields)
            self.assertIn("NaN", prepared.excluded_fields["y"])
            self.assertEqual(prepared.effective_excluded_fields, ["y"])

    def test_incomplete_unselected_columns_do_not_pollute_selection(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "toy.csv"
            pd.DataFrame([
                {"x": 1, "y": 10},
                {"x": 2, "y": None},
            ]).to_csv(path, index=False)

            spec = DatasetSpec(
                name="toy",
                source=SourceSpec(type=SourceType.CSV, path=str(path)),
                fields=[
                    FieldSpec(name="x", value_type=ValueType.INTEGER),
                    FieldSpec(name="y", value_type=ValueType.INTEGER),
                ],
                include_fields=["x"],
            )

            prepared = prepare_dataset(spec)
            self.assertEqual(list(prepared.dataframe.columns), ["x"])
            self.assertEqual(prepared.configured_exclude_fields, [])
            self.assertEqual(prepared.excluded_fields, {})
            self.assertEqual(prepared.effective_excluded_fields, [])

    def test_std_derived_variable(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "toy.csv"
            pd.DataFrame([
                {"a": 1.0, "b": 3.0},
                {"a": 2.0, "b": 2.0},
            ]).to_csv(path, index=False)

            spec = DatasetSpec(
                name="toy",
                source=SourceSpec(type=SourceType.CSV, path=str(path)),
                fields=[
                    FieldSpec(name="a", value_type=ValueType.REAL),
                    FieldSpec(name="b", value_type=ValueType.REAL),
                ],
                derived_variables=[
                    DerivedVariableSpec(
                        name="spread",
                        operation=DerivedOperation.STD,
                        inputs=["a", "b"],
                        value_type=ValueType.REAL,
                    ),
                ],
            )

            prepared = prepare_dataset(spec)
            self.assertAlmostEqual(prepared.dataframe.iloc[0]["spread"], 1.0)
            self.assertAlmostEqual(prepared.dataframe.iloc[1]["spread"], 0.0)


if __name__ == "__main__":
    unittest.main()
