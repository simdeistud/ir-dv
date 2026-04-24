from .utils.query import Atom, Not, And, Or
from .utils import query
from .index import *


class IR:
    def __init__(self, path: str):
        self.index = Index()
        self.index.build(Corpus("NTIS", path))

    def prepare_query(self, querystr: str):
        return query.parse_boolean_query(querystr)

    def retrieve(self, query):
        if isinstance(query, Atom):
            # SYSTEM QUERY
            return self._term(query.value)

        if isinstance(query, Not):
            child_ir = self.retrieve(query.node)
            return self._not(child_ir)

        if isinstance(query, And):
            left_ir = self.retrieve(query.left)
            right_ir = self.retrieve(query.right)
            return self._and(left_ir, right_ir)

        if isinstance(query, Or):
            left_ir = self.retrieve(query.left)
            right_ir = self.retrieve(query.right)
            return self._or(left_ir, right_ir)

        raise TypeError(f"Unknown node {query}")

    def _term(self, term: str) -> set[Posting]:
        return self.index.terms[term].postings

    def _not(self, p: set[Posting]) -> set[Posting]:
        return self.index.docIDs - p

    def _and(self, lp: set[Posting], rp: set[Posting]) -> set[Posting]:
        return lp & rp

    def _or(self, lp: set[Posting], rp: set[Posting]) -> set[Posting]:
        return lp | rp

