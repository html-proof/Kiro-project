import firebase_admin
from firebase_admin import credentials
from app.config import settings

def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.firebase_credentials)
        firebase_admin.initialize_app(cred)
