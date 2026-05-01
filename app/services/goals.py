import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError, ForbiddenError
from app.core.events import EventContext, EventName
from app.models.companion import Companion
from app.models.practice import Goal, GoalCompletion
from app.schemas.goals import (
    GoalCompleteRequest,
    GoalCompleteResponse,
    GoalCreate,
    GoalResponse,
)
from app.services.event_log import log_event
from app.services.rewards import resolve_goal_reward


async def create_goal(db: AsyncSession, user_id: str, payload: GoalCreate) -> GoalResponse:
    uid = uuid.UUID(user_id)
    goal = Goal(
        user_id=uid,
        goal_type=payload.goal_type,
        title=payload.title,
        cadence=payload.cadence,
        difficulty_tier=payload.difficulty_tier,
        duration_minutes=payload.duration_minutes,
        category=payload.category,
        proof_requirement=payload.proof_requirement,
        source="user",
    )
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    return _to_response(goal)


async def list_goals(db: AsyncSession, user_id: str) -> list[GoalResponse]:
    uid = uuid.UUID(user_id)
    result = await db.execute(
        select(Goal).where(Goal.user_id == uid, Goal.active == True).order_by(Goal.created_at)  # noqa: E712
    )
    return [_to_response(g) for g in result.scalars().all()]


async def complete_goal(
    db: AsyncSession, user_id: str, goal_id: str, payload: GoalCompleteRequest
) -> GoalCompleteResponse:
    uid = uuid.UUID(user_id)
    gid = uuid.UUID(goal_id)

    result = await db.execute(select(Goal).where(Goal.id == gid))
    goal = result.scalar_one_or_none()
    if not goal:
        raise NotFoundError("Goal", goal_id)
    if goal.user_id != uid:
        raise ForbiddenError()

    companion_result = await db.execute(
        select(Companion).where(Companion.user_id == uid).limit(1)
    )
    companion = companion_result.scalar_one_or_none()
    if not companion:
        raise NotFoundError("Companion")

    reward = await resolve_goal_reward(db, uid, goal.difficulty_tier, companion.id)

    completion = GoalCompletion(
        goal_id=gid,
        user_id=uid,
        proof_type=payload.proof_type,
        proof_asset_id=payload.proof_asset_id,
        mood_before=payload.mood_before,
        mood_after=payload.mood_after,
        energy_awarded=reward.energy_awarded,
        coins_awarded=reward.coins_awarded,
    )
    db.add(completion)
    await db.commit()
    await db.refresh(completion)

    ctx = EventContext(user_id=uid)
    await log_event(
        db, EventName.GOAL_COMPLETED, ctx,
        goal_id=goal_id, difficulty=goal.difficulty_tier
    )
    await db.commit()

    return GoalCompleteResponse(
        completion_id=str(completion.id),
        energy_awarded=reward.energy_awarded,
        coins_awarded=reward.coins_awarded,
        companion_reaction=reward.companion_reaction,
        level_up=reward.level_up,
    )


async def initiate_proof_upload(db: AsyncSession, user_id: str, goal_id: str) -> dict:
    # Returns a pre-signed upload URL placeholder; real impl hooks into Supabase Storage.
    return {
        "upload_url": f"/v1/goals/{goal_id}/proof-assets/upload",
        "asset_type": "photo",
        "expires_in_seconds": 300,
    }


def _to_response(goal: Goal) -> GoalResponse:
    return GoalResponse(
        id=str(goal.id),
        user_id=str(goal.user_id),
        title=goal.title,
        goal_type=goal.goal_type,
        cadence=goal.cadence,
        difficulty_tier=goal.difficulty_tier,
        duration_minutes=goal.duration_minutes,
        category=goal.category,
        proof_requirement=goal.proof_requirement,
        active=goal.active,
        source=goal.source,
        created_at=goal.created_at,
    )
