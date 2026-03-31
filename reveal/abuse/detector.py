"""
reveal/abuse/detector.py

Core detection module for the Reveal abuse detection layer.
Matches text against pattern dictionaries for seven categories
of abusive, manipulative, and controlling language.
"""

import re
from nltk.tokenize import sent_tokenize
import nltk

nltk.download('punkt_tab', quiet=True)

from reveal.abuse.patterns import (
    ALL_PATTERNS,
    CATEGORY_WEIGHTS,
    MAX_ABUSE_SCORE
)


# ── Text preprocessor ─────────────────────────────────────────────────────────

def preprocess(text):
    """
    Lowercases and normalizes whitespace for pattern matching.

    Parameters:
        text (str): Raw input text.

    Returns:
        str: Cleaned lowercase text.
    """
    if not text:
        return ''
    return ' '.join(text.lower().split())


# ── Core pattern matcher ──────────────────────────────────────────────────────

def match_patterns(text, pattern_list):
    """
    Finds all pattern matches in a text.
    Uses substring matching for phrases and word boundary
    matching for single-word patterns.

    Parameters:
        text (str):         Preprocessed lowercase text.
        pattern_list (list): List of phrase patterns to search for.

    Returns:
        list: All matched patterns found in the text.
    """
    text_lower = preprocess(text)
    matches = []

    for pattern in pattern_list:
        pattern_lower = pattern.lower().strip()
        if ' ' in pattern_lower:
            if pattern_lower in text_lower:
                matches.append(pattern)
        else:
            if re.search(r'\b' + re.escape(pattern_lower) + r'\b', text_lower):
                matches.append(pattern)

    return matches


# ── Category detector ─────────────────────────────────────────────────────────

def detect_categories(text):
    """
    Runs detection across all seven abuse categories.

    Parameters:
        text (str): The text to analyze.

    Returns:
        dict: Category names mapped to lists of matched patterns.
              Only includes categories with at least one match.
    """
    if not text or not text.strip():
        return {}

    results = {}
    for category, patterns in ALL_PATTERNS.items():
        matches = match_patterns(text, patterns)
        if matches:
            results[category] = matches

    return results


# ── Severity calculator ───────────────────────────────────────────────────────

def calculate_severity(category_matches):
    """
    Calculates overall abuse severity based on detected categories.

    Scoring:
        Each detected category contributes its weight to the score.
        Multiple categories compound the severity.
        Score is normalized to 0.0-1.0 then classified.

    Severity levels:
        CRITICAL  >= 0.5  (multiple high-weight categories)
        HIGH      >= 0.3  (one high-weight or multiple medium)
        MEDIUM    >= 0.15 (one medium-weight category)
        LOW       >= 0.05 (one low-weight category)
        NONE      <  0.05 (no matches)

    Parameters:
        category_matches (dict): Output from detect_categories()

    Returns:
        tuple: (severity_label: str, normalized_score: float)
    """
    if not category_matches:
        return 'NONE', 0.0

    raw_score = sum(
        CATEGORY_WEIGHTS.get(cat, 0)
        for cat in category_matches.keys()
    )

    normalized = round(raw_score / MAX_ABUSE_SCORE, 4)

    if normalized >= 0.5:
        severity = 'CRITICAL'
    elif normalized >= 0.3:
        severity = 'HIGH'
    elif normalized >= 0.15:
        severity = 'MEDIUM'
    elif normalized >= 0.05:
        severity = 'LOW'
    else:
        severity = 'NONE'

    return severity, normalized


# ── Sentence level analysis ───────────────────────────────────────────────────

def analyze_sentences(text):
    """
    Analyzes each sentence individually for abuse patterns.
    Useful for identifying which specific sentences contain
    abusive language within a longer text.

    Parameters:
        text (str): The text to analyze.

    Returns:
        list of dicts: One result per sentence containing:
            - sentence:      the original sentence
            - categories:    matched abuse categories and patterns
            - severity:      severity level for this sentence
            - abuse_present: True if any patterns matched
    """
    if not text or not text.strip():
        return []

    sentences = sent_tokenize(text)
    results = []

    for sentence in sentences:
        categories = detect_categories(sentence)
        severity, score = calculate_severity(categories)
        results.append({
            'sentence':      sentence,
            'categories':    categories,
            'severity':      severity,
            'score':         score,
            'abuse_present': len(categories) > 0
        })

    return results


# ── Main analysis function ────────────────────────────────────────────────────

def analyze_abuse(text):
    """
    Performs full abuse detection analysis on a text.

    Parameters:
        text (str): The text to analyze.

    Returns:
        dict: A comprehensive abuse detection report containing:
            - abuse_detected:    True if any patterns found
            - categories:        matched patterns by category
            - active_categories: list of category names with matches
            - severity:          overall severity label
            - score:             normalized score 0.0-1.0
            - sentence_analysis: per-sentence breakdown
            - most_severe_sentence: the highest risk sentence
    """
    if not text or not text.strip():
        return {
            'abuse_detected':       False,
            'categories':           {},
            'active_categories':    [],
            'severity':             'NONE',
            'score':                0.0,
            'sentence_analysis':    [],
            'most_severe_sentence': None
        }

    categories = detect_categories(text)
    severity, score = calculate_severity(categories)
    sentence_analysis = analyze_sentences(text)

    # Find the most severe sentence
    most_severe = None
    if sentence_analysis:
        flagged = [s for s in sentence_analysis if s['abuse_present']]
        if flagged:
            most_severe = max(flagged, key=lambda x: x['score'])

    return {
        'abuse_detected':       len(categories) > 0,
        'categories':           categories,
        'active_categories':    list(categories.keys()),
        'severity':             severity,
        'score':                score,
        'sentence_analysis':    sentence_analysis,
        'most_severe_sentence': most_severe
    }