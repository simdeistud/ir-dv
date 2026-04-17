from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

TOKENIZER = RegexpTokenizer(r"[A-Za-z]+")
STOP_WORDS = set(stopwords.words("english"))
STEMMER = PorterStemmer()

def preprocess_document(document):
    # Text tokenization
    tokens = TOKENIZER.tokenize(document)
    # Text to lowercase
    tokens = [t.lower() for t in tokens]
    # Stopwords removal
    tokens = [t for t in tokens if t not in STOP_WORDS]
    # Stemming
    tokens = [STEMMER.stem(t) for t in tokens]
    return tokens




