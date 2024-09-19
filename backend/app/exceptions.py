from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from firebase_admin import auth

from .logger import log


async def invalid_token_exception_handler(request: Request, exc: auth.InvalidIdTokenError) -> JSONResponse:
    """
    Handle Invalid ID Token error (401 Unauthorized).

    :param request: The request object.
    :param exc: The exception raised for an invalid ID token.
    :return: JSON response with error details.
    """
    log.error(f"invalid id token: {exc}")
    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid authentication token."}
    )


async def expired_token_exception_handler(request: Request, exc: auth.ExpiredIdTokenError) -> JSONResponse:
    """
    Handle Expired ID Token error (401 Unauthorized).

    :param request: The request object.
    :param exc: The exception raised for an expired ID token.
    :return: JSON response with error details.
    """
    log.error(f"expired id token: {exc}")
    return JSONResponse(
        status_code=401,
        content={"detail": "The authentication token has expired."}
    )


async def revoked_token_exception_handler(request: Request, exc: auth.RevokedIdTokenError) -> JSONResponse:
    """
    Handle Revoked ID Token error (401 Unauthorized).

    :param request: The request object.
    :param exc: The exception raised for a revoked ID token.
    :return: JSON response with error details.
    """
    log.error(f"revoked id token: {exc}")
    return JSONResponse(
        status_code=401,
        content={"detail": "The authentication token has been revoked."}
    )


async def certificate_fetch_error_handler(request: Request, exc: auth.CertificateFetchError) -> JSONResponse:
    """
    Handle public certificate fetch errors (500 Internal Server Error).

    :param request: The request object.
    :param exc: The exception raised when fetching the public certificate.
    :return: JSON response with error details.
    """
    log.error(f"certificate fetch error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Error fetching authentication certificate."}
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle FastAPI's request validation errors (422 Unprocessable Entity).

    :param request: The request object.
    :param exc: The exception raised for request validation errors.
    :return: JSON response with error details.
    """
    log.error(f"validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body}
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    General handler for HTTP exceptions (e.g., 400 Bad Request, 403 Forbidden, 404 Not Found).

    :param request: The request object.
    :param exc: The HTTP exception raised.
    :return: JSON response with error details.
    """
    log.error(f"http exception: {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    General handler for uncaught exceptions (500 Internal Server Error).

    :param request: The request object.
    :param exc: The exception raised.
    :return: JSON response with error details.
    """
    log.error(f"internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"An internal server error occurred: {exc}"}
    )


def add_exception_handlers(app) -> None:
    """
    Add exception handlers to the FastAPI application.

    :param app: The FastAPI application instance.
    """
    app.add_exception_handler(auth.InvalidIdTokenError, invalid_token_exception_handler)
    app.add_exception_handler(auth.ExpiredIdTokenError, expired_token_exception_handler)
    app.add_exception_handler(auth.RevokedIdTokenError, revoked_token_exception_handler)
    app.add_exception_handler(auth.CertificateFetchError, certificate_fetch_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
