from fastapi import APIRouter

from . import get_all_orders, get_order_by_id

router = APIRouter()

router.include_router(get_all_orders.router)
router.include_router(get_order_by_id.router)
