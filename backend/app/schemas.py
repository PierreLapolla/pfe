from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    uid: str
    email: str

    class Config:
        orm_mode = True
