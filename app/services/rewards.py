"""
Reward resolution engine. Determines energy and coin awards for completed actions
and updates companion progression state.
"""

import uuid
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.companion import Companion, CompanionStateSnapshot
from app.models.wallet import WalletAccount, WalletTransaction

_DIFFICULTY_ENERGY = {"easy": 10, "medium": 20, "hard": 35}
_DIFFICULTY_COINS = {"easy": 5, "medium": 12, "hard": 22}
_XP_PER_COMPLETION = {"easy": 15, "medium": 30, "hard": 55}
_LEVEL_XP_THRESHOLD = 100  # flat for now; can be a curve later


@dataclass
class RewardResult:
    energy_awarded: int
    coins_awarded: int
    xp_awarded: int
    level_up: bool
    companion_reaction: str


async def resolve_goal_reward(
    db: AsyncSession,
    user_id: uuid.UUID,
    difficulty_tier: str,
    companion_id: uuid.UUID,
) -> RewardResult:
    energy = _DIFFICULTY_ENERGY.get(difficulty_tier, 10)
    coins = _DIFFICULTY_COINS.get(difficulty_tier, 5)
    xp = _XP_PER_COMPLETION.get(difficulty_tier, 15)

    await _credit_wallet(db, user_id, "energy", energy, "goal_completion")
    await _credit_wallet(db, user_id, "coins", coins, "goal_completion")

    level_up = await _apply_xp(db, companion_id, xp)

    reaction = "level_up" if level_up else "happy"
    return RewardResult(
        energy_awarded=energy,
        coins_awarded=coins,
        xp_awarded=xp,
        level_up=level_up,
        companion_reaction=reaction,
    )


async def _credit_wallet(
    db: AsyncSession,
    user_id: uuid.UUID,
    wallet_type: str,
    amount: int,
    reference_type: str,
) -> None:
    result = await db.execute(
        select(WalletAccount).where(
            WalletAccount.user_id == user_id,
            WalletAccount.wallet_type == wallet_type,
        )
    )
    wallet = result.scalar_one_or_none()
    if not wallet:
        wallet = WalletAccount(user_id=user_id, wallet_type=wallet_type, balance=0)
        db.add(wallet)
        await db.flush()

    wallet.balance += amount
    db.add(WalletTransaction(
        wallet_id=wallet.id,
        transaction_type="credit",
        amount=amount,
        reference_type=reference_type,
    ))


async def _apply_xp(db: AsyncSession, companion_id: uuid.UUID, xp: int) -> bool:
    result = await db.execute(
        select(CompanionStateSnapshot).where(CompanionStateSnapshot.companion_id == companion_id)
    )
    snap = result.scalar_one_or_none()
    if not snap:
        return False

    snap.xp += xp
    level_up = False
    while snap.xp >= _LEVEL_XP_THRESHOLD:
        snap.xp -= _LEVEL_XP_THRESHOLD
        snap.level += 1
        level_up = True

    return level_up
