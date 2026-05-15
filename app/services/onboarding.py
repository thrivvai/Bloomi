import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.events import EventContext, EventName
from app.models.companion import Companion, CompanionStateSnapshot
from app.models.practice import Goal
from app.models.user import UserProfile
from app.models.wallet import WalletAccount
from app.schemas.onboarding import OnboardingCompleteRequest, OnboardingCompleteResponse
from app.services.event_log import log_event


async def complete_onboarding(
    db: AsyncSession,
    user_id: str,
    payload: OnboardingCompleteRequest,
) -> OnboardingCompleteResponse:
    uid = uuid.UUID(user_id)

    profile = UserProfile(
        user_id=uid,
        companion_kind=payload.companion_kind,
        onboarding_archetype=payload.archetype,
        emotional_tone_pref=payload.emotional_tone_pref,
        timezone=payload.timezone,
        age_band=payload.age_band,
        notifications_enabled=payload.notifications_enabled,
        notification_quiet_start=payload.notification_quiet_start,
        notification_quiet_end=payload.notification_quiet_end,
    )
    db.add(profile)

    companion = Companion(
        user_id=uid,
        kind=payload.companion_kind,
        name=payload.companion_name,
        species_code=payload.species_code,
        archetype=payload.archetype,
        stage="seedling",
        affinity_score=0,
    )
    db.add(companion)
    await db.flush()

    snapshot = CompanionStateSnapshot(
        companion_id=companion.id,
        level=1,
        xp=0,
        energy=100,
        mood_state="content",
        growth_state="sprouting",
    )
    db.add(snapshot)

    for wallet_type in ("energy", "coins"):
        db.add(WalletAccount(user_id=uid, wallet_type=wallet_type, balance=0))

    goals_created = 0
    for g in payload.starter_goals:
        db.add(
            Goal(
                user_id=uid,
                goal_type="habit",
                title=g.title,
                cadence=g.cadence,
                category=g.category,
                difficulty_tier="easy",
                source="onboarding",
            )
        )
        goals_created += 1

    await db.commit()

    ctx = EventContext(user_id=uid)
    await log_event(db, EventName.ONBOARDING_COMPLETED, ctx, companion_kind=payload.companion_kind)

    return OnboardingCompleteResponse(
        user_id=user_id,
        companion_id=str(companion.id),
        companion_kind=payload.companion_kind,
        companion_name=payload.companion_name,
        stage="seedling",
        goals_created=goals_created,
    )
