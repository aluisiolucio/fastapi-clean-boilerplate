from typing import Protocol
from uuid import UUID

from ..entities.auth_tokens import GeneratedRefreshToken


class RefreshTokenGenerator(Protocol):
    def generate(self, user_id: UUID) -> GeneratedRefreshToken: ...
