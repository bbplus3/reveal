"""
reveal/harm/sentiment.py

Sentiment analysis module for the Reveal library.
Uses VADER (Valence Aware Dictionary and sEntiment Reasoner)
to assess emotional tone of text.

VADER is specifically designed for social media and informal language,
making it well suited for Reveal's public safety use case.
"""

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download vader lexicon if not already present
nltk.download('vader_lexicon', quiet=True)


# ── Analyzer setup ────────────────────────────────────────────────────────────

# Initialize once at module level so it isn't recreated on every call
_analyzer = SentimentIntensityAnalyzer()


# ── Tone classification ───────────────────────────────────────────────────────

def classify_tone(compound_score):
    """
    Converts a VADER compound score into a human-readable tone label.

    VADER compound score ranges from -1.0 (most negative) to +1.0 (most positive).
    Standard thresholds:
        >= 0.05  → positive
        <= -0.05 → negative
        between  → neutral

    We add two extra labels for Reveal's harm detection context:
        <= -0.5  → distressed   (strongly negative, high concern)
        >= 0.5   → strongly positive
    """
    if compound_score <= -0.5:
        return 'distressed'
    elif compound_score <= -0.05:
        return 'negative'
    elif compound_score >= 0.5:
        return 'strongly positive'
    elif compound_score >= 0.05:
        return 'positive'
    else:
        return 'neutral'


# ── Core sentiment function ───────────────────────────────────────────────────

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text using VADER.

    Parameters:
        text (str): The text to analyze.

    Returns:
        dict: A structured sentiment report containing:
            - neg:      negative sentiment score (0.0 to 1.0)
            - neu:      neutral sentiment score (0.0 to 1.0)
            - pos:      positive sentiment score (0.0 to 1.0)
            - compound: overall sentiment score (-1.0 to 1.0)
            - tone:     human-readable tone label
            - concern:  True if text appears distressed or strongly negative
    """
    if not text or not text.strip():
        return {
            'neg':      0.0,
            'neu':      1.0,
            'pos':      0.0,
            'compound': 0.0,
            'tone':     'neutral',
            'concern':  False
        }

    scores = _analyzer.polarity_scores(text)

    tone = classify_tone(scores['compound'])

    # Concern is flagged when tone is distressed or negative
    # AND the negative score is above 0.2 (at least 20% negative content)
    concern = tone in ('distressed', 'negative') and scores['neg'] >= 0.2

    return {
        'neg':      round(scores['neg'], 4),
        'neu':      round(scores['neu'], 4),
        'pos':      round(scores['pos'], 4),
        'compound': round(scores['compound'], 4),
        'tone':     tone,
        'concern':  concern
    }


# ── Sentence-level sentiment ──────────────────────────────────────────────────

def analyze_sentiment_by_sentence(text):
    """
    Breaks text into sentences and analyzes sentiment of each one.
    Useful for finding distressed sentences buried in otherwise neutral text.

    Parameters:
        text (str): The text to analyze.

    Returns:
        list of dicts: One sentiment report per sentence, each including
                       the original sentence text.
    """
    nltk.download('punkt_tab', quiet=True)
    sentences = nltk.sent_tokenize(text)

    results = []
    for sentence in sentences:
        sentiment = analyze_sentiment(sentence)
        sentiment['sentence'] = sentence
        results.append(sentiment)

    return results


# ── Concern summary ───────────────────────────────────────────────────────────

def get_concern_sentences(text):
    """
    Returns only the sentences from a text that triggered a concern flag.
    Useful for quickly surfacing the most worrying parts of a longer text.

    Parameters:
        text (str): The text to analyze.

    Returns:
        list of dicts: Sentiment reports for concerning sentences only.
    """
    all_sentences = analyze_sentiment_by_sentence(text)
    return [s for s in all_sentences if s['concern']]