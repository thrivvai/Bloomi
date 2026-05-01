from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user_id
from app.schemas.goals import (
    GoalCompleteRequest,
    GoalCompleteResponse,
    GoalCreate,
    GoalResponse,
)
from app.services import goals as goals_svc

router = APIRouter(prefix="/v1/goals", tags=["goals"])


@router.post("", response_model=GoalResponse, status_code=201)
async def create_goal(
    payload: GoalCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> GoalResponse:
    return await goals_svc.create_goal(db, user_id, payload)


@router.get("", response_model=list[GoalResponse])
async def list_goals(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> list[GoalResponse]:
    return await goals_svc.list_goals(db, user_id)


@router.post("/{goal_id}/complete", response_model=GoalCompleteResponse)
async def complete_goal(
    goal_id: str,
    payload: GoalCompleteRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> GoalCompleteResponse:
    return await goals_svc.complete_goal(db, user_id, goal_id, payload)


@router.post("/{goal_id}/proof-assets", status_code=201)
async def upload_proof_asset(
    goal_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> dict:
    return await goals_svc.initiate_proof_upload(db, user_id, goal_id)
