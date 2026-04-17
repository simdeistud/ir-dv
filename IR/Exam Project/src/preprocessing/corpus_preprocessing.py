from document_preprocessing import preprocess_document

def preprocess_corpus(corpus):
    return [preprocess_document(document) for document in corpus]