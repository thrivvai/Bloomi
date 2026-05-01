from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class GoalCreate(BaseModel):
    title: str = Field(min_length=1, max_length=256)
    goal_type: Literal["habit", "one_off"] = "habit"
    cadence: Literal["daily", "weekly", "once"] | None = "daily"
    difficulty_tier: Literal["easy", "medium", "hard"] = "easy"
    duration_minutes: int | None = Field(None, ge=1, le=480)
    category: str | None = None
    proof_requirement: Literal["none", "photo", "text", "optional_photo"] = "none"


class GoalResponse(BaseModel):
    id: str
    user_id: str
    title: str
    goal_type: str
    cadence: str | None
    difficulty_tier: str
    duration_minutes: int | None
    category: str | None
    proof_requirement: str
    active: bool
    source: str
    created_at: datetime


class GoalCompleteRequest(BaseModel):
    mood_before: int | None = Field(None, ge=1, le=10)
    mood_after: int | None = Field(None, ge=1, le=10)
    proof_asset_id: UUID | None = None
    proof_type: Literal["photo", "text"] | None = None


class GoalCompleteResponse(BaseModel):
    completion_id: str
    energy_awarded: int
    coins_awarded: int
    companion_reaction: str
    level_up: bool = False
