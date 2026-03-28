"""
reveal/cryptanalysis/ngrams.py

N-gram frequency analysis module for the Reveal library.
Identifies unusual word sequences that deviate from normal
English patterns -- a signal for coded communication,
steganographic content, or anomalous speech patterns.

Bigrams  = pairs of consecutive words   ("the cat")
Trigrams = triplets of consecutive words ("the cat sat")

Unusual n-grams are those that appear rarely or never in
normal English text, or appear with suspicious frequency
within a single document.
"""

import re
from collections import Counter
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt_tab', quiet=True)


# ── Common English bigrams ────────────────────────────────────────────────────

# Most frequent bigrams in normal English prose
# Used as baseline to identify unusual sequences
COMMON_BIGRAMS = {
    'of the', 'in the', 'to the', 'and the', 'on the',
    'at the', 'for the', 'is a', 'with the', 'it is',
    'in a', 'to be', 'was a', 'he was', 'she was',
    'there was', 'have been', 'has been', 'will be',
    'one of', 'out of', 'as a', 'by the', 'from the',
    'that the', 'this is', 'it was', 'do not', 'i am',
    'you are', 'we are', 'they are', 'i was', 'he is',
    'she is', 'it has', 'i have', 'we have', 'you have'
}


# ── Text preprocessing ────────────────────────────────────────────────────────

def preprocess_for_ngrams(text):
    """
    Cleans and tokenizes text for n-gram analysis.
    Lowercases, removes punctuation, and tokenizes.

    Parameters:
        text (str): The text to preprocess.

    Returns:
        list: List of cleaned word tokens.
    """
    if not text or not text.strip():
        return []

    text_lower = text.lower()
    text_clean = re.sub(r'[^\w\s]', '', text_lower)
    tokens = word_tokenize(text_clean)
    tokens = [t for t in tokens if t.strip()]
    return tokens


# ── N-gram generation ─────────────────────────────────────────────────────────

def get_bigrams(text):
    """
    Extracts all bigrams (word pairs) from a text.

    Parameters:
        text (str): The text to analyze.

    Returns:
        list of tuples: All bigrams found in the text.
    """
    tokens = preprocess_for_ngrams(text)
    if len(tokens) < 2:
        return []
    return list(ngrams(tokens, 2))


def get_trigrams(text):
    """
    Extracts all trigrams (word triplets) from a text.

    Parameters:
        text (str): The text to analyze.

    Returns:
        list of tuples: All trigrams found in the text.
    """
    tokens = preprocess_for_ngrams(text)
    if len(tokens) < 3:
        return []
    return list(ngrams(tokens, 3))


# ── Frequency analysis ────────────────────────────────────────────────────────

def get_bigram_frequencies(text):
    """
    Counts frequency of each bigram in a text.

    Parameters:
        text (str): The text to analyze.

    Returns:
        dict: Bigram strings mapped to their frequency counts,
              sorted by frequency descending.
    """
    bigram_list = get_bigrams(text)
    if not bigram_list:
        return {}

    freq = Counter(bigram_list)
    sorted_freq = dict(
        sorted(freq.items(), key=lambda x: x[1], reverse=True)
    )
    return {' '.join(k): v for k, v in sorted_freq.items()}


def get_trigram_frequencies(text):
    """
    Counts frequency of each trigram in a text.

    Parameters:
        text (str): The text to analyze.

    Returns:
        dict: Trigram strings mapped to their frequency counts,
              sorted by frequency descending.
    """
    trigram_list = get_trigrams(text)
    if not trigram_list:
        return {}

    freq = Counter(trigram_list)
    sorted_freq = dict(
        sorted(freq.items(), key=lambda x: x[1], reverse=True)
    )
    return {' '.join(k): v for k, v in sorted_freq.items()}


# ── Unusual sequence detection ────────────────────────────────────────────────

def detect_unusual_bigrams(text):
    """
    Identifies bigrams that do not appear in common English patterns.
    These may indicate coded language, unusual jargon, or anomalous content.

    Parameters:
        text (str): The text to analyze.

    Returns:
        list of str: Bigrams not found in common English baseline.
    """
    bigram_list = get_bigrams(text)
    if not bigram_list:
        return []

    unusual = []
    for bigram in bigram_list:
        bigram_str = ' '.join(bigram)
        if bigram_str not in COMMON_BIGRAMS:
            if bigram_str not in unusual:
                unusual.append(bigram_str)

    return unusual


def detect_repeated_ngrams(text, min_count=2):
    """
    Finds n-grams that repeat more than expected in a text.
    Repeated unusual sequences may indicate templated or
    coded communication patterns.

    Parameters:
        text (str):     The text to analyze.
        min_count (int): Minimum repetitions to flag. Default 2.

    Returns:
        dict: Repeated bigrams and trigrams with their counts.
    """
    bigram_freq = get_bigram_frequencies(text)
    trigram_freq = get_trigram_frequencies(text)

    repeated = {}

    for ngram, count in bigram_freq.items():
        if count >= min_count:
            repeated[ngram] = count

    for ngram, count in trigram_freq.items():
        if count >= min_count:
            repeated[ngram] = count

    return dict(sorted(repeated.items(), key=lambda x: x[1], reverse=True))


# ── Full analysis ─────────────────────────────────────────────────────────────

def analyze_ngrams(text):
    """
    Performs full n-gram analysis on a text.

    Parameters:
        text (str): The text to analyze.

    Returns:
        dict: A comprehensive n-gram report containing:
            - bigram_count:      total unique bigrams found
            - trigram_count:     total unique trigrams found
            - bigram_freq:       top 10 most frequent bigrams
            - trigram_freq:      top 10 most frequent trigrams
            - unusual_bigrams:   bigrams not in common English
            - repeated_ngrams:   sequences that repeat unusually
            - unusual_ratio:     proportion of unusual to total bigrams
            - anomaly_detected:  True if unusual patterns found
    """
    if not text or not text.strip():
        return {
            'bigram_count':     0,
            'trigram_count':    0,
            'bigram_freq':      {},
            'trigram_freq':     {},
            'unusual_bigrams':  [],
            'repeated_ngrams':  {},
            'unusual_ratio':    0.0,
            'anomaly_detected': False
        }

    bigram_freq  = get_bigram_frequencies(text)
    trigram_freq = get_trigram_frequencies(text)
    unusual      = detect_unusual_bigrams(text)
    repeated     = detect_repeated_ngrams(text)

    bigram_count  = len(bigram_freq)
    trigram_count = len(trigram_freq)

    unusual_ratio = round(
        len(unusual) / bigram_count if bigram_count > 0 else 0.0, 4
    )

    # Anomaly detected if more than 80% of bigrams are unusual
    # or if any ngrams repeat more than twice
    anomaly = (
        unusual_ratio > 0.8 or
        any(v > 2 for v in repeated.values())
    )

    # Return top 10 most frequent for readability
    top_bigrams  = dict(list(bigram_freq.items())[:10])
    top_trigrams = dict(list(trigram_freq.items())[:10])

    return {
        'bigram_count':     bigram_count,
        'trigram_count':    trigram_count,
        'bigram_freq':      top_bigrams,
        'trigram_freq':     top_trigrams,
        'unusual_bigrams':  unusual,
        'repeated_ngrams':  repeated,
        'unusual_ratio':    unusual_ratio,
        'anomaly_detected': anomaly
    }