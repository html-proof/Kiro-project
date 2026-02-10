from firebase_admin import auth
import firebase_admin
from fastapi import HTTPException, Header
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

