"""
reveal/linguistic/tone.py

Tone and intent classification module for the Reveal library.
Classifies the purpose and intent of text across multiple
tone categories relevant to harm detection.

Tone categories:
    persuasive    - attempting to influence beliefs or actions
    informative   - presenting facts or information neutrally
    instructional - giving directions or commands
    warning       - alerting to danger or consequences
    sarcastic     - using irony or mockery
    emotional     - expressing strong personal feelings
    accusatory    - blaming or suspecting someone
    manipulative  - exploiting emotions or logic to control
"""

import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt_tab', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)


# ── Tone signal dictionaries ──────────────────────────────────────────────────

TONE_SIGNALS = {
    'persuasive': [
        'you should', 'you must', 'you need to', 'everyone knows',
        'it is clear that', 'obviously', 'certainly', 'undeniably',
        'without a doubt', 'the fact is', 'believe me', 'trust me',
        'the truth is', 'make no mistake', 'you have to admit',
        'any reasonable person', 'it goes without saying',
        'we all know', 'consider this', 'think about it',
        'join us', 'stand with us', 'vote for', 'support our'
    ],
    'informative': [
        'according to', 'research shows', 'studies indicate',
        'data suggests', 'evidence shows', 'it has been found',
        'statistics show', 'experts say', 'reports indicate',
        'findings suggest', 'the study found', 'analysis shows',
        'as reported by', 'based on', 'the report states',
        'it is estimated', 'surveys show', 'records indicate'
    ],
    'instructional': [
        'first', 'second', 'third', 'next', 'then', 'finally',
        'step 1', 'step 2', 'make sure', 'do not', "don't forget",
        'remember to', 'be sure to', 'follow these', 'instructions',
        'how to', 'in order to', 'you will need', 'start by',
        'begin with', 'proceed to', 'complete the following'
    ],
    'warning': [
        'warning', 'caution', 'danger', 'beware', 'alert',
        'do not', 'never', 'avoid', 'stay away', 'watch out',
        'be careful', 'risk', 'threat', 'hazard', 'urgent',
        'immediately', 'critical', 'emergency', 'serious consequences',
        'if you do not', 'failure to', 'will result in'
    ],
    'sarcastic': [
        'yeah right', 'sure', 'oh great', 'wonderful',
        'how convenient', 'what a surprise', 'clearly',
        'obviously not', 'as if', 'right', 'totally',
        'sure thing', 'oh really', 'how shocking',
        'what a coincidence', 'genius', 'brilliant idea',
        'great job', 'well done', 'thanks a lot'
    ],
    'emotional': [
        'i feel', 'i am so', 'i cannot believe', 'i hate',
        'i love', 'i am devastated', 'i am heartbroken',
        'i am furious', 'i am terrified', 'i am overwhelmed',
        'this breaks my heart', 'i am so angry', 'i am so sad',
        'it makes me sick', 'i am disgusted', 'i am shocked',
        'i am so happy', 'i am grateful', 'i am so proud',
        'i cannot stop crying', 'i am so frustrated'
    ],
    'accusatory': [
        'you always', 'you never', 'it is your fault',
        'you did this', 'you caused', 'because of you',
        'you ruined', 'you lied', 'you cheated', 'you betrayed',
        'i blame you', 'you are responsible', 'how could you',
        'you knew', 'you should have', 'this is on you',
        'you made me', 'look what you did', 'you started this'
    ],
    'manipulative': [
        'if you really cared', 'after everything i have done',
        'nobody else will', 'you owe me', 'i did this for you',
        'you are the only one', 'without me you would',
        'look what you made me do', 'you are so selfish',
        'i sacrificed everything', 'you never appreciate',
        'everyone agrees with me', 'no one will believe you',
        'you are imagining things', 'that never happened',
        'you are too sensitive', 'you are overreacting',
        'i am the only one who understands you',
        'you need me', 'you cannot survive without me'
    ]
}


# ── Sentence level tone detection ─────────────────────────────────────────────

