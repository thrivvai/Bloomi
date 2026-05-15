from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user_id
from app.schemas.home import HomeStateResponse
from app.services import home_state as home_state_svc

router = APIRouter(prefix="/v1/home", tags=["home"])


@router.get("/state", response_model=HomeStateResponse)
async def get_home_state(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> HomeStateResponse:
    return await home_state_svc.build_home_state(db, user_id)
