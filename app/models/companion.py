import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Companion(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "companions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    kind: Mapped[str] = mapped_column(String(16), nullable=False)  # "pet" | "plant"
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    species_code: Mapped[str] = mapped_column(String(64), nullable=False)
    archetype: Mapped[str | None] = mapped_column(String(64))
    stage: Mapped[str] = mapped_column(String(32), nullable=False, default="seedling")
    affinity_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    personality_vector: Mapped[dict | None] = mapped_column(JSONB)

    user: Mapped["User"] = relationship("User", back_populates="companions")  # type: ignore[name-defined]
    state_snapshot: Mapped["CompanionStateSnapshot"] = relationship(
        "CompanionStateSnapshot", back_populates="companion", uselist=False
    )
    memories: Mapped[list["CompanionMemory"]] = relationship(
        "CompanionMemory", back_populates="companion"
    )
    adventure_sessions: Mapped[list["AdventureSession"]] = relationship(
        "AdventureSession", back_populates="companion"
    )


class CompanionStateSnapshot(Base):
    __tablename__ = "companion_state_snapshots"

    companion_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companions.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    xp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    energy: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    mood_state: Mapped[str] = mapped_column(String(32), nullable=False, default="content")
    growth_state: Mapped[str] = mapped_column(String(32), nullable=False, default="sprouting")
    appearance_state: Mapped[dict | None] = mapped_column(JSONB)
    environment_state: Mapped[dict | None] = mapped_column(JSONB)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    companion: Mapped["Companion"] = relationship("Companion", back_populates="state_snapshot")


class CompanionMemory(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "companion_memories"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    companion_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("companions.id", ondelete="CASCADE"), nullable=False
    )
    memory_type: Mapped[str] = mapped_column(String(64), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    salience_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    source_event_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))

    companion: Mapped["Companion"] = relationship("Companion", back_populates="memories")


class AdventureSession(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "adventure_sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    companion_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("companions.id", ondelete="CASCADE"), nullable=False
    )
    state: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    destination_slug: Mapped[str] = mapped_column(String(128), nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    rewards_payload: Mapped[dict | None] = mapped_column(JSONB)

    companion: Mapped["Companion"] = relationship("Companion", back_populates="adventure_sessions")
