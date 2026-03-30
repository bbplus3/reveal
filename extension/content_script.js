/**
 * content_script.js
 *
 * Reveal Analyzer - Content Script
 * Runs inside social media pages, extracts post text,
 * sends to Reveal API, and injects risk indicators.
 */

const REVEAL_API = 'https://reveal-production-0326.up.railway.app';

// ── Platform selectors ────────────────────────────────────────────────────────
// CSS selectors for finding post text on each platform.
// These may need updating if platforms change their HTML structure.

const SELECTORS = {
    'twitter.com':    '[data-testid="tweetText"]',
    'x.com':          '[data-testid="tweetText"]',
    'reddit.com':     '[data-testid="post-content"], .RichTextJSON-root, .md, [slot="text-body"]',
    'facebook.com':   '[data-ad-comet-preview="message"], [dir="auto"]',
    'instagram.com':  '._a9zs, .C4VMK span',
    'tiktok.com':     '.tiktok-1ejylhp-DivContainer, [class*="desc"]',
    'linkedin.com':   '.feed-shared-update-v2__description, .share-native-scene',
    'threads.net':    '[data-pressable-container] span'
};


// ── Risk colors ───────────────────────────────────────────────────────────────

const RISK_COLORS = {
    'NONE':     null,
    'LOW':      '#fff8e1',
    'MEDIUM':   '#fff3e0',
    'HIGH':     '#fce4ec',
    'CRITICAL': '#ffcdd2'
};

const RISK_BORDER = {
    'NONE':     null,
    'LOW':      '#f9a825',
    'MEDIUM':   '#e65100',
    'HIGH':     '#c62828',
    'CRITICAL': '#b71c1c'
};


// ── State ─────────────────────────────────────────────────────────────────────

const scannedPosts  = new Map(); // postText -> result
const pendingPosts  = new Set(); // posts currently being scanned
let   serverOnline  = false;
let   scanEnabled   = true;
let   scanCount     = 0;
let   flagCount     = 0;


// ── Utility functions ─────────────────────────────────────────────────────────

function getCurrentSelector() {
    const host = window.location.hostname.replace('www.', '');
    for (const [domain, selector] of Object.entries(SELECTORS)) {
        if (host.includes(domain)) {
            return selector;
        }
    }
    return null;
}

function cleanText(text) {
    return text.replace(/\s+/g, ' ').trim();
}

function generatePostId(element) {
    const text = element.textContent.slice(0, 50);
    return btoa(encodeURIComponent(text)).slice(0, 20);
}


// ── Server check ──────────────────────────────────────────────────────────────

async function checkServer() {
    try {
        const response = await fetch(`${REVEAL_API}/health`, {
            method: 'GET',
            signal: AbortSignal.timeout(2000)
        });
        serverOnline = response.ok;
    } catch {
        serverOnline = false;
    }
    return serverOnline;
}


// ── API call ──────────────────────────────────────────────────────────────────

async function quickScan(text) {
    try {
        const response = await fetch(`${REVEAL_API}/quick`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text}),
            signal: AbortSignal.timeout(5000)
        });
        if (response.ok) {
            return await response.json();
        }
    } catch {
        return null;
    }
    return null;
}

async function fullAnalysis(text) {
    try {
        const response = await fetch(`${REVEAL_API}/analyze`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text}),
            signal: AbortSignal.timeout(10000)
        });
        if (response.ok) {
            return await response.json();
        }
    } catch {
        return null;
    }
    return null;
}


// ── Visual indicators ─────────────────────────────────────────────────────────

function injectIndicator(element, result) {
    const risk = result.risk_level;

    if (risk === 'NONE') return;

    // Find the post container to highlight
    const container = element.closest('article') ||
                      element.closest('[data-testid]') ||
                      element.parentElement;

    if (!container) return;

    // Avoid double-injecting
    if (container.querySelector('.reveal-indicator')) return;

    // Apply background highlight
    const bgColor     = RISK_COLORS[risk];
    const borderColor = RISK_BORDER[risk];

    if (bgColor) {
        container.style.backgroundColor = bgColor;
        container.style.borderLeft = `4px solid ${borderColor}`;
        container.style.transition = 'all 0.3s ease';
    }

    // Create indicator badge
    const badge = document.createElement('div');
    badge.className = 'reveal-indicator';
    badge.setAttribute('data-risk', risk);
    badge.setAttribute('data-signals', (result.active_signals || []).join(', '));
    badge.setAttribute('data-sentiment', result.sentiment_tone || '');

    const signals = (result.active_signals || [])
        .map(s => s.replace(/_/g, ' ').replace(' detected', ''))
        .join(', ');

    badge.innerHTML = `
        <span class="reveal-icon">🔍</span>
        <span class="reveal-risk">${risk}</span>
        ${signals ? `<span class="reveal-signals">${signals}</span>` : ''}
    `;

    // Add click handler for full analysis
    badge.addEventListener('click', async (e) => {
        e.stopPropagation();
        const text = cleanText(element.textContent);
        badge.innerHTML = '<span class="reveal-icon">⏳</span> Analyzing...';
        const full = await fullAnalysis(text);
        if (full) {
            showDetailPanel(full, badge);
        }
    });

    container.style.position = 'relative';
    container.appendChild(badge);

    flagCount++;
    updateBadgeCount();
}


