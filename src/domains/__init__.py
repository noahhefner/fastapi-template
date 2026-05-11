from fastapi import APIRouter

from . import items, orders

router = APIRouter()

router.include_router(
    items.router,
    prefix="/items",
    tags=["items"],
)

router.include_router(
    orders.router,
    prefix="/orders",
    tags=["orders"],
)
