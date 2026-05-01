import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.errors import NotFoundError
from app.models.companion import Companion
from app.schemas.companion import CompanionChatRequest, CompanionChatResponse, CompanionStateResponse


async def get_companion_state(db: AsyncSession, user_id: str) -> CompanionStateResponse:
    uid = uuid.UUID(user_id)
    result = await db.execute(
        select(Companion)
        .where(Companion.user_id == uid)
        .options(selectinload(Companion.state_snapshot))
        .limit(1)
    )
    companion = result.scalar_one_or_none()
    if not companion:
        raise NotFoundError("Companion")

    snap = companion.state_snapshot
    return CompanionStateResponse(
        id=str(companion.id),
        kind=companion.kind,
        name=companion.name,
        species_code=companion.species_code,
        archetype=companion.archetype,
        stage=companion.stage,
        affinity_score=companion.affinity_score,
        level=snap.level if snap else 1,
        xp=snap.xp if snap else 0,
        energy=snap.energy if snap else 100,
        mood_state=snap.mood_state if snap else "content",
        growth_state=snap.growth_state if snap else "sprouting",
        appearance_state=snap.appearance_state if snap else None,
        environment_state=snap.environment_state if snap else None,
    )


async def chat(
    db: AsyncSession, user_id: str, payload: CompanionChatRequest
) -> CompanionChatResponse:
    # Placeholder — AI orchestration module wired in Phase 5.
    # For now returns a safe stub reply so the API contract is exercisable.
    return CompanionChatResponse(
        reply="I'm here with you. What's on your mind?",
        tone_tag="warm",
        quick_replies=["Just checking in", "I need support", "Tell me something kind"],
        suggested_actions=[],
        safety_redirected=False,
    )