// ── Detail panel ──────────────────────────────────────────────────────────────

function showDetailPanel(result, anchor) {
    // Remove any existing panel
    const existing = document.querySelector('.reveal-detail-panel');
    if (existing) existing.remove();

    const panel = document.createElement('div');
    panel.className = 'reveal-detail-panel';

    const reasoning = (result.reasoning || [])
        .map(r => `<li>${r}</li>`)
        .join('');

    const signals = (result.active_signals || [])
        .map(s => `<span class="reveal-signal-tag">${s.replace(/_/g, ' ')}</span>`)
        .join('');

    panel.innerHTML = `
        <div class="reveal-panel-header">
            <span>🔍 Reveal Analysis</span>
            <button class="reveal-close">✕</button>
        </div>
        <div class="reveal-panel-body">
            <div class="reveal-panel-risk reveal-panel-risk-${result.risk_level}">
                Risk Level: ${result.risk_level} 
                (${Math.round(result.normalized_score * 100)}%)
            </div>
            <div class="reveal-panel-section">
                <strong>Sentiment:</strong> 
                ${result.sentiment?.tone || 'unknown'} 
                (${result.sentiment?.compound || 0})
            </div>
            ${signals ? `
            <div class="reveal-panel-section">
                <strong>Signals:</strong><br>${signals}
            </div>` : ''}
            ${reasoning ? `
            <div class="reveal-panel-section">
                <strong>Reasoning:</strong>
                <ul class="reveal-reasoning">${reasoning}</ul>
            </div>` : ''}
        </div>
    `;

    panel.querySelector('.reveal-close').addEventListener('click', () => {
        panel.remove();
    });

    document.body.appendChild(panel);
}


// ── Badge count ───────────────────────────────────────────────────────────────

function updateBadgeCount() {
    chrome.runtime.sendMessage({
        type:      'UPDATE_COUNTS',
        scanCount: scanCount,
        flagCount: flagCount
    });
}


// ── Main scanner ──────────────────────────────────────────────────────────────

async function scanPosts() {
    if (!scanEnabled || !serverOnline) return;

    const selector = getCurrentSelector();
    if (!selector) return;

    const elements = document.querySelectorAll(selector);

    for (const element of elements) {
        const text = cleanText(element.textContent);

        if (!text || text.length < 20) continue;
        if (scannedPosts.has(text)) continue;
        if (pendingPosts.has(text)) continue;

        pendingPosts.add(text);

        const result = await quickScan(text);

        if (result) {
            scannedPosts.set(text, result);
            scanCount++;
            injectIndicator(element, result);
        }

        pendingPosts.delete(text);

        // Small delay between posts to avoid hammering the API
        await new Promise(resolve => setTimeout(resolve, 200));
    }

    updateBadgeCount();
}


// ── Message handler ───────────────────────────────────────────────────────────

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'GET_STATUS') {
        sendResponse({
            serverOnline: serverOnline,
            scanEnabled:  scanEnabled,
            scanCount:    scanCount,
            flagCount:    flagCount,
            url:          window.location.href
        });
    }

    if (message.type === 'TOGGLE_SCAN') {
        scanEnabled = message.enabled;
        sendResponse({scanEnabled});
    }

    if (message.type === 'CLEAR_INDICATORS') {
        document.querySelectorAll('.reveal-indicator').forEach(el => el.remove());
        document.querySelectorAll('[style*="reveal"]').forEach(el => {
            el.style.backgroundColor = '';
            el.style.borderLeft = '';
        });
        scannedPosts.clear();
        scanCount = 0;
        flagCount = 0;
        updateBadgeCount();
        sendResponse({cleared: true});
    }

    return true;
});


// ── Observer for dynamic content ──────────────────────────────────────────────
// Social media feeds load content dynamically as you scroll.
// This watches for new content and scans it automatically.

const observer = new MutationObserver(() => {
    if (scanEnabled && serverOnline) {
        clearTimeout(window._revealScanTimer);
        window._revealScanTimer = setTimeout(scanPosts, 800);
    }
});


// ── Initializer ───────────────────────────────────────────────────────────────

async function initialize() {
    const online = await checkServer();

    if (online) {
        observer.observe(document.body, {
            childList: true,
            subtree:   true
        });
        await scanPosts();
    }

    // Recheck server every 30 seconds
    setInterval(async () => {
        await checkServer();
    }, 30000);
}

initialize();