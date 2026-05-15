import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.events import EventContext, EventName
from app.models.practice import JournalEntry, MoodEntry
from app.schemas.journal import JournalEntryCreate, JournalEntryResponse, WeeklySummaryResponse
from app.services.event_log import log_event


async def create_entry(
    db: AsyncSession, user_id: str, payload: JournalEntryCreate
) -> JournalEntryResponse:
    uid = uuid.UUID(user_id)
    entry = JournalEntry(
        user_id=uid,
        prompt_id=payload.prompt_id,
        entry_type=payload.entry_type,
        body_text=payload.body_text,
        tags=payload.tags,
    )
    db.add(entry)

    if payload.mood_after is not None:
        db.add(MoodEntry(
            user_id=uid,
            source="journal",
            mood_score=payload.mood_after,
        ))

    await db.commit()
    await db.refresh(entry)

    ctx = EventContext(user_id=uid)
    await log_event(db, EventName.JOURNAL_ENTRY_SAVED, ctx, entry_type=payload.entry_type)
    await db.commit()

    return JournalEntryResponse(
        id=str(entry.id),
        entry_type=entry.entry_type,
        prompt_id=entry.prompt_id,
        body_text=entry.body_text,
        tags=entry.tags,
        created_at=entry.created_at,
    )


async def weekly_summary(db: AsyncSession, user_id: str) -> WeeklySummaryResponse:
    uid = uuid.UUID(user_id)
    now = datetime.now(tz=timezone.utc)
    week_start = now - timedelta(days=7)

    mood_result = await db.execute(
        select(func.avg(MoodEntry.mood_score)).where(
            MoodEntry.user_id == uid,
            MoodEntry.created_at >= week_start,
        )
    )
    mood_avg = mood_result.scalar()

    return WeeklySummaryResponse(
        week_start=week_start.date().isoformat(),
        week_end=now.date().isoformat(),
        mood_average=round(float(mood_avg), 1) if mood_avg else None,
        mood_trend=None,
        completions_count=0,
        top_wins=[],
        reflection_highlights=[],
        reset_suggestion="A gentle reset is always available.",
        companion_retelling="Your Bloomi held space for you this week.",
    )
