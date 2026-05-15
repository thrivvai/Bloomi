from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.events import EventContext, EventName
from app.models.analytics import EventLog


async def log_event(
    db: AsyncSession,
    event_name: EventName | str,
    ctx: EventContext,
    **props: Any,
) -> None:
    entry = EventLog(
        user_id=ctx.user_id,
        session_id=ctx.session_id,
        event_name=str(event_name),
        props={k: str(v) for k, v in props.items() if v is not None} or None,
    )
    db.add(entry)
