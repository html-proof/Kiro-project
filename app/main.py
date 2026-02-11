from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Reduce noise from third-party libraries
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("yt_dlp").setLevel(logging.WARNING)

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
    from app.routes import auth_routes, user_routes, music_routes, recommend_routes, playlist_routes, sync_routes, device_routes, websocket_routes
    
    app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
    app.include_router(user_routes.router, prefix="/user", tags=["User"])
    app.include_router(music_routes.router, prefix="/music", tags=["Music"])
    app.include_router(recommend_routes.router, prefix="/recommend", tags=["Recommendations"])
    app.include_router(playlist_routes.router, prefix="/playlist", tags=["Playlists"])
    app.include_router(sync_routes.router, prefix="/sync", tags=["Sync"])
    app.include_router(device_routes.router, prefix="/device", tags=["Device"])
    app.include_router(websocket_routes.router, tags=["WebSocket"])
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
    import time
    return {
        "status": "alive", 
        "timestamp": int(time.time()),
        "message": "Server is running"
    }

# Fallback play endpoint at root level for compatibility
@app.get("/play")
@app.post("/play")
async def root_play_audio(
    request: Request,
    id: str = Query(None),
    quality: str = Query("high")
):
    """Fallback streaming endpoint - handles both GET and POST"""
    from app.services.audio_resolver_service import resolve_audio_stream
    from app.services.proxy_stream_service import proxy_audio_stream
    
    # For POST requests, try to get id from query params or body
    if not id:
        try:
            body = await request.json()
            id = body.get('id') or body.get('video_id')
            quality = body.get('quality', 'saver')
        except:
            # Try form data
            try:
                form = await request.form()
                id = form.get('id') or form.get('video_id')
                quality = form.get('quality', 'saver')
            except:
                pass
    
    if not id:
        return {"success": False, "message": "Missing id parameter"}
    
    stream_data = await resolve_audio_stream(id, quality)
    if stream_data:
        return await proxy_audio_stream(stream_data["stream_url"], None)
    return {"success": False, "message": "Failed to stream"}
