import nltk
nltk.download('punkt_tab')

def tokenize(text: str, normalization: bool = True) -> list[str]:
    return nltk.word_tokenize(text.lower(), language="english") if normalization else nltk.word_tokenize(text, language="english")

def remove_stopwords(tokens: list[str], lang: str = "english") -> list[str]:
    return [word for word in tokens if word.isalnum() and word not in set(nltk.corpus.stopwords.words(lang))]

def stem(tokens: list[str], method: str = "porter") -> list[str]:
    stemmer = {
        "porter": nltk.PorterStemmer().stem,
        "wordnet": nltk.WordNetLemmatizer().lemmatize,
    }[method]
    return [stemmer(word) for word in tokens]