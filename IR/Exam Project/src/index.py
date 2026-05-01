import json
from dataclasses import dataclass
from functools import total_ordering
from .utils import preprocessing
from .utils.corpus import *

class PostingList:
    def __init__(self, postings: dict[str, list[int]] | None = None):
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
        # The main index is a dictionary of posting lists
        self._index: dict[str, PostingList] = {}
        # We keep a set of all the docIDs to make answering NOT queries simpler
        self._postings_index: set[str] = set()

    def build(self, corpus: Corpus) -> None:
        for document in corpus:
            print(f"Adding document to index [{document.docID}]")
            tokens = preprocessing.tokenize(document.title + " " + document.main_text)
            # First we add all the base terms to the main index
            i = 0 # Keep track of token position to fill positional index of every posting
            for t in tokens:
                current = PostingList({document.docID : [i]})
                if t in self._index:
                    self._index[t].merge(current)
                else:
                    self._postings_index.add(document.docID)  # We add the posting to the index
                    self._index[t] = current
                i += 1

    def __getitem__(self, term):
        return self._index[term] if term in self._index else PostingList()
    
    def __iter__(self):
        return iter(self._index)

    def __len__(self):
        return len(self._index)

class PermutermIndex:
    def __init__(self):
        # Create index of permuterms
        self._permuterm_index: dict[str, str] = {}

    def build(self, index: InvertedIndex) -> None:
        for term in index:
            permuterms = PermutermIndex._get_permuterms(term)
            for permuterm in permuterms:
                self._permuterm_index[permuterm] = term

    @staticmethod
    def _get_permuterms(term: str) -> set[str]:
        rotation = f"{term}$"
        rotations = {rotation}
        for i in range(0, len(term)):
            rotation = rotation[1:] + rotation[0]
            rotations.add(rotation)
        return rotations

    def __getitem__(self, permuterm: str) -> str:
        return self._permuterm_index[permuterm] if permuterm in self._permuterm_index else ""
    
    def __iter__(self):
        return iter(self._permuterm_index)

class KGramIndex:
    def __init__(self, k: int):
        # Create index of k-grams
        self._k = k
        self._kgram_index: dict[str, set[str]] = {}
        
    def build(self, index: InvertedIndex) -> None:
        for term in index:
            kgrams = KGramIndex._get_kgrams(f"${term}$", self._k)
            for kgram in kgrams:
                if kgram in self._kgram_index: self._kgram_index[kgram].add(term)
                else: self._kgram_index[kgram] = set(term)

    @staticmethod
    def _get_kgrams(item: str, k: int) -> set[str]:
        if len(item) < k:
            raise ValueError(f"Cannot generate k-grams of strings shorter than {k} characters")
        kgrams: set[str] = set()
        for i in range(0, len(item)-k+1):
            kgrams.add(item[i:i+k])
        return kgrams

    def __getitem__(self, kgram: str) -> set[str]:
        return self._kgram_index[kgram] if kgram in self._kgram_index else set()
    
    def __iter__(self):
        return iter(self._kgram_index)