import gensim


def load_w2v_model(file_name: str):
    print("starting to load a w2v model")
    w2v_model = gensim.models.KeyedVectors.load_word2vec_format(file_name)
    print("w2v model '%s' loaded" % file_name)
    return w2v_model


# Получить вектора массива слов
def get_vectors(words: list, v2w_model) -> list:
    try:
        return [v2w_model[word] for word in words]
    except MemoryError:
        return []


# Получить вектор слова
def get_similarity(word1: str, word2: str, v2w_model) -> list:
    try:
        return v2w_model.similarity(word1, word2)
    except MemoryError:
        return []


# Получить tn ассоциаций
def get_associations(word: str, w2v_model, tn=10) -> list:
    assoc_lst = []
    try:
        assoc_lst = w2v_model.most_similar(positive=[word], topn=tn)
    except MemoryError:
        pass
    finally:
        if assoc_lst == []:
            raise KeyError
        return assoc_lst
