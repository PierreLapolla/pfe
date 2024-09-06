from typing import Dict

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from firebase_admin import auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    decoded_token = auth.verify_id_token(token)
    return decoded_token
