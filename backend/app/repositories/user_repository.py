from typing import Dict, Optional

from ..database import db
from ..logger import log
from ..schemas.auth_schemas import ProfileResponse, RegisterRequest

class UserCache:
    """
    A class to handle caching of user profile data.
    """
    def __init__(self):
        self._cache = {}

    def get(self, uid: str) -> Optional[ProfileResponse]:
        """
        Retrieve a user profile from the cache.
        """
        if uid in self._cache:
            log.debug(f"cache hit for uid: {uid}")
            return self._cache[uid]
        log.debug(f"cache miss for uid: {uid}")
        return None

    def set(self, uid: str, data: ProfileResponse) -> None:
        """
        Set user profile data in the cache.
        """
        log.debug(f"setting cache for uid: {uid}")
        self._cache[uid] = data

    def invalidate(self, uid: str) -> None:
        """
        Invalidate the cache for a specific user.
        """
        if uid in self._cache:
            log.debug(f"invalidating cache for uid: {uid}")
            del self._cache[uid]

class UserRepository:
    _user_cache = UserCache()

    @staticmethod
    def save_user(uid: str, user_data: RegisterRequest) -> None:
        """
        Save a new user to the database and invalidate the cache.
        """
        db.collection("users").document(uid).set({
            "display_name": user_data.display_name,
            "email": user_data.email
        })
        UserRepository._user_cache.invalidate(uid)
        log.debug(f"user saved to database: {user_data.email} {uid}")

    @staticmethod
    def get_profile_user(uid: str) -> ProfileResponse:
        """
        Retrieve a user's profile, checking cache first before querying the database.
        """
        cached_data = UserRepository._user_cache.get(uid)
        if cached_data:
            return cached_data

        user_data: Dict = db.collection("users").document(uid).get().to_dict()
        response = ProfileResponse(uid=uid, **user_data)
        log.debug(f"user profile retrieved: {user_data['email']} {uid}")
        UserRepository._user_cache.set(uid, response)
        return response

    @staticmethod
    def delete_user(uid: str) -> None:
        """
        Delete a user from the database and invalidate the cache.
        """
        user_document = db.collection("users").document(uid)
        user_data: Dict = user_document.get().to_dict()
        user_document.delete()
        UserRepository._user_cache.invalidate(uid)
        log.debug(f"user deleted: {user_data['email']} {uid}")
