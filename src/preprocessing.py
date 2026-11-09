"""Tahap 3 - Preprocessing teks (bahasa Inggris).

Alur: cleaning -> case folding -> tokenizing -> stopword removal -> stemming.
Fungsi dipisah per langkah supaya mudah dijelaskan dan diuji satu per satu.
"""
import re
from functools import lru_cache

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

try:
    STOPWORDS = set(stopwords.words("english"))
except LookupError:                      # pertama kali dijalankan
    nltk.download("stopwords", quiet=True)
    STOPWORDS = set(stopwords.words("english"))

# Kata umum di tweet yang tidak membawa makna pencarian.
STOPWORDS |= {"rt", "via", "amp", "u", "im", "ive", "dont", "cant"}

_stemmer = PorterStemmer()


def clean_text(text: str) -> str:
    """Buang URL, mention, dan karakter non-huruf (angka ikut dibuang)."""
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"@\w+", " ", text)
    text = text.replace("#", " ")
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def case_folding(text: str) -> str:
    return text.lower()


def tokenize(text: str) -> list:
    return text.split()


def remove_stopwords(tokens: list) -> list:
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]


@lru_cache(maxsize=None)
def _stem(word: str) -> str:
    return _stemmer.stem(word)


def stem(tokens: list) -> list:
    return [_stem(t) for t in tokens]


def preprocess(text: str) -> list:
    """Pipeline lengkap, mengembalikan daftar token akhir."""
    text = case_folding(clean_text(text))
    return stem(remove_stopwords(tokenize(text)))


def preprocess_steps(text: str) -> dict:
    """Hasil tiap langkah, berguna untuk laporan dan demo."""
    cleaned = clean_text(text)
    folded = case_folding(cleaned)
    tokens = tokenize(folded)
    no_stop = remove_stopwords(tokens)
    return {"cleaning": cleaned, "case_folding": folded, "tokenizing": tokens,
            "stopword_removal": no_stop, "stemming": stem(no_stop)}


if __name__ == "__main__":
    import json
    s = "RT @bbc: Earthquake hits Nepal!! 1,000 people killed http://t.co/xyz #nepalquake"
    print(json.dumps(preprocess_steps(s), indent=2))
