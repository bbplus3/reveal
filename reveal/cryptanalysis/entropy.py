"""
reveal/cryptanalysis/entropy.py

Shannon entropy analysis module for the Reveal library.
Detects statistical irregularities in text that may indicate
hidden messages, encoded communication, or anomalous content.

High entropy = random, unpredictable, possibly encoded
Low entropy  = repetitive, patterned, possibly templated

Normal English prose typically scores between 3.5 and 5.0 bits.
Scores outside this range warrant further investigation.
"""

import math
from collections import Counter


# ── Constants ─────────────────────────────────────────────────────────────────

# Typical entropy range for normal English prose
NORMAL_ENTROPY_MIN = 3.5
NORMAL_ENTROPY_MAX = 5.0

# Thresholds for anomaly flagging
HIGH_ENTROPY_THRESHOLD = 5.5
LOW_ENTROPY_THRESHOLD  = 2.0


# ── Core entropy functions ────────────────────────────────────────────────────

def shannon_entropy(data):
    """
    Calculates Shannon entropy of a string.
    Measures the average information content per character.

    Formula: H = -sum(p(x) * log2(p(x))) for each unique character x

    Parameters:
        data (str): The string to analyze.

    Returns:
        float: Entropy value in bits. Returns 0.0 for empty input.

    Examples:
        shannon_entropy("AAAAAAAAAA") -> ~0.0  (no randomness)
        shannon_entropy("1a2b3c4d5e") -> ~3.32 (high randomness)
    """
    if not data or len(data) == 0:
        return 0.0

    freq = Counter(data)
    total = len(data)
    entropy = -sum(
        (count / total) * math.log2(count / total)
        for count in freq.values()
    )
    return round(entropy, 4)


def word_entropy(text):
    """
    Calculates Shannon entropy at the word level rather than character level.
    High word entropy means many unique words -- possibly encoded or garbled.
    Low word entropy means highly repetitive vocabulary.

    Parameters:
        text (str): The text to analyze.

    Returns:
        float: Word-level entropy value. Returns 0.0 for empty input.
    """
    if not text or not text.strip():
        return 0.0

    words = text.lower().split()
    if len(words) == 0:
        return 0.0

    freq = Counter(words)
    total = len(words)
    entropy = -sum(
        (count / total) * math.log2(count / total)
        for count in freq.values()
    )
    return round(entropy, 4)


# ── Anomaly detection ─────────────────────────────────────────────────────────

def classify_entropy(entropy_value):
    """
    Classifies an entropy value into a human-readable category.

    Categories:
        very_low   -> highly repetitive, possibly templated
        low        -> below normal, patterned content
        normal     -> typical English prose range
        high       -> above normal, possibly encoded or complex
        very_high  -> extreme randomness, possibly encrypted or gibberish

    Parameters:
        entropy_value (float): Output from shannon_entropy()

    Returns:
        str: Entropy classification label
    """
    if entropy_value <= LOW_ENTROPY_THRESHOLD:
        return 'very_low'
    elif entropy_value < NORMAL_ENTROPY_MIN:
        return 'low'
    elif entropy_value <= NORMAL_ENTROPY_MAX:
        return 'normal'
    elif entropy_value <= HIGH_ENTROPY_THRESHOLD:
        return 'high'
    else:
        return 'very_high'


def detect_anomalous_words(text, threshold=4.5):
    """
    Identifies individual words with unusually high character entropy.
    High entropy words may be encoded strings, random tokens,
    unusual identifiers, or steganographic signals.

    Parameters:
        text (str):      The text to scan.
        threshold (float): Entropy threshold above which a word is flagged.
                           Default 4.5 catches most anomalous tokens.

    Returns:
        list of dicts: Anomalous words with their entropy scores containing:
            - word:    the flagged word
            - entropy: its character-level entropy score
    """
    if not text or not text.strip():
        return []

    words = text.split()
    anomalous = []

    for word in words:
        # Only check words of 4+ characters to avoid false positives
        if len(word) >= 4:
            e = shannon_entropy(word)
            if e >= threshold:
                anomalous.append({
                    'word':    word,
                    'entropy': e
                })

    return sorted(anomalous, key=lambda x: x['entropy'], reverse=True)


# ── Full text analysis ────────────────────────────────────────────────────────

def analyze_entropy(text):
    """
    Performs full entropy analysis on a text.

    Parameters:
        text (str): The text to analyze.

    Returns:
        dict: A comprehensive entropy report containing:
            - char_entropy:       character level entropy score
            - word_entropy:       word level entropy score
            - char_classification: classification of character entropy
            - word_classification: classification of word entropy
            - anomalous_words:    words with unusually high entropy
            - anomaly_detected:   True if any anomalies found
            - high_entropy_flag:  True if char entropy exceeds threshold
            - low_entropy_flag:   True if char entropy below threshold
    """
    if not text or not text.strip():
        return {
            'char_entropy':        0.0,
            'word_entropy':        0.0,
            'char_classification': 'very_low',
            'word_classification': 'very_low',
            'anomalous_words':     [],
            'anomaly_detected':    False,
            'high_entropy_flag':   False,
            'low_entropy_flag':    False
        }

    char_e = shannon_entropy(text)
    word_e = word_entropy(text)
    char_class = classify_entropy(char_e)
    word_class = classify_entropy(word_e)
    anomalous = detect_anomalous_words(text)

    high_flag = char_e > HIGH_ENTROPY_THRESHOLD
    low_flag  = char_e < LOW_ENTROPY_THRESHOLD
    anomaly   = len(anomalous) > 0 or high_flag or low_flag

    return {
        'char_entropy':        char_e,
        'word_entropy':        word_e,
        'char_classification': char_class,
        'word_classification': word_class,
        'anomalous_words':     anomalous,
        'anomaly_detected':    anomaly,
        'high_entropy_flag':   high_flag,
        'low_entropy_flag':    low_flag
    }