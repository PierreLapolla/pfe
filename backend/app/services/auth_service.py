import requests
from fastapi import HTTPException, Response
from firebase_admin import auth

from ..config_loader import config
from ..logger import log
from ..repositories.user_repository import UserRepository
from ..schemas.auth_schemas import ProfileResponse, RegisterRequest


class AuthService:
    @staticmethod
    def register_user(user_data: RegisterRequest) -> None:
        """
        Register a new user.

        :param user_data: The user registration data.
        :type user_data: RegisterRequest
        :return: None
        :rtype: None
        """
        user_record = auth.create_user(
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.display_name
        )
        UserRepository.save_user(user_record.uid, user_data)
        log.info(f"user {user_data.email} has been registered")

    @staticmethod
    def login_user(email: str, password: str) -> str:
        """
        Log in a user.

        :param email: The email address of the user.
        :type email: str
        :param password: The password for the user account.
        :type password: str
        :return: The ID token for the logged-in user.
        :rtype: str
        :raises HTTPException: If the login credentials are invalid.
        """
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={config('FIREBASE_API_KEY')}",
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
        """
        Log out the current user.

        :param response: The response object.
        :type response: Response
        :return: None
        :rtype: None
        """
        response.delete_cookie("id_token")
        response.delete_cookie("refresh_token")
        log.info("user has been logged out")

    @staticmethod
    def get_profile_user(user_id: str) -> ProfileResponse:
        """
        Retrieve the profile of a user.

        :param user_id: The unique identifier for the user.
        :type user_id: str
        :return: The profile data of the user.
        :rtype: ProfileResponse
        """
        profile = UserRepository.get_profile_user(user_id)
        log.info(f"retrieved profile for user {user_id}")
        return profile

    @staticmethod
    def delete_user(user_id: str) -> None:
        """
        Delete a user.

        :param user_id: The unique identifier for the user.
        :type user_id: str
        :return: None
        :rtype: None
        """
        UserRepository.delete_user(user_id)
        auth.delete_user(user_id)
        log.info(f"user {user_id} has been deleted")
