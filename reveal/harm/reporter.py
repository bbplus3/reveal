"""
reveal/harm/reporter.py

Report generation module for the Reveal library.
Combines output from detector.py and sentiment.py into
a single structured report with both machine-readable
and human-readable formats.
"""

import json
from datetime import datetime
from reveal.harm.detector import analyze as detect
from reveal.harm.sentiment import analyze_sentiment, get_concern_sentences


# ── Core report builder ───────────────────────────────────────────────────────

def build_report(text):
    """
    Runs full harm detection and sentiment analysis on a given text
    and combines the results into a single structured report.
    """
    detection_result = detect(text)
    sentiment_result = analyze_sentiment(text)
    concern_sentences = get_concern_sentences(text)

    concerns = [
        {
            'sentence': s['sentence'],
            'tone':     s['tone'],
            'compound': s['compound']
        }
        for s in concern_sentences
    ]

    total_signals = sum([
        detection_result['results']['propaganda']['match_count'],
        detection_result['results']['self_harm']['match_count'],
        detection_result['results']['help_signal']['match_count'],
        detection_result['results']['grooming']['match_count'],
        detection_result['results']['geographic']['match_count']
    ])

    risk_level = _calculate_risk_level(detection_result['flags'], sentiment_result)

    active_flags = [k for k, v in detection_result['flags'].items() if v]
    summary = {
        'risk_level':         risk_level,
        'active_flags':       active_flags,
        'total_signals':      total_signals,
        'sentiment_tone':     sentiment_result['tone'],
        'concern_raised':     sentiment_result['concern'],
        'flagged_categories': list(
            detection_result['results']['propaganda']['category_matches'].keys()
        )
    }

    return {
        'metadata': {
            'timestamp':   datetime.now().isoformat(),
            'text_length': len(text),
            'word_count':  len(text.split())
        },
        'input_text': text,
        'detection':  detection_result['results'],
        'sentiment':  sentiment_result,
        'concerns':   concerns,
        'summary':    summary
    }


# ── Risk level calculator ─────────────────────────────────────────────────────

def _calculate_risk_level(flags, sentiment):
    """
    Calculates an overall risk level based on detected flags and sentiment.
    """
    active_flag_count = sum(1 for v in flags.values() if v)

    if flags.get('grooming_detected'):
        return 'CRITICAL'
    if flags.get('self_harm_detected'):
        return 'CRITICAL'
    if sentiment['tone'] == 'distressed' and active_flag_count >= 1:
        return 'CRITICAL'
    if flags.get('help_signal_detected') and active_flag_count >= 2:
        return 'HIGH'
    if active_flag_count >= 3:
        return 'HIGH'
    if flags.get('help_signal_detected'):
        return 'MEDIUM'
    if active_flag_count >= 2:
        return 'MEDIUM'
    if active_flag_count == 1:
        return 'LOW'

    return 'NONE'


# ── Human readable formatter ──────────────────────────────────────────────────

def format_report(report):
    """
    Formats a structured report dict into a human-readable text report.
    """
    lines = []
    divider = '=' * 60

    lines.append(divider)
    lines.append('           R E V E A L   A N A L Y S I S   R E P O R T')
    lines.append(divider)

    lines.append(f"\nTimestamp  : {report['metadata']['timestamp']}")
    lines.append(f"Word Count : {report['metadata']['word_count']}")
    lines.append(f"Text       : {report['input_text'][:100]}{'...' if len(report['input_text']) > 100 else ''}")

    lines.append(f"\n{'-' * 60}")
    lines.append('SUMMARY')
    lines.append(f"{'-' * 60}")
    lines.append(f"Risk Level     : {report['summary']['risk_level']}")
    lines.append(f"Sentiment Tone : {report['summary']['sentiment_tone']}")
    lines.append(f"Total Signals  : {report['summary']['total_signals']}")
    lines.append(f"Concern Raised : {report['summary']['concern_raised']}")

    lines.append(f"\n{'-' * 60}")
    lines.append('ACTIVE FLAGS')
    lines.append(f"{'-' * 60}")
    if report['summary']['active_flags']:
        for flag in report['summary']['active_flags']:
            lines.append(f"  > {flag}")
    else:
        lines.append('  None')

    lines.append(f"\n{'-' * 60}")
    lines.append('SENTIMENT SCORES')
    lines.append(f"{'-' * 60}")
    s = report['sentiment']
    lines.append(f"  Positive : {s['pos']}")
    lines.append(f"  Neutral  : {s['neu']}")
    lines.append(f"  Negative : {s['neg']}")
    lines.append(f"  Compound : {s['compound']}")

    lines.append(f"\n{'-' * 60}")
    lines.append('DETECTION RESULTS')
    lines.append(f"{'-' * 60}")

    results = report['detection']

    if results['propaganda']['match_count'] > 0:
        lines.append(f"\n  PROPAGANDA ({results['propaganda']['match_count']} signals)")
        lines.append(f"  Words matched : {', '.join(results['propaganda']['word_matches'])}")
        if results['propaganda']['category_matches']:
            lines.append('  Categories    :')
            for cat, phrases in results['propaganda']['category_matches'].items():
                lines.append(f"    * {cat}: {', '.join(phrases)}")

    if results['help_signal']['match_count'] > 0:
        lines.append(f"\n  HELP SIGNALS ({results['help_signal']['match_count']} signals)")
        lines.append(f"  Words matched : {', '.join(results['help_signal']['word_matches'])}")

    if results['self_harm']['match_count'] > 0:
        lines.append(f"\n  SELF HARM ({results['self_harm']['match_count']} signals)")
        lines.append(f"  Words matched : {', '.join(results['self_harm']['word_matches'])}")

    if results['grooming']['match_count'] > 0:
        lines.append(f"\n  GROOMING ({results['grooming']['match_count']} signals)")
        lines.append(f"  Words matched : {', '.join(results['grooming']['word_matches'])}")

    if results['geographic']['match_count'] > 0:
        lines.append(f"\n  GEOGRAPHIC ({results['geographic']['match_count']} signals)")
        lines.append(f"  Words matched : {', '.join(results['geographic']['word_matches'])}")

    if all(results[k]['match_count'] == 0 for k in results):
        lines.append('  No signals detected.')

    lines.append(f"\n{'-' * 60}")
    lines.append('CONCERNING SENTENCES')
    lines.append(f"{'-' * 60}")
    if report['concerns']:
        for c in report['concerns']:
            lines.append(f"  [{c['tone'].upper()}] \"{c['sentence']}\"")
    else:
        lines.append('  None identified.')

    lines.append(f"\n{divider}\n")

    return '\n'.join(lines)


# ── Main entry point ──────────────────────────────────────────────────────────

def reveal(text, fmt='dict'):
    """
    Main entry point for the Reveal harm detection library.

    Parameters:
        text (str): The text to analyze.
        fmt  (str): Output format - 'dict' or 'text'. Default is 'dict'.

    Returns:
        dict or str: Full analysis report in requested format.

    Example:
        from reveal.harm.reporter import reveal
        print(reveal("I feel so alone and trapped.", fmt='text'))
    """
    report = build_report(text)

    if fmt == 'text':
        return format_report(report)
    return report