from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True
