"""Expected business failures raised by use cases."""


class DomainError(Exception):
    """Base class for recoverable domain errors."""


class CommitRequiredError(DomainError):
    """Failure whose pending changes must be committed before propagating."""


class ItemNotFoundError(DomainError):
    def __init__(self, item_id: object) -> None:
        super().__init__(f"item not found: {item_id}")
        self.item_id = item_id


class EmailAlreadyExistsError(DomainError):
    def __init__(self, email: str) -> None:
        super().__init__(f"email already registered: {email}")
        self.email = email


class InvalidCredentialsError(DomainError):
    def __init__(self) -> None:
        super().__init__("invalid email or password")


class InvalidTokenError(DomainError):
    def __init__(self) -> None:
        super().__init__("token is invalid or expired")


class RefreshTokenReuseError(CommitRequiredError):
    def __init__(self) -> None:
        super().__init__("refresh token reuse detected")
