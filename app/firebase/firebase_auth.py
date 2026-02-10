from firebase_admin import auth
import firebase_admin
from fastapi import HTTPException, Header, Depends
from typing import Optional

async def verify_token(authorization: Optional[str] = Header(None)) -> dict:
    # Check if Firebase is initialized
    if not firebase_admin._apps:
        raise HTTPException(
            status_code=503, 
            detail="Firebase Authentication is not configured. Please contact the administrator."
        )
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = authorization.split("Bearer ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

# Alias for compatibility
async def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """Get current user from Firebase token (alias for verify_token)"""
    return await verify_token(authorization)

