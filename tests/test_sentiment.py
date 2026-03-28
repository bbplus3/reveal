"""
tests/test_sentiment.py

Unit tests for reveal.harm.sentiment module.
Run with: pytest tests/
"""

import sys
import os
import pytest

# Make sure reveal package is findable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reveal.harm.sentiment import (
    analyze_sentiment,
    analyze_sentiment_by_sentence,
    get_concern_sentences,
    classify_tone
)


# ── Tests for classify_tone ───────────────────────────────────────────────────

def test_classify_tone_distressed():
    assert classify_tone(-0.8) == 'distressed'

def test_classify_tone_negative():
    assert classify_tone(-0.2) == 'negative'

def test_classify_tone_neutral():
    assert classify_tone(0.0) == 'neutral'

def test_classify_tone_positive():
    assert classify_tone(0.2) == 'positive'

def test_classify_tone_strongly_positive():
    assert classify_tone(0.8) == 'strongly positive'

def test_classify_tone_boundary_negative():
    # Exactly at the boundary should be negative not distressed
    assert classify_tone(-0.05) == 'negative'

def test_classify_tone_boundary_positive():
    # Exactly at the boundary should be positive
    assert classify_tone(0.05) == 'positive'


# ── Tests for analyze_sentiment ───────────────────────────────────────────────

def test_analyze_sentiment_returns_all_keys():
    result = analyze_sentiment("I feel great today.")
    for key in ['neg', 'neu', 'pos', 'compound', 'tone', 'concern']:
        assert key in result

def test_analyze_sentiment_positive_text():
    result = analyze_sentiment("I feel wonderful and happy today!")
    assert result['tone'] in ('positive', 'strongly positive')
    assert result['pos'] > result['neg']

def test_analyze_sentiment_negative_text():
    result = analyze_sentiment("I feel terrible and miserable.")
    assert result['neg'] > result['pos']

def test_analyze_sentiment_distressed_text():
    result = analyze_sentiment("I am hopeless, I want to die, nobody cares about me.")
    assert result['tone'] == 'distressed'
    assert result['concern'] == True

def test_analyze_sentiment_neutral_text():
    result = analyze_sentiment("The meeting is scheduled for Tuesday.")
    assert result['tone'] == 'neutral'
    assert result['concern'] == False

def test_analyze_sentiment_empty_string():
    result = analyze_sentiment("")
    assert result['tone'] == 'neutral'
    assert result['compound'] == 0.0
    assert result['concern'] == False

def test_analyze_sentiment_whitespace_only():
    result = analyze_sentiment("   ")
    assert result['tone'] == 'neutral'
    assert result['concern'] == False

def test_analyze_sentiment_scores_sum_to_one():
    result = analyze_sentiment("This is a sample sentence.")
    total = round(result['neg'] + result['neu'] + result['pos'], 1)
    assert total == 1.0

def test_analyze_sentiment_compound_in_range():
    result = analyze_sentiment("Some text here.")
    assert -1.0 <= result['compound'] <= 1.0


# ── Tests for analyze_sentiment_by_sentence ───────────────────────────────────

def test_analyze_by_sentence_returns_list():
    result = analyze_sentiment_by_sentence("I am happy. The sky is blue.")
    assert isinstance(result, list)

def test_analyze_by_sentence_correct_count():
    result = analyze_sentiment_by_sentence("I am happy. The sky is blue. I feel great.")
    assert len(result) == 3

def test_analyze_by_sentence_contains_sentence_key():
    result = analyze_sentiment_by_sentence("I feel alone.")
    assert 'sentence' in result[0]

def test_analyze_by_sentence_empty_text():
    result = analyze_sentiment_by_sentence("")
    assert result == []


# ── Tests for get_concern_sentences ──────────────────────────────────────────

def test_get_concern_sentences_returns_list():
    result = get_concern_sentences("I feel great. The weather is nice.")
    assert isinstance(result, list)

def test_get_concern_sentences_finds_distressed():
    text = "The meeting went well. I am so hopeless and I cannot take this pain anymore."
    result = get_concern_sentences(text)
    assert len(result) >= 1
    assert any('hopeless' in s['sentence'] or 'pain' in s['sentence'] for s in result)

def test_get_concern_sentences_clean_text_returns_empty():
    result = get_concern_sentences("The weather is lovely today. Everything is going well.")
    assert result == []

def test_get_concern_sentences_all_concerning():
    text = "I feel terrible. I am completely hopeless. Nobody cares about me."
    result = get_concern_sentences(text)
    assert len(result) >= 1