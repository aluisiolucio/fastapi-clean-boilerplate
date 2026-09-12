from typing import Protocol
from uuid import UUID


class TokenService(Protocol):
    """Encodes and decodes access JWTs only. Refresh tokens are opaque."""

    def encode_access_token(self, user_id: UUID) -> str: ...

    def decode_access_token(self, token: str) -> UUID: ...
