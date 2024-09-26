from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .exceptions import add_exception_handlers
from .routes.auth_routes import router

app = FastAPI()


Instrumentator().instrument(app).expose(app)

app.include_router(router)
add_exception_handlers(app)
