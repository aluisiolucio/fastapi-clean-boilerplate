from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from ...domain.exceptions import (
    DomainError,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidTokenError,
    ItemNotFoundError,
    RefreshTokenReuseError,
)

_STATUS: dict[type[DomainError], int] = {
    ItemNotFoundError: 404,
    EmailAlreadyExistsError: 409,
    InvalidCredentialsError: 401,
    InvalidTokenError: 401,
    RefreshTokenReuseError: 401,
}


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, _domain_error_handler)


async def _domain_error_handler(_request: Request, exc: Exception) -> JSONResponse:
    status = _STATUS.get(type(exc), 400)
    return JSONResponse(status_code=status, content={"detail": str(exc)})
