from collections import OrderedDict

class Posting:
    def __init__(self, docID):
        self.docID = docID

    def __eq__(self, other):
        return self.docID == other.docID

    def __gt__(self, other):
        return self.docID > other.docID

    def __str__(self):
        return str(self.docID)

class PostingList:
    def __init__(self):
        self.postings = []

    def add_posting(self, posting):
        self.postings.append(posting)
        self.postings = sorted(self.postings, key=lambda posting: posting.docID)

    def merge(self, other):
        self.postings.extend(other)
        self.postings = sorted(set(self.postings), key=lambda posting: posting.docID)

class Index:
    def __init__(self):
        self.terms = {}

    def build(self, corpus):
        for document in corpus:
            for term in set(document.terms):
                if term not in self.terms:
                    self.terms[term] = PostingList()
                self.terms[term].add_posting(Posting(document.docID))
        self.terms = dict(sorted(self.terms.items()))

    def load(self, path):

    def save(self, path):

    def merge(self, corpus):

