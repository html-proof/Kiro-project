#!/bin/bash

# Git Push Script

echo ""
echo "🚀 Git Push to GitHub"
echo "====================="
echo ""

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed!"
    echo ""
    echo "Install Git:"
    echo "  - Ubuntu: sudo apt install git"
    echo "  - macOS: brew install git"
    echo ""
    exit 1
fi

echo "✅ Git is installed"
echo ""

# Check if .env exists and warn
if [ -f .env ]; then
    echo "⚠️  WARNING: .env file detected"
    echo "   This file contains secrets and should NOT be pushed to GitHub"
    echo "   It is protected by .gitignore"
    echo ""
fi

# Check if already initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo ""
fi

# Check current status
echo "📋 Current Git status:"
git status --short
echo ""

# Ask for confirmation
read -p "Continue with push? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Push cancelled"
    exit 1
fi

echo ""
echo "📝 Adding files..."
git add .

if [ $? -ne 0 ]; then
    echo "❌ Failed to add files"
    exit 1
fi

echo "✅ Files added"
echo ""

# Ask for commit message
read -p "Enter commit message (or press Enter for default): " COMMIT_MSG

if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Initial commit: Complete Musicly Backend"
fi

echo ""
echo "💾 Committing changes..."
git commit -m "$COMMIT_MSG"

if [ $? -ne 0 ]; then
    echo "⚠️  Nothing to commit or commit failed"
    echo ""
fi

echo ""
echo "🌿 Setting main branch..."
git branch -M main

echo ""
echo "🔗 Checking remote..."
git remote -v | grep origin > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "Adding remote origin..."
    git remote add origin https://github.com/html-proof/Kiro-project.git
else
    echo "Remote origin already exists"
fi

echo ""
echo "🚀 Pushing to GitHub