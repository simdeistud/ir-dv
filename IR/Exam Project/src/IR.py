from .utils.query import Atom, Not, And, Or
from .utils import query
from .index import *


class IR:
    def __init__(self, path: str):
        self.index = InvertedPermutermIndex()
        self.index.build(Corpus("NTIS", path))

    def prepare_query(self, querystr: str):
        return query.parse_boolean_query(querystr)

    def retrieve(self, query):
        if isinstance(query, Atom):
            # SINGLE TERM QUERY
            if isinstance(query.value, str) and "*" not in query.value:
                return self._term(query.value)
            # WILDCARD SINGLE TERM QUERY
            elif isinstance(query.value, str) and "*" in query.value:
                return ...
            # PHRASE QUERY
            elif isinstance(query.value, list):
                ...
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

    def _term(self, term: str) -> set[Posting]:
        return set(self.index[f"{term}$"].posting_list())

    def _wildcard_term(self, term: str) -> set[Posting]:
        if term.count("*") > 1:
            raise NotImplementedError("More than 1 wildcard is not supported for permuterm indexes")
        # We create rotate the term until the wildcard is at the end
        term = self._prefix_wildcard(f"{term}$")
        # We obtain the posting lists of all the matches
        posting_lists = [t.posting_list() for t in self.index.get_matching(term)]
        # We return the union of their postings
        result = PostingList()
        for posting_list in posting_lists:
            result.merge(posting_list)
        return set(result)

    def _prefix_wildcard(self, term: str) -> str:
        rotation = term
        while rotation[-1] != "*":
            rotation = rotation[1:] + rotation[0]
        return rotation

    def _not(self, p: set[Posting]) -> set[Posting]:
        return self.index._postings_idx - p

    def _and(self, lp: set[Posting], rp: set[Posting]) -> set[Posting]:
        return lp & rp

    def _or(self, lp: set[Posting], rp: set[Posting]) -> set[Posting]:
        return lp | rp

