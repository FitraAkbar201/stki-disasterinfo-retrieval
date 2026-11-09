from src.preprocessing import (clean_text, case_folding, tokenize,
                               remove_stopwords, stem, preprocess)


def test_clean_text_removes_url_mention_symbol():
    out = clean_text("RT @bbc: Quake hits Nepal!! http://t.co/x #help 100")
    assert "http" not in out and "@" not in out and "#" not in out
    assert "100" not in out and "Nepal" in out


def test_case_folding():
    assert case_folding("FLOOD Hits") == "flood hits"


def test_tokenize():
    assert tokenize("flood hits city") == ["flood", "hits", "city"]


def test_stopword_removal():
    assert remove_stopwords(["the", "flood", "is", "in", "city"]) == ["flood", "city"]


def test_stemming():
    assert stem(["flooding", "floods", "killed"]) == ["flood", "flood", "kill"]


def test_pipeline_same_for_query_variants():
    assert preprocess("Flooding in Colorado!") == preprocess("floods colorado")


def test_pipeline_empty_after_filtering():
    assert preprocess("the of and http://t.co/x") == []
