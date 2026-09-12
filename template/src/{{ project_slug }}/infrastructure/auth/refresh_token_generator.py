import secrets
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from ...domain.entities.auth_tokens import GeneratedRefreshToken
from ...domain.entities.refresh_token import RefreshToken
from .sha256_token_hasher import Sha256TokenHasher


class SecureRefreshTokenGenerator:
    """Cryptographic opaque token; only the hash is persisted.

    >>> gen = SecureRefreshTokenGenerator(expire_days=7, hasher=Sha256TokenHasher())
    >>> issued = gen.generate(UUID(int=1))
    >>> len(issued.plaintext) > 20
    True
    """

    def __init__(self, expire_days: int, hasher: Sha256TokenHasher) -> None:
        self._expire_days = expire_days
        self._hasher = hasher

    def generate(self, user_id: UUID) -> GeneratedRefreshToken:
        plaintext = secrets.token_urlsafe(32)
        entity = RefreshToken(
            id=uuid4(),
            user_id=user_id,
            token_hash=self._hasher.hash(plaintext),
            expires_at=datetime.now(UTC) + timedelta(days=self._expire_days),
            revoked_at=None,
            replaced_by_id=None,
        )
        return GeneratedRefreshToken(plaintext=plaintext, entity=entity)
