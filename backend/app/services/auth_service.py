import os

import requests
from fastapi import HTTPException, Response
from firebase_admin import auth

from ..repositories.user_repository import UserRepository
from ..schemas.auth_schemas import ProfileResponse, RegisterRequest
from ..logger import log


class AuthService:
    @staticmethod
    def register_user(user_data: RegisterRequest) -> None:
        user_record = auth.create_user(
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.display_name
        )
        UserRepository.save_user(user_record.uid, user_data)
        log.info(f"user {user_data.email} has been registered")

    @staticmethod
    def login_user(email: str, password: str) -> str:
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={os.getenv('FIREBASE_API_KEY')}",
            json=payload
        )

        if response.status_code != 200:
            log.error(f"failed to login user {email}")
            raise HTTPException(status_code=response.status_code, detail="Invalid credentials")

        id_token = response.json().get('idToken')
        log.info(f"user {email} has been logged in")
        return id_token

    @staticmethod
    def logout_user(response: Response) -> None:
        response.delete_cookie("id_token")
        response.delete_cookie("refresh_token")
        log.info("user has been logged out")

    @staticmethod
    def get_profile(user_id: str) -> ProfileResponse:
        profile = UserRepository.get_user_profile(user_id)
        log.info(f"retrieved profile for user {user_id}")
        return profile

    @staticmethod
    def delete_account(user_id: str) -> None:
        UserRepository.delete_user(user_id)
        auth.delete_user(user_id)
        log.info(f"user {user_id} has been deleted")
