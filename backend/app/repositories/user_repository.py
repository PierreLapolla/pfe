from functools import wraps
from typing import Callable, Dict

from ..database import db
from ..logger import log
from ..schemas.auth_schemas import ProfileResponse, RegisterRequest


def cache_result(cache_key_func: Callable[[str], str]):
    cache_store: Dict[str, ProfileResponse] = {}

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = cache_key_func(*args, **kwargs)
            if key in cache_store:
                log.debug(f"cache hit for key: {key}")
                return cache_store[key]
            log.debug(f"cache miss for key: {key}")
            result = func(*args, **kwargs)
            cache_store[key] = result
            return result

        def invalidate(key: str):
            if key in cache_store:
                log.debug(f"invalidating cache for key: {key}")
                del cache_store[key]

        wrapper.invalidate = invalidate
        return wrapper

    return decorator


class UserRepository:

    @staticmethod
    @cache_result(lambda uid: uid)
    def get_profile_user(uid: str) -> ProfileResponse:
        """
        Retrieve a user's profile from the database.
        """
        user_data: Dict = db.collection("users").document(uid).get().to_dict()
        response = ProfileResponse(uid=uid, **user_data)
        log.debug(f"user profile retrieved: {user_data['email']} {uid}")
        return response

    @staticmethod
    def save_user(uid: str, user_data: RegisterRequest) -> None:
        """
        Save a new user to the database and invalidate the cache.
        """
        db.collection("users").document(uid).set({
            "display_name": user_data.display_name,
            "email": user_data.email
        })
        UserRepository.get_profile_user.invalidate(uid)
        log.debug(f"user saved to database: {user_data.email} {uid}")

    @staticmethod
    def delete_user(uid: str) -> None:
        """
        Delete a user from the database and invalidate the cache.
        """
        user_document = db.collection("users").document(uid)
        user_data: Dict = user_document.get().to_dict()
        user_document.delete()
        UserRepository.get_profile_user.invalidate(uid)
        log.debug(f"user deleted: {user_data['email']} {uid}")
