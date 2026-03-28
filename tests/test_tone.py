"""
tests/test_tone.py

Unit tests for reveal.linguistic.tone module.
Run with: pytest tests/
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reveal.linguistic.tone import (
    detect_tone_signals,
    classify_dominant_tone,
    analyze_tone_by_sentence,
    analyze_tone
)


# ── Tests for detect_tone_signals ─────────────────────────────────────────────

def test_detect_persuasive():
    result = detect_tone_signals("You should believe me, the truth is obvious.")
    assert 'persuasive' in result

def test_detect_informative():
    result = detect_tone_signals("According to research shows the data suggests this is true.")
    assert 'informative' in result

def test_detect_instructional():
    result = detect_tone_signals("First make sure you follow these instructions carefully.")
    assert 'instructional' in result

def test_detect_warning():
    result = detect_tone_signals("Warning this is a danger zone, beware of the risk.")
    assert 'warning' in result

def test_detect_sarcastic():
    result = detect_tone_signals("Oh great, yeah right, what a surprise totally.")
    assert 'sarcastic' in result

def test_detect_emotional():
    result = detect_tone_signals("I feel so overwhelmed, I am so sad and I cannot believe this.")
    assert 'emotional' in result

def test_detect_accusatory():
    result = detect_tone_signals("You always do this, it is your fault, you lied to me.")
    assert 'accusatory' in result

def test_detect_manipulative():
    result = detect_tone_signals("If you really cared you would stay. You need me, no one will believe you.")
    assert 'manipulative' in result

def test_detect_empty_text():
    result = detect_tone_signals("")
    assert result == {}

def test_detect_clean_text():
    result = detect_tone_signals("The cat sat on the mat.")
    assert result == {}

def test_detect_returns_dict():
    result = detect_tone_signals("You should do this.")
    assert isinstance(result, dict)

def test_detect_multiple_tones():
    result = detect_tone_signals("Warning you should believe me, you always do this.")
    assert len(result) >= 2


# ── Tests for classify_dominant_tone ─────────────────────────────────────────

def test_classify_neutral_when_empty():
    result = classify_dominant_tone({})
    assert result == 'neutral'

def test_classify_single_tone():
    result = classify_dominant_tone({'persuasive': ['you should', 'believe me']})
    assert result == 'persuasive'

def test_classify_priority_manipulative_over_persuasive():
    result = classify_dominant_tone({
        'manipulative': ['you need me', 'no one will believe you'],
        'persuasive': ['you should', 'believe me']
    })
    assert result == 'manipulative'

def test_classify_priority_accusatory_over_warning():
    result = classify_dominant_tone({
        'accusatory': ['you always', 'you lied'],
        'warning': ['danger']
    })
    assert result == 'accusatory'

def test_classify_returns_string():
    result = classify_dominant_tone({'warning': ['danger', 'beware']})
    assert isinstance(result, str)


# ── Tests for analyze_tone_by_sentence ───────────────────────────────────────

def test_by_sentence_returns_list():
    result = analyze_tone_by_sentence("You should do this. Warning this is dangerous.")
    assert isinstance(result, list)

def test_by_sentence_correct_count():
    result = analyze_tone_by_sentence("You should do this. Warning this is dangerous.")
    assert len(result) == 2

def test_by_sentence_has_required_keys():
    result = analyze_tone_by_sentence("You should do this.")
    assert 'sentence' in result[0]
    assert 'tone_matches' in result[0]
    assert 'dominant_tone' in result[0]

def test_by_sentence_empty_text():
    result = analyze_tone_by_sentence("")
    assert result == []

def test_by_sentence_neutral_clean_text():
    result = analyze_tone_by_sentence("The cat sat on the mat.")
    assert result[0]['dominant_tone'] == 'neutral'

def test_by_sentence_preserves_sentence():
    text = "You should do this."
    result = analyze_tone_by_sentence(text)
    assert result[0]['sentence'] == text


# ── Tests for analyze_tone ────────────────────────────────────────────────────

def test_analyze_tone_returns_dict():
    result = analyze_tone("You should do this.")
    assert isinstance(result, dict)

def test_analyze_tone_has_required_keys():
    result = analyze_tone("You should do this.")
    for key in ['sentence_count', 'tone_matches', 'dominant_tone',
                'tone_distribution', 'high_risk_tones', 'sentence_tones']:
        assert key in result

def test_analyze_tone_empty_text():
    result = analyze_tone("")
    assert result['sentence_count'] == 0
    assert result['dominant_tone'] == 'neutral'
    assert result['high_risk_tones'] == []

def test_analyze_tone_clean_text():
    result = analyze_tone("The cat sat on the mat.")
    assert result['dominant_tone'] == 'neutral'
    assert result['high_risk_tones'] == []

def test_analyze_tone_high_risk_manipulative():
    result = analyze_tone("You need me, no one will believe you. If you really cared you would stay.")
    assert 'manipulative' in result['high_risk_tones']

def test_analyze_tone_high_risk_accusatory():
    result = analyze_tone("You always do this. It is your fault. You lied to me.")
    assert 'accusatory' in result['high_risk_tones']

def test_analyze_tone_distribution_is_dict():
    result = analyze_tone("You should do this. Warning this is dangerous.")
    assert isinstance(result['tone_distribution'], dict)

def test_analyze_tone_sentence_count():
    result = analyze_tone("You should do this. Warning this is dangerous. The cat sat.")
    assert result['sentence_count'] == 3

def test_analyze_tone_sentence_tones_is_list():
    result = analyze_tone("You should do this.")
    assert isinstance(result['sentence_tones'], list)

def test_analyze_tone_persuasive_detected():
    result = analyze_tone("You should believe me, the truth is we all know what happened.")
    assert result['dominant_tone'] == 'persuasive'