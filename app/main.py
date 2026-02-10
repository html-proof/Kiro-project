from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.firebase.firebase_init import initialize_firebase
from app.redis.redis_client import initialize_redis
from app.routes import auth_routes, user_routes, music_routes, recommend_routes, playlist_routes, sync_routes, device_routes

app = FastAPI(title="Musicly Backend", version="1.0.0")

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
    initialize_firebase()
    initialize_redis()

# Routes
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(user_routes.router, prefix="/user", tags=["User"])
app.include_router(music_routes.router, tags=["Music"])
app.include_router(recommend_routes.router, prefix="/recommend", tags=["Recommendations"])
app.include_router(playlist_routes.router, prefix="/playlist", tags=["Playlists"])
app.include_router(sync_routes.router, prefix="/sync", tags=["Sync"])
app.include_router(device_routes.router, prefix="/device", tags=["Device"])

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
