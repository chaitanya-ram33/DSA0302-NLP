"""Recursive-descent parser for basic first-order predicate logic (FOPC)."""

import re

TOKEN_PATTERN = re.compile(r"\s*(<->|->|[(),.]|[~&|∀∃]|[A-Za-z][A-Za-z0-9_]*)")
QUANTIFIERS = {"forall", "exists", "∀", "∃"}
OPERATORS = {"->": 1, "<->": 0, "|": 2, "&": 3}


def tokenize(text):
    tokens = []
    position = 0
    while position < len(text):
        match = TOKEN_PATTERN.match(text, position)
        if not match:
            if text[position:].strip() == "":
                break
            raise SyntaxError(f"Unexpected character at position {position}")
        tokens.append(match.group(1))
        position = match.end()
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def peek(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def take(self, expected=None):
        token = self.peek()
        if token is None or (expected is not None and token != expected):
            raise SyntaxError(f"Expected {expected!r}, found {token!r}")
        self.position += 1
        return token

    def formula(self, minimum_precedence=0):
        token = self.peek()
        if token in QUANTIFIERS:
            quantifier = self.take()
            variable = self.take()
            self.take("(")
            body = self.formula()
            self.take(")")
            left = (quantifier, variable, body)
        elif token == "~":
            self.take()
            left = ("not", self.formula(4))
        elif token == "(":
            self.take()
            left = self.formula()
            self.take(")")
        else:
            left = self.predicate()

        while self.peek() in OPERATORS and OPERATORS[self.peek()] >= minimum_precedence:
            operator = self.take()
            precedence = OPERATORS[operator]
            right = self.formula(precedence + 1)
            left = (operator, left, right)
        return left

    def predicate(self):
        name = self.take()
        if not name[0].isupper():
            raise SyntaxError(f"Expected a predicate name, found {name!r}")
        self.take("(")
        arguments = [self.take()]
        while self.peek() == ",":
            self.take(",")
            arguments.append(self.take())
        self.take(")")
        return ("predicate", name, tuple(arguments))


def parse(text):
    parser = Parser(tokenize(text))
    result = parser.formula()
    if parser.peek() is not None:
        raise SyntaxError(f"Unexpected trailing token {parser.peek()!r}")
    return result


if __name__ == "__main__":
    expression = "forall x (Human(x) -> Mortal(x))"
    print(parse(expression))
