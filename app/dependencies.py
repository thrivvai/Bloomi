from typing import AsyncGenerator

from fastapi import Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    factory = get_session_factory()
    async with factory() as session:
        yield session


async def get_current_user_id(x_user_id: str = Header(...)) -> str:
    """
    Stub auth dependency. In production this validates a Supabase JWT and
    extracts the user UUID. For local dev, pass `X-User-Id: <uuid>` header.
    """
    if not x_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing X-User-Id")
    return x_user_id
