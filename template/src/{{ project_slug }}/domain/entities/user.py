from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class User:
    """Registered user. `hashed_password` never leaves the application layer.

    >>> user = User(id=UUID(int=1), email="a@b.com", hashed_password="x")
    >>> user.email
    'a@b.com'
    """

    id: UUID
    email: str
    hashed_password: str

    def __post_init__(self) -> None:
        if "@" not in self.email:
            raise ValueError(f"email must contain '@', got {self.email!r}")
