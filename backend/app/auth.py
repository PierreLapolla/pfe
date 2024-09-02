import os

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Response
from firebase_admin import auth

from .database import db
from .dependencies import get_current_user
from .schemas import LoginRequest, ProfileResponse, RegisterRequest

load_dotenv()

router = APIRouter()

FIREBASE_WEB_API_KEY = os.getenv('FIREBASE_WEB_API_KEY')
if not FIREBASE_WEB_API_KEY:
    raise Exception("FIREBASE_WEB_API_KEY is not set in environment variables")

FIREBASE_AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={FIREBASE_WEB_API_KEY}"


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
        # Verify user's email and password (implement your own verification logic)
        user_record = auth.get_user_by_email(user.email)

        # Generate custom token
        custom_token = auth.create_custom_token(user_record.uid).decode('utf-8')

        # Exchange custom token for ID token
        payload = {
            "token": custom_token,
            "returnSecureToken": True
        }
        response = requests.post(FIREBASE_AUTH_URL, json=payload)
        if response.status_code != 200:
            raise HTTPException(status_code=400,
                                detail=f"Failed to exchange custom token: {response.json().get('error', {}).get('message', 'Unknown error')}")

        id_token = response.json().get('idToken')
        refresh_token = response.json().get('refreshToken')

        return {
            "id_token": id_token,
            "refresh_token": refresh_token,
            "expires_in": response.json().get('expiresIn')
        }
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
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
