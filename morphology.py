from sklearn.externals import joblib
import pandas as pd
from nltk.stem.snowball import SnowballStemmer

from pymorphy2 import MorphAnalyzer

import constants

morph = MorphAnalyzer()
clf = joblib.load(constants.clf_model_file)
stemmer = SnowballStemmer("russian")


def get_part_of_speech(arr: list) -> list:
    try:
        return [f"{i}_{morph.parse(i)[0].tag.POS.replace('ADVB', 'ADV')}" for i in arr]
    finally:
        pass


def get_same_stem_russian(word1: str, word2: str) -> dict:
    if '_' in word1:
        word1 = word1[:word1.find('_')]
    if '_' in word2:
        word2 = word2[:word2.find('_')]

    a = stemmer.stem(word1)
    b = stemmer.stem(word2)

    maxLen = max(len(a), len(b))
    minLen = min(len(a), len(b))

    add, delete, change = levenshtein_distance(a, b)
    df = pd.DataFrame(data=[(maxLen, minLen, add, delete, change)],
                      columns=['maxLen', 'minLen', 'add', 'delete', 'change'])

    return {
        'predict': int(clf.predict(df)[0]),
        'predict_proba': float(clf.predict_proba(df)[:, 1][0])
    }


def levenshtein_distance(a, b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current_row = [(0, i, 0) for i in range(n + 1)]  # Keep current and previous row, not entire matrix
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [(i, 0, 0)] + [(0, 0, 0)] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j], current_row[j - 1], previous_row[j - 1]
            add = (add[0] + 1, add[1], add[2])
            delete = (delete[0], delete[1] + 1, delete[2])
            if a[j - 1] != b[i - 1]:
                change = (change[0], change[1], change[2] + 1)
            current_row[j] = min(add, delete, change, key=lambda x: sum(x))

    return current_row[n]
