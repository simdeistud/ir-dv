import re
from dataclasses import dataclass

# ---------- Query nodes ----------
@dataclass
class Atom:
    value: str | list[str]

@dataclass
class Not:
    node: object

@dataclass
class And:
    left: object
    right: object

@dataclass
class Or:
    left: object
    right: object

def tokenize(s: str, method: str = "regexp", normalization: bool = True):
    tokenizer = {
        "word": nltk.word_tokenize,
        "regexp": nltk.RegexpTokenizer(r'[A-Za-z]\w+').tokenize,
    }[method]
    tokens = tokenizer(s)
    if normalization:
        return [t if t in {"AND", "OR", "NOT"} else t.lower() for t in tokens]
    else:
        return tokens

# ---------- Parser ----------
class BooleanParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, token=None):
        current = self.peek()
        if token and current != token:
            raise SyntaxError(f"Expected {token}, got {current}")
        self.pos += 1
        return current

    def parse(self):
        query = self.expr()
        if self.peek() is not None:
            raise SyntaxError("Unexpected token")
        return query

    # expr := term (OR term)*
    def expr(self):
        node = self.term()
        while self.peek() == "OR":
            self.consume("OR")
            node = Or(node, self.term())
        return node

    # term := factor (AND factor)*
    def term(self):
        node = self.factor()
        while self.peek() == "AND":
            self.consume("AND")
            node = And(node, self.factor())
        return node

    # factor := NOT factor | '(' expr ')' | ATOM
    def factor(self):
        tok = self.peek()
        if tok == "NOT":
            self.consume("NOT")
            return Not(self.factor())
        elif tok == "(":
            self.consume("(")
            node = self.expr()
            self.consume(")")
            return node
        elif tok is not None:
            self.consume()
            return Atom(tok)
        else:
            raise SyntaxError("Unexpected end of input")


# ---------- Convenience ----------
def parse_boolean_query(query: str):
    tokens = tokenize(query)
    return BooleanParser(tokens).parse()