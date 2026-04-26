import json
from functools import total_ordering

from .utils import preprocessing
from .utils.corpus import Corpus

@total_ordering
class Posting:
    def __init__(self, docID: str, positional_idx: set[int] = None):
        self.docID = docID
        if positional_idx is None:
            self._positional_idx = set()
        else:
            self._positional_idx = positional_idx

    def merge(self, other: Posting | int) -> None:
        # We merge together the two positional indexes in place
        if isinstance(other, Posting):
            if self is not other:
                raise ValueError("Cannot merge postings of different documents")
            self._positional_idx.update(other._positional_idx)
        # We add the index to the positional indexes in place
        elif isinstance(other, int):
            self._positional_idx.add(other)
        else: raise TypeError

    def positional_index(self) -> list[int]:
        return sorted(self._positional_idx)

    def __hash__(self):
        return hash(self.docID)
    def __eq__(self, other):
        return self.docID == other.docID
    def __lt__(self, other):
        return self.docID < other.docID
    def __repr__(self):
        return str(self.docID)

class PostingList:
    def __init__(self, postings: list[Posting] = None):
        if postings is None:
            self._postings = list[Posting]()
        else:
            self._postings = postings

    def merge(self, other: PostingList | Posting) -> None:
        # We merge together the two posting lists
        if isinstance(other, PostingList):
            for posting in other: self.merge(posting)
        # We add posting to the posting list in place
        elif isinstance(other, Posting):
            # If the posting has the smallest docID, add it as first element
            if other < self._postings[0]:
                self._postings.insert(0, other)
            # If the posting has the biggest docID, append it
            elif other > self._postings[-1]:
                self._postings.append(other)
            else:
                for i in range(1, len(self._postings)):
                    # If the posting already exists, merge its positional index
                    if self._postings[i] is other:
                        self._postings[i].merge(other)
                        break
                    # If the posting sits between two postings, insert it
                    if self._postings[i-1] < other < self._postings[i]:
                        self._postings.insert(i, other)
                        break
        else: raise TypeError

    def __str__(self):
        return str(self._postings)
    def __len__(self):
        return len(self._postings)
    def __iter__(self):
        return iter(self._postings)

@total_ordering
class Term:
    def __init__(self, value: str, posting_list: PostingList = None):
        self.value = value
        if posting_list is None:
            self._posting_list = PostingList()
        else:
            self._posting_list = posting_list

    def merge(self, other: Term) -> None:
        # We merge together the two posting lists given the same term
        if isinstance(other, Term):
            if self is not other:
                raise ValueError
            self._posting_list.merge(other._posting_list)
        else:
            raise TypeError

    def __eq__(self, other):
        return self.value == other.value
    def __lt__(self, other):
        return self.value < other.value
    def __str__(self):
        return self.value
    def __repr__(self):
        return f"{self.value} : {self._posting_list}"


def _get_permuterms(term: str) -> set[str]:
    rotations = {term}
    for i in range(0, len(term)):
        term = term[1:] + term[0]
        rotations.add(term)
    return rotations


class InvertedPermutermIndex:
    def __init__(self):
        self._dictionary: dict[str, Term] = {}
        # We keep a set of all the docIDs to make answering NOT queries simpler
        self._postings_idx = set[Posting]()

    def build(self, corpus: Corpus):
        for document in corpus.documents:
            print(f"adding document to index [{document.docID}]")
            tokens = preprocessing.tokenize(document.title + " " + document.text)
            # First we add the base permutation (term$) of each term to the dictionary
            i: int = 0
            for t in tokens:
                if f"{t}$" not in self._dictionary:
                    self._dictionary[f"{t}$"] = Term(t)
                self._dictionary[f"{t}$"].merge(Term(t, PostingList([Posting(document.docID, {i})])))
                i += 1
            # Now we map all the rotations of each base term to the same Term object (to avoid posting list duplication)
            for k in self._dictionary.keys():
                permuterms = _get_permuterms(k)
                for permuterm in permuterms:
                    self._dictionary[permuterm] = self._dictionary[k]
            self._postings_idx.add(Posting(document.docID))

    def load(self, path: str):
        with open(path) as f:
            self._dictionary = json.load(f)

    def save(self, path: str):
        with open(path, "w") as f:
            json.dump(self._dictionary, f)