"""
Seed script: populates starter companion species, catalog items, and seeded goals.
Run with: python -m scripts.seed
"""

import asyncio
import uuid

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings
from app.models.catalog import CatalogItem

CATALOG_ITEMS = [
    # Pet outfits
    {"item_type": "outfit", "slug": "pet-cozy-sweater", "name": "Cozy Sweater", "rarity": "common", "price_currency": "coins", "price_amount": 50, "companion_kind_scope": "pet_only"},
    {"item_type": "outfit", "slug": "pet-adventurer-cape", "name": "Adventurer Cape", "rarity": "rare", "price_currency": "coins", "price_amount": 150, "companion_kind_scope": "pet_only"},
    {"item_type": "accessory", "slug": "pet-flower-crown", "name": "Flower Crown", "rarity": "common", "price_currency": "coins", "price_amount": 40, "companion_kind_scope": "pet_only"},

    # Plant items
    {"item_type": "pot", "slug": "plant-terracotta-pot", "name": "Terracotta Pot", "rarity": "common", "price_currency": "coins", "price_amount": 30, "companion_kind_scope": "plant_only"},
    {"item_type": "pot", "slug": "plant-ceramic-moon-pot", "name": "Ceramic Moon Pot", "rarity": "rare", "price_currency": "coins", "price_amount": 120, "companion_kind_scope": "plant_only"},
    {"item_type": "background", "slug": "plant-windowsill-shelf", "name": "Windowsill Shelf", "rarity": "common", "price_currency": "coins", "price_amount": 60, "companion_kind_scope": "plant_only"},

    # Shared room items
    {"item_type": "room_item", "slug": "shared-fairy-lights", "name": "Fairy Lights", "rarity": "common", "price_currency": "coins", "price_amount": 35, "companion_kind_scope": "all"},
    {"item_type": "room_item", "slug": "shared-cozy-rug", "name": "Cozy Rug", "rarity": "common", "price_currency": "coins", "price_amount": 45, "companion_kind_scope": "all"},
    {"item_type": "theme", "slug": "shared-golden-hour", "name": "Golden Hour Theme", "rarity": "rare", "price_currency": "coins", "price_amount": 200, "companion_kind_scope": "all"},
]


async def seed(session: AsyncSession) -> None:
    for item_data in CATALOG_ITEMS:
        item = CatalogItem(
            id=uuid.uuid4(),
            item_type=item_data["item_type"],
            slug=item_data["slug"],
            name=item_data["name"],
            rarity=item_data["rarity"],
            price_currency=item_data["price_currency"],
            price_amount=item_data["price_amount"],
            companion_kind_scope=item_data["companion_kind_scope"],
            active=True,
        )
        session.add(item)

    await session.commit()
    print(f"Seeded {len(CATALOG_ITEMS)} catalog items.")


async def main() -> None:
    settings = get_settings()
    engine = create_async_engine(settings.database_url)
    factory = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with factory() as session:
        await seed(session)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
