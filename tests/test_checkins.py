import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


@pytest.mark.asyncio
async def test_create_morning_checkin(client: AsyncClient, db_session: AsyncSession) -> None:
    from tests.conftest import TEST_USER_ID

    user = User(id=uuid.UUID(TEST_USER_ID), auth_provider="test")
    db_session.add(user)
    await db_session.commit()

    response = await client.post(
        "/v1/checkins",
        json={
            "checkin_type": "morning",
            "mood_score": 7,
            "mood_label": "hopeful",
            "energy_level": 6,
            "intention_text": "Stay present today",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["checkin_type"] == "morning"
    assert data["mood_score"] == 7
    assert "companion_reaction" in data
