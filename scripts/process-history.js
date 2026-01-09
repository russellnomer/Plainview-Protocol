#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const RESULTS_PATH = path.join(__dirname, '..', 'tests', 'test-results', 'results.json');
const HISTORY_PATH = path.join(__dirname, '..', 'dashboard', 'history.json');
const MAX_ENTRIES = 30;

function loadResults() {
    try {
        const data = fs.readFileSync(RESULTS_PATH, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error('Error loading results:', error.message);
        return null;
    }
}

function loadHistory() {
    try {
        if (fs.existsSync(HISTORY_PATH)) {
            const data = fs.readFileSync(HISTORY_PATH, 'utf8');
            return JSON.parse(data);
        }
    } catch (error) {
        console.warn('Could not load history, starting fresh:', error.message);
    }
    return { runs: [] };
}

function saveHistory(history) {
    const dir = path.dirname(HISTORY_PATH);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(HISTORY_PATH, JSON.stringify(history, null, 2));
}

function extractMetrics(results) {
    const stats = results.stats || {};
    const expected = stats.expected || 0;
    const unexpected = stats.unexpected || 0;
    const skipped = stats.skipped || 0;
    
    const passed = expected;
    const failed = unexpected;
    const total = passed + failed + skipped;
    const duration = stats.duration || 0;
    const startTime = stats.startTime || new Date().toISOString();
    
    const successRate = total > 0 ? Math.round((passed / total) * 100) : 0;
    
    return {
        timestamp: startTime,
        total,
        passed,
        failed,
        duration,
        successRate,
        status: failed === 0 ? 'OPERATIONAL' : 'INTEGRITY_CHECK_FAILED'
    };
}

function processHistory() {
    console.log('🔍 Processing test history...');
    
    const results = loadResults();
    if (!results) {
        console.error('❌ No results.json found. Run tests first.');
        process.exit(1);
    }
    
    const history = loadHistory();
    const metrics = extractMetrics(results);
    
    const lastRun = history.runs[history.runs.length - 1];
    if (lastRun && lastRun.timestamp === metrics.timestamp) {
        console.log('⏭️  Results already processed. Skipping.');
        return;
    }
    
    history.runs.push(metrics);
    
    if (history.runs.length > MAX_ENTRIES) {
        history.runs = history.runs.slice(-MAX_ENTRIES);
    }
    
    saveHistory(history);
    
    console.log('✅ History updated successfully!');
    console.log(`   📊 Total runs tracked: ${history.runs.length}`);
    console.log(`   📈 Latest: ${metrics.successRate}% success rate (${metrics.passed}/${metrics.total})`);
    console.log(`   🕐 Timestamp: ${metrics.timestamp}`);
}

if (require.main === module) {
    processHistory();
}

module.exports = { processHistory, extractMetrics };
