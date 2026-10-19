from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints

ItemName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=255),
]


class ItemCreate(BaseModel):
    name: ItemName
    description: str = Field(default="", max_length=5000)


class ItemUpdate(BaseModel):
    name: ItemName | None = None
    description: str | None = Field(default=None, max_length=5000)


class ItemResponse(BaseModel):
    id: UUID
    name: str
    description: str
