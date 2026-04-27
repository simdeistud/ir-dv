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
                intersection_list: list[PostingList] = []
                # All queries are performed and the resulting posting lists are placed in order
                for q in query.value:
                    intersection_list.append(self._term(q))
                # The posting lists are scanned incrementally to check adjacency of terms
                intersection: set[str] = set()
                for docID in intersection_list[0]:
                    for position in intersection_list[0][docID]:
                        phrase_found = True
                        for i in range(1, len(intersection_list)):
                            if docID not in intersection_list[i]:
                                phrase_found = False
                                break
                            if position+i not in intersection_list[i][docID]:
                                phrase_found = False
                                break
                        # We need just one phrase match to add the document to the results, no need to check further
                        if phrase_found:
                            intersection.add(docID)
                            break
                return intersection
            else:
                raise TypeError

        if isinstance(query, Not):
            child_ir = self.retrieve(query.node)
            return self._not(set(child_ir))

        if isinstance(query, And):
            left_ir = self.retrieve(query.left)
            right_ir = self.retrieve(query.right)
            return self._and(set(left_ir), set(right_ir))

        if isinstance(query, Or):
            left_ir = self.retrieve(query.left)
            right_ir = self.retrieve(query.right)
            return self._or(set(left_ir), set(right_ir))

        raise TypeError(f"Unknown value {query}")

    def _term(self, term: str) -> PostingList:
        if "*" in term:
            raise NotImplementedError("Wildcards are not supported")
        return self.index[term]

    def _not(self, p: set[str]) -> set[str]:
        return self.index._postings_idx - p

    def _and(self, lp: set[str], rp: set[str]) -> set[str]:
        return lp & rp

    def _or(self, lp: set[str], rp: set[str]) -> set[str]:
        return lp | rp


class BooleanPermutermIR:
    def __init__(self, path: str):
        self.index = InvertedPermutermIndex()
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
                intersection_list: list[PostingList] = []
                # All queries are performed and the resulting posting lists are placed in order
                for q in query.value:
                    intersection_list.append(self._term(q))
                # The posting lists are scanned incrementally to check adjacency of terms
                intersection: set[str] = set()
                for docID in intersection_list[0]:
                    for position in intersection_list[0][docID]:
                        phrase_found = True
                        for i in range(1, len(intersection_list)):
                            if docID not in intersection_list[i]:
                                phrase_found = False
                                break
                            if position+i not in intersection_list[i][docID]:
                                phrase_found = False
                                break
                        # We need just one phrase match to add the document to the results, no need to check further
                        if phrase_found:
                            intersection.add(docID)
                            break
                return intersection
            else:
                raise TypeError

        if isinstance(query, Not):
            child_ir = self.retrieve(query.node)
            return self._not(set(child_ir))

        if isinstance(query, And):
            left_ir = self.retrieve(query.left)
            right_ir = self.retrieve(query.right)
            return self._and(set(left_ir), set(right_ir))

        if isinstance(query, Or):
            left_ir = self.retrieve(query.left)
            right_ir = self.retrieve(query.right)
            return self._or(set(left_ir), set(right_ir))

        raise TypeError(f"Unknown value {query}")

    def _term(self, term: str) -> PostingList | list[PostingList]:
        if "*" in term:
            if term.count("*") > 1:
                raise NotImplementedError("Permuterm index doesn't support multiple wildcards in the same term")
            # We rotate the term so the wildcard is at the end
            rotated = term
            while rotated[-1] != "*":
                rotated = rotated[-1] + rotated[:-1]
            # We obtain the posting list of all the terms which match the rotated wild card
            postings: list[PostingList] = self.index[rotated]
            # Now we merge the posting lists
            result = PostingList()
            for posting in postings:
                result.merge(posting)
            return result
        return self.index[term]

    def _not(self, p: set[str]) -> set[str]:
        return self.index._postings_idx - p

    def _and(self, lp: set[str], rp: set[str]) -> set[str]:
        return lp & rp

    def _or(self, lp: set[str], rp: set[str]) -> set[str]:
        return lp | rp

