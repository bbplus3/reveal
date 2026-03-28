"""
reveal/reasoning/reporter.py

Unified report generator for the Reveal library.
Combines all analysis layers into a single polished report.
This is the top-level entry point for using Reveal.

Usage:
    from reveal.reasoning.reporter import analyze
    print(analyze("Some text to analyze.", fmt='text'))
"""

from datetime import datetime
from reveal.reasoning.scorer import score


# ── Text report formatter ─────────────────────────────────────────────────────

def format_full_report(result):
    """
    Formats a scored result into a comprehensive human-readable report.

    Parameters:
        result (dict): Output from reveal.reasoning.scorer.score()

    Returns:
        str: A fully formatted text report.
    """
    lines = []
    divider = '=' * 60
    thin    = '-' * 60

    lines.append(divider)
    lines.append('           R E V E A L   A N A L Y S I S   R E P O R T')
    lines.append(divider)

    # Metadata
    lines.append(f"\nTimestamp  : {datetime.now().isoformat()}")
    lines.append(f"Word Count : {len(result['input_text'].split())}")
    preview = result['input_text'][:100]
    ellipsis = '...' if len(result['input_text']) > 100 else ''
    lines.append(f"Text       : {preview}{ellipsis}")

    # Risk summary
    lines.append(f"\n{thin}")
    lines.append('RISK SUMMARY')
    lines.append(thin)
    lines.append(f"Risk Level       : {result['risk_level']}")
    lines.append(f"Risk Score       : {result['raw_score']} / "
                 f"{int(result['normalized_score'] * 100)}%")
    lines.append(f"Confidence       : {result['confidence'].upper()}")

    # Sentiment
    sent = result['analyses'].get('sentiment', {})
    lines.append(f"Sentiment Tone   : {sent.get('tone', 'unknown')}")
    lines.append(f"Compound Score   : {sent.get('compound', 0.0)}")

    # Active signals
    lines.append(f"\n{thin}")
    lines.append('ACTIVE SIGNALS')
    lines.append(thin)
    active = [k for k, v in result['signals'].items() if v]
    if active:
        for signal in active:
            lines.append(f"  > {signal}")
    else:
        lines.append('  None detected.')

    # Reasoning chain
    lines.append(f"\n{thin}")
    lines.append('REASONING')
    lines.append(thin)
    for i, reason in enumerate(result['reasoning'], 1):
        lines.append(f"  {i}. {reason}")

    # Harm detection results
    harm = result['analyses'].get('harm', {})
    results = harm.get('results', {})

    lines.append(f"\n{thin}")
    lines.append('HARM DETECTION')
    lines.append(thin)

    if results.get('propaganda', {}).get('match_count', 0) > 0:
        lines.append(f"\n  PROPAGANDA")
        words = results['propaganda']['word_matches']
        lines.append(f"  Matches    : {', '.join(words)}")
        cats = results['propaganda'].get('category_matches', {})
        if cats:
            for cat, phrases in cats.items():
                lines.append(f"  [{cat}]: {', '.join(phrases)}")

    if results.get('help_signal', {}).get('match_count', 0) > 0:
        lines.append(f"\n  HELP SIGNALS")
        lines.append(f"  Matches : {', '.join(results['help_signal']['word_matches'])}")

    if results.get('self_harm', {}).get('match_count', 0) > 0:
        lines.append(f"\n  SELF HARM")
        lines.append(f"  Matches : {', '.join(results['self_harm']['word_matches'])}")

    if results.get('grooming', {}).get('match_count', 0) > 0:
        lines.append(f"\n  GROOMING")
        lines.append(f"  Matches : {', '.join(results['grooming']['word_matches'])}")

    if results.get('geographic', {}).get('match_count', 0) > 0:
        lines.append(f"\n  GEOGRAPHIC")
        lines.append(f"  Matches : {', '.join(results['geographic']['word_matches'][:5])}")

    if all(results.get(k, {}).get('match_count', 0) == 0
           for k in ['propaganda', 'help_signal', 'self_harm', 'grooming', 'geographic']):
        lines.append('  No harm signals detected.')

    # Linguistic analysis
    voice = result['analyses'].get('voice', {})
    tone  = result['analyses'].get('tone', {})
    pov   = result['analyses'].get('pov', {})

    lines.append(f"\n{thin}")
    lines.append('LINGUISTIC ANALYSIS')
    lines.append(thin)
    lines.append(f"  Voice       : {voice.get('dominant_voice', 'unknown')} "
                 f"({int(voice.get('passive_ratio', 0) * 100)}% passive)")
    lines.append(f"  Tone        : {tone.get('dominant_tone', 'unknown')}")
    lines.append(f"  POV         : {pov.get('dominant_pov', 'unknown')}")
    lines.append(f"  POV Shifts  : {pov.get('shift_count', 0)}")
    if tone.get('high_risk_tones'):
        lines.append(f"  High Risk   : {', '.join(tone['high_risk_tones'])}")

    # Cryptanalysis
    entropy = result['analyses'].get('entropy', {})
    ngrams  = result['analyses'].get('ngrams', {})
    anomaly = result['analyses'].get('anomaly', {})

    lines.append(f"\n{thin}")
    lines.append('CRYPTANALYSIS')
    lines.append(thin)
    lines.append(f"  Char Entropy    : {entropy.get('char_entropy', 0.0)} "
                 f"({entropy.get('char_classification', 'unknown')})")
    lines.append(f"  Entropy Anomaly : {entropy.get('anomaly_detected', False)}")
    lines.append(f"  Ngram Anomaly   : {ngrams.get('anomaly_detected', False)}")
    lines.append(f"  Word Anomaly    : {anomaly.get('anomaly_detected', False)}")
    if anomaly.get('capitalization_anomalies'):
        caps = [a['word'] for a in anomaly['capitalization_anomalies']]
        lines.append(f"  Cap Anomalies   : {', '.join(caps)}")

    # Concerning sentences
    concerns = result['analyses'].get('concerns', [])
    lines.append(f"\n{thin}")
    lines.append('CONCERNING SENTENCES')
    lines.append(thin)
    if concerns:
        for c in concerns:
            lines.append(f"  [{c['tone'].upper()}] \"{c['sentence']}\"")
    else:
        lines.append('  None identified.')

    lines.append(f"\n{divider}\n")
    return '\n'.join(lines)


# ── Main entry point ──────────────────────────────────────────────────────────

def analyze(text, fmt='dict'):
    """
    Main entry point for the Reveal library.
    Runs the complete analysis pipeline and returns results.

    Parameters:
        text (str): The text to analyze.
        fmt  (str): Output format - 'dict' or 'text'. Default 'dict'.

    Returns:
        dict or str: Complete analysis in requested format.

    Example:
        from reveal.reasoning.reporter import analyze
        print(analyze("I feel so alone.", fmt='text'))
    """
    result = score(text)

    if fmt == 'text':
        return format_full_report(result)
    return result