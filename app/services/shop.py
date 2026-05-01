import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ConflictError, NotFoundError
from app.models.catalog import CatalogItem, UserInventory
from app.models.companion import Companion, CompanionStateSnapshot
from app.models.wallet import WalletAccount, WalletTransaction
from app.schemas.shop import (
    CatalogItemResponse,
    EquipRequest,
    EquipResponse,
    PurchaseRequest,
    PurchaseResponse,
    ShopCatalogResponse,
)


async def get_catalog(db: AsyncSession, user_id: str) -> ShopCatalogResponse:
    uid = uuid.UUID(user_id)

    companion_result = await db.execute(
        select(Companion).where(Companion.user_id == uid).limit(1)
    )
    companion = companion_result.scalar_one_or_none()
    kind = companion.kind if companion else "all"

    result = await db.execute(
        select(CatalogItem).where(
            CatalogItem.active == True,  # noqa: E712
            CatalogItem.companion_kind_scope.in_(["all", f"{kind}_only"]),
        )
    )
    items = result.scalars().all()
    item_responses = [_catalog_item_to_response(i) for i in items]

    return ShopCatalogResponse(items=item_responses, featured=item_responses[:3])


async def purchase_item(
    db: AsyncSession, user_id: str, payload: PurchaseRequest
) -> PurchaseResponse:
    uid = uuid.UUID(user_id)
    item_id = uuid.UUID(payload.catalog_item_id)

    item_result = await db.execute(select(CatalogItem).where(CatalogItem.id == item_id))
    item = item_result.scalar_one_or_none()
    if not item:
        raise NotFoundError("CatalogItem", payload.catalog_item_id)

    existing = await db.execute(
        select(UserInventory).where(
            UserInventory.user_id == uid,
            UserInventory.catalog_item_id == item_id,
        )
    )
    if existing.scalar_one_or_none():
        raise ConflictError("Item already owned")

    wallet_result = await db.execute(
        select(WalletAccount).where(
            WalletAccount.user_id == uid,
            WalletAccount.wallet_type == item.price_currency,
        )
    )
    wallet = wallet_result.scalar_one_or_none()
    if not wallet or wallet.balance < item.price_amount:
        raise ConflictError("Insufficient balance")

    wallet.balance -= item.price_amount
    db.add(WalletTransaction(
        wallet_id=wallet.id,
        transaction_type="debit",
        amount=item.price_amount,
        reference_type="purchase",
        reference_id=item_id,
    ))

    inventory = UserInventory(user_id=uid, catalog_item_id=item_id, source="purchase")
    db.add(inventory)
    await db.commit()
    await db.refresh(inventory)

    return PurchaseResponse(
        inventory_id=str(inventory.id),
        catalog_item_id=str(item_id),
        balance_after=wallet.balance,
        currency=item.price_currency,
    )


async def equip_item(db: AsyncSession, user_id: str, payload: EquipRequest) -> EquipResponse:
    uid = uuid.UUID(user_id)
    inv_id = uuid.UUID(payload.inventory_id)

    inv_result = await db.execute(
        select(UserInventory).where(UserInventory.id == inv_id, UserInventory.user_id == uid)
    )
    inv = inv_result.scalar_one_or_none()
    if not inv:
        raise NotFoundError("InventoryItem", payload.inventory_id)

    inv.equipped = True
    await db.commit()

    return EquipResponse(equipped=True)


def _catalog_item_to_response(item: CatalogItem) -> CatalogItemResponse:
    return CatalogItemResponse(
        id=str(item.id),
        item_type=item.item_type,
        slug=item.slug,
        name=item.name,
        rarity=item.rarity,
        price_currency=item.price_currency,
        price_amount=item.price_amount,
        companion_kind_scope=item.companion_kind_scope,
        unlock_rules=item.unlock_rules,
    )
