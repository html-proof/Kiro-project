from firebase_admin import firestore
import firebase_admin

_db = None

def get_firestore_client():
    """Get Firestore client with lazy initialization"""
    global _db
    
    if _db is None:
        # Check if Firebase is initialized
        if not firebase_admin._apps:
            print("⚠️  WARNING: Firebase not initialized, Firestore unavailable")
            return None
        
        try:
            _db = firestore.client()
            print("✅ Firestore client initialized")
        except Exception as e:
            print(f"❌ ERROR: Failed to initialize Firestore: {e}")
            return None
    
    return _db

# Lazy property for backward compatibility
class _FirestoreDB:
    @property
    def db(self):
        return get_firestore_client()

_firestore_db = _FirestoreDB()
db = property(lambda self: get_firestore_client())
