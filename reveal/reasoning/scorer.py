"""
reveal/reasoning/scorer.py

Unified scoring module for the Reveal library.
Synthesizes output from all analysis layers into a single
comprehensive risk score and reasoning summary.

This is the conductor module -- it pulls together:
    - Harm detection signals
    - Sentiment analysis
    - Linguistic analysis (voice, tone, POV)
    - Cryptanalysis (entropy, ngrams, anomaly)

And produces a unified score, confidence level, and
human-readable reasoning chain explaining the findings.
"""

from reveal.harm.detector import analyze as harm_detect
from reveal.harm.sentiment import analyze_sentiment, get_concern_sentences
from reveal.linguistic.voice import analyze_voice
from reveal.linguistic.tone import analyze_tone
from reveal.linguistic.pov import analyze_pov
from reveal.cryptanalysis.entropy import analyze_entropy
from reveal.cryptanalysis.ngrams import analyze_ngrams
from reveal.cryptanalysis.anomaly import analyze_anomalies
from reveal.abuse.classifier import classify_abuse


# ── Risk weights ──────────────────────────────────────────────────────────────

# Each signal type contributes a weighted score to the overall risk
# Weights reflect relative severity in harm detection context
WEIGHTS = {
    'grooming_detected':       25,
    'self_harm_detected':      25,
    'help_signal_detected':    15,
    'propaganda_detected':     10,
    'geo_signal_detected':      5,
    'distressed_sentiment':    20,
    'negative_sentiment':      10,
    'manipulative_tone':       15,
    'accusatory_tone':         12,
    'warning_tone':             8,
    'agency_obscured':          8,
    'pov_shift_detected':      10,
    'entropy_anomaly':          8,
    'ngram_anomaly':            6,
    'word_anomaly':             6,
    'abuse_detected':          30,
    'abuse_threat':            25,
    'abuse_coercive_control':  22,
    'abuse_gaslighting':       18,
    'abuse_emotional':         18,
    'abuse_isolation':         20,
    'abuse_narcissistic':      15,
    'abuse_financial':         15,
    'abuse_escalation':        20,
}

# Maximum possible score (sum of all weights)
MAX_SCORE = sum(WEIGHTS.values())


# ── Score calculator ──────────────────────────────────────────────────────────

def calculate_score(signals):
    """
    Calculates a weighted risk score from a set of detected signals.

    Parameters:
        signals (dict): Boolean signal flags mapped to signal names.

    Returns:
        tuple: (raw_score: int, normalized_score: float 0.0-1.0)
    """
    raw = sum(WEIGHTS.get(k, 0) for k, v in signals.items() if v)
    normalized = round(raw / MAX_SCORE, 4)
    return raw, normalized


def classify_score(normalized_score):
    """
    Converts a normalized score into a risk classification.

    Thresholds:
        >= 0.6  -> CRITICAL
        >= 0.4  -> HIGH
        >= 0.2  -> MEDIUM
        >= 0.05 -> LOW
        <  0.05 -> NONE

    Parameters:
        normalized_score (float): Score from 0.0 to 1.0

    Returns:
        str: Risk classification label
    """
    if normalized_score >= 0.6:
        return 'CRITICAL'
    elif normalized_score >= 0.4:
        return 'HIGH'
    elif normalized_score >= 0.2:
        return 'MEDIUM'
    elif normalized_score >= 0.05:
        return 'LOW'
    return 'NONE'


def classify_confidence(signal_count, text_length):
    """
    Estimates confidence in the analysis based on how many
    signals were detected and how long the text is.

    More signals and longer text = higher confidence.

    Parameters:
        signal_count (int): Number of signals detected.
        text_length  (int): Character length of input text.

    Returns:
        str: Confidence level - 'high', 'medium', or 'low'
    """
    if text_length < 20:
        return 'low'
    if signal_count >= 5 or text_length >= 200:
        return 'high'
    if signal_count >= 2 or text_length >= 50:
        return 'medium'
    return 'low'


# ── Full analysis runner ──────────────────────────────────────────────────────

