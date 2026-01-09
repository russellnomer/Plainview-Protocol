const RESULTS_PATH = '../tests/test-results/results.json';
const HISTORY_PATH = 'history.json';

let trendChart = null;

async function fetchResults() {
    try {
        const response = await fetch(RESULTS_PATH);
        if (!response.ok) throw new Error('Results not found');
        return await response.json();
    } catch (error) {
        console.warn('Could not fetch results:', error);
        return null;
    }
}

async function fetchHistory() {
    try {
        const response = await fetch(HISTORY_PATH);
        if (!response.ok) throw new Error('History not found');
        return await response.json();
    } catch (error) {
        console.warn('Could not fetch history:', error);
        return { runs: [] };
    }
}

function updateStatusIndicator(passed, failed) {
    const indicator = document.getElementById('statusIndicator');
    const statusText = document.getElementById('statusText');
    const statusSubtext = document.getElementById('statusSubtext');
    
    if (failed === 0) {
        indicator.innerHTML = `
            <div class="w-16 h-16 rounded-full bg-green-500 pulse-green"></div>
        `;
        indicator.className = 'inline-flex items-center justify-center w-24 h-24 rounded-full bg-green-500/20';
        statusText.textContent = 'OPERATIONAL';
        statusText.className = 'text-2xl font-bold text-green-400';
        statusSubtext.textContent = `All ${passed} audits passed. Protocol integrity verified.`;
    } else {
        indicator.innerHTML = `
            <div class="w-16 h-16 rounded-full bg-red-500 pulse-red"></div>
        `;
        indicator.className = 'inline-flex items-center justify-center w-24 h-24 rounded-full bg-red-500/20';
        statusText.textContent = 'INTEGRITY CHECK FAILED';
        statusText.className = 'text-2xl font-bold text-red-400';
        statusSubtext.textContent = `${failed} of ${passed + failed} audits require attention.`;
    }
}

function updateMetrics(results) {
    const stats = results.stats || {};
    const expected = stats.expected || 0;
    const unexpected = stats.unexpected || 0;
    const skipped = stats.skipped || 0;
    
    const passed = expected;
    const failed = unexpected;
    const total = passed + failed + skipped;
    const duration = stats.duration || 0;
    
    document.getElementById('totalTests').textContent = total;
    
    const successRate = total > 0 ? Math.round((passed / total) * 100) : 0;
    const successRateEl = document.getElementById('successRate');
    successRateEl.textContent = `${successRate}%`;
    successRateEl.className = `text-4xl font-bold ${successRate === 100 ? 'text-green-400' : successRate >= 80 ? 'text-yellow-400' : 'text-red-400'}`;
    
    const durationSec = (duration / 1000).toFixed(1);
    document.getElementById('buildDuration').textContent = `${durationSec}s`;
    
    return { passed, failed, total, duration, successRate };
}

function updateTimestamp(results) {
    const startTime = results.stats?.startTime;
    const timestampEl = document.getElementById('lastAuditTimestamp');
    
    if (startTime) {
        const date = new Date(startTime);
        timestampEl.textContent = date.toLocaleString('en-US', {
            weekday: 'short',
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            timeZoneName: 'short'
        });
    } else {
        timestampEl.textContent = 'Unknown';
    }
}

function renderTestLedger(results) {
    const ledger = document.getElementById('testLedger');
    const suites = results.suites || [];
    
    if (suites.length === 0) {
        ledger.innerHTML = '<p class="text-gray-500">No test results available.</p>';
        return;
    }
    
    let html = '';
    
    function processSpecs(specs, suiteName) {
        specs.forEach(spec => {
            const testResults = spec.tests || [];
            testResults.forEach(test => {
                const status = test.status;
                const statusIcon = status === 'passed' ? '✅' : status === 'failed' ? '❌' : '⏭️';
                const statusColor = status === 'passed' ? 'text-green-400' : status === 'failed' ? 'text-red-400' : 'text-gray-400';
                const duration = test.results?.[0]?.duration || 0;
                
                html += `
                    <div class="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg">
                        <div class="flex items-center gap-3">
                            <span class="${statusColor}">${statusIcon}</span>
                            <div>
                                <p class="font-medium">${spec.title}</p>
                                <p class="text-sm text-gray-400">${suiteName}</p>
                            </div>
                        </div>
                        <span class="text-sm text-gray-400">${(duration / 1000).toFixed(2)}s</span>
                    </div>
                `;
            });
        });
    }
    
    function processSuite(suite) {
        if (suite.specs) {
            processSpecs(suite.specs, suite.title);
        }
        if (suite.suites) {
            suite.suites.forEach(processSuite);
        }
    }
    
    suites.forEach(processSuite);
    
    ledger.innerHTML = html || '<p class="text-gray-500">No test results available.</p>';
}

function renderTrendChart(history) {
    const ctx = document.getElementById('trendChart').getContext('2d');
    const runs = history.runs || [];
    
    const last30 = runs.slice(-30);
    
    const labels = last30.map(run => {
        const date = new Date(run.timestamp);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });
    
    const successRates = last30.map(run => run.successRate || 0);
    
    if (trendChart) {
        trendChart.destroy();
    }
    
    trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels.length ? labels : ['No Data'],
            datasets: [{
                label: 'Success Rate %',
                data: successRates.length ? successRates : [0],
                borderColor: '#22c55e',
                backgroundColor: 'rgba(34, 197, 94, 0.1)',
                fill: true,
                tension: 0.3,
                pointRadius: 4,
                pointBackgroundColor: '#22c55e'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    min: 0,
                    max: 100,
                    ticks: {
                        callback: value => value + '%',
                        color: '#94a3b8'
                    },
                    grid: {
                        color: 'rgba(148, 163, 184, 0.1)'
                    }
                },
                x: {
                    ticks: {
                        color: '#94a3b8'
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

async function init() {
    const results = await fetchResults();
    const history = await fetchHistory();
    
    if (results) {
        const metrics = updateMetrics(results);
        updateStatusIndicator(metrics.passed, metrics.failed);
        updateTimestamp(results);
        renderTestLedger(results);
    } else {
        document.getElementById('statusText').textContent = 'NO DATA';
        document.getElementById('statusSubtext').textContent = 'Run tests to generate results.';
    }
    
    renderTrendChart(history);
}

document.addEventListener('DOMContentLoaded', init);

if (typeof module !== 'undefined') {
    module.exports = { fetchResults, fetchHistory, updateMetrics };
}
