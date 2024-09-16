from ..database import db
from ..logger import log
from ..schemas.auth_schemas import ProfileResponse, RegisterRequest


class UserRepository:
    @staticmethod
    def save_user(uid: str, user_data: RegisterRequest) -> None:
        """
        Save a new user to the database.

        :param uid: The unique identifier for the user.
        :type uid: str
        :param user_data: The user data to be saved, including display name and email.
        :type user_data: RegisterRequest
        :return: None
        :rtype: None
        """
        db.collection("users").document(uid).set({
            "display_name": user_data.display_name,
            "email": user_data.email
        })
        log.info(f"user {uid} saved")

    @staticmethod
    def get_profile_user(uid: str) -> ProfileResponse:
        """
        Retrieve a user's profile from the database.

        :param uid: The unique identifier for the user.
        :type uid: str
        :return: The user's profile data.
        :rtype: ProfileResponse
        """
        user_data = db.collection("users").document(uid).get().to_dict()
        response = ProfileResponse(uid=uid, **user_data)
        log.info(f"retrieved user {uid} profile")
        return response

    @staticmethod
    def delete_user(uid: str) -> None:
        """
        Delete a user from the database.

        :param uid: The unique identifier for the user.
        :type uid: str
        :return: None
        :rtype: None
        """
        db.collection("users").document(uid).delete()
        log.info(f"user {uid} deleted")
