"""
server.py

Reveal API Server
A lightweight Flask API that wraps the Reveal library
and makes it accessible to the browser extension.

Run with: python server.py
Listens on: http://localhost:5000
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

sys.path.insert(0, '.')

from reveal.reasoning.scorer import score
from reveal.harm.detector import analyze as harm_detect
from reveal.harm.sentiment import analyze_sentiment

app = Flask(__name__)
CORS(app, 
     resources={r"/*": {"origins": "*"}},
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"]
)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Private-Network'] = 'true'
    return response

# ── Health check ──────────────────────────────────────────────────────────────

@app.route('/health', methods=['GET'])
def health():
    """
    Simple health check endpoint.
    The extension calls this to verify Reveal is running.
    """
    return jsonify({
        'status': 'ok',
        'library': 'reveal-nlp',
        'version': '0.1.0'
    })

@app.route('/test', methods=['GET', 'POST'])
def test_route():
    return jsonify({'test': 'ok'})

# ── Full analysis endpoint ────────────────────────────────────────────────────

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Full analysis endpoint.
    Accepts a JSON body with a 'text' field.
    Returns the complete Reveal score report.

    Request:
        POST /analyze
        Content-Type: application/json
        {"text": "Text to analyze here"}

    Response:
        {
            "risk_level": "HIGH",
            "normalized_score": 0.45,
            "raw_score": 67,
            "confidence": "high",
            "signals": {...},
            "reasoning": [...],
            "sentiment": {...}
        }
    """
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text'].strip()

    if not text:
        return jsonify({'error': 'Empty text provided'}), 400

    if len(text) > 10000:
        text = text[:10000]

    try:
        result = score(text)

        # Return a clean subset for the extension
        return jsonify({
            'risk_level':       result['risk_level'],
            'normalized_score': result['normalized_score'],
            'raw_score':        result['raw_score'],
            'confidence':       result['confidence'],
            'signals':          result['signals'],
            'reasoning':        result['reasoning'],
            'sentiment':        result['analyses']['sentiment'],
            'active_signals':   [k for k, v in result['signals'].items() if v]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Quick scan endpoint ───────────────────────────────────────────────────────

@app.route('/quick', methods=['POST'])
def quick_scan():
    """
    Lightweight quick scan endpoint.
    Runs only harm detection and sentiment -- much faster
    than the full analysis. Used for real-time page scanning
    where speed matters more than depth.

    Request:
        POST /quick
        Content-Type: application/json
        {"text": "Text to analyze here"}

    Response:
        {
            "risk_level": "LOW",
            "flags": {...},
            "sentiment_tone": "neutral",
            "concern": false
        }
    """
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text'].strip()

    if not text:
        return jsonify({'error': 'Empty text provided'}), 400

    if len(text) > 10000:
        text = text[:10000]

    try:
        harm    = harm_detect(text)
        sent    = analyze_sentiment(text)

        # Quick risk level based on harm flags and sentiment only
        flags = harm['flags']
        active = [k for k, v in flags.items() if v]

        if flags['grooming_detected'] or flags['self_harm_detected']:
            risk = 'CRITICAL'
        elif flags['help_signal_detected'] and sent['tone'] == 'distressed':
            risk = 'HIGH'
        elif flags['help_signal_detected']:
            risk = 'MEDIUM'
        elif len(active) >= 2:
            risk = 'MEDIUM'
        elif len(active) == 1:
            risk = 'LOW'
        else:
            risk = 'NONE'

        return jsonify({
            'risk_level':     risk,
            'flags':          flags,
            'active_signals': active,
            'sentiment_tone': sent['tone'],
            'sentiment_score': sent['compound'],
            'concern':        sent['concern']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Batch scan endpoint ───────────────────────────────────────────────────────

@app.route('/batch', methods=['POST'])
def batch_scan():
    """
    Batch scan endpoint.
    Accepts multiple texts at once and quick scans each.
    Used when the extension finds multiple posts on a page.

    Request:
        POST /batch
        Content-Type: application/json
        {"texts": [{"id": "post_1", "text": "..."}, ...]}

    Response:
        {"results": [{"id": "post_1", "risk_level": "LOW", ...}, ...]}
    """
    data = request.get_json()

    if not data or 'texts' not in data:
        return jsonify({'error': 'No texts provided'}), 400

    texts = data['texts']

    if not isinstance(texts, list):
        return jsonify({'error': 'texts must be a list'}), 400

    if len(texts) > 50:
        texts = texts[:50]

    results = []

    for item in texts:
        if not isinstance(item, dict) or 'text' not in item:
            continue

        text = item['text'].strip()
        post_id = item.get('id', 'unknown')

        if not text:
            continue

        try:
            harm = harm_detect(text)
            sent = analyze_sentiment(text)
            flags = harm['flags']
            active = [k for k, v in flags.items() if v]

            if flags['grooming_detected'] or flags['self_harm_detected']:
                risk = 'CRITICAL'
            elif flags['help_signal_detected'] and sent['tone'] == 'distressed':
                risk = 'HIGH'
            elif flags['help_signal_detected']:
                risk = 'MEDIUM'
            elif len(active) >= 2:
                risk = 'MEDIUM'
            elif len(active) == 1:
                risk = 'LOW'
            else:
                risk = 'NONE'

            results.append({
                'id':             post_id,
                'risk_level':     risk,
                'active_signals': active,
                'sentiment_tone': sent['tone'],
                'concern':        sent['concern']
            })

        except Exception as e:
            results.append({
                'id':    post_id,
                'error': str(e)
            })

    return jsonify({'results': results})

# ── Abuse detection endpoint ──────────────────────────────────────────────────

@app.route('/abuse', methods=['POST'])
def abuse_scan():
    """
    Full abuse detection endpoint.
    Runs the complete abuse classification pipeline including
    category detection, profile matching, and escalation analysis.

    Request:
        POST /abuse
        Content-Type: application/json
        {"text": "Text to analyze here"}

    Response:
        {
            "abuse_detected": true,
            "severity": "CRITICAL",
            "score": 0.69,
            "active_categories": ["gaslighting", "threat"],
            "profiles": [...],
            "escalation": {...},
            "reasoning": [...],
            "most_severe_sentence": {...}
        }
    """
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text'].strip()

    if not text:
        return jsonify({'error': 'Empty text provided'}), 400

    if len(text) > 10000:
        text = text[:10000]

    try:
        from reveal.abuse.classifier import classify_abuse
        result = classify_abuse(text)

        return jsonify({
            'abuse_detected':    result['abuse_detected'],
            'severity':          result['severity'],
            'score':             result['score'],
            'active_categories': result['active_categories'],
            'profiles': [
                {
                    'profile':     p['profile'],
                    'description': p['description'],
                    'amplified':   p['amplified']
                }
                for p in result['profiles']
            ],
            'escalation': {
                'escalation_detected': result['escalation']['escalation_detected'],
                'escalation_level':    result['escalation']['escalation_level'],
                'escalation_signals':  result['escalation']['escalation_signals']
            },
            'reasoning':            result['reasoning'],
            'most_severe_sentence': result['most_severe_sentence']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Abuse quick scan endpoint ─────────────────────────────────────────────────

@app.route('/abuse/quick', methods=['POST'])
def abuse_quick():
    """
    Lightweight abuse quick scan.
    Returns only the key flags without full profile analysis.
    Faster than /abuse for real-time scanning.

    Request:
        POST /abuse/quick
        Content-Type: application/json
        {"text": "Text to analyze here"}

    Response:
        {
            "abuse_detected": true,
            "severity": "HIGH",
            "active_categories": ["gaslighting", "threat"],
            "escalation_detected": true,
            "escalation_level": "HIGH"
        }
    """
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text'].strip()

    if not text:
        return jsonify({'error': 'Empty text provided'}), 400

    if len(text) > 10000:
        text = text[:10000]

    try:
        from reveal.abuse.detector import analyze_abuse
        result = analyze_abuse(text)

        return jsonify({
            'abuse_detected':    result['abuse_detected'],
            'severity':          result['severity'],
            'score':             result['score'],
            'active_categories': result['active_categories'],
            'escalation_detected': result['escalation']['escalation_detected'] if 'escalation' in result else False,
            'escalation_level':    result['escalation']['escalation_level'] if 'escalation' in result else 'NONE'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── Run server ────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Reveal API Server on port {port}...")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )