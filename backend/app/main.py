from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db
from . import crud, schemas, redis_cache

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to My Game Backend!"}

@app.get("/items/{item_id}", response_model=schemas.Item)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await crud.get_item(db, item_id=item_id)
    return item

@app.get("/cache/{key}")
async def get_cache_value(key: str):
    value = await redis_cache.get_redis_value(key)
    return {"key": key, "value": value}
