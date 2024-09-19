from functools import lru_cache
from typing import Dict

from ..config_loader import config
from ..database import db
from ..logger import log
from ..schemas.auth_schemas import ProfileResponse, RegisterRequest


class UserRepository:
    @staticmethod
    def save_user(uid: str, user_data: RegisterRequest) -> None:
        """
        Save a new user to the database.

        :param uid: The unique identifier for the user.
        :param user_data: The user data to be saved.
        :return: None
        """
        db.collection("users").document(uid).set({
            "display_name": user_data.display_name,
            "email": user_data.email
        })
        UserRepository.get_profile_user.cache_clear()
        log.debug(f"user saved to database: {user_data.email} {uid}")

    @staticmethod
    @lru_cache(maxsize=config('cache_size', 10))
    def get_profile_user(uid: str) -> ProfileResponse:
        """
        Retrieve a user's profile from the database.

        :param uid: The unique identifier for the user.
        :return: The user's profile data.
        """
        user_data: Dict = db.collection("users").document(uid).get().to_dict()
        response = ProfileResponse(uid=uid, **user_data)
        log.debug(f"user profile retrieved: {user_data['email']} {uid}")
        return response

    @staticmethod
    def delete_user(uid: str) -> None:
        """
        Delete a user from the database.

        :param uid: The unique identifier for the user.
        :return: None
        """
        user_document = db.collection("users").document(uid)
        user_data: Dict = user_document.get().to_dict()
        user_document.delete()
        UserRepository.get_profile_user.cache_clear()
        log.debug(f"user deleted: {user_data['email']}  {uid}")
