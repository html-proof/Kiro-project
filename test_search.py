#!/usr/bin/env python3
"""
Quick test script to verify the search endpoint returns streamUrl
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_search():
    print("Testing search endpoint...")
    response = requests.get(f"{BASE_URL}/music/search", params={"q": "test"})
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    data = response.json()
    if data.get('success'):
        results = data.get('data', [])
        print(f"\nFound {len(results)} results")
        if results:
            first = results[0]
            print(f"\nFirst result:")
            print(f"  Title: {first.get('title')}")
            print(f"  ID: {first.get('id')}")
            print(f"  StreamURL: {first.get('streamUrl')}")
            
            if first.get('streamUrl'):
                print("\n✅ streamUrl is present!")
            else:
                print("\n❌ streamUrl is missing!")
    else:
        print(f"❌ Error: {data.get('message')}")

if __name__ == "__main__":
    test_search()
