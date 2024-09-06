from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    display_name: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ProfileResponse(BaseModel):
    uid: str
    email: EmailStr
    display_name: str
