"""
Quick API test script
Run: python test_api.py
"""
import requests

BASE_URL = "http://localhost:8000"

def test_health():
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_search():
    print("Testing search endpoint...")
    response = requests.get(f"{BASE_URL}/search", params={"q": "arijit singh"})
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data.get('data', []))} results")
    if data.get('data'):
        print(f"First result: {data['data'][0]['title']}\n")

def test_resolve():
    print("Testing resolve endpoint...")
    # Use a sample video ID (replace with actual)
    response = requests.get(f"{BASE_URL}/resolve", params={"id": "dQw4w9WgXcQ", "quality": "saver"})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

if __name__ == "__main__":
    print("=== Musicly Backend API Tests ===\n")
    
    try:
        test_health()
        test_search()
        # test_resolve()  # Uncomment to test
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to server. Make sure it's running on port 8000")
    except Exception as e:
        print(f"Error: {e}")
