import requests
import os
from fastapi import APIRouter, Depends, HTTPException, Response
from firebase_admin import auth

from .database import db
from .dependencies import get_current_user
from .schemas import LoginRequest, ProfileResponse, RegisterRequest

router = APIRouter()


@router.post("/register")
async def register_user(user: RegisterRequest):
    try:
        user_record = auth.create_user(
            email=user.email,
            password=user.password,
            display_name=user.display_name
        )
        db.collection("users").document(user_record.uid).set({
            "display_name": user.display_name,
            "email": user.email
        })
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")


@router.post("/login")
async def login_user(user: LoginRequest):
    try:
        payload = {
            "email": user.email,
            "password": user.password,
            "returnSecureToken": True
        }
        response = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={os.getenv('FIREBASE_API_KEY')}",
            json=payload
        )
        if response.status_code != 200:
            raise HTTPException(status_code=400,
                                detail=f"Login failed: {response.json().get('error', {}).get('message', 'Unknown error')}")

        id_token = response.json().get('idToken')
        return {"id_token": id_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Login failed: {str(e)}")


@router.get("/profile", response_model=ProfileResponse)
async def get_profile(current_user=Depends(get_current_user)):
    try:
        user_doc = db.collection("users").document(current_user['uid']).get()
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = user_doc.to_dict()
        return ProfileResponse(uid=current_user['uid'], **user_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch profile: {str(e)}")


@router.post("/logout")
async def logout_user(response: Response):
    try:
        response.delete_cookie("id_token")
        response.delete_cookie("refresh_token")
        return {"message": "User logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Logout failed: {str(e)}")
