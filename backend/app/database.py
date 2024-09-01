from .firebase_config import db


def add_user(user_id, user_data):
    db.collection('users').document(user_id).set(user_data)


def get_user(user_id):
    doc = db.collection('users').document(user_id).get()
    return doc.to_dict() if doc.exists else None
