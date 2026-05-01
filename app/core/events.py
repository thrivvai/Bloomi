"""
Analytics event taxonomy and logging interface.
Events are written to the event_log table and can be streamed to a warehouse.
"""

from enum import StrEnum
from typing import Any
from uuid import UUID


class EventName(StrEnum):
    # Engagement
    APP_OPENED = "app_opened"
    SESSION_STARTED = "session_started"
    NOTIFICATION_OPENED = "notification_opened"

    # Emotional
    MOOD_LOGGED = "mood_logged"
    REFLECTION_COMPLETED = "reflection_completed"
    STRESS_CHECK_FINISHED = "stress_check_finished"

    # Practice
    GOAL_COMPLETED = "goal_completed"
    BREATHWORK_FINISHED = "breathwork_finished"
    PHOTO_PROOF_SUBMITTED = "photo_proof_submitted"
    CHECKIN_COMPLETED = "checkin_completed"
    JOURNAL_ENTRY_SAVED = "journal_entry_saved"

    # Economy
    ENERGY_AWARDED = "energy_awarded"
    ITEM_PURCHASED = "item_purchased"
    OUTFIT_EQUIPPED = "outfit_equipped"

    # Companion
    GROWTH_STARTED = "growth_started"
    STAGE_UPGRADED = "stage_upgraded"
    MEMORY_CREATED = "memory_created"

    # Onboarding
    ONBOARDING_COMPLETED = "onboarding_completed"
    COMPANION_CHOSEN = "companion_chosen"

    # AI
    CHAT_STARTED = "chat_started"
    PROMPT_SERVED = "prompt_served"
    SAFETY_REDIRECT_TRIGGERED = "safety_redirect_triggered"


def build_event_props(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


class EventContext:
    """Carries per-request identifiers bound into each event."""

    def __init__(self, user_id: UUID | None = None, session_id: str | None = None) -> None:
        self.user_id = user_id
        self.session_id = session_id
