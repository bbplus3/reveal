"""
reveal/abuse/classifier.py

Contextual classification module for the Reveal abuse detection layer.
Analyzes co-occurrence of abuse patterns across categories to identify
compound abuse profiles and escalation signals.

Co-occurrence matters because:
    - Gaslighting + isolation = classic coercive control profile
    - Threat + emotional abuse = high danger escalation signal
    - Financial control + isolation = economic abuse profile
    - Narcissistic abuse + gaslighting = narcissistic abuse cycle
"""

from reveal.abuse.detector import analyze_abuse


# ── Compound abuse profiles ───────────────────────────────────────────────────
# Known combinations of categories that indicate specific abuse profiles

ABUSE_PROFILES = {
    'coercive_control_profile': {
        'required':    ['coercive_control'],
        'amplified_by': ['isolation', 'gaslighting', 'threat'],
        'description': 'Coercive control pattern — systematic control '
                       'of behavior, freedom, and autonomy.'
    },
    'narcissistic_abuse_cycle': {
        'required':    ['narcissistic_abuse'],
        'amplified_by': ['gaslighting', 'emotional_abuse'],
        'description': 'Narcissistic abuse cycle — idealization, '
                       'devaluation, and discard patterns detected.'
    },
    'economic_abuse_profile': {
        'required':    ['financial_control'],
        'amplified_by': ['isolation', 'coercive_control'],
        'description': 'Economic abuse profile — financial control '
                       'used to enforce dependency and restrict freedom.'
    },
    'danger_escalation': {
        'required':    ['threat'],
        'amplified_by': ['emotional_abuse', 'coercive_control'],
        'description': 'DANGER ESCALATION — threat language combined '
                       'with abuse patterns indicates elevated risk.'
    },
    'psychological_abuse_profile': {
        'required':    ['gaslighting', 'emotional_abuse'],
        'amplified_by': ['narcissistic_abuse', 'isolation'],
        'description': 'Psychological abuse profile — reality distortion '
                       'combined with worth attacks detected.'
    },
    'isolation_campaign': {
        'required':    ['isolation'],
        'amplified_by': ['coercive_control', 'emotional_abuse'],
        'description': 'Isolation campaign — systematic separation from '
                       'support networks detected.'
    }
}


# ── Profile detector ──────────────────────────────────────────────────────────

def detect_abuse_profiles(active_categories):
    """
    Identifies compound abuse profiles based on co-occurring categories.

    Parameters:
        active_categories (list): List of detected abuse category names.

    Returns:
        list of dicts: Detected profiles, each containing:
            - profile:     profile name
            - description: human readable description
            - amplified:   True if amplifying categories also present
    """
    if not active_categories:
        return []

    detected_profiles = []
    active_set = set(active_categories)

    for profile_name, profile_def in ABUSE_PROFILES.items():
        required = set(profile_def['required'])
        amplifiers = set(profile_def['amplified_by'])

        if required.issubset(active_set):
            amplified = bool(amplifiers.intersection(active_set))
            detected_profiles.append({
                'profile':     profile_name,
                'description': profile_def['description'],
                'amplified':   amplified
            })

    return detected_profiles


# ── Escalation detector ───────────────────────────────────────────────────────

def detect_escalation(analysis_result):
    """
    Detects escalation signals — combinations of categories that
    suggest the abuse may be intensifying or becoming dangerous.

    Escalation signals:
        - Threat + any other category
        - Three or more categories present simultaneously
        - Financial control + isolation (trapped victim profile)
        - Gaslighting + threat (reality distortion + danger)

    Parameters:
        analysis_result (dict): Output from analyze_abuse()

    Returns:
        dict: Escalation assessment containing:
            - escalation_detected: True if escalation signals found
            - escalation_level:    'HIGH', 'MEDIUM', or 'NONE'
            - escalation_signals:  list of detected signals
    """
    active = set(analysis_result.get('active_categories', []))
    signals = []

    if not active:
        return {
            'escalation_detected': False,
            'escalation_level':    'NONE',
            'escalation_signals':  []
        }

    # Threat combined with any other category
    if 'threat' in active and len(active) > 1:
        signals.append(
            'Threat language combined with other abuse patterns — '
            'elevated danger signal.'
        )

    # Three or more categories
    if len(active) >= 3:
        signals.append(
            f'{len(active)} abuse categories detected simultaneously — '
            f'compound abuse profile.'
        )

    # Trapped victim profile
    if 'financial_control' in active and 'isolation' in active:
        signals.append(
            'Financial control combined with isolation — '
            'victim may be trapped with limited escape options.'
        )

    # Reality distortion + danger
    if 'gaslighting' in active and 'threat' in active:
        signals.append(
            'Gaslighting combined with threats — '
            'victim reality being distorted while under threat.'
        )

    # Coercive control + threat
    if 'coercive_control' in active and 'threat' in active:
        signals.append(
            'Coercive control combined with threats — '
            'high-risk domestic abuse pattern.'
        )

    # Determine escalation level
    if 'threat' in active or len(signals) >= 2:
        level = 'HIGH'
    elif signals:
        level = 'MEDIUM'
    else:
        level = 'NONE'

    return {
        'escalation_detected': len(signals) > 0,
        'escalation_level':    level,
        'escalation_signals':  signals
    }


