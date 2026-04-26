import json
from dataclasses import dataclass
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
    def __init__(self, postings: Posting | list[Posting] = None):
        if postings is None:
            self._postings = list[Posting]()
        elif isinstance(postings, list):
            self._postings = postings
            self._postings.sort()
        elif isinstance(postings, Posting):
            self._postings = [postings]
        else:
            raise TypeError

    def merge(self, other: PostingList | Posting) -> None:
        # We merge together the two posting lists
        if isinstance(other, PostingList):
            for posting in other: self.merge(posting)
        # We add posting to the posting list in place
        elif isinstance(other, Posting):
            for i in range(0, len(self)):
                if other < self._postings[i]:
                    self._postings.insert(i, other)
                    return
            self._postings.append(other)
        else:
            raise TypeError

    def __str__(self):
        return str(self._postings)
    def __len__(self):
        return len(self._postings)
    def __iter__(self):
        return iter(self._postings)

class InvertedIndex:
    def __init__(self):
        # The main index is an ordered list of Terms
        self._index: dict[str, PostingList] = {}
        # We keep a set of all the docIDs to make answering NOT queries simpler
        self._postings_idx: set[Posting] = set()

    def build(self, corpus: Corpus) -> None:
        for document in corpus:
            print(f"adding document to index [{document.docID}]")
            tokens = preprocessing.tokenize(document.title + " " + document.text)
            # First we add all the base terms to the main index
            for t in tokens:
                posting = Posting(document.docID)
                if t in self._index:
                    self._index[t].merge(posting)
                else:
                    self._postings_idx.add(posting)  # We add the posting to the index
                    self._index[t] = PostingList(Posting(document.docID))

    def __getitem__(self, item):
        return self._index[item]

    def __len__(self):
        return len(self._index)

class InvertedPermutermIndex:
    def __init__(self):
        # The main index is an ordered list of Terms
        self._index: dict[str, PostingList] = {}
        # We keep a set of all the docIDs to make answering NOT queries simpler
        self._postings_idx: set[Posting] = set()

    def build(self, corpus: Corpus):
        for document in corpus:
            print(f"adding document to index [{document.docID}]")
            tokens = preprocessing.tokenize(document.title + " " + document.text)
            # First we add all the base terms to the main index
            for t in tokens:
                posting = Posting(document.docID)
                self._postings_idx.add(posting) # We add the posting to the index
                if t in self._index:
                    self._index[t].merge(posting)
                else:
                    self._index[t] = PostingList([Posting(document.docID)])

    def _get_permuterms(self, term: str) -> list[str]:
        rotations = {f"{term}$"}
        for i in range(0, len(term)):
            term = term[1:] + term[0]
            rotations.add(term)
        return list(rotations)

    def get(self, term: str) -> Term:
        return self._index[self._index.index(Term(term))]

    def get_matchings(self, term: str) -> list[Term]:
        return [match for match in self._index if match.value.startswith(term)]

    def __len__(self):
        return len(self._index)