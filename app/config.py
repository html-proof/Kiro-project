import os
import json
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    firebase_service_account_json: Optional[str] = None
    redis_url: str = "redis://localhost:6379"
    allowed_origins: str = "*"
    app_env: str = "development"
    
    @property
    def firebase_credentials(self) -> Optional[dict]:
        if not self.firebase_service_account_json:
            return None
        try:
            return json.loads(self.firebase_service_account_json)
        except json.JSONDecodeError as e:
            print(f"⚠️  WARNING: Invalid Firebase JSON: {e}")
            return None
    
    @property
    def origins_list(self) -> list:
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

# Startup validation
if not settings.firebase_service_account_json:
    print("⚠️  WARNING: FIREBASE_SERVICE_ACCOUNT_JSON not set!")
    print("📌 Firebase Authentication will NOT work until you add this environment variable.")
    print("📌 Add it in Railway Dashboard → Variables → FIREBASE_SERVICE_ACCOUNT_JSON")
else:
    print("✅ Firebase credentials loaded successfully")
