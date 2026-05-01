import uuid
from datetime import date, datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.events import EventContext, EventName
from app.models.practice import DailyCheckin, MoodEntry
from app.schemas.checkins import CheckinCreate, CheckinResponse
from app.services.event_log import log_event

_COMPANION_REACTIONS = {
    "morning": "Your Bloomi stretches and smiles at you.",
    "day": "Your Bloomi feels the warmth of your check-in.",
    "evening": "Your Bloomi settles in peacefully alongside you.",
}


async def create_checkin(
    db: AsyncSession, user_id: str, payload: CheckinCreate
) -> CheckinResponse:
    uid = uuid.UUID(user_id)
    today = date.today()

    checkin = DailyCheckin(
        user_id=uid,
        checkin_date=today,
        checkin_type=payload.checkin_type,
        mood_score=payload.mood_score,
        mood_label=payload.mood_label,
        energy_level=payload.energy_level,
        intention_text=payload.intention_text,
        gratitude_text=payload.gratitude_text,
        stress_score=payload.stress_score,
    )
    db.add(checkin)

    if payload.mood_score is not None:
        db.add(MoodEntry(
            user_id=uid,
            source="checkin",
            mood_score=payload.mood_score,
            mood_label=payload.mood_label,
        ))

    await db.commit()
    await db.refresh(checkin)

    ctx = EventContext(user_id=uid)
    await log_event(
        db, EventName.CHECKIN_COMPLETED, ctx,
        checkin_type=payload.checkin_type,
        mood_score=payload.mood_score,
    )
    await db.commit()

    reaction = _COMPANION_REACTIONS.get(payload.checkin_type, "Your Bloomi glows softly.")

    return CheckinResponse(
        id=str(checkin.id),
        checkin_date=checkin.checkin_date,
        checkin_type=checkin.checkin_type,
        mood_score=checkin.mood_score,
        mood_label=checkin.mood_label,
        energy_level=checkin.energy_level,
        intention_text=checkin.intention_text,
        companion_reaction=reaction,
        created_at=checkin.created_at,
    )
