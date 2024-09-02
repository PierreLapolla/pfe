from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    password: str
    display_name: str


class UserProfile(BaseModel):
    uid: str
    display_name: str
    email: EmailStr
