from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import pandas as pd

from netnomos.ast import formula_to_dict
from netnomos.cli import main
from netnomos.dsl import parse_formula
from netnomos.specs import DatasetSpec, FieldSpec, GrammarSpec, SourceSpec, SourceType, ValueType


class CliTest(unittest.TestCase):
    def test_interpret_can_write_to_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            data_path = tmp / "toy.csv"
            dataset_path = tmp / "dataset.json"
            grammar_path = tmp / "grammar.json"
            rules_path = tmp / "rules.json"
            output_path = tmp / "interpreted_rules.clj"

            pd.DataFrame([{"Bytes": 10}, {"Bytes": 20}]).to_csv(data_path, index=False)

            dataset = DatasetSpec(
                name="toy",
                source=SourceSpec(type=SourceType.CSV, path=str(data_path)),
                fields=[FieldSpec(name="Bytes", value_type=ValueType.INTEGER)],
            )
            grammar = GrammarSpec(name="toy")
            dataset_path.write_text(dataset.model_dump_json(indent=2))
            grammar_path.write_text(grammar.model_dump_json(indent=2))
            rules_path.write_text(json.dumps([{
                "rule_id": "r00001",
                "formula": formula_to_dict(parse_formula("Bytes >= 10")),
                "display": "Bytes >= 10",
                "support": 1.0,
                "source": {},
            }], indent=2))

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main([
                    "interpret",
                    "--dataset-spec", str(dataset_path),
                    "--grammar-spec", str(grammar_path),
                    "--rules", str(rules_path),
                    "--output", str(output_path),
                ])

            self.assertEqual(exit_code, 0)
            payload = json.loads(stdout.getvalue())
            self.assertEqual(payload["output"], str(output_path))
            self.assertEqual(payload["rules"], 1)
            self.assertEqual(output_path.read_text().strip(), "Bytes >= 10")

    def test_convert_script_accepts_json_rule_exports(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            input_path = tmp / "legacy.json"
            output_dir = tmp / "converted"
            input_path.write_text(json.dumps([
                "Eq(TcpFlags1, 0) >> Eq(TcpFlags2, 1)",
                "Eq(TcpHdrLen1 % 4, 0)",
            ], indent=2))

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/convert_golden_rules.py",
                    "--input", str(input_path),
                    "--output-dir", str(output_dir),
                    "--name", "legacy",
                    "--field-mode", "pcap",
                ],
                cwd=Path(__file__).resolve().parents[1],
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(result.stdout)
            self.assertEqual(payload["rule_count"], 2)
            rules = json.loads((output_dir / "rules.json").read_text())
            self.assertEqual(rules[0]["display"], "(tcp.flags_ctx0 = 0) -> (tcp.flags_ctx1 = 1)")
            interpreted = (output_dir / "interpreted_rules.clj").read_text().splitlines()
            self.assertEqual(interpreted[1], "MOD(tcp.hdr_len_ctx0, 4) = 0")


if __name__ == "__main__":
    unittest.main()
