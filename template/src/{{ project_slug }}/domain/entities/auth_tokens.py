from dataclasses import dataclass
from uuid import UUID

from .refresh_token import RefreshToken


@dataclass(frozen=True)
class GeneratedRefreshToken:
    """Plaintext (returned to the client once) plus the entity to persist."""

    plaintext: str
    entity: RefreshToken


@dataclass(frozen=True)
class AuthTokens:
    """Access JWT plus opaque refresh token issued together."""

    access_token: str
    refresh_token: str
    refresh_token_id: UUID
    expires_in: int
    token_type: str = "bearer"
