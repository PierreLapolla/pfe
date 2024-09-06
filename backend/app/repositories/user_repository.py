from ..database import db
from ..schemas.auth_schemas import ProfileResponse, RegisterRequest


class UserRepository:
    @staticmethod
    def save_user(uid: str, user_data: RegisterRequest):
        db.collection("users").document(uid).set({
            "display_name": user_data.display_name,
            "email": user_data.email
        })

    @staticmethod
    def get_user_profile(uid: str):
        user_doc = db.collection("users").document(uid).get()
        user_data = user_doc.to_dict()
        return ProfileResponse(uid=uid, **user_data)
