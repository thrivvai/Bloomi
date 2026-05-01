from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user_id
from app.schemas.checkins import CheckinCreate, CheckinResponse
from app.services import checkins as checkins_svc

router = APIRouter(prefix="/v1/checkins", tags=["checkins"])


@router.post("", response_model=CheckinResponse, status_code=201)
async def create_checkin(
    payload: CheckinCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> CheckinResponse:
    return await checkins_svc.create_checkin(db, user_id, payload)
