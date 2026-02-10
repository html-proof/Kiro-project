import os
import json
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    firebase_service_account_json: str
    redis_url: str = "redis://localhost:6379"
    allowed_origins: str = "http://localhost:3000"
    app_env: str = "development"
    
    @property
    def firebase_credentials(self) -> dict:
        return json.loads(self.firebase_service_account_json)
    
    @property
    def origins_list(self) -> list:
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
