"""
reveal/linguistic/voice.py

Voice detection module for the Reveal library.
Detects whether text is written in active or passive voice,
and identifies specific passive constructions.

Active voice:  "The dog bit the man."
Passive voice: "The man was bitten by the dog."

Passive voice is significant in harm detection because it is
commonly used to obscure agency and responsibility -- a key
feature of propaganda, gaslighting, and deceptive writing.
"""

import re
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt_tab', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)


# Forms of "to be" that can signal passive constructions
BE_FORMS = {
    'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being'
}

# Common irregular past participles that appear in passive constructions
IRREGULAR_PARTICIPLES = {
    'born', 'beaten', 'begun', 'bent', 'bitten', 'blown', 'broken',
    'brought', 'built', 'burned', 'bought', 'caught', 'chosen', 'come',
    'cost', 'cut', 'dealt', 'done', 'drawn', 'driven', 'eaten', 'fallen',
    'felt', 'fought', 'found', 'frozen', 'given', 'gone', 'grown', 'heard',
    'held', 'hidden', 'hit', 'hurt', 'kept', 'known', 'laid', 'led', 'left',
    'lent', 'let', 'lost', 'made', 'meant', 'met', 'paid', 'put', 'quit',
    'read', 'ridden', 'risen', 'run', 'said', 'seen', 'sent', 'set', 'sewn',
    'shown', 'shut', 'sung', 'sunk', 'sat', 'slept', 'spoken', 'spent',
    'stood', 'stolen', 'struck', 'sworn', 'swept', 'taken', 'taught',
    'told', 'thought', 'thrown', 'understood', 'woken', 'worn', 'won',
    'written'
}


def _get_pos_tags(sentence):
    """Returns part-of-speech tags for a sentence using NLTK."""
    tokens = nltk.word_tokenize(sentence)
    return nltk.pos_tag(tokens)


def _is_passive_sentence(sentence):
    """
    Determines whether a single sentence is passive voice.

    Parameters:
        sentence (str): A single sentence to analyze.

    Returns:
        tuple: (is_passive: bool, evidence: str or None)
    """
    if not sentence or not sentence.strip():
        return False, None

    tagged = _get_pos_tags(sentence)
    words = [w.lower() for w, t in tagged]
    tags = [t for w, t in tagged]

    for i, (word, tag) in enumerate(zip(words, tags)):
        if word in BE_FORMS:
            for j in range(i + 1, min(i + 4, len(tags))):
                next_word = words[j]
                next_tag = tags[j]

                if next_tag in ('RB', 'RBR', 'RBS', 'DT', 'CC'):
                    continue

                if next_tag == 'VBN':
                    evidence = f"'{word} {words[j]}'"
                    return True, evidence

                if next_word in IRREGULAR_PARTICIPLES:
                    evidence = f"'{word} {next_word}'"
                    return True, evidence

                if next_tag in ('VBZ', 'VBP', 'VBD', 'MD', '.', ','):
                    break

    return False, None


def analyze_voice_by_sentence(text):
    """
    Analyzes voice for each sentence in a text.

    Parameters:
        text (str): The text to analyze.

    Returns:
        list of dicts: One result per sentence containing:
            - sentence:   the original sentence
            - is_passive: True if passive voice detected
            - evidence:   the be+participle construction found, or None
    """
    if not text or not text.strip():
        return []

    sentences = sent_tokenize(text)
    results = []

    for sentence in sentences:
        is_passive, evidence = _is_passive_sentence(sentence)
        results.append({
            'sentence':   sentence,
            'is_passive': is_passive,
            'evidence':   evidence
        })

    return results


def analyze_voice(text):
    """
    Analyzes the overall voice profile of a text.

    Parameters:
        text (str): The text to analyze.

    Returns:
        dict: A voice analysis report containing:
            - sentence_count:    total sentences analyzed
            - passive_count:     number of passive sentences
            - active_count:      number of active sentences
            - passive_ratio:     proportion of passive sentences (0.0-1.0)
            - dominant_voice:    'passive', 'active', or 'mixed'
            - passive_sentences: list of passive sentence details
            - agency_obscured:   True if passive ratio exceeds threshold
    """
    if not text or not text.strip():
        return {
            'sentence_count':    0,
            'passive_count':     0,
            'active_count':      0,
            'passive_ratio':     0.0,
            'dominant_voice':    'unknown',
            'passive_sentences': [],
            'agency_obscured':   False
        }

    sentence_results = analyze_voice_by_sentence(text)

    sentence_count = len(sentence_results)
    passive_sentences = [s for s in sentence_results if s['is_passive']]
    passive_count = len(passive_sentences)
    active_count = sentence_count - passive_count
    passive_ratio = round(passive_count / sentence_count, 4) if sentence_count > 0 else 0.0

    if passive_ratio >= 0.6:
        dominant_voice = 'passive'
    elif passive_ratio <= 0.3:
        dominant_voice = 'active'
    else:
        dominant_voice = 'mixed'

    agency_obscured = passive_ratio >= 0.5

    return {
        'sentence_count':    sentence_count,
        'passive_count':     passive_count,
        'active_count':      active_count,
        'passive_ratio':     passive_ratio,
        'dominant_voice':    dominant_voice,
        'passive_sentences': passive_sentences,
        'agency_obscured':   agency_obscured
    }