import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.companion import Companion, CompanionStateSnapshot
from app.models.user import User
from app.models.wallet import WalletAccount


async def _seed_user_with_companion(db: AsyncSession, user_id: str) -> None:
    uid = uuid.UUID(user_id)
    user = User(id=uid, auth_provider="test")
    db.add(user)
    companion = Companion(
        user_id=uid, kind="pet", name="Pip", species_code="test_species", stage="seedling"
    )
    db.add(companion)
    await db.flush()
    db.add(CompanionStateSnapshot(companion_id=companion.id))
    db.add(WalletAccount(user_id=uid, wallet_type="energy", balance=0))
    db.add(WalletAccount(user_id=uid, wallet_type="coins", balance=0))
    await db.commit()


@pytest.mark.asyncio
async def test_create_and_list_goals(client: AsyncClient, db_session: AsyncSession) -> None:
    from tests.conftest import TEST_USER_ID

    await _seed_user_with_companion(db_session, TEST_USER_ID)

    create_resp = await client.post(
        "/v1/goals",
        json={"title": "Morning stretch", "goal_type": "habit", "cadence": "daily"},
    )
    assert create_resp.status_code == 201
    goal = create_resp.json()
    assert goal["title"] == "Morning stretch"
    assert goal["active"] is True

    list_resp = await client.get("/v1/goals")
    assert list_resp.status_code == 200
    goals = list_resp.json()
    assert any(g["title"] == "Morning stretch" for g in goals)


@pytest.mark.asyncio
async def test_complete_goal_awards_rewards(client: AsyncClient, db_session: AsyncSession) -> None:
    from tests.conftest import TEST_USER_ID

    create_resp = await client.post(
        "/v1/goals",
        json={"title": "Read 10 pages", "goal_type": "habit", "difficulty_tier": "easy"},
    )
    assert create_resp.status_code == 201
    goal_id = create_resp.json()["id"]

    complete_resp = await client.post(
        f"/v1/goals/{goal_id}/complete",
        json={"mood_before": 5, "mood_after": 7},
    )
    assert complete_resp.status_code == 200
    data = complete_resp.json()
    assert data["energy_awarded"] > 0
    assert data["coins_awarded"] > 0
    assert data["companion_reaction"] in ("happy", "level_up")
