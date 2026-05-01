from datetime import datetime

from pydantic import BaseModel, Field


class CompanionStateResponse(BaseModel):
    id: str
    kind: str
    name: str
    species_code: str
    archetype: str | None
    stage: str
    affinity_score: int
    level: int
    xp: int
    energy: int
    mood_state: str
    growth_state: str
    appearance_state: dict | None
    environment_state: dict | None


class ChatMessage(BaseModel):
    role: str
    content: str


class CompanionChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    session_id: str | None = None


class CompanionChatResponse(BaseModel):
    reply: str
    tone_tag: str | None = None
    quick_replies: list[str] = []
    suggested_actions: list[dict] = []
    safety_redirected: bool = False
