from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt

from ...domain.exceptions import InvalidTokenError
from ...domain.interfaces.token_service import TokenService
from ..config.settings import Settings

_ALGORITHM = "HS256"


class JwtTokenService(TokenService):
    """HS256 access tokens. Refresh tokens are not JWTs.

    >>> JwtTokenService(settings).encode_access_token(user_id)  # doctest: +SKIP
    """

    def __init__(self, settings: Settings) -> None:
        self._secret = settings.secret_key
        self._expire_minutes = settings.access_token_expire_minutes

    def encode_access_token(self, user_id: UUID) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + timedelta(minutes=self._expire_minutes),
            "type": "access",
        }
        return jwt.encode(payload, self._secret, algorithm=_ALGORITHM)

    def decode_access_token(self, token: str) -> UUID:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[_ALGORITHM])
        except jwt.PyJWTError as exc:
            raise InvalidTokenError() from exc
        if payload.get("type") != "access":
            raise InvalidTokenError()
        subject = payload.get("sub")
        if not isinstance(subject, str):
            raise InvalidTokenError()
        try:
            return UUID(subject)
        except ValueError as exc:
            raise InvalidTokenError() from exc
