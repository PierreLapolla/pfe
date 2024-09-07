from ..database import db
from ..schemas.auth_schemas import ProfileResponse, RegisterRequest


class UserRepository:
    @staticmethod
    def save_user(uid: str, user_data: RegisterRequest) -> None:
        db.collection("users").document(uid).set({
            "display_name": user_data.display_name,
            "email": user_data.email
        })

    @staticmethod
    def get_user_profile(uid: str) -> ProfileResponse:
        user_data = db.collection("users").document(uid).get().to_dict()
        return ProfileResponse(uid=uid, **user_data)

    @staticmethod
    def delete_user(uid: str) -> None:
        db.collection("users").document(uid).delete()
