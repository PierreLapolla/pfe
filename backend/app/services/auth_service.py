import requests
from fastapi import HTTPException, Response
from firebase_admin import auth

from ..config_loader import config
from ..logger import log
from ..repositories.user_repository import UserRepository
from ..schemas.auth_schemas import LoginRequest, ProfileResponse, RegisterRequest


class AuthService:
    @staticmethod
    def register_user(user_data: RegisterRequest) -> None:
        """
        Register a new user.

        :param user_data: The user registration data.
        :return: None
        """
        user_record = auth.create_user(
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.display_name
        )
        UserRepository.save_user(user_record.uid, user_data)
        log.info(f"user registered: {user_data.email} {user_record.uid}")

    @staticmethod
    def login_user(user_data: LoginRequest) -> str:
        """
        Log in a user.

        :param user_data: The user login data.
        :return: The ID token for the logged-in user.
        :raises HTTPException: If the login credentials are invalid.
        """
        payload = {
            "email": user_data.email,
            "password": user_data.password,
            "returnSecureToken": True
        }

        response = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={config('FIREBASE_API_KEY')}",
            json=payload
        )

        if response.status_code != 200:
            log.error(f"user login failed: {user_data.email}")
            raise HTTPException(status_code=response.status_code, detail="Invalid credentials")

        id_token = response.json().get('idToken')
        log.info(f"user logged in: {user_data.email} {id_token}")
        return id_token

    @staticmethod
    def logout_user(uid: str, response: Response) -> None:
        """
        Log out the current user by revoking the Firebase token and deleting cookies.

        :param response: The response object.
        :param uid: The unique identifier for the user.
        :return: None
        """
        auth.revoke_refresh_tokens(uid)
        response.delete_cookie("id_token")
        response.delete_cookie("refresh_token")
        log.info(f"user logged out and token invalidated: {uid}")


    @staticmethod
    def get_profile_user(uid: str) -> ProfileResponse:
        """
        Retrieve the profile of a user.

        :param uid: The unique identifier for the user.
        :return: The profile data of the user.
        """
        profile = UserRepository.get_profile_user(uid)
        log.info(f"user profile retrieved: {profile.email} {uid}")
        return profile

    @staticmethod
    def delete_user(uid: str) -> None:
        """
        Delete a user.

        :param uid: The unique identifier for the user.
        :return: None
        """
        UserRepository.delete_user(uid)
        auth.delete_user(uid)
        log.info(f"user deleted: {uid}")
