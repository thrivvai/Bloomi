import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


@pytest.mark.asyncio
async def test_complete_onboarding_pet(client: AsyncClient, db_session: AsyncSession) -> None:
    from tests.conftest import TEST_USER_ID

    user = User(id=uuid.UUID(TEST_USER_ID), auth_provider="test")
    db_session.add(user)
    await db_session.commit()

    response = await client.post(
        "/v1/onboarding/complete",
        json={
            "companion_kind": "pet",
            "companion_name": "Fern",
            "species_code": "fluffy_bean",
            "archetype": "adventurer",
            "emotional_tone_pref": "warm",
            "timezone": "America/New_York",
            "starter_goals": [
                {"title": "Drink water", "cadence": "daily"},
                {"title": "Go outside", "cadence": "daily"},
            ],
            "notifications_enabled": True,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["companion_kind"] == "pet"
    assert data["companion_name"] == "Fern"
    assert data["stage"] == "seedling"
    assert data["goals_created"] == 2


@pytest.mark.asyncio
async def test_complete_onboarding_plant(client: AsyncClient, db_session: AsyncSession) -> None:
    from tests.conftest import TEST_USER_ID

    response = await client.post(
        "/v1/onboarding/complete",
        json={
            "companion_kind": "plant",
            "companion_name": "Moss",
            "species_code": "monstera",
            "emotional_tone_pref": "calm",
            "timezone": "Europe/London",
            "starter_goals": [],
            "notifications_enabled": False,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["companion_kind"] == "plant"
    assert data["companion_name"] == "Moss"
