from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GetAllItems(BaseModel):
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    quantity: int