def run_all_analyses(text):
    """
    Runs all Reveal analysis modules on a given text.

    Parameters:
        text (str): The text to analyze.

    Returns:
        dict: Raw results from all eight analysis modules.
    """
    return {
        'harm':     harm_detect(text),
        'sentiment': analyze_sentiment(text),
        'concerns':  get_concern_sentences(text),
        'voice':     analyze_voice(text),
        'tone':      analyze_tone(text),
        'pov':       analyze_pov(text),
        'entropy':   analyze_entropy(text),
        'ngrams':    analyze_ngrams(text),
        'anomaly':   analyze_anomalies(text),
        'abuse':     classify_abuse(text)
    }


# ── Signal extractor ──────────────────────────────────────────────────────────

def extract_signals(analyses):
    """
    Extracts boolean signals from all analysis results.
    Maps each signal to its weight key for scoring.

    Parameters:
        analyses (dict): Output from run_all_analyses()

    Returns:
        dict: Signal names mapped to boolean values.
    """
    harm     = analyses['harm']
    sent     = analyses['sentiment']
    voice    = analyses['voice']
    tone     = analyses['tone']
    pov      = analyses['pov']
    entropy  = analyses['entropy']
    ngrams   = analyses['ngrams']
    anomaly  = analyses['anomaly']
    abuse    = analyses['abuse']

    return {
        'grooming_detected':    harm['flags']['grooming_detected'],
        'self_harm_detected':   harm['flags']['self_harm_detected'],
        'help_signal_detected': harm['flags']['help_signal_detected'],
        'propaganda_detected':  harm['flags']['propaganda_detected'],
        'geo_signal_detected':  harm['flags']['geo_signal_detected'],
        'distressed_sentiment': sent['tone'] == 'distressed',
        'negative_sentiment':   sent['tone'] in ('negative', 'distressed'),
        'manipulative_tone':    'manipulative' in tone.get('high_risk_tones', []),
        'accusatory_tone':      'accusatory' in tone.get('high_risk_tones', []),
        'warning_tone':         tone.get('dominant_tone') == 'warning',
        'agency_obscured':      voice.get('agency_obscured', False),
        'pov_shift_detected':   pov.get('shift_detected', False),
        'entropy_anomaly':      entropy.get('anomaly_detected', False),
        'ngram_anomaly':        ngrams.get('anomaly_detected', False),
        'word_anomaly':         anomaly.get('anomaly_detected', False),
        'abuse_detected':       abuse.get('abuse_detected', False),
        'abuse_threat':         'threat' in abuse.get('active_categories', []),
        'abuse_coercive_control': 'coercive_control' in abuse.get('active_categories', []),
        'abuse_gaslighting':    'gaslighting' in abuse.get('active_categories', []),
        'abuse_emotional':      'emotional_abuse' in abuse.get('active_categories', []),
        'abuse_isolation':      'isolation' in abuse.get('active_categories', []),
        'abuse_narcissistic':   'narcissistic_abuse' in abuse.get('active_categories', []),
        'abuse_financial':      'financial_control' in abuse.get('active_categories', []),
        'abuse_escalation':     abuse.get('escalation', {}).get('escalation_detected', False)
    }


# ── Reasoning chain builder ───────────────────────────────────────────────────

