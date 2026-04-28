from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from netnomos.ast import (
    BinaryTerm,
    BoolAnd,
    BoolConst,
    BoolNot,
    BoolOr,
    Compare,
    Constant,
    Exists,
    ForAll,
    FuncCall,
    Formula,
    Implies,
    IndexedRef,
    SymbolRef,
    Term,
)


TOKEN_RE = re.compile(
    r"""
    (?P<SPACE>\s+)
    |(?P<ARROW>->)
    |(?P<GE>>=)
    |(?P<LE><=)
    |(?P<NE>!=)
    |(?P<GT>>)
    |(?P<LT><)
    |(?P<EQ>=)
    |(?P<LPAREN>\()
    |(?P<RPAREN>\))
    |(?P<LBRACE>\{)
    |(?P<RBRACE>\})
    |(?P<LBRACK>\[)
    |(?P<RBRACK>\])
    |(?P<COMMA>,)
    |(?P<COLON>:)
    |(?P<PLUS>\+)
    |(?P<MINUS>-)
    |(?P<STAR>\*)
    |(?P<SLASH>/)
    |(?P<NUMBER>\d+(?:\.\d+)?)
    |(?P<STRING>'[^']*'|"[^"]*")
    |(?P<IDENT>[A-Za-z_][A-Za-z0-9_.]*)
    """,
    re.VERBOSE,
)


KEYWORDS = {"and", "or", "not", "forall", "exists", "in", "true", "false"}


@dataclass(frozen=True, slots=True)
class Token:
    kind: str
    value: str


def tokenize(text: str) -> list[Token]:
    tokens: list[Token] = []
    pos = 0
    while pos < len(text):
        match = TOKEN_RE.match(text, pos)
        if match is None:
            raise ValueError(f"Unexpected token at position {pos}: {text[pos:pos + 20]!r}")
        pos = match.end()
        kind = match.lastgroup
        value = match.group()
        if kind == "SPACE":
            continue
        if kind == "IDENT" and value.lower() in KEYWORDS:
            tokens.append(Token(value.lower(), value.lower()))
        else:
            tokens.append(Token(kind, value))
    return tokens


class FormulaParser:
    def __init__(self, text: str):
        self.tokens = tokenize(text)
        self.index = 0

    def parse(self) -> Formula:
        formula = self.parse_implication()
        if self.index != len(self.tokens):
            raise ValueError(f"Unexpected trailing token: {self.tokens[self.index]!r}")
        return formula

    def parse_implication(self) -> Formula:
        left = self.parse_or()
        if self.match("ARROW"):
            right = self.parse_implication()
            return Implies(left, right)
        return left

    def parse_or(self) -> Formula:
        values = [self.parse_and()]
        while self.match("or"):
            values.append(self.parse_and())
        if len(values) == 1:
            return values[0]
        return BoolOr(tuple(values))

    def parse_and(self) -> Formula:
        values = [self.parse_unary_formula()]
        while self.match("and"):
            values.append(self.parse_unary_formula())
        if len(values) == 1:
            return values[0]
        return BoolAnd(tuple(values))

    def parse_unary_formula(self) -> Formula:
        if self.match("not"):
            return BoolNot(self.parse_unary_formula())
        if self.peek("forall") or self.peek("exists"):
            return self.parse_quantified()
        if self.match("LPAREN"):
            inner = self.parse_implication()
            self.expect("RPAREN")
            return inner
        if self.peek("true"):
            self.expect("true")
            return BoolConst(True)
        if self.peek("false"):
            self.expect("false")
            return BoolConst(False)
        return self.parse_comparison()

    def parse_quantified(self) -> Formula:
        quantifier = self.expect("forall", "exists")
        variable = self.expect("IDENT").value
        self.expect("in")
        domain = self.parse_domain()
        self.expect("COLON")
        body = self.parse_implication()
        if quantifier.kind == "forall":
            return ForAll(variable=variable, domain=domain, body=body)
        return Exists(variable=variable, domain=domain, body=body)

    def parse_domain(self) -> tuple[Any, ...]:
        self.expect("LBRACE")
        values: list[Any] = []
        while True:
            if self.peek("NUMBER"):
                token = self.expect("NUMBER")
                values.append(float(token.value) if "." in token.value else int(token.value))
            elif self.peek("STRING"):
                token = self.expect("STRING")
                values.append(token.value[1:-1])
            else:
                values.append(self.expect("IDENT").value)
            if not self.match("COMMA"):
                break
        self.expect("RBRACE")
        return tuple(values)

    def parse_comparison(self) -> Formula:
        left = self.parse_term()
        token = self.expect("EQ", "NE", "GT", "GE", "LT", "LE")
        right = self.parse_term()
        op_map = {
            "EQ": "=",
            "NE": "!=",
            "GT": ">",
            "GE": ">=",
            "LT": "<",
            "LE": "<=",
        }
        return Compare(op_map[token.kind], left, right)

    def parse_term(self) -> Term:
        node = self.parse_factor()
        while self.peek("PLUS") or self.peek("MINUS"):
            op = self.expect("PLUS", "MINUS").value
            node = BinaryTerm(op, node, self.parse_factor())
        return node

    def parse_factor(self) -> Term:
        node = self.parse_atom()
        while self.peek("STAR") or self.peek("SLASH"):
            op = self.expect("STAR", "SLASH").value
            node = BinaryTerm(op, node, self.parse_atom())
        return node

    def parse_atom(self) -> Term:
        if self.match("LPAREN"):
            inner = self.parse_term()
            self.expect("RPAREN")
            return inner
        if self.match("MINUS"):
            return BinaryTerm("*", Constant(-1), self.parse_atom())
        if self.peek("NUMBER"):
            token = self.expect("NUMBER")
            return Constant(float(token.value) if "." in token.value else int(token.value))
        if self.peek("STRING"):
            return Constant(self.expect("STRING").value[1:-1])
        ident = self.expect("IDENT").value
        if self.match("LBRACK"):
            if self.peek("NUMBER"):
                token = self.expect("NUMBER")
                index: int | str = int(token.value)
            else:
                index = self.expect("IDENT").value
            self.expect("RBRACK")
            return IndexedRef(ident, index)
        if self.match("LPAREN"):
            args: list[Term] = []
            if not self.peek("RPAREN"):
                args.append(self.parse_term())
                while self.match("COMMA"):
                    args.append(self.parse_term())
            self.expect("RPAREN")
            return FuncCall(ident, tuple(args))
        return SymbolRef(ident)

    def match(self, *kinds: str) -> Token | None:
        if self.index >= len(self.tokens):
            return None
        token = self.tokens[self.index]
        if token.kind in kinds:
            self.index += 1
            return token
        return None

    def peek(self, kind: str) -> bool:
        return self.index < len(self.tokens) and self.tokens[self.index].kind == kind

    def expect(self, *kinds: str) -> Token:
        token = self.match(*kinds)
        if token is None:
            expected = " or ".join(kinds)
            actual = self.tokens[self.index].kind if self.index < len(self.tokens) else "EOF"
            raise ValueError(f"Expected {expected}, got {actual}")
        return token


def parse_formula(text: str) -> Formula:
    return FormulaParser(text).parse()

