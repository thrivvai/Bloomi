import uuid
from datetime import date, datetime

from sqlalchemy import JSON, Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class DailyCheckin(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "daily_checkins"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    checkin_date: Mapped[date] = mapped_column(Date, nullable=False)
    checkin_type: Mapped[str] = mapped_column(String(32), nullable=False)  # morning | day | evening
    mood_score: Mapped[int | None] = mapped_column(Integer)
    mood_label: Mapped[str | None] = mapped_column(String(64))
    energy_level: Mapped[int | None] = mapped_column(Integer)
    intention_text: Mapped[str | None] = mapped_column(Text)
    gratitude_text: Mapped[str | None] = mapped_column(Text)
    stress_score: Mapped[int | None] = mapped_column(Integer)
    payload: Mapped[dict | None] = mapped_column(JSON)


class Goal(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "goals"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    goal_type: Mapped[str] = mapped_column(String(32), nullable=False)  # habit | one_off
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    cadence: Mapped[str | None] = mapped_column(String(32))  # daily | weekly | once
    difficulty_tier: Mapped[str] = mapped_column(String(16), nullable=False, default="easy")
    duration_minutes: Mapped[int | None] = mapped_column(Integer)
    category: Mapped[str | None] = mapped_column(String(64))
    proof_requirement: Mapped[str] = mapped_column(
        String(32), nullable=False, default="none"
    )  # none | photo | text | optional_photo
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    source: Mapped[str] = mapped_column(String(32), nullable=False, default="user")  # user | seeded

    completions: Mapped[list["GoalCompletion"]] = relationship(
        "GoalCompletion", back_populates="goal"
    )


class GoalCompletion(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "goal_completions"

    goal_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    proof_type: Mapped[str | None] = mapped_column(String(32))
    proof_asset_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("proof_assets.id", ondelete="SET NULL")
    )
    mood_before: Mapped[int | None] = mapped_column(Integer)
    mood_after: Mapped[int | None] = mapped_column(Integer)
    energy_awarded: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    coins_awarded: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSON)

    goal: Mapped["Goal"] = relationship("Goal", back_populates="completions")
    proof_asset: Mapped["ProofAsset | None"] = relationship("ProofAsset")


class ProofAsset(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "proof_assets"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    asset_type: Mapped[str] = mapped_column(String(32), nullable=False)  # photo | text
    storage_path: Mapped[str] = mapped_column(String(512), nullable=False)
    thumbnail_path: Mapped[str | None] = mapped_column(String(512))
    captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    verification_state: Mapped[str] = mapped_column(
        String(32), nullable=False, default="pending"
    )  # pending | verified | rejected
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSON)


class JournalEntry(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "journal_entries"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    prompt_id: Mapped[str | None] = mapped_column(String(128))
    entry_type: Mapped[str] = mapped_column(String(32), nullable=False, default="free")
    body_text: Mapped[str] = mapped_column(Text, nullable=False)
    sentiment_score: Mapped[float | None] = mapped_column(Float)
    tags: Mapped[list[str] | None] = mapped_column(JSON)  # ARRAY(String) on PG via migration


class MoodEntry(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "mood_entries"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    source: Mapped[str] = mapped_column(String(32), nullable=False)  # checkin | standalone | goal
    mood_score: Mapped[int] = mapped_column(Integer, nullable=False)
    mood_label: Mapped[str | None] = mapped_column(String(64))
    context: Mapped[dict | None] = mapped_column(JSON)
