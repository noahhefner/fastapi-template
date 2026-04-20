from uuid import UUID

from pydantic import BaseModel


class GetAllItems(BaseModel):
    id: UUID
    name: str
    quantity: int
