from pwdlib import PasswordHash

from ...domain.interfaces.password_hasher import PasswordHasher


class PwdlibPasswordHasher(PasswordHasher):
    """Argon2 via pwdlib.recommended().

    >>> PwdlibPasswordHasher().verify("secret", PwdlibPasswordHasher().hash("secret"))
    True
    """

    def __init__(self) -> None:
        self._password_hash = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        return self._password_hash.hash(password)

    def verify(self, password: str, hashed: str) -> bool:
        return self._password_hash.verify(password, hashed)
