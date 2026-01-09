#!/bin/bash

echo "🛡️  PLAINVIEW PROTOCOL - ACCOUNTABILITY AUDIT SUITE"
echo "===================================================="
echo "📅 Timestamp: $(date)"
echo ""

cd tests

if [ ! -d "node_modules" ]; then
  echo "📦 Installing audit dependencies..."
  npm install
  npx playwright install chromium
fi

echo ""
echo "🔍 Running Protocol Integrity Audits..."
echo ""

npx playwright test "$@"

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
  echo "✅ ALL AUDITS PASSED. PROTOCOL INTEGRITY VERIFIED."
else
  echo "❌ AUDIT FAILURES DETECTED. CHECK REPORT."
fi

exit $EXIT_CODE
