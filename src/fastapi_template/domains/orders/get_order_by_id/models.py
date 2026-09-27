from uuid import UUID

from pydantic import BaseModel


class OrderResponse(BaseModel):
    """Response model for a single order."""

    id: UUID
    quantity: int
    item_id: UUID
