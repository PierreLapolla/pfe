from typing import Dict

from fastapi import APIRouter, Depends, Response

from ..dependencies import get_current_user_token
from ..logger import log
from ..schemas.auth_schemas import LoginRequest, ProfileResponse, RegisterRequest
from ..services.auth_service import AuthService

router = APIRouter()


@router.post("/auth/register")
async def register_user(user: RegisterRequest) -> Dict:
    """
    Register a new user.

    :param user: The user registration data.
    :return: A message indicating successful user creation.
    """
    AuthService.register_user(user)
    log.debug(f"user registered: {user.email}")
    return {"message": "User registered successfully"}


@router.post("/auth/login")
async def login_user(user: LoginRequest) -> Dict:
    """
    Log in a user.

    :param user: The user login data.
    :return: The ID token for the logged-in user.
    """
    id_token = AuthService.login_user(user)
    log.debug(f"user logged in: {user.email} {id_token}")
    return {"id_token": id_token}


@router.post("/auth/logout")
async def logout_user(response: Response, current_user: Dict = Depends(get_current_user_token)) -> Dict:
    """
    Log out the current user.

    :param response: The response object.
    :param current_user: The current authenticated user.
    :return: A message indicating successful user logout.
    """
    AuthService.logout_user(current_user['uid'], response)
    log.debug(f"user logged out: {current_user['uid']}")
    return {"message": "User logged out successfully"}


@router.post("/auth/delete")
async def delete_user(current_user: Dict = Depends(get_current_user_token)) -> Dict:
    """
    Delete the current user.

    :param current_user: The current authenticated user.
    :return: A message indicating successful user deletion.
    """
    AuthService.delete_user(current_user['uid'])
    log.debug(f"user deleted: {current_user['uid']}")
    return {"message": "User deleted successfully"}


@router.get("/auth/profile", response_model=ProfileResponse)
async def get_profile_user(current_user: Dict = Depends(get_current_user_token)) -> ProfileResponse:
    """
    Retrieve the profile of the current user.

    :param current_user: The current authenticated user.
    :return: The profile data of the current user.
    """
    profile = AuthService.get_profile_user(current_user['uid'])
    log.debug(f"user profile retrieved: {profile.email} {profile.uid}")
    return profile
