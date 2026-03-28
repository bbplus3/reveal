"""
tests/test_pov.py

Unit tests for reveal.linguistic.pov module.
Run with: pytest tests/
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reveal.linguistic.pov import (
    detect_pov_signals,
    classify_pov,
    analyze_pov_by_sentence,
    detect_pov_shifts,
    analyze_pov
)


# ── Tests for detect_pov_signals ──────────────────────────────────────────────

def test_detect_first_person():
    result = detect_pov_signals("I feel alone and my heart is broken.")
    assert result['first_person']['count'] > 0
    assert 'i' in result['first_person']['pronouns']

def test_detect_second_person():
    result = detect_pov_signals("You always do this and it is your fault.")
    assert result['second_person']['count'] > 0
    assert 'you' in result['second_person']['pronouns']

def test_detect_third_person():
    result = detect_pov_signals("She went to the store and they followed her.")
    assert result['third_person']['count'] > 0
    assert 'she' in result['third_person']['pronouns']

def test_detect_empty_text():
    result = detect_pov_signals("")
    assert result['first_person']['count'] == 0
    assert result['second_person']['count'] == 0
    assert result['third_person']['count'] == 0

def test_detect_no_pronouns():
    result = detect_pov_signals("The cat sat on the mat.")
    assert result['first_person']['count'] == 0
    assert result['second_person']['count'] == 0

def test_detect_we_as_first_person():
    result = detect_pov_signals("We are all in this together.")
    assert result['first_person']['count'] > 0
    assert 'we' in result['first_person']['pronouns']

def test_detect_returns_dict():
    result = detect_pov_signals("I went to the store.")
    assert isinstance(result, dict)
    for key in ['first_person', 'second_person', 'third_person']:
        assert key in result

def test_detect_count_accuracy():
    result = detect_pov_signals("I told you that I was right.")
    assert result['first_person']['count'] == 2
    assert result['second_person']['count'] == 1

def test_detect_yourself_as_second_person():
    result = detect_pov_signals("Do it yourself.")
    assert result['second_person']['count'] > 0


# ── Tests for classify_pov ────────────────────────────────────────────────────

def test_classify_first_person():
    signals = {
        'first_person':  {'count': 5, 'pronouns': []},
        'second_person': {'count': 0, 'pronouns': []},
        'third_person':  {'count': 1, 'pronouns': []}
    }
    assert classify_pov(signals) == 'first'

def test_classify_second_person():
    signals = {
        'first_person':  {'count': 0, 'pronouns': []},
        'second_person': {'count': 5, 'pronouns': []},
        'third_person':  {'count': 0, 'pronouns': []}
    }
    assert classify_pov(signals) == 'second'

def test_classify_third_person():
    signals = {
        'first_person':  {'count': 0, 'pronouns': []},
        'second_person': {'count': 0, 'pronouns': []},
        'third_person':  {'count': 5, 'pronouns': []}
    }
    assert classify_pov(signals) == 'third'

def test_classify_unknown_no_pronouns():
    signals = {
        'first_person':  {'count': 0, 'pronouns': []},
        'second_person': {'count': 0, 'pronouns': []},
        'third_person':  {'count': 0, 'pronouns': []}
    }
    assert classify_pov(signals) == 'unknown'

def test_classify_mixed():
    signals = {
        'first_person':  {'count': 3, 'pronouns': []},
        'second_person': {'count': 3, 'pronouns': []},
        'third_person':  {'count': 2, 'pronouns': []}
    }
    assert classify_pov(signals) == 'mixed'

def test_classify_returns_string():
    signals = {
        'first_person':  {'count': 5, 'pronouns': []},
        'second_person': {'count': 0, 'pronouns': []},
        'third_person':  {'count': 0, 'pronouns': []}
    }
    assert isinstance(classify_pov(signals), str)


# ── Tests for analyze_pov_by_sentence ────────────────────────────────────────

def test_by_sentence_returns_list():
    result = analyze_pov_by_sentence("I feel alone. You did this to me.")
    assert isinstance(result, list)

def test_by_sentence_correct_count():
    result = analyze_pov_by_sentence("I feel alone. You did this to me.")
    assert len(result) == 2

def test_by_sentence_has_required_keys():
    result = analyze_pov_by_sentence("I feel alone.")
    assert 'sentence' in result[0]
    assert 'pov_signals' in result[0]
    assert 'dominant_pov' in result[0]

def test_by_sentence_empty_text():
    result = analyze_pov_by_sentence("")
    assert result == []

def test_by_sentence_first_person():
    result = analyze_pov_by_sentence("I feel so alone and lost.")
    assert result[0]['dominant_pov'] == 'first'

def test_by_sentence_second_person():
    result = analyze_pov_by_sentence("You always do this. You never listen. You lied.")
    assert result[0]['dominant_pov'] == 'second'

def test_by_sentence_preserves_sentence():
    text = "I feel alone."
    result = analyze_pov_by_sentence(text)
    assert result[0]['sentence'] == text


# ── Tests for detect_pov_shifts ───────────────────────────────────────────────

def test_detect_shifts_returns_list():
    sentence_results = [
        {'sentence': 'I feel alone.', 'dominant_pov': 'first', 'pov_signals': {}},
        {'sentence': 'You did this.', 'dominant_pov': 'second', 'pov_signals': {}}
    ]
    result = detect_pov_shifts(sentence_results)
    assert isinstance(result, list)

def test_detect_shifts_found():
    sentence_results = [
        {'sentence': 'I feel alone.', 'dominant_pov': 'first', 'pov_signals': {}},
        {'sentence': 'You did this.', 'dominant_pov': 'second', 'pov_signals': {}}
    ]
    result = detect_pov_shifts(sentence_results)
    assert len(result) == 1
    assert result[0]['from_pov'] == 'first'
    assert result[0]['to_pov'] == 'second'

def test_detect_no_shifts_same_pov():
    sentence_results = [
        {'sentence': 'I feel alone.', 'dominant_pov': 'first', 'pov_signals': {}},
        {'sentence': 'I am lost.', 'dominant_pov': 'first', 'pov_signals': {}}
    ]
    result = detect_pov_shifts(sentence_results)
    assert result == []

def test_detect_shifts_has_required_keys():
    sentence_results = [
        {'sentence': 'I feel alone.', 'dominant_pov': 'first', 'pov_signals': {}},
        {'sentence': 'You did this.', 'dominant_pov': 'second', 'pov_signals': {}}
    ]
    result = detect_pov_shifts(sentence_results)
    for key in ['sentence', 'from_pov', 'to_pov', 'index']:
        assert key in result[0]

def test_detect_shifts_empty_list():
    result = detect_pov_shifts([])
    assert result == []


# ── Tests for analyze_pov ─────────────────────────────────────────────────────

def test_analyze_pov_returns_dict():
    result = analyze_pov("I feel alone.")
    assert isinstance(result, dict)

def test_analyze_pov_has_required_keys():
    result = analyze_pov("I feel alone.")
    for key in ['sentence_count', 'pov_signals', 'dominant_pov',
                'pov_shifts', 'shift_count', 'shift_detected', 'sentence_povs']:
        assert key in result

def test_analyze_pov_empty_text():
    result = analyze_pov("")
    assert result['sentence_count'] == 0
    assert result['dominant_pov'] == 'unknown'
    assert result['shift_detected'] == False

def test_analyze_pov_first_person():
    result = analyze_pov("I feel alone. I am so lost. I need help.")
    assert result['dominant_pov'] == 'first'

def test_analyze_pov_second_person():
    result = analyze_pov("You always do this. You never listen. You lied.")
    assert result['dominant_pov'] == 'second'

def test_analyze_pov_shift_detected():
    result = analyze_pov("I feel alone. I am lost. You did this. You always lie.")
    assert result['shift_detected'] == True
    assert result['shift_count'] >= 1

def test_analyze_pov_no_shift():
    result = analyze_pov("I feel alone. I am lost. I need someone.")
    assert result['shift_detected'] == False

def test_analyze_pov_sentence_count():
    result = analyze_pov("I feel alone. You did this. She left.")
    assert result['sentence_count'] == 3

def test_analyze_pov_shift_count():
    result = analyze_pov("I feel alone. I am lost. You did this. You always lie.")
    assert result['shift_count'] >= 1
    assert result['shift_count'] == len(result['pov_shifts'])