from fastapi import APIRouter

from fastapi_template.domains.items import get_all_items, get_item_by_id

router = APIRouter()

router.include_router(get_all_items.router)
router.include_router(get_item_by_id.router)
