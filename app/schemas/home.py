from pydantic import BaseModel


class CompanionExpressionState(BaseModel):
    companion_id: str
    kind: str
    name: str
    stage: str
    mood_state: str
    growth_state: str
    energy: int
    level: int
    xp: int
    appearance_state: dict | None = None
    environment_state: dict | None = None


class QuickAction(BaseModel):
    action_type: str
    title: str
    duration_seconds: int | None = None
    goal_id: str | None = None


class WalletBalance(BaseModel):
    wallet_type: str
    balance: int


class HomeStateResponse(BaseModel):
    companion: CompanionExpressionState
    quick_actions: list[QuickAction]
    wallet_balances: list[WalletBalance]
    suggested_next_action: QuickAction | None = None
    contextual_greeting: str
    pending_rewards: list[dict] = []
