from fastapi import FastAPI
from .routes.auth_routes import router
from .exceptions import add_exception_handlers

app = FastAPI()

add_exception_handlers(app)

app.include_router(router)
