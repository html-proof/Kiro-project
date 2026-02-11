import firebase_admin
from firebase_admin import credentials
from app.config import settings

def initialize_firebase():
    if not firebase_admin._apps:
        if not settings.firebase_credentials:
            print("⚠️  WARNING: Firebase not initialized - credentials missing")
            print("📌 Authentication endpoints will return 503 Service Unavailable")
            return False
        
        try:
            cred = credentials.Certificate(settings.firebase_credentials)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://sample-music-65323-default-rtdb.asia-southeast1.firebasedatabase.app/'
            })
            print("✅ Firebase initialized successfully")
            print("✅ Realtime Database URL configured")
            return True
        except Exception as e:
            print(f"❌ ERROR: Failed to initialize Firebase: {e}")
            return False
    return True

