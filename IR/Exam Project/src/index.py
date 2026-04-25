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
    def __init__(self):
        self.postings = set[Posting]()

    def add_posting(self, posting: Posting):
        self.postings.add(posting)
        self.postings = self.postings

    def merge(self, other: PostingList):
        self.postings.union(other.postings)
        self.postings = self.postings

    def __repr__(self):
        return str(self.postings)

class Index:
    def __init__(self):
        self.terms = { str : PostingList() }
        self.docIDs = set[Posting]()

    def build(self, corpus: Corpus):
        for document in corpus.documents:
            print(f"adding document to index [{document.docID}]")
            types = set(preprocessing.tokenize(document.title + " " + document.text))
            for term in types:
                if term not in self.terms:
                    self.terms[term] = PostingList()
                self.terms[term].add_posting(Posting(document.docID))
            self.docIDs.add(Posting(document.docID))

    def load(self, path: str):
        with open(path) as f:
            self.terms = json.load(f)

    def save(self, path: str):
        with open(path, "w") as f:
            json.dump(self.terms, f)

    def merge(self, index: Index):
        None

    def merge(self, corpus: Corpus):
        None

