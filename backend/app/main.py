from fastapi import FastAPI

from .exceptions import add_exception_handlers
from .routes.auth_routes import router

app = FastAPI()

add_exception_handlers(app)

app.include_router(router)
