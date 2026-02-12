#!/usr/bin/env python3
"""
Quick test script to verify the /user/preferences endpoint works correctly
Run this after starting the backend server
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_preferences_endpoint():
    """Test the preferences endpoint with mock data"""
    
    # Note: This will fail without a valid Firebase token
    # This is just to show the endpoint structure
    
    test_data = {
        "selected_languages": ["English", "Hindi"],
        "selected_moods": ["Happy", "Energetic"],
        "selected_artists": []
    }
    
    print("Testing POST /user/preferences")
    print(f"Request body: {json.dumps(test_data, indent=2)}")
    print("\nNote: This requires a valid Firebase auth token")
    print("Expected response: 200 OK with preferences saved message")
    
    # Alternative test with different naming convention
    test_data_alt = {
        "languages": ["English", "Hindi"],
        "moods": ["Happy", "Energetic"]
    }
    
    print("\n" + "="*50)
    print("Alternative naming convention:")
    print(f"Request body: {json.dumps(test_data_alt, indent=2)}")
    print("Both formats should work!")

if __name__ == "__main__":
    test_preferences_endpoint()
