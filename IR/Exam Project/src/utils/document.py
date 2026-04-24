import nltk

class Document:
    def __init__(self, docID, title, authors, metadata, text):
        self.docID = docID
        self.title = title
        self.authors = authors
        self.metadata = metadata
        self.text = text
        self.tokens = []

def tokenize(document):

def normalize(document):

def remove_stopwords(document):

def stem(document):