#!/bin/bash

# Security Check Script - Verify no secrets in Git

echo ""
echo "🔒 Security Check"
echo "================="
echo ""

echo "Checking for sensitive files in Git..."
echo ""

# Check if .env is tracked
if git ls-files | grep -E "^\.env$" > /dev/null; then
    echo "❌ DANGER: .env file is tracked by Git!"
    echo "   Run: git rm --cached .env"
    echo ""
else
    echo "✅ .env file is NOT in Git"
fi

# Check for Firebase JSON files
if git ls-files | grep "firebase.*\.json" > /dev/null; then
    echo "❌ DANGER: Firebase JSON file is tracked by Git!"
    echo "   Run: git rm --cached app/*firebase*.json"
    echo ""
else
    echo "✅ No Firebase JSON files in Git"
fi

# Check .gitignore exists
if [ -f .gitignore ]; then
    echo "✅ .gitignore file exists"
else
    echo "❌ WARNING: .gitignore file missing!"
fi

# Check if .gitignore has .env
if grep -q "\.env" .gitignore; then
    echo "✅ .env is in .gitignore"
else
    echo "❌ WARNING: .env not in .gitignore!"
fi

# Check if .gitignore has firebase pattern
if grep -q "firebase" .gitignore; then
    echo "✅ Firebase files are in .gitignore"
else
    echo "❌ WARNING: Firebase pattern not in .gitignore!"
fi

echo ""
echo "📋 Sensitive files in Git (should be empty):"
git ls-files | grep -E "\.env|firebase|secret|key" || echo "   (none found - good!)"

echo ""
echo "🔍 Untracked files:"
git status --short | grep "^??" || echo "   (none)"

echo ""
echo "✅ Security check complete!"
echo ""
