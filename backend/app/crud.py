from fastapi import HTTPException
from firebase_admin import auth


async def create_user(email: str, password: str):
    try:
        user = auth.create_user(email=email, password=password)
        return {"uid": user.uid, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating user: {e}")


async def get_user_by_email(email: str):
    try:
        user = auth.get_user_by_email(email)
        return {"uid": user.uid, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"User not found: {e}")
