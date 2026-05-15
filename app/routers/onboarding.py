from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user_id
from app.schemas.onboarding import OnboardingCompleteRequest, OnboardingCompleteResponse
from app.services import onboarding as onboarding_svc

router = APIRouter(prefix="/v1/onboarding", tags=["onboarding"])


@router.post("/complete", response_model=OnboardingCompleteResponse, status_code=201)
async def complete_onboarding(
    payload: OnboardingCompleteRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> OnboardingCompleteResponse:
    return await onboarding_svc.complete_onboarding(db, user_id, payload)
