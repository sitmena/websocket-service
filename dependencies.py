from fastapi import HTTPException, Depends
import jwt
from .config import settings

async def get_current_user(token: str):
    try:
        payload = jwt.decode(token, settings.public_key, algorithms=["RS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
