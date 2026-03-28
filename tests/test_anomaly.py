"""
tests/test_anomaly.py

Unit tests for reveal.cryptanalysis.anomaly module.
Run with: pytest tests/
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reveal.cryptanalysis.anomaly import (
    extract_word_features,
    extract_features_from_text,
    detect_length_outliers,
    detect_capitalization_anomalies,
    detect_isolation_forest_outliers,
    analyze_anomalies
)


# ── Tests for extract_word_features ──────────────────────────────────────────

def test_extract_features_empty():
    result = extract_word_features("")
    assert result == [0.0, 0.0, 0.0, 0.0, 0.0]

def test_extract_features_returns_list():
    result = extract_word_features("hello")
    assert isinstance(result, list)

def test_extract_features_length():
    result = extract_word_features("hello")
    assert len(result) == 5

def test_extract_features_word_length():
    result = extract_word_features("hello")
    assert result[0] == 5.0

def test_extract_features_all_caps():
    result = extract_word_features("HELLO")
    assert result[1] == 1.0

def test_extract_features_no_caps():
    result = extract_word_features("hello")
    assert result[1] == 0.0

def test_extract_features_all_digits():
    result = extract_word_features("12345")
    assert result[2] == 1.0

def test_extract_features_ratios_in_range():
    result = extract_word_features("Hello123!")
    for ratio in result[1:]:
        assert 0.0 <= ratio <= 1.0


# ── Tests for extract_features_from_text ─────────────────────────────────────

def test_extract_from_text_empty():
    words, features = extract_features_from_text("")
    assert words == []
    assert features == []

def test_extract_from_text_returns_tuple():
    result = extract_features_from_text("hello world")
    assert isinstance(result, tuple)
    assert len(result) == 2

def test_extract_from_text_word_count():
    words, features = extract_features_from_text("hello world today")
    assert len(words) == 3
    assert len(features) == 3

def test_extract_from_text_features_length():
    words, features = extract_features_from_text("hello world")
    assert len(features[0]) == 5


# ── Tests for detect_length_outliers ─────────────────────────────────────────

def test_length_outliers_empty():
    assert detect_length_outliers("") == []

def test_length_outliers_too_few_words():
    assert detect_length_outliers("hello world") == []

def test_length_outliers_returns_list():
    result = detect_length_outliers("the cat sat on the mat today")
    assert isinstance(result, list)

def test_length_outliers_finds_long_word():
    text = "the cat sat on the mat supercalifragilisticexpialidocious today"
    result = detect_length_outliers(text)
    assert any(o['word'] == 'supercalifragilisticexpialidocious' for o in result)

def test_length_outliers_has_required_keys():
    text = "the cat sat on the mat supercalifragilisticexpialidocious today"
    result = detect_length_outliers(text)
    if result:
        for key in ['word', 'length', 'deviation', 'direction']:
            assert key in result[0]

def test_length_outliers_direction_long():
    text = "the cat sat on the mat supercalifragilisticexpialidocious today"
    result = detect_length_outliers(text)
    long_words = [o for o in result if o['direction'] == 'long']
    assert len(long_words) >= 1

def test_length_outliers_sorted_by_deviation():
    text = "the cat sat on the mat supercalifragilisticexpialidocious pneumonoultramicroscopicsilicovolcanoconiosis"
    result = detect_length_outliers(text)
    if len(result) >= 2:
        assert result[0]['deviation'] >= result[1]['deviation']

def test_length_outliers_uniform_text():
    result = detect_length_outliers("cat bat hat mat rat sat")
    assert result == []


# ── Tests for detect_capitalization_anomalies ─────────────────────────────────

def test_cap_anomalies_empty():
    assert detect_capitalization_anomalies("") == []

def test_cap_anomalies_returns_list():
    result = detect_capitalization_anomalies("The cat sat on the mat.")
    assert isinstance(result, list)

def test_cap_anomalies_normal_text():
    result = detect_capitalization_anomalies("The cat sat on the mat.")
    assert result == []

def test_cap_anomalies_all_caps_word():
    result = detect_capitalization_anomalies("Please contact ADMIN for help.")
    assert any(o['word'] == 'ADMIN' for o in result)

def test_cap_anomalies_mixed_case():
    result = detect_capitalization_anomalies("Please contact camelCaseWord for help.")
    assert any(o['pattern'] == 'mixed_case' for o in result)

def test_cap_anomalies_has_required_keys():
    result = detect_capitalization_anomalies("Please contact ADMIN for help.")
    if result:
        assert 'word' in result[0]
        assert 'pattern' in result[0]

def test_cap_anomalies_all_caps_pattern():
    result = detect_capitalization_anomalies("The quick BROWN fox jumps.")
    patterns = [o['pattern'] for o in result]
    assert 'all_caps' in patterns


# ── Tests for detect_isolation_forest_outliers ────────────────────────────────

def test_isolation_empty():
    assert detect_isolation_forest_outliers("") == []

def test_isolation_too_few_words():
    assert detect_isolation_forest_outliers("hello world") == []

def test_isolation_returns_list():
    text = "the cat sat on the mat today and yesterday and tomorrow"
    result = detect_isolation_forest_outliers(text)
    assert isinstance(result, list)

def test_isolation_has_required_keys():
    text = "the cat sat on the mat today and yesterday and tomorrow"
    result = detect_isolation_forest_outliers(text)
    if result:
        assert 'word' in result[0]
        assert 'features' in result[0]

def test_isolation_features_length():
    text = "the cat sat on the mat today and yesterday and tomorrow"
    result = detect_isolation_forest_outliers(text)
    if result:
        assert len(result[0]['features']) == 5


# ── Tests for analyze_anomalies ───────────────────────────────────────────────

def test_analyze_anomalies_returns_dict():
    result = analyze_anomalies("The cat sat on the mat.")
    assert isinstance(result, dict)

def test_analyze_anomalies_has_required_keys():
    result = analyze_anomalies("The cat sat on the mat.")
    for key in ['length_outliers', 'capitalization_anomalies',
                'isolation_outliers', 'total_anomalies', 'anomaly_detected']:
        assert key in result

def test_analyze_anomalies_empty_text():
    result = analyze_anomalies("")
    assert result['total_anomalies'] == 0
    assert result['anomaly_detected'] == False

def test_analyze_anomalies_flag_is_bool():
    result = analyze_anomalies("The cat sat on the mat.")
    assert isinstance(result['anomaly_detected'], bool)

def test_analyze_anomalies_total_count():
    result = analyze_anomalies("The cat sat on the mat.")
    expected = (
        len(result['length_outliers']) +
        len(result['capitalization_anomalies']) +
        len(result['isolation_outliers'])
    )
    assert result['total_anomalies'] == expected

def test_analyze_anomalies_detects_caps():
    result = analyze_anomalies("Please contact ADMIN and camelCaseWord for help today.")
    assert len(result['capitalization_anomalies']) >= 1

def test_analyze_anomalies_detects_long_word():
    text = "the cat sat on the mat supercalifragilisticexpialidocious today here"
    result = analyze_anomalies(text)
    assert len(result['length_outliers']) >= 1
    assert result['anomaly_detected'] == True