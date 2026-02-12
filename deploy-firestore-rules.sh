#!/bin/bash

echo "========================================"
echo "  Firestore Rules Deployment Script"
echo "========================================"
echo ""

echo "Checking if Firebase CLI is installed..."
if ! command -v firebase &> /dev/null; then
    echo "[ERROR] Firebase CLI not found!"
    echo ""
    echo "Please install it first:"
    echo "  npm install -g firebase-tools"
    echo ""
    exit 1
fi

echo "[OK] Firebase CLI found"
echo ""

echo "Logging in to Firebase..."
firebase login
if [ $? -ne 0 ]; then
    echo "[ERROR] Login failed"
    exit 1
fi

echo ""
echo "Deploying Firestore rules..."
firebase deploy --only firestore:rules
if [ $? -ne 0 ]; then
    echo "[ERROR] Deployment failed"
    exit 1
fi

echo ""
echo "========================================"
echo "  SUCCESS! Rules deployed"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Test the Flutter app"
echo "2. Check logs for PERMISSION_DENIED errors"
echo "3. Verify play history and likes are saving"
echo ""
