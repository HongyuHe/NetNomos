from __future__ import annotations

import unittest

from netnomos.ast import BinaryTerm, Compare, Constant, FuncCall, Implies, SymbolRef, formula_to_string
from netnomos.dsl import parse_formula
from netnomos.interpreter import interpret_formula


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

    def test_render_uses_uppercase_keywords_and_functions(self) -> None:
        formula = parse_formula("A > 1 and B = 2 -> C != 0")
        self.assertEqual(formula_to_string(formula), "((A > 1) AND (B = 2)) -> (C != 0)")

        aggregate = Compare(">=", FuncCall("min", (SymbolRef("A"), SymbolRef("B"))), Constant(1))
        self.assertEqual(formula_to_string(aggregate), "MIN(A, B) >= 1")
        self.assertEqual(interpret_formula(aggregate, {}), "MIN(A, B) >= 1")


if __name__ == "__main__":
    unittest.main()
