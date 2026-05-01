from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user_id
from app.schemas.shop import EquipRequest, EquipResponse, PurchaseRequest, PurchaseResponse, ShopCatalogResponse
from app.services import shop as shop_svc

router = APIRouter(prefix="/v1/shop", tags=["shop"])


@router.get("/catalog", response_model=ShopCatalogResponse)
async def get_catalog(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> ShopCatalogResponse:
    return await shop_svc.get_catalog(db, user_id)


@router.post("/purchase", response_model=PurchaseResponse, status_code=201)
async def purchase_item(
    payload: PurchaseRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> PurchaseResponse:
    return await shop_svc.purchase_item(db, user_id, payload)


@router.post("/equip", response_model=EquipResponse)
async def equip_item(
    payload: EquipRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> EquipResponse:
    return await shop_svc.equip_item(db, user_id, payload)
