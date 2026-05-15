from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user_id
from app.schemas.journal import JournalEntryCreate, JournalEntryResponse, WeeklySummaryResponse
from app.services import journal as journal_svc

router = APIRouter(prefix="/v1", tags=["journal"])


@router.post("/journal-entries", response_model=JournalEntryResponse, status_code=201)
async def create_journal_entry(
    payload: JournalEntryCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> JournalEntryResponse:
    return await journal_svc.create_entry(db, user_id, payload)


@router.get("/insights/weekly-summary", response_model=WeeklySummaryResponse)
async def weekly_summary(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> WeeklySummaryResponse:
    return await journal_svc.weekly_summary(db, user_id)
