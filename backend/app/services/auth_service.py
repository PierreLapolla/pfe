import requests
from firebase_admin import auth
from fastapi import HTTPException
from ..repositories.user_repository import UserRepository
from ..schemas.auth_schemas import RegisterRequest

API_KEY = 'AIzaSyDq6djBTsk4OMxXOLJe39WxbiBKQoG40mo'

class AuthService:
    @staticmethod
    def register_user(user_data: RegisterRequest):
        user_record = auth.create_user(
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.display_name
        )
        UserRepository.save_user(user_record.uid, user_data)

    @staticmethod
    def login_user(email: str, password: str) -> str:
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}",
            json=payload
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Invalid credentials")
        id_token = response.json().get('idToken')
        return id_token

    @staticmethod
    def get_profile(user_id: str):
        profile = UserRepository.get_user_profile(user_id)
        return profile
