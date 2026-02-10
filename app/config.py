import os
import json
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    firebase_service_account_json: Optional[str] = None
    firebase_credentials_path: Optional[str] = None
    redis_url: str = "redis://localhost:6379"
    allowed_origins: str = "*"
    app_env: str = "development"
    
    @property
    def firebase_credentials(self) -> Optional[dict]:
        # Try to load from file path first (for local development)
        if self.firebase_credentials_path and os.path.exists(self.firebase_credentials_path):
            try:
                with open(self.firebase_credentials_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  WARNING: Could not read Firebase credentials file: {e}")
        
        # Fall back to JSON string (for production/Railway)
        if self.firebase_service_account_json:
            try:
                return json.loads(self.firebase_service_account_json)
            except json.JSONDecodeError as e:
                print(f"⚠️  WARNING: Invalid Firebase JSON: {e}")
                return None
        
        return None
    
    @property
    def origins_list(self) -> list:
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

# Startup validation
if settings.firebase_credentials:
    print("✅ Firebase credentials loaded successfully")
else:
    print("⚠️  WARNING: Firebase credentials not found!")
    print("📌 Set FIREBASE_CREDENTIALS_PATH (local) or FIREBASE_SERVICE_ACCOUNT_JSON (production)")
    print("📌 Firebase Authentication will NOT work until credentials are configured.")
