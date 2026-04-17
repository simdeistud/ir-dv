
def build_index(corpus):
    reverse_index = {}
    for i in range(0, len(corpus)):
        dictionary = {}
        for token in corpus[i]:
            dictionary[token] = i
        for term in dictionary.keys:
            reverse_index[term].append(i)
    return reverse_index
