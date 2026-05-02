from .utils.query import Atom, Not, And, Or
from .utils import query
from .index import *
import regex as re

class BooleanIR:
    def __init__(self):
        self.index = InvertedIndex()
    
    def build(self, path: str):
        corpus: Corpus = CranfieldCorpus()
        corpus.build(path)
        self.index.build(corpus)

    def retrieve(self, querystr: str) -> list[str]:
        return sorted(self._evaluate_query(query.parse_boolean_query(querystr)))

    def _evaluate_query(self, query) -> set[str]:
        if isinstance(query, Atom):
            # SINGLE TERM QUERY
            if isinstance(query.value, str):
                return self._term(query.value)
            # PHRASE QUERY
            elif isinstance(query.value, list):
                return self._evaluate_phrase_query(query.value)
            else:
                raise TypeError
        
        if isinstance(query, Not):
            child_ir = self._evaluate_query(query.node)
            return self._not(set(child_ir))

        if isinstance(query, And):
            left_ir = self._evaluate_query(query.left)
            right_ir = self._evaluate_query(query.right)
            return self._and(set(left_ir), set(right_ir))

        if isinstance(query, Or):
            left_ir = self._evaluate_query(query.left)
            right_ir = self._evaluate_query(query.right)
            return self._or(set(left_ir), set(right_ir))

        raise TypeError(f"Unknown value {query}")
    
    def _evaluate_phrase_query(self, phrase: list[str]) -> set[str]:
        intersection_list: list[PostingList] = []
        # All queries are performed and the resulting posting lists are placed in order
        for q in phrase:
            intersection_list.append(self._term_postings(q))
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

    def _term(self, term: str) -> set[str]:
        return set(self._term_postings(term))
    
    def _term_postings(self, term: str) -> PostingList:
        return self.index[term]

    def _not(self, p: set[str]) -> set[str]:
        return self.index._postings_index - p

    def _and(self, lp: set[str], rp: set[str]) -> set[str]:
        return lp & rp

    def _or(self, lp: set[str], rp: set[str]) -> set[str]:
        return lp | rp


class BooleanPermutermIR(BooleanIR):
    def __init__(self):
        super().__init__()
        self._permuterm_index = PermutermIndex()

    def build(self, path: str):
        super().build(path)
        self._permuterm_index.build(self.index)

    def _term_postings(self, s: str) -> PostingList:
        if "*" in s:
            # If the query contains multiple wildcards, we extract the simplified query and use it
            # to search for candidate terms in the permuterm index, which we then filter using regular expressions
            if s.count("*") > 1:
                rotated = f"*{s.split('*')[-1]}$"
            else: rotated = f"{s}$"
            # We rotate the term so the wildcard is at the end
            while rotated[-1] != "*":
                rotated = rotated[-1] + rotated[:-1]
            # We remove the *
            prefix = rotated[:-1]
            # We obtain all the permuterms that start with the prefix
            prefix_permuterms = [permuterm for permuterm in self._permuterm_index if permuterm.startswith(prefix)]
            # We map the permuterms to the respective terms in the index and remove duplicates using a set
            terms: set[str] = set(self._permuterm_index[permuterm] for permuterm in prefix_permuterms)
            # If there are multiple wildcards, we need to filter the terms using regular expressions, 
            # since the permuterm index doesn't support multiple wildcards
            if s.count("*") > 1:
                pattern = re.escape(s)
                pattern = pattern.replace(r'\*', '.*')
                pattern = f"^{pattern}$"
                terms = set(term for term in terms if re.match(pattern, term))
            # Now we merge the posting lists
            result = PostingList()
            for term in terms:
                result.merge(self.index[term])
            return result
        return self.index[s]

class BooleanKGRamIR(BooleanIR):   
    def __init__(self, k: int):
        super().__init__()
        self._k = k
        self._kgram_index = KGramIndex(self._k)

    def build(self, path: str):
        super().build(path)
        self._kgram_index.build(self.index)

    def _term_postings(self, s: str) -> PostingList:
        if "*" in s:    
            # We add $s at the beginning and end, and split the string between wildcards
            splits = f"${s}$".split("*")
            # For each split, we compute its k-grams and search for matching terms
            terms: set[str] = set(self.index)
            for split in splits:
                # We skip empty splits, which can be generated by consecutive wildcards
                # or wildcards at the beginning/end of the string
                if split == "$" or split == "":
                    continue
                if len(split) < self._k:
                    raise ValueError(f"Wildcards are too close (<{self._k})")
                kgrams = KGramIndex._get_kgrams(split, self._k)
                for kgram in kgrams:
                    #print(f"Terms for k-gram '{kgram}': {self._kgram_index[kgram]}")
                    terms.intersection_update(self._kgram_index[kgram])
            # Since searching for k-grams may return false positives (wrong order, missing k-gram, etc.),
            # we use regular expressions on the set of candidate terms to filter out unwanted results     
            pattern = re.escape(s)
            pattern = pattern.replace(r'\*', '.*')
            pattern = f"^{pattern}$"
            terms = set(term for term in terms if re.match(pattern, term))
            # Now we merge the posting lists
            result = PostingList()
            for term in terms:
                result.merge(self.index[term])
            return result
        return self.index[s]

