from ..database import db
from ..schemas.auth_schemas import ProfileResponse, RegisterRequest
from ..logger import log


class UserRepository:
    @staticmethod
    def save_user(uid: str, user_data: RegisterRequest) -> None:
        db.collection("users").document(uid).set({
            "display_name": user_data.display_name,
            "email": user_data.email
        })
        log.info(f"user {uid} saved")

    @staticmethod
    def get_user_profile(uid: str) -> ProfileResponse:
        user_data = db.collection("users").document(uid).get().to_dict()
        response = ProfileResponse(uid=uid, **user_data)
        log.info(f"retrieved user {uid} profile")
        return response

    @staticmethod
    def delete_user(uid: str) -> None:
        db.collection("users").document(uid).delete()
        log.info(f"user {uid} deleted")
