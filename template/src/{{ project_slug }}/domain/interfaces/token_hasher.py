from typing import Protocol


class TokenHasher(Protocol):
    """Hashes opaque refresh tokens before lookup or persistence."""

    def hash(self, raw_token: str) -> str: ...