def build_reasoning(signals, analyses):
    """
    Builds a human-readable reasoning chain explaining
    why each signal was flagged and what it means.

    Parameters:
        signals  (dict): Output from extract_signals()
        analyses (dict): Output from run_all_analyses()

    Returns:
        list of str: Reasoning statements in priority order.
    """
    reasons = []
    harm    = analyses['harm']
    sent    = analyses['sentiment']
    tone    = analyses['tone']
    voice   = analyses['voice']
    pov     = analyses['pov']
    abuse   = analyses.get('abuse', {})

    if signals['grooming_detected']:
        words = harm['results']['grooming']['word_matches']
        reasons.append(
            f"GROOMING SIGNALS detected: {', '.join(words)}. "
            f"These terms are associated with predatory communication."
        )

    if signals['self_harm_detected']:
        words = harm['results']['self_harm']['word_matches']
        reasons.append(
            f"SELF HARM SIGNALS detected: {', '.join(words)}. "
            f"These coded terms may indicate self-harm intent."
        )

    if signals['distressed_sentiment']:
        reasons.append(
            f"DISTRESSED SENTIMENT detected with compound score "
            f"{sent['compound']}. Text shows extreme negative emotional tone."
        )

    if signals['help_signal_detected']:
        words = harm['results']['help_signal']['word_matches']
        reasons.append(
            f"HELP SIGNALS detected: {', '.join(words)}. "
            f"These terms may indicate a person in distress seeking help."
        )

    if signals['manipulative_tone']:
        reasons.append(
            f"MANIPULATIVE TONE detected. Text contains language "
            f"patterns associated with emotional manipulation and control."
        )

    if signals['accusatory_tone']:
        reasons.append(
            f"ACCUSATORY TONE detected. Text contains blame-shifting "
            f"and accusatory language patterns."
        )

    if signals['propaganda_detected']:
        cats = list(harm['results']['propaganda']['category_matches'].keys())
        reasons.append(
            f"PROPAGANDA detected ({', '.join(cats)}). "
            f"Text uses known persuasion and manipulation techniques."
        )

    if signals['pov_shift_detected']:
        shifts = pov.get('shift_count', 0)
        reasons.append(
            f"POV SHIFTS detected ({shifts} shift(s)). "
            f"Sudden changes between first and second person "
            f"are common in manipulative communication."
        )

    if signals['agency_obscured']:
        ratio = voice.get('passive_ratio', 0)
        reasons.append(
            f"AGENCY OBSCURED: {round(ratio * 100)}% of sentences use "
            f"passive voice, which can mask responsibility and intent."
        )

    if signals['warning_tone']:
        reasons.append(
            f"WARNING TONE detected. Text uses language "
            f"designed to create fear or urgency."
        )

    if signals['entropy_anomaly']:
        reasons.append(
            f"ENTROPY ANOMALY detected. Statistical analysis found "
            f"unusual character distribution patterns in the text."
        )

    if signals['ngram_anomaly']:
        reasons.append(
            f"NGRAM ANOMALY detected. Unusual word sequence "
            f"patterns found that deviate from normal English."
        )

    if signals['word_anomaly']:
        reasons.append(
            f"WORD ANOMALY detected. Statistically outlier words "
            f"found that may indicate coded or unusual communication."
        )

    if signals['geo_signal_detected']:
        words = harm['results']['geographic']['word_matches']
        reasons.append(
            f"GEOGRAPHIC SIGNALS detected: {', '.join(words[:5])}. "
            f"Text contains location-related language."
        )

    if signals.get('abuse_detected'):
        abuse_cats = abuse.get('active_categories', [])
        esc = abuse.get('escalation', {})
        reasons.append(
            f"ABUSE DETECTED ({', '.join(abuse_cats)}). "
            f"Severity: {abuse.get('severity', 'UNKNOWN')}."
        )
        if esc.get('escalation_detected'):
            reasons.append(
                f"ABUSE ESCALATION [{esc.get('escalation_level')}]: "
                f"{esc.get('escalation_signals', [''])[0]}"
            )

    if not reasons:
        reasons.append("No significant risk signals detected in this text.")

    return reasons


# ── Main scorer ───────────────────────────────────────────────────────────────

def score(text):
    """
    Main entry point for the Reveal reasoning and scoring engine.
    Runs all analyses, extracts signals, calculates risk score,
    and builds a reasoning chain.

    Parameters:
        text (str): The text to analyze.

    Returns:
        dict: A comprehensive scored report containing:
            - input_text:      the original text
            - signals:         all detected boolean signals
            - raw_score:       weighted integer risk score
            - normalized_score: score normalized to 0.0-1.0
            - risk_level:      NONE/LOW/MEDIUM/HIGH/CRITICAL
            - confidence:      low/medium/high
            - reasoning:       list of explanation strings
            - analyses:        raw output from all modules
    """
    if not text or not text.strip():
        return {
            'input_text':       text,
            'signals':          {},
            'raw_score':        0,
            'normalized_score': 0.0,
            'risk_level':       'NONE',
            'confidence':       'low',
            'reasoning':        ['No text provided for analysis.'],
            'analyses':         {}
        }

    analyses = run_all_analyses(text)
    signals  = extract_signals(analyses)
    raw_score, normalized_score = calculate_score(signals)
    risk_level  = classify_score(normalized_score)
    signal_count = sum(1 for v in signals.values() if v)
    confidence  = classify_confidence(signal_count, len(text))
    reasoning   = build_reasoning(signals, analyses)

    return {
        'input_text':       text,
        'signals':          signals,
        'raw_score':        raw_score,
        'normalized_score': normalized_score,
        'risk_level':       risk_level,
        'confidence':       confidence,
        'reasoning':        reasoning,
        'analyses':         analyses
    }