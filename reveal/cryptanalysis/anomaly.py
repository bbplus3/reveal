"""
reveal/cryptanalysis/anomaly.py

Anomaly detection module for the Reveal library.
Uses statistical methods and machine learning to identify
outlier words and suspicious patterns in text.

Detects:
    - Unusually long or short words
    - Suspicious capitalization patterns
    - Statistically anomalous tokens
    - Words that don't fit surrounding text profile
"""

import re
import numpy as np
from collections import Counter
from sklearn.ensemble import IsolationForest


# ── Word feature extraction ───────────────────────────────────────────────────

def extract_word_features(word):
    """
    Extracts numerical features from a single word for anomaly detection.

    Features extracted:
        - length:          number of characters
        - uppercase_ratio: proportion of uppercase letters
        - digit_ratio:     proportion of digit characters
        - special_ratio:   proportion of non-alphanumeric characters
        - unique_ratio:    proportion of unique characters to total

    Parameters:
        word (str): The word to extract features from.

    Returns:
        list: Five numerical features as floats.
    """
    if not word:
        return [0.0, 0.0, 0.0, 0.0, 0.0]

    length = len(word)
    uppercase = sum(1 for c in word if c.isupper())
    digits    = sum(1 for c in word if c.isdigit())
    special   = sum(1 for c in word if not c.isalnum())
    unique    = len(set(word))

    return [
        float(length),
        uppercase / length,
        digits / length,
        special / length,
        unique / length
    ]


def extract_features_from_text(text):
    """
    Extracts word features for all words in a text.

    Parameters:
        text (str): The text to process.

    Returns:
        tuple: (words list, features matrix as list of lists)
    """
    if not text or not text.strip():
        return [], []

    words = text.split()
    features = [extract_word_features(w) for w in words]
    return words, features


# ── Statistical anomaly detection ─────────────────────────────────────────────

def detect_length_outliers(text):
    """
    Identifies words with unusually long or short lengths
    compared to the average word length in the text.
    Uses standard deviation to define outlier boundaries.

    Parameters:
        text (str): The text to analyze.

    Returns:
        list of dicts: Outlier words with their lengths and deviation,
                       each containing:
                           - word:      the outlier word
                           - length:    character count
                           - deviation: how many std devs from mean
                           - direction: 'long' or 'short'
    """
    if not text or not text.strip():
        return []

    words = text.split()
    if len(words) < 3:
        return []

    lengths = [len(w) for w in words]
    mean_len = np.mean(lengths)
    std_len  = np.std(lengths)

    if std_len == 0:
        return []

    outliers = []
    for word, length in zip(words, lengths):
        deviation = abs(length - mean_len) / std_len
        if deviation > 2.0:
            outliers.append({
                'word':      word,
                'length':    length,
                'deviation': round(deviation, 4),
                'direction': 'long' if length > mean_len else 'short'
            })

    return sorted(outliers, key=lambda x: x['deviation'], reverse=True)


def detect_capitalization_anomalies(text):
    """
    Identifies words with unusual capitalization patterns.
    Flags words that are not at the start of a sentence but
    are fully uppercase, or have mixed case patterns like
    camelCase or alternating caps (often used in coded messages).

    Parameters:
        text (str): The text to analyze.

    Returns:
        list of dicts: Words with anomalous capitalization, each containing:
                           - word:    the flagged word
                           - pattern: description of the anomaly
    """
    if not text or not text.strip():
        return []

    words = text.split()
    anomalies = []

    for i, word in enumerate(words):
        clean = re.sub(r'[^a-zA-Z]', '', word)
        if len(clean) < 2:
            continue

        # All uppercase word not at start of sentence
        if clean.isupper() and i > 0:
            anomalies.append({
                'word':    word,
                'pattern': 'all_caps'
            })

        # Mixed case that is not standard Title Case
        elif (any(c.isupper() for c in clean[1:]) and
              not clean.istitle() and
              not clean.isupper()):
            anomalies.append({
                'word':    word,
                'pattern': 'mixed_case'
            })

    return anomalies


# ── Isolation Forest detection ────────────────────────────────────────────────

def detect_isolation_forest_outliers(text, contamination=0.1):
    """
    Uses scikit-learn Isolation Forest to detect statistically
    anomalous words based on their extracted features.

    Isolation Forest works by randomly partitioning features
    and flagging points that are isolated quickly as outliers.

    Parameters:
        text (str):            The text to analyze.
        contamination (float): Expected proportion of outliers (0.0-0.5).
                               Default 0.1 means expect 10% outliers.

    Returns:
        list of dicts: Outlier words detected by Isolation Forest,
                       each containing:
                           - word:     the flagged word
                           - features: the feature vector used
    """
    if not text or not text.strip():
        return []

    words, features = extract_features_from_text(text)

    if len(words) < 5:
        return []

    features_array = np.array(features)

    model = IsolationForest(
        contamination=contamination,
        random_state=42
    )
    predictions = model.fit_predict(features_array)

    outliers = []
    for word, feature, pred in zip(words, features, predictions):
        if pred == -1:
            outliers.append({
                'word':     word,
                'features': [round(f, 4) for f in feature]
            })

    return outliers


# ── Full analysis ─────────────────────────────────────────────────────────────

def analyze_anomalies(text):
    """
    Performs full anomaly analysis on a text combining
    statistical and machine learning approaches.

    Parameters:
        text (str): The text to analyze.

    Returns:
        dict: A comprehensive anomaly report containing:
            - length_outliers:       words with unusual lengths
            - capitalization_anomalies: words with odd capitalization
            - isolation_outliers:    ML detected outlier words
            - total_anomalies:       combined count of all anomalies
            - anomaly_detected:      True if any anomalies found
    """
    if not text or not text.strip():
        return {
            'length_outliers':           [],
            'capitalization_anomalies':  [],
            'isolation_outliers':        [],
            'total_anomalies':           0,
            'anomaly_detected':          False
        }

    length_outliers  = detect_length_outliers(text)
    cap_anomalies    = detect_capitalization_anomalies(text)
    iso_outliers     = detect_isolation_forest_outliers(text)

    total = len(length_outliers) + len(cap_anomalies) + len(iso_outliers)

    return {
        'length_outliers':          length_outliers,
        'capitalization_anomalies': cap_anomalies,
        'isolation_outliers':       iso_outliers,
        'total_anomalies':          total,
        'anomaly_detected':         total > 0
    }