#!/bin/bash
set -e

echo '🛡️  PLAINVIEW PROTOCOL - CITIZEN AUDIT CAPSULE'
echo '================================================'
echo ''
echo '📊 Running full accountability audit...'
echo ''

npx playwright test --project=chromium --reporter=list

echo ''
echo '📝 Processing audit history...'
node scripts/process-history.js

echo ''
echo '✅ Audit complete. Results saved to test-results/'
echo '🔍 View dashboard/index.html for visual report'
