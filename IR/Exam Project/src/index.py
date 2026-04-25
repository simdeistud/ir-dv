import json
from functools import total_ordering

from .utils import preprocessing
from .utils.corpus import Corpus

@total_ordering
class Posting:
    def __init__(self, docID: str):
        self.docID = docID
    def __hash__(self):
        return hash(self.docID)
    def __eq__(self, other):
        return self.docID == other.docID
    def __lt__(self, other):
        return self.docID < other.docID
    def __repr__(self):
        return str(self.docID)

class PostingList:
    def __init__(self, postings = None):
        if postings is None:
            self.postings = set[Posting]()
        else:
            self.postings = postings
    def __add__(self, other) -> PostingList:
        # We merge together the two posting lists
        if isinstance(other, PostingList):
            return PostingList(self.postings | other.postings)
        # We add the posting to the posting list
        if isinstance(other, Posting):
            return PostingList(self.postings | {other})
        raise TypeError
    def __str__(self):
        return str(self.postings)
    def __len__(self):
        return len(self.postings)
    def __iter__(self):
        return iter(self.postings)

@total_ordering
class Term:
    def __init__(self, value: str, posting_list: PostingList = None):
        self.value = value
        if posting_list is None:
            self.posting_list = PostingList()
        else:
           self.posting_list = posting_list
    def add_posting(self, posting: Posting):
        self.posting_list += posting
    def merge_postings(self, postings: PostingList):
        self.posting_list += postings
    def __eq__(self, other):
        return self.value == other.value
    def __lt__(self, other):
        return self.value < other.value
    def __add__(self, other) -> Term:
        # We merge together the two posting lists given the same term
        if isinstance(other, Term):
            if self is not other:
                raise ValueError
            return Term(self.value, self.posting_list + other.posting_list)
        else:
            raise TypeError
    def __str__(self):
        return self.value
    def __repr__(self):
        return f"{self.value} : {self.posting_list}"

class InvertedPermutermIndex:
    def __init__(self):
        self._dictionary: dict[str, Term] = {}
        self._postings_idx = set[Posting]()

    def build(self, corpus: Corpus):
        for document in corpus.documents:
            print(f"adding document to index [{document.docID}]")
            types = set(preprocessing.tokenize(document.title + " " + document.text))
            # First we add the base permutation (term$) of each term to the dictionary
            for t in types:
                if f"{t}$" not in self._dictionary:
                    self._dictionary[f"{t}$"] = Term(t)
                self._dictionary[f"{t}$"] += Term(t, PostingList({Posting(document.docID)}))
            # Now we map all the rotations of each base term to the same Term object (to avoid posting list duplication)
            for k in self._dictionary.keys():
                permuterms = self._get_permutations(k)
                for permuterm in permuterms:
                    self._dictionary[permuterm] = self._dictionary[k]
            self._postings_idx.add(Posting(document.docID))

    def load(self, path: str):
        with open(path) as f:
            self._dictionary = json.load(f)

    def save(self, path: str):
        with open(path, "w") as f:
            json.dump(self._dictionary, f)

    def _get_permutations(self, term: str) -> set[str]:
        rotations = {term}
        for i in range(0, len(term)):
            term = term[1:] + term[0]
            rotations.add(term)
        return rotations

