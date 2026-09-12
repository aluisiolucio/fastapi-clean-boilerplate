from dataclasses import dataclass, replace
from uuid import UUID


@dataclass(frozen=True)
class Item:
    """Catalog item identified by UUID.

    >>> item = Item(id=UUID(int=0), name="Notebook", description="A4")
    >>> item.name
    'Notebook'
    """

    id: UUID
    name: str
    description: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError(f"name must be non-empty, got {self.name!r}")

    def with_updates(self, name: str | None, description: str | None) -> "Item":
        return replace(
            self,
            name=self.name if name is None else name,
            description=self.description if description is None else description,
        )
