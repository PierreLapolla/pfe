from typing import Dict

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from firebase_admin import auth

from .logger import log

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    """
    Retrieve the current authenticated user based on the provided token.

    :param token: The OAuth2 token provided by the user.
    :return: The decoded token containing user information.
    """
    decoded_token = auth.verify_id_token(token)
    log.info(f"decoded token: {decoded_token}")
    return decoded_token
