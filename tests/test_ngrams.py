"""
tests/test_ngrams.py

Unit tests for reveal.cryptanalysis.ngrams module.
Run with: pytest tests/
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reveal.cryptanalysis.ngrams import (
    preprocess_for_ngrams,
    get_bigrams,
    get_trigrams,
    get_bigram_frequencies,
    get_trigram_frequencies,
    detect_unusual_bigrams,
    detect_repeated_ngrams,
    analyze_ngrams
)


# ── Tests for preprocess_for_ngrams ──────────────────────────────────────────

def test_preprocess_empty():
    assert preprocess_for_ngrams("") == []

def test_preprocess_whitespace():
    assert preprocess_for_ngrams("   ") == []

def test_preprocess_lowercases():
    result = preprocess_for_ngrams("Hello World")
    assert 'hello' in result
    assert 'world' in result

def test_preprocess_removes_punctuation():
    result = preprocess_for_ngrams("Hello, world!")
    assert ',' not in result
    assert '!' not in result

def test_preprocess_returns_list():
    result = preprocess_for_ngrams("Hello world")
    assert isinstance(result, list)


# ── Tests for get_bigrams ─────────────────────────────────────────────────────

def test_get_bigrams_empty():
    assert get_bigrams("") == []

def test_get_bigrams_single_word():
    assert get_bigrams("hello") == []

def test_get_bigrams_two_words():
    result = get_bigrams("hello world")
    assert len(result) == 1
    assert result[0] == ('hello', 'world')

def test_get_bigrams_returns_list():
    result = get_bigrams("the cat sat on the mat")
    assert isinstance(result, list)

def test_get_bigrams_correct_count():
    result = get_bigrams("the cat sat on the mat")
    assert len(result) == 5

def test_get_bigrams_are_tuples():
    result = get_bigrams("hello world today")
    assert isinstance(result[0], tuple)


# ── Tests for get_trigrams ────────────────────────────────────────────────────

def test_get_trigrams_empty():
    assert get_trigrams("") == []

def test_get_trigrams_two_words():
    assert get_trigrams("hello world") == []

def test_get_trigrams_three_words():
    result = get_trigrams("the cat sat")
    assert len(result) == 1
    assert result[0] == ('the', 'cat', 'sat')

def test_get_trigrams_returns_list():
    result = get_trigrams("the cat sat on the mat")
    assert isinstance(result, list)

def test_get_trigrams_correct_count():
    result = get_trigrams("the cat sat on the mat")
    assert len(result) == 4


# ── Tests for get_bigram_frequencies ─────────────────────────────────────────

def test_bigram_freq_empty():
    assert get_bigram_frequencies("") == {}

def test_bigram_freq_returns_dict():
    result = get_bigram_frequencies("the cat sat on the mat")
    assert isinstance(result, dict)

def test_bigram_freq_counts_correctly():
    result = get_bigram_frequencies("the cat the cat the cat")
    assert result.get('the cat') == 3

def test_bigram_freq_keys_are_strings():
    result = get_bigram_frequencies("the cat sat on the mat")
    for key in result:
        assert isinstance(key, str)


# ── Tests for get_trigram_frequencies ────────────────────────────────────────

def test_trigram_freq_empty():
    assert get_trigram_frequencies("") == {}

def test_trigram_freq_returns_dict():
    result = get_trigram_frequencies("the cat sat on the mat")
    assert isinstance(result, dict)

def test_trigram_freq_counts_correctly():
    result = get_trigram_frequencies("the cat sat the cat sat the cat sat")
    assert result.get('the cat sat') == 3

def test_trigram_freq_keys_are_strings():
    result = get_trigram_frequencies("the cat sat on the mat")
    for key in result:
        assert isinstance(key, str)


# ── Tests for detect_unusual_bigrams ─────────────────────────────────────────

def test_unusual_bigrams_empty():
    assert detect_unusual_bigrams("") == []

def test_unusual_bigrams_returns_list():
    result = detect_unusual_bigrams("the cat sat on the mat")
    assert isinstance(result, list)

def test_unusual_bigrams_common_text():
    result = detect_unusual_bigrams("it is in the of the")
    assert 'it is' not in result
    assert 'in the' not in result
    assert 'of the' not in result

def test_unusual_bigrams_unusual_text():
    result = detect_unusual_bigrams("zyx wvu tsr qpo nml")
    assert len(result) > 0

def test_unusual_bigrams_no_duplicates():
    result = detect_unusual_bigrams("cat dog cat dog cat dog")
    assert len(result) == len(set(result))


# ── Tests for detect_repeated_ngrams ─────────────────────────────────────────

def test_repeated_ngrams_empty():
    assert detect_repeated_ngrams("") == {}

def test_repeated_ngrams_returns_dict():
    result = detect_repeated_ngrams("the cat sat the cat sat")
    assert isinstance(result, dict)

def test_repeated_ngrams_finds_repeated():
    result = detect_repeated_ngrams("the cat sat the cat sat the cat sat")
    assert 'the cat' in result or 'cat sat' in result

def test_repeated_ngrams_min_count():
    result = detect_repeated_ngrams("hello world hello world hello world", min_count=3)
    assert all(v >= 3 for v in result.values())

def test_repeated_ngrams_no_singles():
    result = detect_repeated_ngrams("the cat sat on the mat today")
    assert all(v >= 2 for v in result.values())


# ── Tests for analyze_ngrams ──────────────────────────────────────────────────

def test_analyze_ngrams_returns_dict():
    result = analyze_ngrams("The cat sat on the mat.")
    assert isinstance(result, dict)

def test_analyze_ngrams_has_required_keys():
    result = analyze_ngrams("The cat sat on the mat.")
    for key in ['bigram_count', 'trigram_count', 'bigram_freq',
                'trigram_freq', 'unusual_bigrams', 'repeated_ngrams',
                'unusual_ratio', 'anomaly_detected']:
        assert key in result

def test_analyze_ngrams_empty_text():
    result = analyze_ngrams("")
    assert result['bigram_count'] == 0
    assert result['anomaly_detected'] == False

def test_analyze_ngrams_counts_positive():
    result = analyze_ngrams("The cat sat on the mat today.")
    assert result['bigram_count'] > 0
    assert result['trigram_count'] > 0

def test_analyze_ngrams_unusual_ratio_range():
    result = analyze_ngrams("The cat sat on the mat today.")
    assert 0.0 <= result['unusual_ratio'] <= 1.0

def test_analyze_ngrams_repeated_detection():
    text = "the cat sat the cat sat the cat sat the cat sat"
    result = analyze_ngrams(text)
    assert len(result['repeated_ngrams']) > 0

def test_analyze_ngrams_anomaly_repeated():
    text = "abc def abc def abc def abc def"
    result = analyze_ngrams(text)
    assert result['anomaly_detected'] == True

def test_analyze_ngrams_flags_are_bool():
    result = analyze_ngrams("The cat sat on the mat.")
    assert isinstance(result['anomaly_detected'], bool)

def test_analyze_ngrams_bigram_freq_is_dict():
    result = analyze_ngrams("The cat sat on the mat.")
    assert isinstance(result['bigram_freq'], dict)

def test_analyze_ngrams_unusual_bigrams_is_list():
    result = analyze_ngrams("The cat sat on the mat.")
    assert isinstance(result['unusual_bigrams'], list)