from fastapi import APIRouter

from . import get_all_items, get_item_by_id

router = APIRouter(prefix="/api/items", tags=["items"])


router.include_router(get_all_items.router)
router.include_router(get_item_by_id.router)