def detect_tone_signals(text):
    """
    Scans text for tone signals from all tone categories.
    Returns matched signals grouped by tone category.

    Parameters:
        text (str): The text to analyze.

    Returns:
        dict: Tone categories with their matched signal phrases.
              Only includes categories with at least one match.
    """
    if not text or not text.strip():
        return {}

    text_lower = text.lower()
    matches = {}

    for tone, signals in TONE_SIGNALS.items():
        found = []
        for signal in signals:
            if signal in text_lower:
                found.append(signal)
        if found:
            matches[tone] = found

    return matches


# ── Dominant tone classifier ──────────────────────────────────────────────────

def classify_dominant_tone(tone_matches):
    """
    Determines the dominant tone from a set of tone matches.
    In case of a tie, priority is given to higher-risk tones.

    Priority order (highest to lowest):
        manipulative > accusatory > warning > persuasive >
        emotional > sarcastic > instructional > informative

    Parameters:
        tone_matches (dict): Output from detect_tone_signals()

    Returns:
        str: The dominant tone label, or 'neutral' if no matches.
    """
    if not tone_matches:
        return 'neutral'

    priority = [
        'manipulative', 'accusatory', 'warning', 'persuasive',
        'emotional', 'sarcastic', 'instructional', 'informative'
    ]

    # Score each detected tone by number of signals found
    scored = {tone: len(signals) for tone, signals in tone_matches.items()}

    # Return highest priority tone among those with the most signals
    max_score = max(scored.values())
    top_tones = [t for t, s in scored.items() if s == max_score]

    for tone in priority:
        if tone in top_tones:
            return tone

    return top_tones[0]


# ── Sentence level analysis ───────────────────────────────────────────────────

def analyze_tone_by_sentence(text):
    """
    Analyzes tone for each sentence in a text.

    Parameters:
        text (str): The text to analyze.

    Returns:
        list of dicts: One result per sentence containing:
            - sentence:       the original sentence
            - tone_matches:   detected tone signals by category
            - dominant_tone:  the primary tone of the sentence
    """
    if not text or not text.strip():
        return []

    sentences = sent_tokenize(text)
    results = []

    for sentence in sentences:
        tone_matches = detect_tone_signals(sentence)
        dominant_tone = classify_dominant_tone(tone_matches)
        results.append({
            'sentence':      sentence,
            'tone_matches':  tone_matches,
            'dominant_tone': dominant_tone
        })

    return results


# ── Document level analysis ───────────────────────────────────────────────────

def analyze_tone(text):
    """
    Analyzes the overall tone profile of a text.

    Parameters:
        text (str): The text to analyze.

    Returns:
        dict: A tone analysis report containing:
            - sentence_count:     total sentences analyzed
            - tone_matches:       all signals detected across full text
            - dominant_tone:      primary tone of the overall text
            - tone_distribution:  count of sentences per tone
            - high_risk_tones:    manipulative or accusatory tones detected
            - sentence_tones:     per sentence tone breakdown
    """
    if not text or not text.strip():
        return {
            'sentence_count':    0,
            'tone_matches':      {},
            'dominant_tone':     'neutral',
            'tone_distribution': {},
            'high_risk_tones':   [],
            'sentence_tones':    []
        }

    # Full text tone matches
    tone_matches = detect_tone_signals(text)
    dominant_tone = classify_dominant_tone(tone_matches)

    # Per sentence breakdown
    sentence_tones = analyze_tone_by_sentence(text)
    sentence_count = len(sentence_tones)

    # Count how many sentences have each dominant tone
    tone_distribution = {}
    for s in sentence_tones:
        tone = s['dominant_tone']
        tone_distribution[tone] = tone_distribution.get(tone, 0) + 1

    # Flag high risk tones
    high_risk = ['manipulative', 'accusatory']
    high_risk_tones = [t for t in high_risk if t in tone_matches]

    return {
        'sentence_count':    sentence_count,
        'tone_matches':      tone_matches,
        'dominant_tone':     dominant_tone,
        'tone_distribution': tone_distribution,
        'high_risk_tones':   high_risk_tones,
        'sentence_tones':    sentence_tones
    }