"""
Test script for Smart Recommendation System
Tests all endpoints and validates responses
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "https://web-production-9c9b.up.railway.app"
# Replace with your Firebase ID token
ID_TOKEN = "YOUR_FIREBASE_ID_TOKEN_HERE"

headers = {
    "Authorization": f"Bearer {ID_TOKEN}",
    "Content-Type": "application/json"
}


def test_smart_recommendations():
    """Test GET /recommend/smart/recommendations"""
    print("\n" + "="*60)
    print("TEST 1: Smart Recommendations")
    print("="*60)
    
    url = f"{BASE_URL}/recommend/smart/recommendations"
    params = {
        "limit": 10,
        "quality": "medium_quality"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {data.get('success')}")
            print(f"📊 Count: {data.get('count')}")
            print(f"🎯 Quality Level: {data.get('quality_level')}")
            
            context = data.get('context', {})
            print(f"\n📅 Context:")
            print(f"  - Time of Day: {context.get('time_of_day')}")
            print(f"  - Date: {context.get('weekday')}, {context.get('month')} {context.get('day')}, {context.get('year')}")
            print(f"  - Season: {context.get('season')}")
            print(f"  - Weekend: {context.get('is_weekend')}")
            
            recommendations = data.get('recommendations', [])
            if recommendations:
                print(f"\n🎵 Sample Songs:")
                for i, song in enumerate(recommendations[:3], 1):
                    print(f"\n  {i}. {song.get('title')}")
                    print(f"     Channel: {song.get('channel')}")
                    print(f"     Views: {song.get('views'):,}" if isinstance(song.get('views'), int) else f"     Views: {song.get('views')}")
                    print(f"     Trust Score: {song.get('trust_score', 'N/A')}")
                    print(f"     Duration: {song.get('duration')}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")


def test_continuous_feed():
    """Test GET /recommend/smart/feed"""
    print("\n" + "="*60)
    print("TEST 2: Continuous Feed (Pagination)")
    print("="*60)
    
    url = f"{BASE_URL}/recommend/smart/feed"
    
    for page in [1, 2]:
        print(f"\n📄 Page {page}:")
        params = {
            "page": page,
            "page_size": 5
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success: {data.get('success')}")
                print(f"📊 Total: {data.get('total')}")
                print(f"📄 Page: {data.get('page')}/{data.get('page_size')}")
                print(f"➡️ Has More: {data.get('has_more')}")
                
                songs = data.get('songs', [])
                if songs:
                    print(f"\n🎵 Songs on this page:")
                    for i, song in enumerate(songs, 1):
                        print(f"  {i}. {song.get('title')}")
            else:
                print(f"❌ Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")


def test_time_context():
    """Test GET /recommend/smart/time-context"""
    print("\n" + "="*60)
    print("TEST 3: Time Context")
    print("="*60)
    
    url = f"{BASE_URL}/recommend/smart/time-context"
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {data.get('success')}")
            print(f"💬 Message: {data.get('message')}")
            
            context = data.get('context', {})
            print(f"\n📅 Full Context:")
            for key, value in context.items():
                print(f"  - {key}: {value}")
            
            moods = data.get('recommended_moods', [])
            print(f"\n😊 Recommended Moods for Current Time:")
            for mood in moods:
                print(f"  - {mood}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")


def test_quality_stats():
    """Test GET /recommend/smart/quality-stats"""
    print("\n" + "="*60)
    print("TEST 4: Quality Stats")
    print("="*60)
    
    url = f"{BASE_URL}/recommend/smart/quality-stats"
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {data.get('success')}")
            
            quality_levels = data.get('quality_levels', {})
            print(f"\n📊 Quality Levels:")
            for level, info in quality_levels.items():
                print(f"\n  {level}:")
                print(f"    Min Views: {info.get('min_views'):,}")
                print(f"    Description: {info.get('description')}")
            
            trusted = data.get('trusted_channels', {})
            print(f"\n🏆 Trusted Channels:")
            for key, count in trusted.items():
                print(f"  - {key}: {count}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 SMART RECOMMENDATION SYSTEM - TEST SUITE")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if ID_TOKEN == "YOUR_FIREBASE_ID_TOKEN_HERE":
        print("\n⚠️ WARNING: Please set your Firebase ID token in the script!")
        print("You can get it from:")
        print("1. Login to your Flutter app")
        print("2. Check the auth_token in secure storage")
        print("3. Or use Firebase Auth REST API")
        return
    
    # Run tests
    test_smart_recommendations()
    test_continuous_feed()
    test_time_context()
    test_quality_stats()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()
