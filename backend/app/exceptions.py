from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from firebase_admin import auth


# Handle Invalid ID Token error (401 Unauthorized)
async def invalid_token_exception_handler(request: Request, exc: auth.InvalidIdTokenError):
    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid authentication token."}
    )


# Handle Expired ID Token error (401 Unauthorized)
async def expired_token_exception_handler(request: Request, exc: auth.ExpiredIdTokenError):
    return JSONResponse(
        status_code=401,
        content={"detail": "The authentication token has expired."}
    )


# Handle Revoked ID Token error (401 Unauthorized)
async def revoked_token_exception_handler(request: Request, exc: auth.RevokedIdTokenError):
    return JSONResponse(
        status_code=401,
        content={"detail": "The authentication token has been revoked."}
    )


# Handle public certificate fetch errors (500 Internal Server Error)
async def certificate_fetch_error_handler(request: Request, exc: auth.CertificateFetchError):
    return JSONResponse(
        status_code=500,
        content={"detail": "Error fetching authentication certificate."}
    )


# Handle FastAPI's request validation errors (422 Unprocessable Entity)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body}
    )


# General handler for HTTP exceptions (e.g., 400 Bad Request, 403 Forbidden, 404 Not Found)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


# General handler for uncaught exceptions (500 Internal Server Error)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"An internal server error occurred: {exc}"}
    )


def add_exception_handlers(app):
    app.add_exception_handler(auth.InvalidIdTokenError, invalid_token_exception_handler)
    app.add_exception_handler(auth.ExpiredIdTokenError, expired_token_exception_handler)
    app.add_exception_handler(auth.RevokedIdTokenError, revoked_token_exception_handler)
    app.add_exception_handler(auth.CertificateFetchError, certificate_fetch_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
