import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    auth_provider: Mapped[str] = mapped_column(String(64), nullable=False, default="supabase")
    last_active_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="user", uselist=False)
    companions: Mapped[list["Companion"]] = relationship("Companion", back_populates="user")  # type: ignore[name-defined]


class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, nullable=False
    )
    display_name: Mapped[str | None] = mapped_column(String(128))
    timezone: Mapped[str] = mapped_column(String(64), nullable=False, default="UTC")
    age_band: Mapped[str | None] = mapped_column(String(32))
    companion_kind: Mapped[str | None] = mapped_column(String(16))
    onboarding_archetype: Mapped[str | None] = mapped_column(String(64))
    emotional_tone_pref: Mapped[str | None] = mapped_column(String(32))
    accessibility_prefs: Mapped[dict | None] = mapped_column(JSONB)
    notification_quiet_start: Mapped[str | None] = mapped_column(String(5))
    notification_quiet_end: Mapped[str | None] = mapped_column(String(5))
    notifications_enabled: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="profile")
