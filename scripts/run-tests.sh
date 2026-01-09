#!/bin/bash

echo "🛡️  PLAINVIEW PROTOCOL - ACCOUNTABILITY AUDIT SUITE"
echo "===================================================="
echo "📅 Audit Timestamp: $(date)"
echo ""

if [ ! -d "node_modules" ]; then
  echo "📦 Installing Audit dependencies..."
  npm install
  npx playwright install chromium
fi

mkdir -p tests/test-results

echo ""
echo "🔍 Running Security Audit..."
echo "🔍 Running E2E Audit..."
echo "🔍 Running Protocol Integrity Audit..."
echo ""

npx playwright test "$@"

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
  echo "✅ ALL AUDITS PASSED. PROTOCOL INTEGRITY VERIFIED."
  echo "📊 Audit Report: tests/test-results/results.json"
else
  echo "❌ AUDIT FAILURES DETECTED. CHECK REPORT."
  echo "📊 Audit Report: tests/test-results/results.json"
fi

exit $EXIT_CODE
