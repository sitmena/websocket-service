from fastapi import HTTPException, Depends
import jwt
import os


JWT_TOKEN_KEY = os.getenv("JWT_KEY")


async def get_current_user_id(token: str):
    try:
        payload = jwt.decode(token, JWT_TOKEN_KEY, algorithms=["HS256"])

        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
