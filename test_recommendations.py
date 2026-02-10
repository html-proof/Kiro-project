"""
Test script to verify the recommendation system works correctly
"""
import asyncio
from app.services.recommendation_service import (
    get_user_recommendations,
    get_similar_songs,
    get_recommendations_by_artist,
    get_because_you_liked_recommendations
)

async def test_recommendations():
    print("Testing Recommendation System...")
    print("=" * 50)
    
    # Test 1: Get personalized recommendations for a user
    print("\n1. Testing personalized recommendations...")
    try:
        test_uid = "test_user_123"
        recommendations = await get_user_recommendations(test_uid)
        print(f"✓ Got {len(recommendations)} personalized recommendations")
        if recommendations:
            print(f"  Sample: {recommendations[0].get('title', 'N/A')}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 2: Get similar songs
    print("\n2. Testing similar songs...")
    try:
        similar = await get_similar_songs("test_video_id", "test_user_123")
        print(f"✓ Got {len(similar)} similar songs")
        if similar:
            print(f"  Sample: {similar[0].get('title', 'N/A')}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 3: Get recommendations by artist
    print("\n3. Testing artist recommendations...")
    try:
        artist_recs = await get_recommendations_by_artist("Taylor Swift", "English")
        print(f"✓ Got {len(artist_recs)} artist recommendations")
        if artist_recs:
            print(f"  Sample: {artist_recs[0].get('title', 'N/A')}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 4: Get "because you liked" recommendations
    print("\n4. Testing 'because you liked' recommendations...")
    try:
        liked_recs = await get_because_you_liked_recommendations("test_user_123")
        print(f"✓ Got {len(liked_recs)} 'because you liked' recommendations")
        if liked_recs:
            print(f"  Sample: {liked_recs[0].get('title', 'N/A')}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 50)
    print("Recommendation system test complete!")

if __name__ == "__main__":
    asyncio.run(test_recommendations())
