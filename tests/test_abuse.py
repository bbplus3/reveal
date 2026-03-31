"""
tests/test_abuse.py

Unit tests for the reveal.abuse module.
Run with: pytest tests/
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reveal.abuse.detector import (
    preprocess,
    match_patterns,
    detect_categories,
    calculate_severity,
    analyze_sentences,
    analyze_abuse
)
from reveal.abuse.classifier import (
    detect_abuse_profiles,
    detect_escalation,
    build_abuse_reasoning,
    classify_abuse
)
from reveal.abuse.reporter import analyze, format_abuse_report
from reveal.abuse.patterns import ALL_PATTERNS, CATEGORY_WEIGHTS, MAX_ABUSE_SCORE


# ── Tests for preprocess ──────────────────────────────────────────────────────

def test_preprocess_lowercase():
    assert preprocess("YOU ARE CRAZY") == "you are crazy"

def test_preprocess_whitespace():
    assert preprocess("you   are   crazy") == "you are crazy"

def test_preprocess_empty():
    assert preprocess("") == ""

def test_preprocess_none():
    assert preprocess(None) == ""


# ── Tests for match_patterns ──────────────────────────────────────────────────

def test_match_patterns_finds_phrase():
    result = match_patterns("that never happened", ["that never happened"])
    assert "that never happened" in result

def test_match_patterns_case_insensitive():
    result = match_patterns("THAT NEVER HAPPENED", ["that never happened"])
    assert "that never happened" in result

def test_match_patterns_empty_text():
    result = match_patterns("", ["that never happened"])
    assert result == []

def test_match_patterns_no_match():
    result = match_patterns("the weather is nice", ["that never happened"])
    assert result == []

def test_match_patterns_multiple_matches():
    result = match_patterns(
        "you are crazy and you are imagining things",
        ["you are crazy", "you are imagining things"]
    )
    assert len(result) == 2


# ── Tests for detect_categories ──────────────────────────────────────────────

def test_detect_gaslighting():
    result = detect_categories("You are imagining things. That never happened.")
    assert 'gaslighting' in result

def test_detect_coercive_control():
    result = detect_categories("If you loved me you would do this.")
    assert 'coercive_control' in result

def test_detect_emotional_abuse():
    result = detect_categories("You are worthless and pathetic.")
    assert 'emotional_abuse' in result

def test_detect_narcissistic_abuse():
    result = detect_categories("After everything I have done for you, you are ungrateful.")
    assert 'narcissistic_abuse' in result

def test_detect_financial_control():
    result = detect_categories("I control the money and you need to ask before spending.")
    assert 'financial_control' in result

def test_detect_isolation():
    result = detect_categories("Your friends are bad for you and you don't need anyone else.")
    assert 'isolation' in result

def test_detect_threat():
    result = detect_categories("You will regret this. I am warning you.")
    assert 'threat' in result

def test_detect_empty_text():
    result = detect_categories("")
    assert result == {}

def test_detect_clean_text():
    result = detect_categories("The weather is nice today.")
    assert result == {}

def test_detect_returns_dict():
    result = detect_categories("You are crazy.")
    assert isinstance(result, dict)


# ── Tests for calculate_severity ─────────────────────────────────────────────

def test_severity_none_empty():
    severity, score = calculate_severity({})
    assert severity == 'NONE'
    assert score == 0.0

def test_severity_low_single():
    severity, score = calculate_severity({'financial_control': ['test']})
    assert severity in ('LOW', 'MEDIUM')
    assert score > 0.0

def test_severity_critical_multiple():
    categories = {
        'threat':           ['test'],
        'coercive_control': ['test'],
        'isolation':        ['test'],
        'emotional_abuse':  ['test'],
        'gaslighting':      ['test']
    }
    severity, score = calculate_severity(categories)
    assert severity in ('HIGH', 'CRITICAL')

def test_severity_returns_tuple():
    result = calculate_severity({'threat': ['test']})
    assert isinstance(result, tuple)
    assert len(result) == 2

def test_severity_score_in_range():
    _, score = calculate_severity({'threat': ['test']})
    assert 0.0 <= score <= 1.0


# ── Tests for analyze_sentences ───────────────────────────────────────────────

def test_analyze_sentences_returns_list():
    result = analyze_sentences("You are imagining things.")
    assert isinstance(result, list)

def test_analyze_sentences_correct_count():
    result = analyze_sentences("You are crazy. The weather is nice.")
    assert len(result) == 2

def test_analyze_sentences_has_required_keys():
    result = analyze_sentences("You are imagining things.")
    assert 'sentence' in result[0]
    assert 'categories' in result[0]
    assert 'severity' in result[0]
    assert 'abuse_present' in result[0]

def test_analyze_sentences_empty():
    result = analyze_sentences("")
    assert result == []

def test_analyze_sentences_flags_abuse():
    result = analyze_sentences("You are worthless and pathetic.")
    assert result[0]['abuse_present'] == True

def test_analyze_sentences_clean_text():
    result = analyze_sentences("The cat sat on the mat.")
    assert result[0]['abuse_present'] == False


# ── Tests for analyze_abuse ───────────────────────────────────────────────────

def test_analyze_abuse_returns_dict():
    result = analyze_abuse("You are imagining things.")
    assert isinstance(result, dict)

def test_analyze_abuse_has_required_keys():
    result = analyze_abuse("You are imagining things.")
    for key in ['abuse_detected', 'categories', 'active_categories',
                'severity', 'score', 'sentence_analysis',
                'most_severe_sentence']:
        assert key in result

def test_analyze_abuse_empty_text():
    result = analyze_abuse("")
    assert result['abuse_detected'] == False
    assert result['severity'] == 'NONE'

def test_analyze_abuse_detects_gaslighting():
    result = analyze_abuse("You are imagining things. That never happened.")
    assert result['abuse_detected'] == True
    assert 'gaslighting' in result['active_categories']

def test_analyze_abuse_detects_threat():
    result = analyze_abuse("You will regret this. I am warning you.")
    assert result['abuse_detected'] == True
    assert 'threat' in result['active_categories']

def test_analyze_abuse_clean_text():
    result = analyze_abuse("The weather is lovely today.")
    assert result['abuse_detected'] == False

def test_analyze_abuse_most_severe_sentence():
    result = analyze_abuse("You are worthless. The weather is nice.")
    assert result['most_severe_sentence'] is not None

def test_analyze_abuse_score_positive():
    result = analyze_abuse("You are imagining things.")
    assert result['score'] >= 0.0


# ── Tests for detect_abuse_profiles ──────────────────────────────────────────

def test_detect_profiles_returns_list():
    result = detect_abuse_profiles(['coercive_control', 'isolation'])
    assert isinstance(result, list)

def test_detect_profiles_coercive_control():
    result = detect_abuse_profiles(['coercive_control'])
    profiles = [p['profile'] for p in result]
    assert 'coercive_control_profile' in profiles

def test_detect_profiles_danger_escalation():
    result = detect_abuse_profiles(['threat', 'emotional_abuse'])
    profiles = [p['profile'] for p in result]
    assert 'danger_escalation' in profiles

def test_detect_profiles_amplified():
    result = detect_abuse_profiles(['coercive_control', 'isolation', 'gaslighting'])
    amplified = [p for p in result if p['amplified']]
    assert len(amplified) >= 1

def test_detect_profiles_empty():
    result = detect_abuse_profiles([])
    assert result == []

def test_detect_profiles_has_required_keys():
    result = detect_abuse_profiles(['threat'])
    if result:
        assert 'profile' in result[0]
        assert 'description' in result[0]
        assert 'amplified' in result[0]


# ── Tests for detect_escalation ───────────────────────────────────────────────

def test_detect_escalation_returns_dict():
    analysis = analyze_abuse("You will regret this.")
    result = detect_escalation(analysis)
    assert isinstance(result, dict)

def test_detect_escalation_has_required_keys():
    analysis = analyze_abuse("You will regret this.")
    result = detect_escalation(analysis)
    for key in ['escalation_detected', 'escalation_level', 'escalation_signals']:
        assert key in result

def test_detect_escalation_threat_plus_other():
    analysis = {'active_categories': ['threat', 'emotional_abuse']}
    result = detect_escalation(analysis)
    assert result['escalation_detected'] == True

def test_detect_escalation_three_categories():
    analysis = {'active_categories': ['threat', 'isolation', 'gaslighting']}
    result = detect_escalation(analysis)
    assert result['escalation_detected'] == True
    assert result['escalation_level'] == 'HIGH'

def test_detect_escalation_clean():
    analysis = {'active_categories': []}
    result = detect_escalation(analysis)
    assert result['escalation_detected'] == False
    assert result['escalation_level'] == 'NONE'


# ── Tests for classify_abuse ──────────────────────────────────────────────────

def test_classify_abuse_returns_dict():
    result = classify_abuse("You are imagining things.")
    assert isinstance(result, dict)

def test_classify_abuse_has_required_keys():
    result = classify_abuse("You are imagining things.")
    for key in ['abuse_detected', 'categories', 'active_categories',
                'severity', 'score', 'profiles', 'escalation',
                'reasoning', 'sentence_analysis', 'most_severe_sentence']:
        assert key in result

def test_classify_abuse_empty_text():
    result = classify_abuse("")
    assert result['abuse_detected'] == False

def test_classify_abuse_reasoning_is_list():
    result = classify_abuse("You are imagining things.")
    assert isinstance(result['reasoning'], list)

def test_classify_abuse_profiles_is_list():
    result = classify_abuse("You are imagining things.")
    assert isinstance(result['profiles'], list)

def test_classify_abuse_compound():
    text = ("You are imagining things. You are worthless. "
            "You will regret this. You don't need your friends.")
    result = classify_abuse(text)
    assert result['abuse_detected'] == True
    assert len(result['active_categories']) >= 3


# ── Tests for reporter ────────────────────────────────────────────────────────

def test_analyze_returns_dict():
    result = analyze("You are imagining things.")
    assert isinstance(result, dict)

def test_analyze_text_format():
    result = analyze("You are imagining things.", fmt='text')
    assert isinstance(result, str)

def test_analyze_text_contains_header():
    result = analyze("You are imagining things.", fmt='text')
    assert 'R E V E A L' in result

def test_analyze_text_contains_summary():
    result = analyze("You are imagining things.", fmt='text')
    assert 'SUMMARY' in result

def test_analyze_text_contains_reasoning():
    result = analyze("You are imagining things.", fmt='text')
    assert 'REASONING' in result

def test_format_abuse_report_returns_string():
    result = classify_abuse("You are imagining things.")
    report = format_abuse_report(result)
    assert isinstance(report, str)

def test_analyze_default_is_dict():
    result = analyze("Some text here.")
    assert isinstance(result, dict)