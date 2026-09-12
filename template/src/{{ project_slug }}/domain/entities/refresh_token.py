from dataclasses import dataclass, replace
from datetime import UTC, datetime
from uuid import UUID


@dataclass(frozen=True)
class RefreshToken:
    """Persisted refresh token. Only the hash is stored; plaintext is shown once."""

    id: UUID
    user_id: UUID
    token_hash: str
    expires_at: datetime
    revoked_at: datetime | None
    replaced_by_id: UUID | None

    def is_expired(self, now: datetime | None = None) -> bool:
        current = now or datetime.now(UTC)
        return self.expires_at <= current

    def is_revoked(self) -> bool:
        return self.revoked_at is not None

    def revoke(
        self,
        replaced_by_id: UUID | None = None,
        now: datetime | None = None,
    ) -> "RefreshToken":
        return replace(
            self,
            revoked_at=now or datetime.now(UTC),
            replaced_by_id=replaced_by_id,
        )
