
from pathlib import Path
import re

import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem


def normalize_text(filename):
    with open(filename, encoding="utf-8") as source:
        text = source.read()

    try:
        russian_stopwords = set(stopwords.words("russian"))
    except LookupError:
        nltk.download("stopwords", quiet=True)
        russian_stopwords = set(stopwords.words("russian"))

    mystem = Mystem()
    lemmas = mystem.lemmatize(text.lower())
    words = [lemma.strip() for lemma in lemmas if lemma.strip().isalpha()]
    words = [word for word in words if word not in russian_stopwords]
    result = " ".join(words)
    Path("result.txt").write_text(result, encoding="utf-8")
    return result


if __name__ == "__main__":
    normalize_text("text.txt")
