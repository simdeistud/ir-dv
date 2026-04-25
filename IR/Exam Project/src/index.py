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

