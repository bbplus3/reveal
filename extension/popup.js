/**
 * popup.js
 *
 * Reveal Analyzer - Popup Script
 * Handles the popup UI logic and communicates
 * with the background service worker.
 */

// ── Supported platforms ───────────────────────────────────────────────────────

const SUPPORTED_DOMAINS = [
    'twitter.com', 'x.com', 'reddit.com', 'facebook.com',
    'instagram.com', 'tiktok.com', 'linkedin.com', 'threads.net'
];

function isSupportedUrl(url) {
    if (!url) return false;
    try {
        const hostname = new URL(url).hostname.replace('www.', '');
        return SUPPORTED_DOMAINS.some(d => hostname.includes(d));
    } catch {
        return false;
    }
}


// ── Risk label helpers ────────────────────────────────────────────────────────

const RISK_LABELS = {
    'NONE':     'No signals detected',
    'LOW':      'Low risk signals detected',
    'MEDIUM':   'Medium risk signals detected',
    'HIGH':     'High risk signals detected',
    'CRITICAL': 'CRITICAL signals detected'
};

function getRiskLabel(risk, flagCount) {
    if (flagCount === 0) return 'No signals detected';
    return RISK_LABELS[risk] || 'Unknown risk level';
}

function getHighestRisk(flagCount) {
    if (flagCount === 0) return 'NONE';
    // We rely on background to track highest risk
    // For now derive from flag count as approximation
    if (flagCount >= 5) return 'HIGH';
    if (flagCount >= 3) return 'MEDIUM';
    if (flagCount >= 1) return 'LOW';
    return 'NONE';
}


// ── UI updaters ───────────────────────────────────────────────────────────────

function updateServerStatus(online) {
    const dot  = document.getElementById('statusDot');
    const text = document.getElementById('statusText');
    const msg  = document.getElementById('serverOfflineMsg');

    if (online) {
        dot.classList.add('online');
        text.textContent = 'Server online';
        msg.style.display = 'none';
    } else {
        dot.classList.remove('online');
        text.textContent = 'Server offline';
        msg.style.display = 'block';
    }
}

function updateStats(scanCount, flagCount) {
    document.getElementById('scanCount').textContent = scanCount || 0;
    document.getElementById('flagCount').textContent = flagCount || 0;
}

function updateRiskBanner(flagCount) {
    const banner = document.getElementById('riskBanner');
    const risk   = getHighestRisk(flagCount);
    const label  = getRiskLabel(risk, flagCount);

    // Remove all risk classes
    banner.className = 'risk-banner';
    banner.classList.add(`risk-${risk}`);
    banner.textContent = label;
}

function showMainContent(show) {
    document.getElementById('mainContent').style.display = show ? 'block' : 'none';
    document.getElementById('notSupported').style.display = show ? 'none' : 'block';
}


// ── Initialize popup ──────────────────────────────────────────────────────────

async function initialize() {
    // Get tab stats from background
    chrome.runtime.sendMessage(
        {type: 'GET_TAB_STATS'},
        (response) => {
            if (!response) return;

            const {url, stats, serverOnline} = response;

            updateServerStatus(serverOnline);

            const supported = isSupportedUrl(url);
            showMainContent(supported);

            if (supported && stats) {
                updateStats(stats.scanCount, stats.flagCount);
                updateRiskBanner(stats.flagCount);
            }
        }
    );
}


// ── Event listeners ───────────────────────────────────────────────────────────

document.getElementById('scanToggle').addEventListener('change', (e) => {
    chrome.runtime.sendMessage({
        type:    'TOGGLE_SCAN',
        enabled: e.target.checked
    });
});

document.getElementById('clearBtn').addEventListener('click', () => {
    chrome.runtime.sendMessage({type: 'CLEAR_TAB'}, () => {
        updateStats(0, 0);
        updateRiskBanner(0);
    });
});


// ── Run ───────────────────────────────────────────────────────────────────────

initialize();

// Refresh stats every 2 seconds while popup is open
setInterval(initialize, 2000);