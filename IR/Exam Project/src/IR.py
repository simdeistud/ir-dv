from .utils.query import Atom, Not, And, Or
from .utils import query
from .index import *


class BooleanIR:
    def __init__(self, path: str):
        self.index = InvertedIndex()
        self.index.build(Corpus("NTIS", path))

    def prepare_query(self, querystr: str):
        return query.parse_boolean_query(querystr)

    def retrieve(self, query):
        if isinstance(query, Atom):
            # SINGLE TERM QUERY
            if isinstance(query.value, str):
                return self._term(query.value)
            # PHRASE QUERY
            elif isinstance(query.value, list):
                # TODO: IMPLEMENT PHRASE QUERY HANDLING
                raise NotImplementedError("Phrase queries are not supported")
            else:
                raise TypeError

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

        raise TypeError(f"Unknown value {query}")

    def _term(self, term: str) -> set[str]:
        if "*" in term:
            raise NotImplementedError("Wildcards are not supported")
        return set(self.index[term])

    def _not(self, p: set[str]) -> set[str]:
        return self.index._postings_idx - p

    def _and(self, lp: set[str], rp: set[str]) -> set[str]:
        return lp & rp

    def _or(self, lp: set[str], rp: set[str]) -> set[str]:
        return lp | rp

