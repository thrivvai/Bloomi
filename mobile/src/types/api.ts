export type CompanionKind = 'pet' | 'plant';
export type EmotionalTone = 'calm' | 'playful' | 'grounded' | 'warm';
export type CheckinType = 'morning' | 'day' | 'evening';
export type DifficultyTier = 'easy' | 'medium' | 'hard';
export type ProofRequirement = 'none' | 'photo' | 'text' | 'optional_photo';

export interface CompanionState {
  id: string;
  kind: CompanionKind;
  name: string;
  species_code: string;
  archetype: string | null;
  stage: string;
  affinity_score: number;
  level: number;
  xp: number;
  energy: number;
  mood_state: string;
  growth_state: string;
  appearance_state: Record<string, unknown> | null;
  environment_state: Record<string, unknown> | null;
}

export interface QuickAction {
  action_type: string;
  title: string;
  duration_seconds: number | null;
  goal_id: string | null;
}

export interface WalletBalance {
  wallet_type: string;
  balance: number;
}

export interface HomeState {
  companion: CompanionState;
  quick_actions: QuickAction[];
  wallet_balances: WalletBalance[];
  suggested_next_action: QuickAction | null;
  contextual_greeting: string;
  pending_rewards: unknown[];
}

export interface Goal {
  id: string;
  user_id: string;
  title: string;
  goal_type: string;
  cadence: string | null;
  difficulty_tier: DifficultyTier;
  duration_minutes: number | null;
  category: string | null;
  proof_requirement: ProofRequirement;
  active: boolean;
  source: string;
  created_at: string;
}

export interface GoalCompletion {
  completion_id: string;
  energy_awarded: number;
  coins_awarded: number;
  companion_reaction: string;
  level_up: boolean;
}

export interface Checkin {
  id: string;
  checkin_date: string;
  checkin_type: CheckinType;
  mood_score: number | null;
  mood_label: string | null;
  energy_level: number | null;
  intention_text: string | null;
  companion_reaction: string;
  created_at: string;
}

export interface JournalEntry {
  id: string;
  entry_type: string;
  prompt_id: string | null;
  body_text: string;
  tags: string[] | null;
  created_at: string;
}

export interface WeeklySummary {
  week_start: string;
  week_end: string;
  mood_average: number | null;
  mood_trend: string | null;
  completions_count: number;
  top_wins: string[];
  reflection_highlights: string[];
  reset_suggestion: string | null;
  companion_retelling: string;
}

export interface CatalogItem {
  id: string;
  item_type: string;
  slug: string;
  name: string;
  rarity: string;
  price_currency: string;
  price_amount: number;
  companion_kind_scope: string;
  unlock_rules: Record<string, unknown> | null;
}

export interface OnboardingPayload {
  companion_kind: CompanionKind;
  companion_name: string;
  species_code: string;
  archetype?: string;
  emotional_tone_pref?: EmotionalTone;
  timezone: string;
  starter_goals: Array<{ title: string; cadence: string }>;
  notifications_enabled: boolean;
}

export interface OnboardingResult {
  user_id: string;
  companion_id: string;
  companion_kind: CompanionKind;
  companion_name: string;
  stage: string;
  goals_created: number;
}

export interface CompanionChatResponse {
  reply: string;
  tone_tag: string | null;
  quick_replies: string[];
  suggested_actions: unknown[];
  safety_redirected: boolean;
}
