"""
tests/test_scorer.py

Unit tests for reveal.reasoning.scorer and reporter modules.
Run with: pytest tests/
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reveal.reasoning.scorer import (
    calculate_score,
    classify_score,
    classify_confidence,
    extract_signals,
    build_reasoning,
    run_all_analyses,
    score,
    WEIGHTS,
    MAX_SCORE
)
from reveal.reasoning.reporter import analyze, format_full_report


# ── Tests for calculate_score ─────────────────────────────────────────────────

def test_calculate_score_no_signals():
    signals = {k: False for k in WEIGHTS}
    raw, normalized = calculate_score(signals)
    assert raw == 0
    assert normalized == 0.0

def test_calculate_score_all_signals():
    signals = {k: True for k in WEIGHTS}
    raw, normalized = calculate_score(signals)
    assert raw == MAX_SCORE
    assert normalized == 1.0

def test_calculate_score_single_signal():
    signals = {k: False for k in WEIGHTS}
    signals['grooming_detected'] = True
    raw, normalized = calculate_score(signals)
    assert raw == WEIGHTS['grooming_detected']
    assert normalized > 0.0

def test_calculate_score_returns_tuple():
    signals = {k: False for k in WEIGHTS}
    result = calculate_score(signals)
    assert isinstance(result, tuple)
    assert len(result) == 2

def test_calculate_score_normalized_in_range():
    signals = {k: False for k in WEIGHTS}
    signals['help_signal_detected'] = True
    _, normalized = calculate_score(signals)
    assert 0.0 <= normalized <= 1.0


# ── Tests for classify_score ──────────────────────────────────────────────────

def test_classify_score_none():
    assert classify_score(0.0) == 'NONE'

def test_classify_score_low():
    assert classify_score(0.1) == 'LOW'

def test_classify_score_medium():
    assert classify_score(0.3) == 'MEDIUM'

def test_classify_score_high():
    assert classify_score(0.5) == 'HIGH'

def test_classify_score_critical():
    assert classify_score(0.7) == 'CRITICAL'

def test_classify_score_returns_string():
    assert isinstance(classify_score(0.5), str)

def test_classify_score_boundary_low():
    assert classify_score(0.05) == 'LOW'

def test_classify_score_boundary_medium():
    assert classify_score(0.2) == 'MEDIUM'

def test_classify_score_boundary_high():
    assert classify_score(0.4) == 'HIGH'

def test_classify_score_boundary_critical():
    assert classify_score(0.6) == 'CRITICAL'


# ── Tests for classify_confidence ─────────────────────────────────────────────

def test_confidence_short_text():
    assert classify_confidence(5, 10) == 'low'

def test_confidence_many_signals():
    assert classify_confidence(6, 100) == 'high'

def test_confidence_long_text():
    assert classify_confidence(0, 300) == 'high'

def test_confidence_medium():
    assert classify_confidence(3, 80) == 'medium'

def test_confidence_returns_string():
    assert isinstance(classify_confidence(2, 50), str)

def test_confidence_no_signals_short():
    assert classify_confidence(0, 15) == 'low'


# ── Tests for run_all_analyses ────────────────────────────────────────────────

def test_run_all_analyses_returns_dict():
    result = run_all_analyses("The cat sat on the mat.")
    assert isinstance(result, dict)

def test_run_all_analyses_has_required_keys():
    result = run_all_analyses("The cat sat on the mat.")
    for key in ['harm', 'sentiment', 'concerns', 'voice',
                'tone', 'pov', 'entropy', 'ngrams', 'anomaly']:
        assert key in result

def test_run_all_analyses_empty_text():
    result = run_all_analyses("")
    assert isinstance(result, dict)


# ── Tests for extract_signals ─────────────────────────────────────────────────

def test_extract_signals_returns_dict():
    analyses = run_all_analyses("The cat sat on the mat.")
    result = extract_signals(analyses)
    assert isinstance(result, dict)

def test_extract_signals_has_required_keys():
    analyses = run_all_analyses("The cat sat on the mat.")
    result = extract_signals(analyses)
    for key in WEIGHTS.keys():
        assert key in result

def test_extract_signals_values_are_bool():
    analyses = run_all_analyses("The cat sat on the mat.")
    result = extract_signals(analyses)
    for v in result.values():
        assert isinstance(v, bool)

def test_extract_signals_clean_text():
    analyses = run_all_analyses("The dog ran across the field.")
    result = extract_signals(analyses)
    assert result['grooming_detected'] == False
    assert result['self_harm_detected'] == False

def test_extract_signals_help_detected():
    analyses = run_all_analyses("I feel so alone and trapped please help me.")
    result = extract_signals(analyses)
    assert result['help_signal_detected'] == True

def test_extract_signals_distressed():
    analyses = run_all_analyses("I am hopeless I want to die nobody cares.")
    result = extract_signals(analyses)
    assert result['distressed_sentiment'] == True


# ── Tests for build_reasoning ─────────────────────────────────────────────────

def test_build_reasoning_returns_list():
    analyses = run_all_analyses("The cat sat on the mat.")
    signals = extract_signals(analyses)
    result = build_reasoning(signals, analyses)
    assert isinstance(result, list)

def test_build_reasoning_no_signals():
    from reveal.reasoning.scorer import WEIGHTS
    analyses = run_all_analyses("The weather is nice today.")
    signals = {k: False for k in WEIGHTS}
    result = build_reasoning(signals, analyses)
    assert any('No significant' in r for r in result)

def test_build_reasoning_help_signal():
    analyses = run_all_analyses("I feel so alone and trapped please help me.")
    signals = extract_signals(analyses)
    result = build_reasoning(signals, analyses)
    assert any('HELP' in r for r in result)

def test_build_reasoning_distressed():
    analyses = run_all_analyses("I am hopeless I want to die nobody cares.")
    signals = extract_signals(analyses)
    result = build_reasoning(signals, analyses)
    assert any('DISTRESSED' in r or 'SELF HARM' in r for r in result)


# ── Tests for score ───────────────────────────────────────────────────────────

def test_score_returns_dict():
    result = score("The cat sat on the mat.")
    assert isinstance(result, dict)

def test_score_has_required_keys():
    result = score("The cat sat on the mat.")
    for key in ['input_text', 'signals', 'raw_score', 'normalized_score',
                'risk_level', 'confidence', 'reasoning', 'analyses']:
        assert key in result

def test_score_empty_text():
    result = score("")
    assert result['risk_level'] == 'NONE'
    assert result['raw_score'] == 0

def test_score_clean_text():
    result = score("The cat sat on the mat.")
    assert result['risk_level'] in ('NONE', 'LOW')

def test_score_distressed_text():
    result = score("I feel so alone and hopeless. I need someone to help me please. I am so trapped and in pain.")
    assert result['risk_level'] in ('MEDIUM', 'HIGH', 'CRITICAL')

def test_score_normalized_in_range():
    result = score("Some sample text here.")
    assert 0.0 <= result['normalized_score'] <= 1.0

def test_score_preserves_input():
    text = "Some sample text here."
    result = score(text)
    assert result['input_text'] == text

def test_score_reasoning_is_list():
    result = score("Some sample text here.")
    assert isinstance(result['reasoning'], list)

def test_score_signals_is_dict():
    result = score("Some sample text here.")
    assert isinstance(result['signals'], dict)


# ── Tests for analyze (reporter) ──────────────────────────────────────────────

def test_analyze_dict_format():
    result = analyze("The cat sat on the mat.")
    assert isinstance(result, dict)

def test_analyze_text_format():
    result = analyze("The cat sat on the mat.", fmt='text')
    assert isinstance(result, str)

def test_analyze_text_contains_header():
    result = analyze("The cat sat on the mat.", fmt='text')
    assert 'R E V E A L' in result

def test_analyze_text_contains_risk():
    result = analyze("The cat sat on the mat.", fmt='text')
    assert 'RISK' in result

def test_analyze_text_contains_reasoning():
    result = analyze("The cat sat on the mat.", fmt='text')
    assert 'REASONING' in result

def test_analyze_text_contains_linguistic():
    result = analyze("The cat sat on the mat.", fmt='text')
    assert 'LINGUISTIC' in result

def test_analyze_text_contains_cryptanalysis():
    result = analyze("The cat sat on the mat.", fmt='text')
    assert 'CRYPTANALYSIS' in result

def test_analyze_default_is_dict():
    result = analyze("Some text here.")
    assert isinstance(result, dict)

def test_analyze_critical_text():
    result = analyze("I feel so alone and hopeless. I need someone to help me please. I am so trapped and in pain.")
    assert result['risk_level'] in ('MEDIUM', 'HIGH', 'CRITICAL')

def test_analyze_empty_text():
    result = analyze("")
    assert result['risk_level'] == 'NONE'