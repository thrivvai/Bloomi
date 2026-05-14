import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class CatalogItem(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "catalog_items"

    item_type: Mapped[str] = mapped_column(String(64), nullable=False)  # outfit | pot | room | etc.
    slug: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    rarity: Mapped[str] = mapped_column(String(32), nullable=False, default="common")
    price_currency: Mapped[str] = mapped_column(String(16), nullable=False, default="coins")
    price_amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    unlock_rules: Mapped[dict | None] = mapped_column(JSON)
    companion_kind_scope: Mapped[str] = mapped_column(
        String(16), nullable=False, default="all"
    )  # all | pet_only | plant_only
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    inventory_entries: Mapped[list["UserInventory"]] = relationship(
        "UserInventory", back_populates="catalog_item"
    )


class UserInventory(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "user_inventory"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    catalog_item_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("catalog_items.id", ondelete="CASCADE"),
        nullable=False,
    )
    equipped: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    acquired_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    source: Mapped[str] = mapped_column(String(32), nullable=False, default="purchase")

    catalog_item: Mapped["CatalogItem"] = relationship(
        "CatalogItem", back_populates="inventory_entries"
    )
