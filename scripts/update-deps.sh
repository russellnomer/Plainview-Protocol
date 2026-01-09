#!/bin/bash
echo "🛡️  Plainview Protocol - Dependency Update Utility"
echo "==================================================="
echo ""
echo "📦 Updating Playwright browsers..."
npx playwright install --with-deps chromium
echo ""
echo "✅ Playwright browsers updated successfully!"
echo "🔍 Run 'npx playwright test --project=chromium' to verify"
