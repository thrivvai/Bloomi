from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class JournalEntryCreate(BaseModel):
    body_text: str = Field(min_length=1, max_length=10_000)
    entry_type: Literal["free", "guided", "reflection"] = "free"
    prompt_id: str | None = None
    tags: list[str] | None = None
    mood_after: int | None = Field(None, ge=1, le=10)


class JournalEntryResponse(BaseModel):
    id: str
    entry_type: str
    prompt_id: str | None
    body_text: str
    tags: list[str] | None
    created_at: datetime


class WeeklySummaryResponse(BaseModel):
    week_start: str
    week_end: str
    mood_average: float | None
    mood_trend: str | None
    completions_count: int
    top_wins: list[str]
    reflection_highlights: list[str]
    reset_suggestion: str | None
    companion_retelling: str
