"""
tests/test_voice.py

Unit tests for reveal.linguistic.voice module.
Run with: pytest tests/
"""

import sys
import os
import pytest

# Make sure reveal package is findable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reveal.linguistic.voice import (
    analyze_voice,
    analyze_voice_by_sentence,
    _is_passive_sentence
)


# ── Tests for _is_passive_sentence ────────────────────────────────────────────

def test_passive_simple():
    is_passive, evidence = _is_passive_sentence("The man was bitten by the dog.")
    assert is_passive == True
    assert evidence is not None

def test_passive_was_verb():
    is_passive, evidence = _is_passive_sentence("The report was written by the team.")
    assert is_passive == True

def test_passive_is_verb():
    is_passive, evidence = _is_passive_sentence("The law is enforced by the police.")
    assert is_passive == True

def test_passive_been_verb():
    is_passive, evidence = _is_passive_sentence("The decision has been made.")
    assert is_passive == True

def test_passive_were_verb():
    is_passive, evidence = _is_passive_sentence("The documents were destroyed.")
    assert is_passive == True

def test_active_simple():
    is_passive, evidence = _is_passive_sentence("The dog bit the man.")
    assert is_passive == False
    assert evidence is None

def test_active_subject_verb_object():
    is_passive, evidence = _is_passive_sentence("She wrote the report yesterday.")
    assert is_passive == False

def test_active_present_tense():
    is_passive, evidence = _is_passive_sentence("The team builds the software every day.")
    assert is_passive == False

def test_empty_sentence():
    is_passive, evidence = _is_passive_sentence("")
    assert is_passive == False
    assert evidence is None

def test_passive_irregular_participle():
    is_passive, evidence = _is_passive_sentence("The message was hidden inside the text.")
    assert is_passive == True


# ── Tests for analyze_voice_by_sentence ───────────────────────────────────────

def test_by_sentence_returns_list():
    result = analyze_voice_by_sentence("The dog bit the man.")
    assert isinstance(result, list)

def test_by_sentence_correct_count():
    result = analyze_voice_by_sentence("The dog bit the man. The cat was chased.")
    assert len(result) == 2

def test_by_sentence_has_required_keys():
    result = analyze_voice_by_sentence("The dog bit the man.")
    assert 'sentence' in result[0]
    assert 'is_passive' in result[0]
    assert 'evidence' in result[0]

def test_by_sentence_empty_text():
    result = analyze_voice_by_sentence("")
    assert result == []

def test_by_sentence_mixed_voices():
    text = "She wrote the report. The report was reviewed by the manager."
    result = analyze_voice_by_sentence(text)
    assert result[0]['is_passive'] == False
    assert result[1]['is_passive'] == True

def test_by_sentence_preserves_original():
    sentence = "The dog bit the man."
    result = analyze_voice_by_sentence(sentence)
    assert result[0]['sentence'] == sentence


# ── Tests for analyze_voice ───────────────────────────────────────────────────

def test_analyze_voice_returns_dict():
    result = analyze_voice("The dog bit the man.")
    assert isinstance(result, dict)

def test_analyze_voice_has_required_keys():
    result = analyze_voice("The dog bit the man.")
    for key in ['sentence_count', 'passive_count', 'active_count',
                'passive_ratio', 'dominant_voice', 'passive_sentences',
                'agency_obscured']:
        assert key in result

def test_analyze_voice_empty_text():
    result = analyze_voice("")
    assert result['sentence_count'] == 0
    assert result['dominant_voice'] == 'unknown'
    assert result['agency_obscured'] == False

def test_analyze_voice_all_active():
    text = "She wrote the report. He built the system. They launched the product."
    result = analyze_voice(text)
    assert result['passive_count'] == 0
    assert result['dominant_voice'] == 'active'
    assert result['agency_obscured'] == False

def test_analyze_voice_all_passive():
    text = "The report was written. The system was built. The product was launched."
    result = analyze_voice(text)
    assert result['passive_count'] == 3
    assert result['dominant_voice'] == 'passive'
    assert result['agency_obscured'] == True

def test_analyze_voice_counts_correct():
    text = "She wrote the report. The report was reviewed by the manager."
    result = analyze_voice(text)
    assert result['sentence_count'] == 2
    assert result['active_count'] == 1
    assert result['passive_count'] == 1

def test_analyze_voice_passive_ratio():
    text = "The report was written. The system was built. She launched the product."
    result = analyze_voice(text)
    assert result['passive_ratio'] == round(2/3, 4)

def test_analyze_voice_mixed():
    text = "She wrote the report. The system was built by the team. He launched it."
    result = analyze_voice(text)
    assert result['dominant_voice'] == 'mixed'

def test_analyze_voice_agency_obscured_threshold():
    # 2 out of 2 passive = ratio 1.0, should be obscured
    text = "The report was written. The system was built."
    result = analyze_voice(text)
    assert result['agency_obscured'] == True

def test_analyze_voice_passive_sentences_list():
    text = "The report was written. She launched the product."
    result = analyze_voice(text)
    assert len(result['passive_sentences']) == 1
    assert result['passive_sentences'][0]['is_passive'] == True