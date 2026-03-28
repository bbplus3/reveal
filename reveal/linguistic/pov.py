"""
reveal/linguistic/pov.py

Point of view detection module for the Reveal library.
Detects whether text is written in first, second, or third
person and identifies POV shifts within a text.

POV shifts are significant in harm detection because sudden
shifts between first and second person are common in
manipulative, accusatory, and grooming communication.

First person:  "I feel alone. We need help."
Second person: "You should do this. You always lie."
Third person:  "She went to the store. They decided to leave."
"""

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt_tab', quiet=True)


# ── POV word lists ────────────────────────────────────────────────────────────

FIRST_PERSON = {
    'i', 'me', 'my', 'mine', 'myself',
    'we', 'us', 'our', 'ours', 'ourselves'
}

SECOND_PERSON = {
    'you', 'your', 'yours', 'yourself', 'yourselves'
}

THIRD_PERSON = {
    'he', 'him', 'his', 'himself',
    'she', 'her', 'hers', 'herself',
    'it', 'its', 'itself',
    'they', 'them', 'their', 'theirs', 'themselves',
    'one', 'ones'
}


# ── Core POV detection ────────────────────────────────────────────────────────

def detect_pov_signals(text):
    """
    Counts first, second, and third person pronouns in a text.

    Parameters:
        text (str): The text to analyze.

    Returns:
        dict: Pronoun counts and lists by POV category containing:
            - first_person:  count and matched pronouns
            - second_person: count and matched pronouns
            - third_person:  count and matched pronouns
    """
    if not text or not text.strip():
        return {
            'first_person':  {'count': 0, 'pronouns': []},
            'second_person': {'count': 0, 'pronouns': []},
            'third_person':  {'count': 0, 'pronouns': []}
        }

    tokens = word_tokenize(text.lower())

    first  = [t for t in tokens if t in FIRST_PERSON]
    second = [t for t in tokens if t in SECOND_PERSON]
    third  = [t for t in tokens if t in THIRD_PERSON]

    return {
        'first_person':  {'count': len(first),  'pronouns': first},
        'second_person': {'count': len(second), 'pronouns': second},
        'third_person':  {'count': len(third),  'pronouns': third}
    }


def classify_pov(pov_signals):
    """
    Determines the dominant point of view from pronoun counts.

    If counts are equal, priority goes to second person first
    (highest risk in harm detection), then first, then third.

    Parameters:
        pov_signals (dict): Output from detect_pov_signals()

    Returns:
        str: 'first', 'second', 'third', 'mixed', or 'unknown'
    """
    first  = pov_signals['first_person']['count']
    second = pov_signals['second_person']['count']
    third  = pov_signals['third_person']['count']

    total = first + second + third

    if total == 0:
        return 'unknown'

    # Mixed if no single POV accounts for more than 60% of pronouns
    dominant_count = max(first, second, third)
    if dominant_count / total < 0.6:
        return 'mixed'

    if dominant_count == second:
        return 'second'
    if dominant_count == first:
        return 'first'
    return 'third'


# ── Sentence level analysis ───────────────────────────────────────────────────

def analyze_pov_by_sentence(text):
    """
    Analyzes point of view for each sentence in a text.

    Parameters:
        text (str): The text to analyze.

    Returns:
        list of dicts: One result per sentence containing:
            - sentence:     the original sentence
            - pov_signals:  pronoun counts by category
            - dominant_pov: primary POV of the sentence
    """
    if not text or not text.strip():
        return []

    sentences = sent_tokenize(text)
    results = []

    for sentence in sentences:
        pov_signals = detect_pov_signals(sentence)
        dominant_pov = classify_pov(pov_signals)
        results.append({
            'sentence':     sentence,
            'pov_signals':  pov_signals,
            'dominant_pov': dominant_pov
        })

    return results


# ── POV shift detection ───────────────────────────────────────────────────────

def detect_pov_shifts(sentence_results):
    """
    Identifies sentences where the point of view shifts from
    the previous sentence. POV shifts are a signal of manipulative
    or accusatory communication patterns.

    Parameters:
        sentence_results (list): Output from analyze_pov_by_sentence()

    Returns:
        list of dicts: Sentences where a POV shift was detected, containing:
            - sentence:    the sentence where the shift occurred
            - from_pov:    the POV of the previous sentence
            - to_pov:      the POV of this sentence
            - index:       position in the sentence list
    """
    shifts = []
    known_povs = [r for r in sentence_results if r['dominant_pov'] != 'unknown']

    for i in range(1, len(known_povs)):
        prev = known_povs[i - 1]['dominant_pov']
        curr = known_povs[i]['dominant_pov']

        if prev != curr and curr != 'mixed' and prev != 'mixed':
            shifts.append({
                'sentence': known_povs[i]['sentence'],
                'from_pov': prev,
                'to_pov':   curr,
                'index':    i
            })

    return shifts


# ── Document level analysis ───────────────────────────────────────────────────

def analyze_pov(text):
    """
    Analyzes the overall point of view profile of a text.

    Parameters:
        text (str): The text to analyze.

    Returns:
        dict: A POV analysis report containing:
            - sentence_count:  total sentences analyzed
            - pov_signals:     pronoun counts across full text
            - dominant_pov:    primary POV of the overall text
            - pov_shifts:      list of detected POV shifts
            - shift_count:     number of POV shifts detected
            - shift_detected:  True if any POV shifts found
            - sentence_povs:   per sentence POV breakdown
    """
    if not text or not text.strip():
        return {
            'sentence_count': 0,
            'pov_signals':    {
                'first_person':  {'count': 0, 'pronouns': []},
                'second_person': {'count': 0, 'pronouns': []},
                'third_person':  {'count': 0, 'pronouns': []}
            },
            'dominant_pov':   'unknown',
            'pov_shifts':     [],
            'shift_count':    0,
            'shift_detected': False,
            'sentence_povs':  []
        }

    pov_signals = detect_pov_signals(text)
    dominant_pov = classify_pov(pov_signals)
    sentence_povs = analyze_pov_by_sentence(text)
    pov_shifts = detect_pov_shifts(sentence_povs)

    return {
        'sentence_count': len(sentence_povs),
        'pov_signals':    pov_signals,
        'dominant_pov':   dominant_pov,
        'pov_shifts':     pov_shifts,
        'shift_count':    len(pov_shifts),
        'shift_detected': len(pov_shifts) > 0,
        'sentence_povs':  sentence_povs
    }