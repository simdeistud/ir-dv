import json
from .utils import preprocessing
from .utils.corpus import Corpus

class Posting:
    def __init__(self, docID: str):
        self.docID = docID

    def __eq__(self, other):
        return self.docID == other.docID

    def __gt__(self, other):
        return self.docID > other.docID

    def __repr__(self):
        return str(self.docID)

class PostingList:
    def __init__(self):
        self.postings = []

    def add_posting(self, posting: Posting):
        self.postings.append(posting)
        self.postings = sorted(self.postings)

    def merge(self, other: PostingList):
        self.postings.extend(other.postings)
        self.postings = sorted(set(self.postings))

    def __repr__(self):
        return str(self.postings)

class Index:
    def __init__(self):
        self.terms = { str : PostingList }

    def build(self, corpus: Corpus):
        for document in corpus.documents:
            print(f"adding document to index [{document.docID}]")
            types = set(preprocessing.tokenize(document.title + " " + document.text))
            for term in types:
                if term not in self.terms:
                    self.terms[term] = PostingList()
                self.terms[term].add_posting(Posting(document.docID))

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

