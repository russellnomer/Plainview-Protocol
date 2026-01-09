#!/bin/bash
echo "🛡️  Plainview Protocol - Accountability Report Generator"
echo "========================================================="

echo ""
echo "📊 Step 1: Running full audit suite..."
npx playwright test --project=chromium

echo ""
echo "📝 Step 2: Processing test history..."
node scripts/process-history.js

echo ""
echo "🌐 Step 3: Launching Accountability Dashboard..."
echo "   Dashboard URL: http://localhost:3000"
echo "   Press Ctrl+C to stop"
echo ""

python scripts/serve-dashboard.py
