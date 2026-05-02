import nltk
nltk.download('punkt_tab')

def tokenize(text: str, method: str = "regexp", normalization: bool = True) -> list[str]:
    tokenizer = {
        "word": nltk.word_tokenize,
        "regexp": nltk.RegexpTokenizer(r'[A-Za-z]+').tokenize,
    }[method]
    return tokenizer(text.lower()) if normalization else tokenizer(text)

def remove_stopwords(tokens: list[str], lang: str = "english") -> list[str]:
    return [word for word in tokens if word.isalnum() and word not in set(nltk.corpus.stopwords.words(lang))]

def stem(tokens: list[str], method: str = "porter") -> list[str]:
    stemmer = {
        "porter": nltk.PorterStemmer().stem,
        "wordnet": nltk.WordNetLemmatizer().lemmatize,
    }[method]
    return [stemmer(word) for word in tokens]