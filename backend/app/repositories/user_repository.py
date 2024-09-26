from functools import wraps
from typing import Dict

from ..database import db
from ..logger import log
from ..schemas.auth_schemas import ProfileResponse, RegisterRequest

_user_cache = {}


def cache_user_profile(func):
    """
    Decorator to cache the user profile data to limit database queries.
    Provides a mechanism to invalidate the cache based on uid.
    """

    @wraps(func)
    def wrapper(uid, *args, **kwargs):
        if uid in _user_cache:
            log.debug(f"cache hit for uid: {uid}")
            return _user_cache[uid]
        else:
            log.debug(f"cache miss for uid: {uid}. Fetching from database.")
            result = func(uid, *args, **kwargs)
            _user_cache[uid] = result
            return result

    def invalidate_cache(uid):
        """
        Invalidate the cache for a specific user.

        :param uid: The unique identifier for the user.
        """
        if uid in _user_cache:
            log.debug(f"invalidating cache for uid: {uid}")
            del _user_cache[uid]

    wrapper.invalidate_cache = invalidate_cache
    return wrapper


class UserRepository:
    @staticmethod
    def save_user(uid: str, user_data: RegisterRequest) -> None:
        """
        Save a new user to the database and invalidate the cache.
        """
        db.collection("users").document(uid).set({
            "display_name": user_data.display_name,
            "email": user_data.email
        })
        UserRepository.get_profile_user.invalidate_cache(uid)
        log.debug(f"user saved to database: {user_data.email} {uid}")

    @staticmethod
    @cache_user_profile
    def get_profile_user(uid: str) -> ProfileResponse:
        """
        Retrieve a user's profile from the database.
        """
        user_data: Dict = db.collection("users").document(uid).get().to_dict()
        response = ProfileResponse(uid=uid, **user_data)
        log.debug(f"user profile retrieved: {user_data['email']} {uid}")
        return response

    @staticmethod
    def delete_user(uid: str) -> None:
        """
        Delete a user from the database and invalidate the cache.
        """
        user_document = db.collection("users").document(uid)
        user_data: Dict = user_document.get().to_dict()
        user_document.delete()
        UserRepository.get_profile_user.invalidate_cache(uid)
        log.debug(f"user deleted: {user_data['email']}  {uid}")
