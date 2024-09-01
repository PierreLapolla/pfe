from fastapi import Depends, FastAPI, HTTPException

from .auth import get_current_user
from .crud import create_user, get_user_by_email
from .schemas import UserCreate, UserOut

app = FastAPI()


@app.post("/register", response_model=UserOut)
async def register_user(user: UserCreate):
    return await create_user(user.email, user.password)


@app.post("/login", response_model=UserOut)
async def login_user(user: UserCreate):
    db_user = await get_user_by_email(user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    # You might want to generate a token here if needed for authentication
    return db_user


@app.get("/me", response_model=UserOut)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
