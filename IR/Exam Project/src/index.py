import json
from dataclasses import dataclass
from functools import total_ordering
from .utils import preprocessing
from .utils.corpus import Corpus

class PostingList:
    def __init__(self, postings: dict[str, list[int]] = None):
        if postings:
            self._postings: dict[str, list[int]] = postings
            for docID in self._postings:
                self._postings[docID].sort()
        else: self._postings: dict[str, list[int]] = {}

    def merge(self, other: PostingList) -> None:
        # We merge together the two posting lists
        if isinstance(other, PostingList):
            for docID in other:
                if docID in self._postings:
                    self._postings[docID] = sorted(set(self._postings[docID] + other._postings[docID]))
                else:
                    self._postings[docID] = other._postings[docID]
        else:
            raise TypeError

    def __str__(self):
        return str(self._postings)
    def __len__(self):
        return len(self._postings)
    def __getitem__(self, docID):
        return self._postings[docID]
    def __iter__(self):
        return iter(self._postings)

class InvertedIndex:
    def __init__(self):
        # The main index is an ordered list of Terms
        self._index: dict[str, PostingList] = {}
        # We keep a set of all the docIDs to make answering NOT queries simpler
        self._postings_idx: set[str] = set()

    def build(self, corpus: Corpus) -> None:
        for document in corpus:
            print(f"adding document to index [{document.docID}]")
            tokens = preprocessing.tokenize(document.title + " " + document.text)
            # First we add all the base terms to the main index
            i = 0 # Keep track of token position to fill positional index of every posting
            for t in tokens:
                current = PostingList({document.docID : [i]})
                if t in self._index:
                    self._index[t].merge(current)
                else:
                    self._postings_idx.add(document.docID)  # We add the posting to the index
                    self._index[t] = current
                i += 1

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