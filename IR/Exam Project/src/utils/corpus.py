from .document import *

class Corpus:
    def __init__(self):
        self._documents = []
    
    def build(self, path: str):
        pass

    def __getitem__(self, index):
        return self._documents[index]
        
    def __iter__(self):
        return iter(self._documents)
    
class CranfieldCorpus(Corpus):
    def __init__(self):
        super().__init__()
    
    def build(self, path: str):
        self._documents = CranfieldCorpus._parse(path)
    
    @staticmethod
    def _parse(path: str) -> list[CranfieldDocument]:
        documents: list[CranfieldDocument] = []
        # Parse the Cranfield file to divide it into document chunks
        # which will be parsed individually by the document class
        # and added to the corpus accordingly.
        with open(path) as f:
            doc_raw_text: str = "" 
            for line in f:
                if line.startswith(".I"):
                    # Special case for the first document
                    if len(doc_raw_text) == 0:
                        doc_raw_text = line
                    else:
                        # The next time we encounter .I it means our current document
                        # has ended and we should parse it and add it to the corpus.
                        document = CranfieldDocument(doc_raw_text)
                        documents.append(document)
                        doc_raw_text = line
                else:
                    doc_raw_text += line
            # Add last document, since it ends with EOF and not another .I
            document = CranfieldDocument(doc_raw_text)
            documents.append(document)
        return documents