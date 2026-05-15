from typing import Literal

from pydantic import BaseModel, Field


class StarterGoal(BaseModel):
    title: str = Field(min_length=1, max_length=256)
    category: str | None = None
    cadence: Literal["daily", "weekly", "once"] = "daily"


class OnboardingCompleteRequest(BaseModel):
    companion_kind: Literal["pet", "plant"]
    companion_name: str = Field(min_length=1, max_length=128)
    species_code: str = Field(min_length=1, max_length=64)
    archetype: str | None = None
    emotional_tone_pref: Literal["calm", "playful", "grounded", "warm"] | None = None
    timezone: str = "UTC"
    age_band: Literal["under_18", "18_24", "25_34", "35_44", "45_plus"] | None = None
    starter_goals: list[StarterGoal] = Field(default_factory=list, max_length=5)
    notifications_enabled: bool = True
    notification_quiet_start: str | None = Field(None, pattern=r"^\d{2}:\d{2}$")
    notification_quiet_end: str | None = Field(None, pattern=r"^\d{2}:\d{2}$")


class OnboardingCompleteResponse(BaseModel):
    user_id: str
    companion_id: str
    companion_kind: str
    companion_name: str
    stage: str
    goals_created: int
