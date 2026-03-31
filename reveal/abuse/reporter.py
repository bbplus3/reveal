"""
reveal/abuse/reporter.py

Report generation module for the Reveal abuse detection layer.
Produces structured and human-readable reports from classifier output.
"""

from datetime import datetime
from reveal.abuse.classifier import classify_abuse


# ── Text report formatter ─────────────────────────────────────────────────────

def format_abuse_report(result):
    """
    Formats a classified abuse result into a human-readable report.

    Parameters:
        result (dict): Output from classify_abuse()

    Returns:
        str: A formatted human-readable report.
    """
    lines = []
    divider = '=' * 60
    thin    = '-' * 60

    lines.append(divider)
    lines.append('         R E V E A L   A B U S E   A N A L Y S I S')
    lines.append(divider)

    lines.append(f"\nTimestamp : {datetime.now().isoformat()}")

    # Overall result
    lines.append(f"\n{thin}")
    lines.append('SUMMARY')
    lines.append(thin)
    lines.append(f"Abuse Detected : {result['abuse_detected']}")
    lines.append(f"Severity       : {result['severity']}")
    lines.append(f"Score          : {result['score']} "
                 f"({int(result['score'] * 100)}%)")

    # Escalation
    esc = result['escalation']
    if esc['escalation_detected']:
        lines.append(f"Escalation     : {esc['escalation_level']} RISK")
    else:
        lines.append(f"Escalation     : None detected")

    # Active categories
    lines.append(f"\n{thin}")
    lines.append('DETECTED CATEGORIES')
    lines.append(thin)
    if result['active_categories']:
        for cat in result['active_categories']:
            matches = result['categories'].get(cat, [])
            lines.append(f"\n  {cat.upper().replace('_', ' ')}")
            for match in matches[:5]:
                lines.append(f"    • \"{match}\"")
            if len(matches) > 5:
                lines.append(f"    ... and {len(matches) - 5} more")
    else:
        lines.append('  None detected.')

    # Abuse profiles
    if result['profiles']:
        lines.append(f"\n{thin}")
        lines.append('ABUSE PROFILES IDENTIFIED')
        lines.append(thin)
        for profile in result['profiles']:
            amp = ' [AMPLIFIED]' if profile['amplified'] else ''
            lines.append(f"  • {profile['profile'].upper().replace('_', ' ')}{amp}")
            lines.append(f"    {profile['description']}")

    # Escalation signals
    if esc['escalation_signals']:
        lines.append(f"\n{thin}")
        lines.append(f"ESCALATION SIGNALS [{esc['escalation_level']}]")
        lines.append(thin)
        for signal in esc['escalation_signals']:
            lines.append(f"  ⚠ {signal}")

    # Reasoning
    lines.append(f"\n{thin}")
    lines.append('REASONING')
    lines.append(thin)
    for i, reason in enumerate(result['reasoning'], 1):
        lines.append(f"  {i}. {reason}")

    # Most severe sentence
    if result['most_severe_sentence']:
        lines.append(f"\n{thin}")
        lines.append('MOST CONCERNING SENTENCE')
        lines.append(thin)
        s = result['most_severe_sentence']
        lines.append(f"  Severity : {s['severity']}")
        lines.append(f"  Text     : \"{s['sentence']}\"")
        cats = list(s['categories'].keys())
        if cats:
            lines.append(f"  Types    : {', '.join(cats)}")

    # Sentence breakdown
    flagged = [s for s in result['sentence_analysis'] if s['abuse_present']]
    if flagged:
        lines.append(f"\n{thin}")
        lines.append('FLAGGED SENTENCES')
        lines.append(thin)
        for s in flagged:
            cats = list(s['categories'].keys())
            lines.append(f"\n  [{s['severity']}] \"{s['sentence']}\"")
            lines.append(f"  Types: {', '.join(cats)}")

    lines.append(f"\n{divider}\n")
    return '\n'.join(lines)


# ── Main entry point ──────────────────────────────────────────────────────────

def analyze(text, fmt='dict'):
    """
    Main entry point for the Reveal abuse detection layer.

    Parameters:
        text (str): The text to analyze.
        fmt  (str): Output format - 'dict' or 'text'. Default 'dict'.

    Returns:
        dict or str: Complete abuse analysis in requested format.

    Example:
        from reveal.abuse.reporter import analyze
        print(analyze("You are imagining things. You need me.", fmt='text'))
    """
    result = classify_abuse(text)

    if fmt == 'text':
        return format_abuse_report(result)
    return result