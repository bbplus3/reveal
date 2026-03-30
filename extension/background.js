/**
 * background.js
 *
 * Reveal Analyzer - Background Service Worker
 * Coordinates communication between content scripts
 * and manages extension state across tabs.
 */

const REVEAL_API = 'https://reveal-production-0326.up.railway.app';


// ── State ─────────────────────────────────────────────────────────────────────

let globalStats = {
    totalScanned: 0,
    totalFlagged: 0,
    serverOnline: false,
    tabStats:     {}
};


// ── Server health check ───────────────────────────────────────────────────────

async function checkServer() {
    try {
        const response = await fetch(`${REVEAL_API}/health`, {
            signal: AbortSignal.timeout(3000)
        });
        globalStats.serverOnline = response.ok;
    } catch {
        globalStats.serverOnline = false;
    }

    // Update all tab icons based on server status
    updateAllIcons();
    return globalStats.serverOnline;
}


// ── Icon updater ──────────────────────────────────────────────────────────────

function updateAllIcons() {
    chrome.tabs.query({}, (tabs) => {
        tabs.forEach(tab => {
            updateTabIcon(tab.id);
        });
    });
}

function updateTabIcon(tabId) {
    const stats = globalStats.tabStats[tabId] || {};
    const flagCount = stats.flagCount || 0;

    // Set badge text to number of flagged posts
    chrome.action.setBadgeText({
        tabId: tabId,
        text:  flagCount > 0 ? String(flagCount) : ''
    });

    // Badge color based on highest risk found
    const highestRisk = stats.highestRisk || 'NONE';
    const badgeColor = {
        'NONE':     '#4caf50',
        'LOW':      '#ff9800',
        'MEDIUM':   '#ff5722',
        'HIGH':     '#f44336',
        'CRITICAL': '#b71c1c'
    }[highestRisk] || '#4caf50';

    chrome.action.setBadgeBackgroundColor({
        tabId:  tabId,
        color:  badgeColor
    });
}


// ── Message handler ───────────────────────────────────────────────────────────

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    const tabId = sender.tab?.id;

    // Content script reporting scan counts
    if (message.type === 'UPDATE_COUNTS') {
        if (tabId) {
            if (!globalStats.tabStats[tabId]) {
                globalStats.tabStats[tabId] = {
                    scanCount:   0,
                    flagCount:   0,
                    highestRisk: 'NONE'
                };
            }

            globalStats.tabStats[tabId].scanCount = message.scanCount || 0;
            globalStats.tabStats[tabId].flagCount  = message.flagCount || 0;

            globalStats.totalScanned = Object.values(globalStats.tabStats)
                .reduce((sum, t) => sum + (t.scanCount || 0), 0);
            globalStats.totalFlagged = Object.values(globalStats.tabStats)
                .reduce((sum, t) => sum + (t.flagCount || 0), 0);

            updateTabIcon(tabId);
        }
        sendResponse({ok: true});
    }

    // Popup requesting global stats
    if (message.type === 'GET_GLOBAL_STATS') {
        sendResponse({
            stats:       globalStats,
            serverOnline: globalStats.serverOnline
        });
    }

    // Popup requesting status of current tab
    if (message.type === 'GET_TAB_STATS') {
        chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
            const activeTab = tabs[0];
            if (activeTab) {
                const stats = globalStats.tabStats[activeTab.id] || {
                    scanCount:   0,
                    flagCount:   0,
                    highestRisk: 'NONE'
                };
                sendResponse({
                    tabId:       activeTab.id,
                    url:         activeTab.url,
                    stats:       stats,
                    serverOnline: globalStats.serverOnline
                });
            }
        });
        return true;
    }

    // Popup toggling scan on/off
    if (message.type === 'TOGGLE_SCAN') {
        chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
            const activeTab = tabs[0];
            if (activeTab) {
                chrome.tabs.sendMessage(activeTab.id, {
                    type:    'TOGGLE_SCAN',
                    enabled: message.enabled
                });
            }
        });
        sendResponse({ok: true});
    }

    // Popup requesting clear
    if (message.type === 'CLEAR_TAB') {
        chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
            const activeTab = tabs[0];
            if (activeTab) {
                chrome.tabs.sendMessage(activeTab.id, {
                    type: 'CLEAR_INDICATORS'
                });
                globalStats.tabStats[activeTab.id] = {
                    scanCount:   0,
                    flagCount:   0,
                    highestRisk: 'NONE'
                };
                updateTabIcon(activeTab.id);
            }
        });
        sendResponse({ok: true});
    }

    return true;
});


// ── Tab cleanup ───────────────────────────────────────────────────────────────

chrome.tabs.onRemoved.addListener((tabId) => {
    delete globalStats.tabStats[tabId];
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo) => {
    if (changeInfo.status === 'loading') {
        globalStats.tabStats[tabId] = {
            scanCount:   0,
            flagCount:   0,
            highestRisk: 'NONE'
        };
        updateTabIcon(tabId);
    }
});


// ── Startup ───────────────────────────────────────────────────────────────────

checkServer();

// Check server health every 30 seconds
setInterval(checkServer, 30000);