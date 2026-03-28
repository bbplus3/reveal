"""
tests/test_reporter.py

Unit tests for reveal.harm.reporter module.
Run with: pytest tests/
"""

import sys
import os
import pytest

# Make sure reveal package is findable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reveal.harm.reporter import build_report, format_report, reveal, _calculate_risk_level


# ── Tests for _calculate_risk_level ──────────────────────────────────────────

def test_risk_level_none():
    flags = {
        'propaganda_detected':  False,
        'self_harm_detected':   False,
        'help_signal_detected': False,
        'grooming_detected':    False,
        'geo_signal_detected':  False
    }
    sentiment = {'tone': 'neutral', 'concern': False}
    assert _calculate_risk_level(flags, sentiment) == 'NONE'

def test_risk_level_low():
    flags = {
        'propaganda_detected':  True,
        'self_harm_detected':   False,
        'help_signal_detected': False,
        'grooming_detected':    False,
        'geo_signal_detected':  False
    }
    sentiment = {'tone': 'neutral', 'concern': False}
    assert _calculate_risk_level(flags, sentiment) == 'LOW'

def test_risk_level_medium_help_alone():
    flags = {
        'propaganda_detected':  False,
        'self_harm_detected':   False,
        'help_signal_detected': True,
        'grooming_detected':    False,
        'geo_signal_detected':  False
    }
    sentiment = {'tone': 'negative', 'concern': False}
    assert _calculate_risk_level(flags, sentiment) == 'MEDIUM'

def test_risk_level_medium_two_flags():
    flags = {
        'propaganda_detected':  True,
        'self_harm_detected':   False,
        'help_signal_detected': False,
        'grooming_detected':    False,
        'geo_signal_detected':  True
    }
    sentiment = {'tone': 'neutral', 'concern': False}
    assert _calculate_risk_level(flags, sentiment) == 'MEDIUM'

def test_risk_level_high_help_plus_other():
    flags = {
        'propaganda_detected':  True,
        'self_harm_detected':   False,
        'help_signal_detected': True,
        'grooming_detected':    False,
        'geo_signal_detected':  False
    }
    sentiment = {'tone': 'negative', 'concern': True}
    assert _calculate_risk_level(flags, sentiment) == 'HIGH'

def test_risk_level_critical_grooming():
    flags = {
        'propaganda_detected':  False,
        'self_harm_detected':   False,
        'help_signal_detected': False,
        'grooming_detected':    True,
        'geo_signal_detected':  False
    }
    sentiment = {'tone': 'neutral', 'concern': False}
    assert _calculate_risk_level(flags, sentiment) == 'CRITICAL'

def test_risk_level_critical_self_harm():
    flags = {
        'propaganda_detected':  False,
        'self_harm_detected':   True,
        'help_signal_detected': False,
        'grooming_detected':    False,
        'geo_signal_detected':  False
    }
    sentiment = {'tone': 'neutral', 'concern': False}
    assert _calculate_risk_level(flags, sentiment) == 'CRITICAL'

def test_risk_level_critical_distressed_with_flag():
    flags = {
        'propaganda_detected':  True,
        'self_harm_detected':   False,
        'help_signal_detected': False,
        'grooming_detected':    False,
        'geo_signal_detected':  False
    }
    sentiment = {'tone': 'distressed', 'concern': True}
    assert _calculate_risk_level(flags, sentiment) == 'CRITICAL'


# ── Tests for build_report ────────────────────────────────────────────────────

def test_build_report_returns_dict():
    result = build_report("The weather is nice today.")
    assert isinstance(result, dict)

def test_build_report_has_required_keys():
    result = build_report("The weather is nice today.")
    for key in ['metadata', 'input_text', 'detection', 'sentiment', 'concerns', 'summary']:
        assert key in result

def test_build_report_metadata_keys():
    result = build_report("The weather is nice today.")
    for key in ['timestamp', 'text_length', 'word_count']:
        assert key in result['metadata']

def test_build_report_summary_keys():
    result = build_report("The weather is nice today.")
    for key in ['risk_level', 'active_flags', 'total_signals', 'sentiment_tone',
                'concern_raised', 'flagged_categories']:
        assert key in result['summary']

def test_build_report_clean_text():
    result = build_report("The weather is nice today.")
    assert result['summary']['risk_level'] == 'NONE'
    assert result['summary']['active_flags'] == []
    assert result['summary']['total_signals'] == 0

def test_build_report_propaganda_text():
    result = build_report("Most Americans support this cause and it will lead to disaster.")
    assert result['summary']['risk_level'] != 'NONE'
    assert result['summary']['total_signals'] > 0

def test_build_report_help_signal_text():
    result = build_report("I feel so alone and trapped, I need someone to help me.")
    assert 'help_signal_detected' in result['summary']['active_flags']
    assert result['summary']['risk_level'] in ('MEDIUM', 'HIGH', 'CRITICAL')

def test_build_report_distressed_text():
    result = build_report("I am hopeless, I want to die, nobody cares about me.")
    assert result['summary']['risk_level'] == 'CRITICAL'

def test_build_report_word_count():
    text = "This is a five word sentence here."
    result = build_report(text)
    assert result['metadata']['word_count'] == 7

def test_build_report_input_text_preserved():
    text = "Some sample text for testing."
    result = build_report(text)
    assert result['input_text'] == text

def test_build_report_concerns_is_list():
    result = build_report("The weather is nice today.")
    assert isinstance(result['concerns'], list)

def test_build_report_concern_keys():
    result = build_report("I am hopeless and in so much pain. Nobody cares.")
    if result['concerns']:
        for concern in result['concerns']:
            for key in ['sentence', 'tone', 'compound']:
                assert key in concern


# ── Tests for format_report ───────────────────────────────────────────────────

def test_format_report_returns_string():
    report = build_report("The weather is nice today.")
    result = format_report(report)
    assert isinstance(result, str)

def test_format_report_contains_reveal():
    report = build_report("The weather is nice today.")
    result = format_report(report)
    assert 'R E V E A L' in result

def test_format_report_contains_risk_level():
    report = build_report("The weather is nice today.")
    result = format_report(report)
    assert 'Risk Level' in result

def test_format_report_contains_sentiment():
    report = build_report("The weather is nice today.")
    result = format_report(report)
    assert 'SENTIMENT' in result

def test_format_report_contains_summary():
    report = build_report("The weather is nice today.")
    result = format_report(report)
    assert 'SUMMARY' in result

def test_format_report_no_signals_message():
    report = build_report("The weather is nice today.")
    result = format_report(report)
    assert 'No signals detected' in result


# ── Tests for reveal ──────────────────────────────────────────────────────────

def test_reveal_dict_format():
    result = reveal("The weather is nice today.")
    assert isinstance(result, dict)

def test_reveal_text_format():
    result = reveal("The weather is nice today.", fmt='text')
    assert isinstance(result, str)

def test_reveal_text_format_contains_report_header():
    result = reveal("The weather is nice today.", fmt='text')
    assert 'R E V E A L' in result

def test_reveal_default_format_is_dict():
    result = reveal("Some text here.")
    assert isinstance(result, dict)

def test_reveal_critical_text():
    result = reveal("I am hopeless, I want to die, nobody cares about me.")
    assert result['summary']['risk_level'] == 'CRITICAL'