from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from firebase_admin import auth
from app.firestore.firestore_collections import get_user_ref
from app.utils.time_utils import now_timestamp
from app.utils.response_utils import success_response

router = APIRouter()

class LoginRequest(BaseModel):
    id_token: str

@router.post("/login")
async def login(request: LoginRequest):
    try:
        decoded_token = auth.verify_id_token(request.id_token)
        uid = decoded_token["uid"]
        email = decoded_token.get("email", "")
        name = decoded_token.get("name", "")
        picture = decoded_token.get("picture", "")
        
        user_ref = get_user_ref(uid)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            user_data = {
                "uid": uid,
                "email": email,
                "name": name,
                "photo_url": picture,
                "selected_languages": [],
                "selected_artists": [],
                "created_at": now_timestamp()
            }
            user_ref.set(user_data)
        else:
            user_data = user_doc.to_dict()
        
        return success_response(user_data, "Login successful")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
