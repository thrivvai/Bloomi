import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.errors import NotFoundError
from app.models.companion import Companion
from app.models.practice import Goal
from app.models.wallet import WalletAccount
from app.schemas.home import (
    CompanionExpressionState,
    HomeStateResponse,
    QuickAction,
    WalletBalance,
)

_GREETINGS_BY_TONE: dict[str, list[str]] = {
    "calm": ["A gentle moment just for you.", "Take it slow today."],
    "playful": ["Ready for a little fun?", "Your Bloomi is excited to see you!"],
    "grounded": ["Good to have you back.", "Let's keep it steady today."],
    "warm": ["You came back. That matters.", "Your Bloomi noticed the care you gave yourself."],
}
_DEFAULT_GREETINGS = ["A tiny step still counts.", "Let's keep this gentle today."]


async def build_home_state(db: AsyncSession, user_id: str) -> HomeStateResponse:
    uid = uuid.UUID(user_id)

    companion_result = await db.execute(
        select(Companion)
        .where(Companion.user_id == uid)
        .options(selectinload(Companion.state_snapshot))
        .limit(1)
    )
    companion = companion_result.scalar_one_or_none()
    if not companion:
        raise NotFoundError("Companion")

    snap = companion.state_snapshot

    wallets_result = await db.execute(
        select(WalletAccount).where(WalletAccount.user_id == uid)
    )
    wallets = wallets_result.scalars().all()

    active_goals_result = await db.execute(
        select(Goal).where(Goal.user_id == uid, Goal.active == True).limit(5)  # noqa: E712
    )
    active_goals = active_goals_result.scalars().all()

    quick_actions: list[QuickAction] = [
        QuickAction(action_type="checkin", title="Morning check-in", duration_seconds=60),
        QuickAction(action_type="breathwork", title="Quick breath reset", duration_seconds=20),
    ]
    for goal in active_goals:
        quick_actions.append(
            QuickAction(
                action_type="goal",
                title=goal.title,
                duration_seconds=(goal.duration_minutes or 5) * 60,
                goal_id=str(goal.id),
            )
        )

    companion_state = CompanionExpressionState(
        companion_id=str(companion.id),
        kind=companion.kind,
        name=companion.name,
        stage=companion.stage,
        mood_state=snap.mood_state if snap else "content",
        growth_state=snap.growth_state if snap else "sprouting",
        energy=snap.energy if snap else 100,
        level=snap.level if snap else 1,
        xp=snap.xp if snap else 0,
        appearance_state=snap.appearance_state if snap else None,
        environment_state=snap.environment_state if snap else None,
    )

    import random

    greeting = random.choice(_DEFAULT_GREETINGS)

    return HomeStateResponse(
        companion=companion_state,
        quick_actions=quick_actions[:6],
        wallet_balances=[WalletBalance(wallet_type=w.wallet_type, balance=w.balance) for w in wallets],
        suggested_next_action=quick_actions[0] if quick_actions else None,
        contextual_greeting=greeting,
    )
