"""
app.py

Reveal Analyzer - Streamlit Demo App
Interactive demonstration of the Reveal NLP library.

Run with: streamlit run app.py
"""

import sys
import os
sys.path.insert(0, '.')

import streamlit as st
import json

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Reveal Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    .risk-none     { background:#e8f5e9; color:#2e7d32; padding:8px 16px; border-radius:8px; font-weight:bold; font-size:1.2em; }
    .risk-low      { background:#fff8e1; color:#f57f17; padding:8px 16px; border-radius:8px; font-weight:bold; font-size:1.2em; }
    .risk-medium   { background:#fff3e0; color:#e65100; padding:8px 16px; border-radius:8px; font-weight:bold; font-size:1.2em; }
    .risk-high     { background:#fce4ec; color:#b71c1c; padding:8px 16px; border-radius:8px; font-weight:bold; font-size:1.2em; }
    .risk-critical { background:#b71c1c; color:white;   padding:8px 16px; border-radius:8px; font-weight:bold; font-size:1.2em; }
    .signal-box    { background:#f5f5f5; border-left:4px solid #1976d2; padding:8px 12px; margin:4px 0; border-radius:4px; }
    .concern-box   { background:#fff8e1; border-left:4px solid #f57f17; padding:8px 12px; margin:4px 0; border-radius:4px; }
    .reason-box    { background:#e3f2fd; border-left:4px solid #1565c0; padding:8px 12px; margin:6px 0; border-radius:4px; }
    .abuse-box     { background:#fce4ec; border-left:4px solid #b71c1c; padding:8px 12px; margin:6px 0; border-radius:4px; }
    .escalation-box { background:#b71c1c; color:white; padding:8px 12px; margin:6px 0; border-radius:4px; }
    .profile-box   { background:#f3e5f5; border-left:4px solid #7b1fa2; padding:8px 12px; margin:6px 0; border-radius:4px; }
</style>
""", unsafe_allow_html=True)


# ── Risk badge helper ─────────────────────────────────────────────────────────

def risk_badge(level):
    css = {
        'NONE':     'risk-none',
        'LOW':      'risk-low',
        'MEDIUM':   'risk-medium',
        'HIGH':     'risk-high',
        'CRITICAL': 'risk-critical'
    }.get(level, 'risk-none')
    return f'<span class="{css}">⚑ {level}</span>'


# ── Load dictionaries ─────────────────────────────────────────────────────────

@st.cache_data
def load_dictionaries():
    dict_path = os.path.join('reveal', 'dictionaries')
    dicts = {}
    files = {
        'Propaganda Words':   'prop_words.json',
        'Propaganda Types':   'prop_dict.json',
        'Self Harm Signals':  'harm_words.json',
        'Help Signals':       'help_words.json',
        'Grooming Signals':   'groom_words.json',
        'Geographic Signals': 'geo_words.json'
    }
    for name, filename in files.items():
        path = os.path.join(dict_path, filename)
        with open(path, 'r', encoding='utf-8') as f:
            dicts[name] = json.load(f)
    return dicts


# ── Header ────────────────────────────────────────────────────────────────────

st.title("🔍 Reveal Analyzer")
st.markdown(
    "An open-source Python library for intelligent harm detection, "
    "linguistic analysis, and abuse pattern recognition in text."
)
st.markdown("---")


# ── Tabs ──────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Analyze Text",
    "🛡️ Abuse Detection",
    "📄 Full Report",
    "🔬 Module Explorer",
    "📚 Word List Explorer",
    "ℹ️ About Reveal"
])


# ── Tab 1: Analyze Text ───────────────────────────────────────────────────────

with tab1:
    st.subheader("Analyze Text")
    st.markdown(
        "Enter any text below and Reveal will analyze it for harmful signals, "
        "sentiment, linguistic patterns, and cryptanalytic anomalies."
    )

    sample_texts = {
        "Select a sample...": "",
        "Help signal": "I feel so alone and hopeless. I am so trapped and in pain. Please someone help me, I need someone.",
        "Propaganda": "Most Americans support this cause. We must act now or it will lead to disaster. Join us today.",
        "Manipulative": "If you really cared you would stay. You need me. No one else will ever understand you like I do.",
        "Gaslighting": "You are imagining things. That never happened. You are too sensitive and always overreacting.",
        "Coercive control": "You are not allowed to see your friends. I control the money. You will do what I say.",
        "Clean text": "The weather today is sunny and warm. It is a beautiful day to go for a walk in the park.",
    }

    sample = st.selectbox("Or load a sample text:", list(sample_texts.keys()))
    default_text = sample_texts[sample]

    text_input = st.text_area(
        "Enter text to analyze:",
        value=default_text,
        height=150,
        placeholder="Type or paste any text here..."
    )

    analyze_clicked = st.button("🔍 Analyze", type="primary")

    if analyze_clicked and text_input.strip():
        with st.spinner("Analyzing..."):
            try:
                from reveal.reasoning.scorer import score
                result = score(text_input)

                st.session_state['result'] = result
                st.session_state['text']   = text_input

                # Risk level
                st.markdown("### Risk Assessment")
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(
                        risk_badge(result['risk_level']),
                        unsafe_allow_html=True
                    )
                with col2:
                    st.metric("Risk Score", f"{int(result['normalized_score'] * 100)}%")
                with col3:
                    st.metric("Confidence", result['confidence'].upper())

                # Active signals
                active = [k for k, v in result['signals'].items() if v]
                if active:
                    st.markdown("### Active Signals")
                    cols = st.columns(3)
                    for i, signal in enumerate(active):
                        with cols[i % 3]:
                            st.markdown(
                                f'<div class="signal-box">⚑ {signal}</div>',
                                unsafe_allow_html=True
                            )

                # Reasoning
                st.markdown("### Analysis Reasoning")
                for reason in result['reasoning']:
                    st.markdown(
                        f'<div class="reason-box">{reason}</div>',
                        unsafe_allow_html=True
                    )

                # Concerning sentences
                concerns = result['analyses'].get('concerns', [])
                if concerns:
                    st.markdown("### Concerning Sentences")
                    for c in concerns:
                        st.markdown(
                            f'<div class="concern-box">'
                            f'<strong>[{c["tone"].upper()}]</strong> '
                            f'"{c["sentence"]}"</div>',
                            unsafe_allow_html=True
                        )

                # Abuse summary if detected
                abuse = result['analyses'].get('abuse', {})
                if abuse.get('abuse_detected'):
                    st.markdown("### ⚠️ Abuse Patterns Detected")
                    st.markdown(
                        f'<div class="abuse-box">'
                        f'<strong>Severity: {abuse["severity"]}</strong> — '
                        f'Categories: {", ".join(abuse["active_categories"])}'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    st.info("See the **Abuse Detection** tab for full details.")

            except Exception as e:
                st.error(f"Analysis error: {e}")

    elif analyze_clicked:
        st.warning("Please enter some text to analyze.")


# ── Tab 2: Abuse Detection ────────────────────────────────────────────────────

with tab2:
    st.subheader("Abuse Detection")
    st.markdown(
        "Reveal detects seven categories of abusive, manipulative, and "
        "controlling language using pattern-based sentence analysis."
    )

    abuse_samples = {
        "Select a sample...": "",
        "Gaslighting": "You are imagining things. That never happened. You are too sensitive and always overreacting.",
        "Coercive control": "If you loved me you would do this. You are not allowed to see your friends without my permission.",
        "Emotional abuse": "You are worthless and pathetic. Nobody else would ever put up with you. You ruin everything.",
        "Narcissistic abuse": "After everything I have done for you, you are so ungrateful. You owe me.",
        "Financial control": "I control the money and you need to ask before spending. You have no money of your own.",
        "Isolation": "Your friends are bad for you. You don't need anyone else. It is me or them.",
        "Threat": "You will regret this. I am warning you. Be careful what you do next.",
        "Compound abuse": "You are imagining things. After everything I have done for you. You will regret this. Your friends are bad for you. I control the money.",
    }

    abuse_sample = st.selectbox(
        "Or load a sample:",
        list(abuse_samples.keys()),
        key='abuse_sample'
    )
    abuse_default = abuse_samples[abuse_sample]

    abuse_input = st.text_area(
        "Enter text to analyze for abuse patterns:",
        value=abuse_default,
        height=150,
        placeholder="Type or paste any text here...",
        key='abuse_input'
    )

    abuse_clicked = st.button("🛡️ Analyze for Abuse", type="primary")

    if abuse_clicked and abuse_input.strip():
        with st.spinner("Analyzing for abuse patterns..."):
            try:
                from reveal.abuse.classifier import classify_abuse
                result = classify_abuse(abuse_input)

                st.session_state['abuse_result'] = result

                # Summary
                st.markdown("### Summary")
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(
                        risk_badge(result['severity']),
                        unsafe_allow_html=True
                    )
                with col2:
                    st.metric("Abuse Score", f"{int(result['score'] * 100)}%")
                with col3:
                    esc = result['escalation']
                    st.metric(
                        "Escalation",
                        esc['escalation_level'] if esc['escalation_detected'] else "None"
                    )

                # Detected categories
                if result['active_categories']:
                    st.markdown("### Detected Categories")
                    cols = st.columns(3)
                    for i, cat in enumerate(result['active_categories']):
                        with cols[i % 3]:
                            matches = result['categories'].get(cat, [])
                            label = cat.replace('_', ' ').title()
                            st.markdown(
                                f'<div class="abuse-box">'
                                f'<strong>{label}</strong><br>'
                                f'{len(matches)} pattern(s) matched'
                                f'</div>',
                                unsafe_allow_html=True
                            )

                # Pattern matches
                st.markdown("### Pattern Matches")
                for cat, matches in result['categories'].items():
                    label = cat.replace('_', ' ').title()
                    with st.expander(f"{label} — {len(matches)} match(es)"):
                        for match in matches:
                            st.markdown(f'• "{match}"')

                # Abuse profiles
                if result['profiles']:
                    st.markdown("### Abuse Profiles Identified")
                    for profile in result['profiles']:
                        amp = " **[AMPLIFIED]**" if profile['amplified'] else ""
                        label = profile['profile'].replace('_', ' ').title()
                        st.markdown(
                            f'<div class="profile-box">'
                            f'<strong>{label}</strong>{amp}<br>'
                            f'{profile["description"]}'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                # Escalation signals
                esc = result['escalation']
                if esc['escalation_detected']:
                    st.markdown(f"### ⚠️ Escalation Signals [{esc['escalation_level']}]")
                    for signal in esc['escalation_signals']:
                        st.markdown(
                            f'<div class="escalation-box">⚠ {signal}</div>',
                            unsafe_allow_html=True
                        )

                # Reasoning
                st.markdown("### Reasoning")
                for i, reason in enumerate(result['reasoning'], 1):
                    st.markdown(
                        f'<div class="reason-box">{i}. {reason}</div>',
                        unsafe_allow_html=True
                    )

                # Flagged sentences
                flagged = [s for s in result['sentence_analysis'] if s['abuse_present']]
                if flagged:
                    st.markdown("### Flagged Sentences")
                    for s in flagged:
                        cats = list(s['categories'].keys())
                        label = ', '.join(c.replace('_', ' ').title() for c in cats)
                        st.markdown(
                            f'<div class="abuse-box">'
                            f'<strong>[{s["severity"]}]</strong> '
                            f'<em>{label}</em><br>'
                            f'"{s["sentence"]}"'
                            f'</div>',
                            unsafe_allow_html=True
                        )

            except Exception as e:
                st.error(f"Abuse analysis error: {e}")

    elif abuse_clicked:
        st.warning("Please enter some text to analyze.")


# ── Tab 3: Full Report ────────────────────────────────────────────────────────

with tab3:
    st.subheader("Full Report")

    if 'result' not in st.session_state:
        st.info("Run an analysis in the Analyze Text tab first.")
    else:
        try:
            from reveal.reasoning.reporter import format_full_report
            report = format_full_report(st.session_state['result'])
            st.code(report, language=None)
        except Exception as e:
            st.error(f"Report error: {e}")


# ── Tab 4: Module Explorer ────────────────────────────────────────────────────

with tab4:
    st.subheader("Module Explorer")
    st.markdown("Detailed breakdown from each analysis module.")

    if 'result' not in st.session_state:
        st.info("Run an analysis in the Analyze Text tab first.")
    else:
        result = st.session_state['result']
        analyses = result['analyses']

        # Sentiment
        with st.expander("😊 Sentiment Analysis", expanded=True):
            sent = analyses.get('sentiment', {})
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Tone", sent.get('tone', 'unknown').upper())
                st.metric("Compound Score", sent.get('compound', 0.0))
                st.metric("Concern Raised", str(sent.get('concern', False)))
            with col2:
                scores = {
                    'Positive': sent.get('pos', 0),
                    'Neutral':  sent.get('neu', 0),
                    'Negative': sent.get('neg', 0)
                }
                st.bar_chart(scores)

        # Voice
        with st.expander("🗣️ Voice Analysis"):
            voice = analyses.get('voice', {})
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Dominant Voice", voice.get('dominant_voice', 'unknown').upper())
                st.metric("Passive Ratio", f"{int(voice.get('passive_ratio', 0) * 100)}%")
                st.metric("Agency Obscured", str(voice.get('agency_obscured', False)))
            with col2:
                counts = {
                    'Active':  voice.get('active_count', 0),
                    'Passive': voice.get('passive_count', 0)
                }
                st.bar_chart(counts)

        # Tone
        with st.expander("🎭 Tone Analysis"):
            tone = analyses.get('tone', {})
            st.metric("Dominant Tone", tone.get('dominant_tone', 'unknown').upper())
            if tone.get('high_risk_tones'):
                st.warning(f"High risk tones: {', '.join(tone['high_risk_tones'])}")
            dist = tone.get('tone_distribution', {})
            if dist:
                st.bar_chart(dist)

        # POV
        with st.expander("👁️ Point of View Analysis"):
            pov = analyses.get('pov', {})
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Dominant POV", pov.get('dominant_pov', 'unknown').upper())
                st.metric("POV Shifts", pov.get('shift_count', 0))
                st.metric("Shift Detected", str(pov.get('shift_detected', False)))
            with col2:
                signals = pov.get('pov_signals', {})
                counts = {
                    'First Person':  signals.get('first_person', {}).get('count', 0),
                    'Second Person': signals.get('second_person', {}).get('count', 0),
                    'Third Person':  signals.get('third_person', {}).get('count', 0)
                }
                st.bar_chart(counts)

        # Entropy
        with st.expander("📊 Entropy Analysis"):
            entropy = analyses.get('entropy', {})
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Char Entropy", entropy.get('char_entropy', 0.0))
                st.metric("Classification", entropy.get('char_classification', 'unknown').upper())
                st.metric("Anomaly Detected", str(entropy.get('anomaly_detected', False)))
            with col2:
                scores = {
                    'Char Entropy': entropy.get('char_entropy', 0.0),
                    'Word Entropy': entropy.get('word_entropy', 0.0)
                }
                st.bar_chart(scores)

        # Anomaly
        with st.expander("🔎 Word Anomaly Detection"):
            anomaly = analyses.get('anomaly', {})
            st.metric("Total Anomalies", anomaly.get('total_anomalies', 0))
            st.metric("Anomaly Detected", str(anomaly.get('anomaly_detected', False)))
            if anomaly.get('capitalization_anomalies'):
                caps = [a['word'] for a in anomaly['capitalization_anomalies']]
                st.write(f"Capitalization anomalies: {', '.join(caps)}")
            if anomaly.get('length_outliers'):
                longs = [a['word'] for a in anomaly['length_outliers']]
                st.write(f"Length outliers: {', '.join(longs)}")

        # Abuse
        with st.expander("🛡️ Abuse Pattern Detection"):
            abuse = analyses.get('abuse', {})
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Abuse Detected", str(abuse.get('abuse_detected', False)))
                st.metric("Severity", abuse.get('severity', 'NONE'))
                st.metric("Score", f"{int(abuse.get('score', 0) * 100)}%")
            with col2:
                if abuse.get('active_categories'):
                    cat_counts = {
                        cat.replace('_', ' ').title(): 1
                        for cat in abuse.get('active_categories', [])
                    }
                    st.bar_chart(cat_counts)

            if abuse.get('profiles'):
                st.write("**Profiles identified:**")
                for p in abuse['profiles']:
                    label = p['profile'].replace('_', ' ').title()
                    amp = " [AMPLIFIED]" if p['amplified'] else ""
                    st.write(f"• {label}{amp}")

            esc = abuse.get('escalation', {})
            if esc.get('escalation_detected'):
                st.error(f"Escalation: {esc['escalation_level']}")
                for signal in esc.get('escalation_signals', []):
                    st.write(f"⚠ {signal}")


# ── Tab 5: Word List Explorer ─────────────────────────────────────────────────

with tab5:
    st.subheader("Word List Explorer")
    st.markdown(
        "Browse the dictionaries that power Reveal's harm detection engine. "
        "These lists are open source and community maintained."
    )

    try:
        dicts = load_dictionaries()
        selected = st.selectbox("Select a dictionary:", list(dicts.keys()))
        data = dicts[selected]

        if 'words' in data:
            st.markdown(f"**{len(data['words'])} entries**")
            search = st.text_input("Search words:", placeholder="Type to filter...")
            words = data['words']
            if search:
                words = [w for w in words if search.lower() in w.lower()]
            st.write(words)

        elif 'categories' in data:
            st.markdown(f"**{len(data['categories'])} categories**")
            for cat, phrases in data['categories'].items():
                with st.expander(f"{cat} ({len(phrases)} phrases)"):
                    st.write(phrases)

        st.markdown("---")
        st.markdown(
            "Want to contribute new words or validate existing ones? "
            "[Open a pull request on GitHub](https://github.com/bbplus3/reveal)"
        )

    except Exception as e:
        st.error(f"Could not load dictionaries: {e}")


# ── Tab 6: About Reveal ───────────────────────────────────────────────────────

with tab6:
    st.subheader("About Reveal")

    st.markdown("""
Reveal is an open-source Python library for intelligent harm detection,
linguistic analysis, and abuse pattern recognition in text.

### What Reveal Detects

**Harm Detection**
- Propaganda and persuasion techniques (22 categories)
- Grooming and predatory language
- Self-harm coded language
- Help signals from victims of abuse or bullying
- Geographic location indicators

**Abuse Detection**
- Gaslighting and reality denial
- Coercive control and ultimatums
- Emotional abuse and degradation
- Narcissistic abuse patterns
- Financial control language
- Isolation tactics
- Threat and intimidation

**Linguistic Analysis**
- Active vs passive voice
- Tone classification (8 categories)
- Point of view and POV shifts

**Cryptanalysis**
- Shannon entropy anomalies
- Unusual n-gram sequences
- Statistically anomalous words

### Install Reveal
```bash
pip install reveal-nlp
```

### Quick Start
```python
from reveal.reasoning.reporter import analyze
result = analyze("Some text to analyze.", fmt='text')
print(result)
```

### Links

- GitHub: https://github.com/bbplus3/reveal
- PyPI: https://pypi.org/project/reveal-nlp/
- API: https://reveal-production-0326.up.railway.app

### License

MIT License — free to use, modify, and distribute.
""")