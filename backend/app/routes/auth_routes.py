from typing import Dict

from fastapi import APIRouter, Depends, Response

from ..dependencies import get_current_user
from ..schemas.auth_schemas import LoginRequest, ProfileResponse, RegisterRequest
from ..services.auth_service import AuthService
from ..logger import log

router = APIRouter()


@router.post("/auth/register")
async def register_user(user: RegisterRequest) -> Dict:
    AuthService.register_user(user)
    log.info(f"user {user.email} registered successfully")
    return {"message": "User created successfully"}


@router.post("/auth/login")
async def login_user(user: LoginRequest) -> Dict:
    id_token = AuthService.login_user(user.email, user.password)
    log.info(f"user {user.email} logged in successfully")
    return {"id_token": id_token}


@router.post("/auth/logout")
async def logout_user(response: Response) -> Dict:
    AuthService.logout_user(response)
    log.info(f"user logged out successfully")
    return {"message": "User logged out successfully"}


@router.post("/auth/delete")
async def delete_user(current_user=Depends(get_current_user)) -> Dict:
    AuthService.delete_user(current_user['uid'])
    log.info(f"user {current_user['email']} deleted successfully")
    return {"message": "User deleted successfully"}


@router.get("/auth/profile", response_model=ProfileResponse)
async def get_profile_user(current_user=Depends(get_current_user)) -> ProfileResponse:
    profile = AuthService.get_profile_user(current_user['uid'])
    log.info(f"user {profile.email} profile retrieved successfully")
    return profile
