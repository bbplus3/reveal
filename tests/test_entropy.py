"""
tests/test_entropy.py

Unit tests for reveal.cryptanalysis.entropy module.
Run with: pytest tests/
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reveal.cryptanalysis.entropy import (
    shannon_entropy,
    word_entropy,
    classify_entropy,
    detect_anomalous_words,
    analyze_entropy
)


# ── Tests for shannon_entropy ─────────────────────────────────────────────────

def test_shannon_entropy_empty():
    assert shannon_entropy("") == 0.0

def test_shannon_entropy_single_char():
    assert shannon_entropy("AAAAAAAAAA") == 0.0

def test_shannon_entropy_two_chars():
    result = shannon_entropy("ABABABABAB")
    assert result == 1.0

def test_shannon_entropy_high_randomness():
    result = shannon_entropy("1a2b3c4d5e")
    assert result > 3.0

def test_shannon_entropy_returns_float():
    result = shannon_entropy("hello world")
    assert isinstance(result, float)

def test_shannon_entropy_positive():
    result = shannon_entropy("hello world")
    assert result >= 0.0

def test_shannon_entropy_normal_text():
    result = shannon_entropy("The quick brown fox jumps over the lazy dog")
    assert 3.5 <= result <= 5.0

def test_shannon_entropy_repeated_pattern():
    result = shannon_entropy("abcabcabcabc")
    assert result < 2.0


# ── Tests for word_entropy ────────────────────────────────────────────────────

def test_word_entropy_empty():
    assert word_entropy("") == 0.0

def test_word_entropy_single_word():
    result = word_entropy("hello hello hello hello")
    assert result == 0.0

def test_word_entropy_all_unique():
    result = word_entropy("the quick brown fox jumps")
    assert result > 2.0

def test_word_entropy_returns_float():
    result = word_entropy("some sample text here")
    assert isinstance(result, float)

def test_word_entropy_positive():
    result = word_entropy("some sample text here")
    assert result >= 0.0

def test_word_entropy_whitespace_only():
    assert word_entropy("   ") == 0.0


# ── Tests for classify_entropy ────────────────────────────────────────────────

def test_classify_very_low():
    assert classify_entropy(1.0) == 'very_low'

def test_classify_low():
    assert classify_entropy(2.5) == 'low'

def test_classify_normal():
    assert classify_entropy(4.0) == 'normal'

def test_classify_high():
    assert classify_entropy(5.2) == 'high'

def test_classify_very_high():
    assert classify_entropy(6.0) == 'very_high'

def test_classify_boundary_low():
    assert classify_entropy(2.0) == 'very_low'

def test_classify_boundary_normal_min():
    assert classify_entropy(3.5) == 'normal'

def test_classify_boundary_normal_max():
    assert classify_entropy(5.0) == 'normal'

def test_classify_returns_string():
    assert isinstance(classify_entropy(4.0), str)


# ── Tests for detect_anomalous_words ─────────────────────────────────────────

def test_detect_anomalous_empty():
    result = detect_anomalous_words("")
    assert result == []

def test_detect_anomalous_normal_text():
    result = detect_anomalous_words("The cat sat on the mat today.")
    assert isinstance(result, list)

def test_detect_anomalous_finds_random_token():
    result = detect_anomalous_words("Please contact xK9mP2qRzZbVwWnN for details.", threshold=3.5)
    assert len(result) >= 1

def test_detect_anomalous_returns_list_of_dicts():
    result = detect_anomalous_words("Normal text with xK9mP2qR inside.")
    if result:
        assert 'word' in result[0]
        assert 'entropy' in result[0]

def test_detect_anomalous_sorted_by_entropy():
    result = detect_anomalous_words("xK9mP2qR zZzZzZzZ normal words here today")
    if len(result) >= 2:
        assert result[0]['entropy'] >= result[1]['entropy']

def test_detect_anomalous_skips_short_words():
    result = detect_anomalous_words("ab cd ef gh")
    assert result == []


# ── Tests for analyze_entropy ─────────────────────────────────────────────────

def test_analyze_entropy_returns_dict():
    result = analyze_entropy("The cat sat on the mat.")
    assert isinstance(result, dict)

def test_analyze_entropy_has_required_keys():
    result = analyze_entropy("The cat sat on the mat.")
    for key in ['char_entropy', 'word_entropy', 'char_classification',
                'word_classification', 'anomalous_words', 'anomaly_detected',
                'high_entropy_flag', 'low_entropy_flag']:
        assert key in result

def test_analyze_entropy_empty_text():
    result = analyze_entropy("")
    assert result['char_entropy'] == 0.0
    assert result['anomaly_detected'] == False

def test_analyze_entropy_normal_text():
    result = analyze_entropy("The quick brown fox jumps over the lazy dog.")
    assert result['char_classification'] == 'normal'
    assert result['high_entropy_flag'] == False

def test_analyze_entropy_repetitive_text():
    result = analyze_entropy("aaaaaaaaaaaaaaaaaaaaaaaa")
    assert result['low_entropy_flag'] == True
    assert result['anomaly_detected'] == True

def test_analyze_entropy_anomalous_word_detected():
    result = detect_anomalous_words("Please send to xK9mP2qRzZbVwWnNjJ for processing.", threshold=3.5)
    assert len(result) >= 1

def test_analyze_entropy_flags_are_bool():
    result = analyze_entropy("Some text here.")
    assert isinstance(result['high_entropy_flag'], bool)
    assert isinstance(result['low_entropy_flag'], bool)
    assert isinstance(result['anomaly_detected'], bool)

def test_analyze_entropy_char_entropy_positive():
    result = analyze_entropy("Some text here.")
    assert result['char_entropy'] >= 0.0

def test_analyze_entropy_word_entropy_positive():
    result = analyze_entropy("Some text here.")
    assert result['word_entropy'] >= 0.0