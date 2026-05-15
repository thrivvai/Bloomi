from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


class CheckinCreate(BaseModel):
    checkin_type: Literal["morning", "day", "evening"]
    mood_score: int | None = Field(None, ge=1, le=10)
    mood_label: str | None = None
    energy_level: int | None = Field(None, ge=1, le=10)
    intention_text: str | None = Field(None, max_length=512)
    gratitude_text: str | None = Field(None, max_length=512)
    stress_score: int | None = Field(None, ge=1, le=10)


class CheckinResponse(BaseModel):
    id: str
    checkin_date: date
    checkin_type: str
    mood_score: int | None
    mood_label: str | None
    energy_level: int | None
    intention_text: str | None
    companion_reaction: str
    created_at: datetime
