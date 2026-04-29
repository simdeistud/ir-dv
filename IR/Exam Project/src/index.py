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
        return self._index[item] if item in self._index else PostingList()

    def __len__(self):
        return len(self._index)

class InvertedPermutermIndex:
    def __init__(self):
        # The main index is an ordered list of Terms
        self._index: dict[str, PostingList] = {}
        self._permuterm_index: dict[str, str] = {}
        # We keep a set of all the docIDs to make answering NOT queries simpler
        self._postings_idx: set[str] = set()

    def build(self, corpus: Corpus) -> None:
        for document in corpus:
            print(f"adding document to index [{document.docID}]")
            tokens = preprocessing.tokenize(document.title + " " + document.text)
            # First we add all the base terms to the main index
            i = 0  # Keep track of token position to fill positional index of every posting
            for t in tokens:
                current = PostingList({document.docID: [i]})
                if t in self._index:
                    self._index[t].merge(current)
                else:
                    self._postings_idx.add(document.docID)  # We add the posting to the index
                    self._index[t] = current
                i += 1
        for term in self._index:
            permuterms = self._get_permuterms(term)
            for permuterm in permuterms:
                self._permuterm_index[permuterm] = term

    def _get_permuterms(self, term: str) -> set[str]:
        rotation = f"{term}$"
        rotations = {rotation}
        for i in range(0, len(term)):
            rotation = rotation[1:] + rotation[0]
            rotations.add(rotation)
        return rotations

    def __getitem__(self, item: str) -> PostingList | list[PostingList]:
        if item[-1] == "*":
            prefix = item[:-1]
            terms = set(self._permuterm_index[match] for match in self._permuterm_index if match.startswith(prefix))
            return [self._index[term] for term in terms]
        else: return self._index[item] if item in self._index else PostingList()

    def __len__(self):
        return len(self._index)

class InvertedKGramIndex:
    def __init__(self, k: int):
        # The main index is an ordered list of Terms
        self._index: dict[str, PostingList] = {}
        self._kgram_index: dict[str, set[str]] = {}
        self._k = k
        # We keep a set of all the docIDs to make answering NOT queries simpler
        self._postings_idx: set[str] = set()

    def build(self, corpus: Corpus) -> None:
        for document in corpus:
            print(f"adding document to index [{document.docID}]")
            tokens = preprocessing.tokenize(document.title + " " + document.text)
            # First we add all the base terms to the main index
            i = 0  # Keep track of token position to fill positional index of every posting
            for t in tokens:
                current = PostingList({document.docID: [i]})
                if t in self._index:
                    self._index[t].merge(current)
                else:
                    self._postings_idx.add(document.docID)  # We add the posting to the index
                    self._index[t] = current
                i += 1
        for term in self._index:
            kgrams = self._get_kgrams(f"${term}$")
            for kgram in kgrams:
                if kgram in self._kgram_index: self._kgram_index[kgram].add(term)
                else: self._kgram_index[kgram] = set(term)

    def _get_kgrams(self, item: str) -> set[str]:
        if len(item) < self._k:
            raise ValueError(f"Cannot generate k-grams of strings shorter than {self._k} characters")
        kgrams: set[str] = set()
        for i in range(0, len(item)-self._k+1):
            kgrams.add(item[i:i+self._k])
        return kgrams

    def get_from_term(self, term: str) -> PostingList:
        return self._index[term] if term in self._index else PostingList()

    def get_from_kgram(self, kgram: str) -> PostingList:
        result: PostingList = PostingList()
        if kgram in self._kgram_index:
            for term in self._kgram_index[kgram]:
                result.merge(self.get_from_term(term))
        return result

    def __getitem__(self, item: str) -> PostingList:
        result: PostingList = PostingList()
        # If the search term doesn't contain a wildcard, we simply obtain its k-grams, find the common term by intersection, and merge their posting lists
        if "*" not in item:
            kgrams = self._get_kgrams(f"${item}$")
            # We find all the common term by intersection
            common_termset: set[str] = set(self._index)
            for kgram in kgrams:
                common_termset.intersection_update(self._kgram_index[kgram])
            # We merge the posting lists of the terms
            for term in common_termset:
                result.merge(self.get_from_term(term))
        # If the search term contains a wildcard, we split it into substrings and then intersect their results
        else:
            # TODO: separate this code
            common_termset: set[str] = set(self._index)
            for substring in f"${item}$".split("*"):
                # If the wildcard is at the start or end, the substring will be just "$", so we can skip it
                if substring == "$":
                    continue
                kgrams = self._get_kgrams(substring)
                for kgram in kgrams:
                    common_termset.intersection_update(self._kgram_index[kgram])
                # We merge the posting lists of the terms
                for term in common_termset:
                    result.merge(self.get_from_term(term))
        return result

    def __len__(self):
        return len(self._index)