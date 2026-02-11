from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Musicly Backend", version="1.0.1")  # Version bump to force rebuild

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=False,  # Must be False when allow_origins is ["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Starting Musicly Backend...")
    
    try:
        from app.firebase.firebase_init import initialize_firebase
        firebase_ok = initialize_firebase()
        if not firebase_ok:
            logger.warning("⚠️ Running without Firebase authentication")
    except Exception as e:
        logger.error(f"❌ Firebase initialization failed: {e}")
        logger.warning("⚠️ Running without Firebase authentication")
    
    try:
        from app.redis.redis_client import initialize_redis
        initialize_redis()
    except Exception as e:
        logger.error(f"❌ Redis initialization failed: {e}")
        logger.warning("⚠️ Running without Redis cache")
    
    logger.info("✅ Startup complete!")

# Import routes after app is created to avoid circular imports
try:
    from app.routes import auth_routes, user_routes, music_routes, recommend_routes, playlist_routes, sync_routes, device_routes
    
    app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
    app.include_router(user_routes.router, prefix="/user", tags=["User"])
    app.include_router(music_routes.router, prefix="/music", tags=["Music"])
    app.include_router(recommend_routes.router, prefix="/recommend", tags=["Recommendations"])
    app.include_router(playlist_routes.router, prefix="/playlist", tags=["Playlists"])
    app.include_router(sync_routes.router, prefix="/sync", tags=["Sync"])
    app.include_router(device_routes.router, prefix="/device", tags=["Device"])
    logger.info("✅ All routes loaded successfully")
except Exception as e:
    logger.error(f"❌ Failed to load routes: {e}")
    logger.error(f"Traceback: ", exc_info=True)
    # Don't exit - let the app start with just health endpoints

@app.get("/")
async def root():
    return {"message": "Musicly Backend API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/ping")
async def ping():
    """Keepalive endpoint to prevent container sleep"""
    return {"status": "alive", "timestamp": "ok"}
