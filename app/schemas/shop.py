from pydantic import BaseModel


class CatalogItemResponse(BaseModel):
    id: str
    item_type: str
    slug: str
    name: str
    rarity: str
    price_currency: str
    price_amount: int
    companion_kind_scope: str
    unlock_rules: dict | None = None


class ShopCatalogResponse(BaseModel):
    items: list[CatalogItemResponse]
    featured: list[CatalogItemResponse] = []


class PurchaseRequest(BaseModel):
    catalog_item_id: str


class PurchaseResponse(BaseModel):
    inventory_id: str
    catalog_item_id: str
    balance_after: int
    currency: str


class EquipRequest(BaseModel):
    inventory_id: str


class EquipResponse(BaseModel):
    equipped: bool
    appearance_state: dict | None = None
