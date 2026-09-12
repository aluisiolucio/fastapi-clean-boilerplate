import hashlib


class Sha256TokenHasher:
    """SHA-256 hex digest of an opaque refresh token."""

    def hash(self, raw_token: str) -> str:
        return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
