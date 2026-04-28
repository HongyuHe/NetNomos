from __future__ import annotations

import unittest

from netnomos.ast import BinaryTerm, Compare, Implies
from netnomos.dsl import parse_formula


class DslParserTest(unittest.TestCase):
    def test_parse_implication(self) -> None:
        formula = parse_formula("A > 1 and B = 2 -> C != 0")
        self.assertIsInstance(formula, Implies)

    def test_parse_arithmetic_comparison(self) -> None:
        formula = parse_formula("Packet * 65535 <= Bytes + Header")
        self.assertIsInstance(formula, Compare)
        self.assertIsInstance(formula.left, BinaryTerm)
        self.assertEqual(formula.left.op, "*")
        self.assertIsInstance(formula.right, BinaryTerm)
        self.assertEqual(formula.right.op, "+")


if __name__ == "__main__":
    unittest.main()
