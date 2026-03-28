"""
reveal/harm/detector.py

Core harm detection module for the Reveal library.
Loads word list dictionaries and searches text for matches.
"""

import json
import os
import re


# ── Path setup ────────────────────────────────────────────────────────────────

# This finds the dictionaries folder no matter where the user runs the code from
DICT_DIR = os.path.join(os.path.dirname(__file__), '..', 'dictionaries')


# ── Dictionary loader ─────────────────────────────────────────────────────────

def load_dictionary(filename):
    """
    Loads a JSON dictionary file from the dictionaries folder.
    Returns the parsed JSON as a Python dict.
    """
    filepath = os.path.join(DICT_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


# ── Text preprocessor ─────────────────────────────────────────────────────────

def preprocess(text):
    """
    Lowercases text and strips extra whitespace.
    Keeps punctuation intact so multi-word phrases still match.
    """
    return text.lower().strip()


# ── Core match function ───────────────────────────────────────────────────────

def find_matches(text, word_list):
    """
    Searches text for any word or phrase from a given list.
    Returns a list of matches found.
    Handles both single words and multi-word phrases.
    """
    text_lower = preprocess(text)
    matches = []

    for term in word_list:
        term_lower = term.lower().strip()
        # Use word boundary matching for single words
        # Use plain substring matching for multi-word phrases
        if ' ' in term_lower:
            if term_lower in text_lower:
                matches.append(term)
        else:
            pattern = r'\b' + re.escape(term_lower) + r'\b'
            if re.search(pattern, text_lower):
                matches.append(term)

    return matches


# ── Category match function (for prop_dict) ───────────────────────────────────

def find_category_matches(text, category_dict):
    """
    Searches text against a categorized dictionary (like prop_dict).
    Returns a dict of category names and their matched phrases.
    Only includes categories that had at least one match.
    """
    text_lower = preprocess(text)
    results = {}

    for category, phrases in category_dict.items():
        matches = find_matches(text_lower, phrases)
        if matches:
            results[category] = matches

    return results


# ── Main analysis function ────────────────────────────────────────────────────

def analyze(text):
    """
    Runs the full harm detection analysis on a given text.
    Checks against all six dictionaries and returns a structured report.

    Parameters:
        text (str): The text to analyze.

    Returns:
        dict: A structured report with matches from each dictionary.
    """

    # Load all dictionaries
    prop_words_data   = load_dictionary('prop_words.json')
    prop_dict_data    = load_dictionary('prop_dict.json')
    harm_words_data   = load_dictionary('harm_words.json')
    help_words_data   = load_dictionary('help_words.json')
    groom_words_data  = load_dictionary('groom_words.json')
    geo_words_data    = load_dictionary('geo_words.json')

    # Run matches
    prop_word_matches    = find_matches(text, prop_words_data['words'])
    prop_cat_matches     = find_category_matches(text, prop_dict_data['categories'])
    harm_matches         = find_matches(text, harm_words_data['words'])
    help_matches         = find_matches(text, help_words_data['words'])
    groom_matches        = find_matches(text, groom_words_data['words'])
    geo_matches          = find_matches(text, geo_words_data['words'])

    # Build report
    report = {
        'input_text': text,
        'results': {
            'propaganda': {
                'word_matches': prop_word_matches,
                'category_matches': prop_cat_matches,
                'match_count': len(prop_word_matches)
            },
            'self_harm': {
                'word_matches': harm_matches,
                'match_count': len(harm_matches)
            },
            'help_signal': {
                'word_matches': help_matches,
                'match_count': len(help_matches)
            },
            'grooming': {
                'word_matches': groom_matches,
                'match_count': len(groom_matches)
            },
            'geographic': {
                'word_matches': geo_matches,
                'match_count': len(geo_matches)
            }
        },
        'flags': {
            'propaganda_detected':  len(prop_word_matches) > 0,
            'self_harm_detected':   len(harm_matches) > 0,
            'help_signal_detected': len(help_matches) > 0,
            'grooming_detected':    len(groom_matches) > 0,
            'geo_signal_detected':  len(geo_matches) > 0
        }
    }

    return report