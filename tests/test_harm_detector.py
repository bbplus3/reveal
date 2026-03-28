"""
tests/test_harm_detector.py

Unit tests for reveal.harm.detector module.
Run with: pytest tests/
"""

import sys
import os
import pytest

# Make sure reveal package is findable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reveal.harm.detector import analyze, find_matches, load_dictionary


# ── Tests for load_dictionary ─────────────────────────────────────────────────

def test_load_prop_words():
    data = load_dictionary('prop_words.json')
    assert 'words' in data
    assert isinstance(data['words'], list)
    assert len(data['words']) > 0

def test_load_prop_dict():
    data = load_dictionary('prop_dict.json')
    assert 'categories' in data
    assert isinstance(data['categories'], dict)

def test_load_harm_words():
    data = load_dictionary('harm_words.json')
    assert 'words' in data
    assert len(data['words']) > 0

def test_load_help_words():
    data = load_dictionary('help_words.json')
    assert 'words' in data
    assert len(data['words']) > 0

def test_load_groom_words():
    data = load_dictionary('groom_words.json')
    assert 'words' in data
    assert len(data['words']) > 0

def test_load_geo_words():
    data = load_dictionary('geo_words.json')
    assert 'words' in data
    assert len(data['words']) > 0


# ── Tests for find_matches ────────────────────────────────────────────────────

def test_find_matches_single_word():
    matches = find_matches("I need help please", ["help", "alone"])
    assert "help" in matches
    assert "alone" not in matches

def test_find_matches_multiword_phrase():
    matches = find_matches("I can't take it anymore", ["can't take it anymore", "hopeless"])
    assert "can't take it anymore" in matches

def test_find_matches_case_insensitive():
    matches = find_matches("HELP me please", ["help"])
    assert "help" in matches

def test_find_matches_no_partial_words():
    # "cat" should not match "category"
    matches = find_matches("This is a category of things", ["cat"])
    assert "cat" not in matches

def test_find_matches_empty_text():
    matches = find_matches("", ["help", "alone"])
    assert matches == []

def test_find_matches_empty_list():
    matches = find_matches("I need help", [])
    assert matches == []


# ── Tests for analyze ─────────────────────────────────────────────────────────

def test_analyze_clean_text():
    result = analyze("The weather today is sunny and warm.")
    assert result['flags']['propaganda_detected']  == False
    assert result['flags']['self_harm_detected']   == False
    assert result['flags']['help_signal_detected'] == False
    assert result['flags']['grooming_detected']    == False
    assert result['flags']['geo_signal_detected']  == False

def test_analyze_propaganda_detected():
    result = analyze("Most Americans support this cause and we must act now or it will lead to disaster.")
    assert result['flags']['propaganda_detected'] == True
    assert 'plain folks' in result['results']['propaganda']['category_matches']
    assert 'slippery slope' in result['results']['propaganda']['category_matches']

def test_analyze_help_signal_detected():
    result = analyze("I feel so alone and trapped, I just need someone to help me please.")
    assert result['flags']['help_signal_detected'] == True
    assert 'alone' in result['results']['help_signal']['word_matches']
    assert 'trapped' in result['results']['help_signal']['word_matches']

def test_analyze_mixed_signals():
    result = analyze("I feel hopeless. Most Americans would agree this war has caused too much pain.")
    assert result['flags']['propaganda_detected']  == True
    assert result['flags']['help_signal_detected'] == True

def test_analyze_returns_input_text():
    text = "Some sample text."
    result = analyze(text)
    assert result['input_text'] == text

def test_analyze_result_structure():
    result = analyze("Any text here.")
    assert 'input_text' in result
    assert 'results' in result
    assert 'flags' in result
    for key in ['propaganda', 'self_harm', 'help_signal', 'grooming', 'geographic']:
        assert key in result['results']
    for key in ['propaganda_detected', 'self_harm_detected', 'help_signal_detected',
                'grooming_detected', 'geo_signal_detected']:
        assert key in result['flags']