# ── Reasoning builder ─────────────────────────────────────────────────────────

def build_abuse_reasoning(analysis_result, profiles, escalation):
    """
    Builds a human-readable reasoning chain explaining the findings.
    """
    reasons = []
    categories = analysis_result.get('categories', {})

    if not categories:
        return ['No abusive language patterns detected in this text.']

    if 'threat' in categories:
        matches = ', '.join(categories['threat'][:3])
        reasons.append(
            f"THREAT LANGUAGE detected: {matches}. "
            f"This text contains intimidation or threat patterns."
        )

    if 'coercive_control' in categories:
        matches = ', '.join(categories['coercive_control'][:3])
        reasons.append(
            f"COERCIVE CONTROL detected: {matches}. "
            f"Patterns of control, ultimatums, or permission enforcement found."
        )

    if 'gaslighting' in categories:
        matches = ', '.join(categories['gaslighting'][:3])
        reasons.append(
            f"GASLIGHTING detected: {matches}. "
            f"Reality denial or sanity questioning patterns found."
        )

    if 'emotional_abuse' in categories:
        matches = ', '.join(categories['emotional_abuse'][:3])
        reasons.append(
            f"EMOTIONAL ABUSE detected: {matches}. "
            f"Degradation or worth-attack patterns found."
        )

    if 'isolation' in categories:
        matches = ', '.join(categories['isolation'][:3])
        reasons.append(
            f"ISOLATION TACTICS detected: {matches}. "
            f"Patterns of separating victim from support networks found."
        )

    if 'narcissistic_abuse' in categories:
        matches = ', '.join(categories['narcissistic_abuse'][:3])
        reasons.append(
            f"NARCISSISTIC ABUSE detected: {matches}. "
            f"Entitlement or victim-blaming patterns found."
        )

    if 'financial_control' in categories:
        matches = ', '.join(categories['financial_control'][:3])
        reasons.append(
            f"FINANCIAL CONTROL detected: {matches}. "
            f"Economic abuse or financial dependency patterns found."
        )

    for profile in profiles:
        amp = " Amplifying factors present." if profile['amplified'] else ""
        reasons.append(f"PROFILE: {profile['description']}{amp}")

    for signal in escalation.get('escalation_signals', []):
        reasons.append(f"ESCALATION: {signal}")

    return reasons


# ── Main classifier ───────────────────────────────────────────────────────────

def classify_abuse(text):
    """
    Main entry point for the abuse classification module.
    Runs full detection, profile matching, escalation analysis,
    and reasoning generation.

    Parameters:
        text (str): The text to analyze.

    Returns:
        dict: A comprehensive abuse classification report containing:
            - abuse_detected:      True if any patterns found
            - categories:          matched patterns by category
            - active_categories:   list of category names
            - severity:            overall severity label
            - score:               normalized score 0.0-1.0
            - profiles:            detected compound abuse profiles
            - escalation:          escalation assessment
            - reasoning:           explanation strings
            - sentence_analysis:   per sentence breakdown
            - most_severe_sentence: highest risk sentence
    """
    if not text or not text.strip():
        return {
            'abuse_detected':       False,
            'categories':           {},
            'active_categories':    [],
            'severity':             'NONE',
            'score':                0.0,
            'profiles':             [],
            'escalation': {
                'escalation_detected': False,
                'escalation_level':    'NONE',
                'escalation_signals':  []
            },
            'reasoning':            ['No text provided.'],
            'sentence_analysis':    [],
            'most_severe_sentence': None
        }

    analysis   = analyze_abuse(text)
    profiles   = detect_abuse_profiles(analysis['active_categories'])
    escalation = detect_escalation(analysis)
    reasoning  = build_abuse_reasoning(analysis, profiles, escalation)

    return {
        'abuse_detected':       analysis['abuse_detected'],
        'categories':           analysis['categories'],
        'active_categories':    analysis['active_categories'],
        'severity':             analysis['severity'],
        'score':                analysis['score'],
        'profiles':             profiles,
        'escalation':           escalation,
        'reasoning':            reasoning,
        'sentence_analysis':    analysis['sentence_analysis'],
        'most_severe_sentence': analysis['most_severe_sentence']
    }