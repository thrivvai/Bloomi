from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user_id
from app.schemas.companion import (
    CompanionChatRequest,
    CompanionChatResponse,
    CompanionStateResponse,
)
from app.services import companion as companion_svc

router = APIRouter(prefix="/v1/companion", tags=["companion"])


@router.get("/state", response_model=CompanionStateResponse)
async def get_companion_state(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> CompanionStateResponse:
    return await companion_svc.get_companion_state(db, user_id)


@router.post("/chat", response_model=CompanionChatResponse)
async def companion_chat(
    payload: CompanionChatRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> CompanionChatResponse:
    return await companion_svc.chat(db, user_id, payload)
