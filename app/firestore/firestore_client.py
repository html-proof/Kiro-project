from firebase_admin import firestore

def get_firestore_client():
    return firestore.client()

db = get_firestore_client()
