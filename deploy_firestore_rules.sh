#!/bin/bash

# Firestore Rules Deployment Script
# This script helps you deploy Firestore security rules

echo "🔒 Firestore Rules Deployment"
echo "=============================="
echo ""

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null
then
    echo "❌ Firebase CLI not found!"
    echo ""
    echo "Install it with:"
    echo "  npm install -g firebase-tools"
    echo ""
    exit 1
fi

echo "✅ Firebase CLI found"
echo ""

# Check if logged in
echo "Checking Firebase login status..."
firebase projects:list &> /dev/null

if [ $? -ne 0 ]; then
    echo "❌ Not logged in to Firebase"
    echo ""
    echo "Please login:"
    firebase login
    echo ""
fi

echo "✅ Logged in to Firebase"
echo ""

# Show current project
echo "Current Firebase project:"
firebase use
echo ""

# Ask for confirmation
echo "📋 This will deploy the rules from: firestore.rules"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "❌ Deployment cancelled"
    exit 1
fi

# Deploy rules
echo ""
echo "🚀 Deploying Firestore rules..."
firebase deploy --only firestore:rules

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Rules deployed successfully!"
    echo ""
    echo "🔗 View rules at:"
    echo "   https://console.firebase.google.com/project/music-app-f2e65/firestore/rules"
    echo ""
    echo "🧪 Test rules at:"
    echo "   https://console.firebase.google.com/project/music-app-f2e65/firestore/rules"
    echo "   (Click 'Rules Playground' tab)"
    echo ""
else
    echo ""
    echo "❌ Deployment failed!"
    echo ""
    echo "Try deploying manually:"
    echo "1. Go to: https://console.firebase.google.com/project/music-app-f2e65/firestore/rules"
    echo "2. Copy contents from firestore.rules"
    echo "3. Paste and click 'Publish'"
    echo ""
fi
