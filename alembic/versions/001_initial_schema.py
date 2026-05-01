"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-05-01

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("auth_provider", sa.String(64), nullable=False, server_default="supabase"),
        sa.Column("last_active_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "user_profiles",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False),
        sa.Column("display_name", sa.String(128), nullable=True),
        sa.Column("timezone", sa.String(64), nullable=False, server_default="UTC"),
        sa.Column("age_band", sa.String(32), nullable=True),
        sa.Column("companion_kind", sa.String(16), nullable=True),
        sa.Column("onboarding_archetype", sa.String(64), nullable=True),
        sa.Column("emotional_tone_pref", sa.String(32), nullable=True),
        sa.Column("accessibility_prefs", postgresql.JSONB, nullable=True),
        sa.Column("notification_quiet_start", sa.String(5), nullable=True),
        sa.Column("notification_quiet_end", sa.String(5), nullable=True),
        sa.Column("notifications_enabled", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "companions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("kind", sa.String(16), nullable=False),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("species_code", sa.String(64), nullable=False),
        sa.Column("archetype", sa.String(64), nullable=True),
        sa.Column("stage", sa.String(32), nullable=False, server_default="seedling"),
        sa.Column("affinity_score", sa.Integer, nullable=False, server_default="0"),
        sa.Column("personality_vector", postgresql.JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_companions_user_id", "companions", ["user_id"])

    op.create_table(
        "companion_state_snapshots",
        sa.Column("companion_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companions.id", ondelete="CASCADE"), primary_key=True, nullable=False),
        sa.Column("level", sa.Integer, nullable=False, server_default="1"),
        sa.Column("xp", sa.Integer, nullable=False, server_default="0"),
        sa.Column("energy", sa.Integer, nullable=False, server_default="100"),
        sa.Column("mood_state", sa.String(32), nullable=False, server_default="content"),
        sa.Column("growth_state", sa.String(32), nullable=False, server_default="sprouting"),
        sa.Column("appearance_state", postgresql.JSONB, nullable=True),
        sa.Column("environment_state", postgresql.JSONB, nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "companion_memories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("companion_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("memory_type", sa.String(64), nullable=False),
        sa.Column("summary", sa.Text, nullable=False),
        sa.Column("salience_score", sa.Float, nullable=False, server_default="0.5"),
        sa.Column("source_event_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_companion_memories_user_id", "companion_memories", ["user_id"])

    op.create_table(
        "adventure_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("companion_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("state", sa.String(32), nullable=False, server_default="active"),
        sa.Column("destination_slug", sa.String(128), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rewards_payload", postgresql.JSONB, nullable=True),
    )
    op.create_index("ix_adventure_sessions_user_id", "adventure_sessions", ["user_id"])

    op.create_table(
        "daily_checkins",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("checkin_date", sa.Date, nullable=False),
        sa.Column("checkin_type", sa.String(32), nullable=False),
        sa.Column("mood_score", sa.Integer, nullable=True),
        sa.Column("mood_label", sa.String(64), nullable=True),
        sa.Column("energy_level", sa.Integer, nullable=True),
        sa.Column("intention_text", sa.Text, nullable=True),
        sa.Column("gratitude_text", sa.Text, nullable=True),
        sa.Column("stress_score", sa.Integer, nullable=True),
        sa.Column("payload", postgresql.JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_daily_checkins_user_id", "daily_checkins", ["user_id"])

    op.create_table(
        "goals",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("goal_type", sa.String(32), nullable=False),
        sa.Column("title", sa.String(256), nullable=False),
        sa.Column("cadence", sa.String(32), nullable=True),
        sa.Column("difficulty_tier", sa.String(16), nullable=False, server_default="easy"),
        sa.Column("duration_minutes", sa.Integer, nullable=True),
        sa.Column("category", sa.String(64), nullable=True),
        sa.Column("proof_requirement", sa.String(32), nullable=False, server_default="none"),
        sa.Column("active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("source", sa.String(32), nullable=False, server_default="user"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_goals_user_id", "goals", ["user_id"])

    op.create_table(
        "proof_assets",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("asset_type", sa.String(32), nullable=False),
        sa.Column("storage_path", sa.String(512), nullable=False),
        sa.Column("thumbnail_path", sa.String(512), nullable=True),
        sa.Column("captured_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("verification_state", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("metadata", postgresql.JSONB, nullable=True),
    )
    op.create_index("ix_proof_assets_user_id", "proof_assets", ["user_id"])

    op.create_table(
        "goal_completions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("goal_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("goals.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("proof_type", sa.String(32), nullable=True),
        sa.Column("proof_asset_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("proof_assets.id", ondelete="SET NULL"), nullable=True),
        sa.Column("mood_before", sa.Integer, nullable=True),
        sa.Column("mood_after", sa.Integer, nullable=True),
        sa.Column("energy_awarded", sa.Integer, nullable=False, server_default="0"),
        sa.Column("coins_awarded", sa.Integer, nullable=False, server_default="0"),
        sa.Column("metadata", postgresql.JSONB, nullable=True),
    )
    op.create_index("ix_goal_completions_goal_id", "goal_completions", ["goal_id"])
    op.create_index("ix_goal_completions_user_id", "goal_completions", ["user_id"])

    op.create_table(
        "journal_entries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("prompt_id", sa.String(128), nullable=True),
        sa.Column("entry_type", sa.String(32), nullable=False, server_default="free"),
        sa.Column("body_text", sa.Text, nullable=False),
        sa.Column("sentiment_score", sa.Float, nullable=True),
        sa.Column("tags", postgresql.ARRAY(sa.String), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_journal_entries_user_id", "journal_entries", ["user_id"])

    op.create_table(
        "mood_entries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source", sa.String(32), nullable=False),
        sa.Column("mood_score", sa.Integer, nullable=False),
        sa.Column("mood_label", sa.String(64), nullable=True),
        sa.Column("context", postgresql.JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_mood_entries_user_id", "mood_entries", ["user_id"])

    op.create_table(
        "wallet_accounts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("wallet_type", sa.String(32), nullable=False),
        sa.Column("balance", sa.Integer, nullable=False, server_default="0"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_wallet_accounts_user_id", "wallet_accounts", ["user_id"])

    op.create_table(
        "wallet_transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("wallet_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("wallet_accounts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("transaction_type", sa.String(32), nullable=False),
        sa.Column("amount", sa.Integer, nullable=False),
        sa.Column("reference_type", sa.String(64), nullable=True),
        sa.Column("reference_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_wallet_transactions_wallet_id", "wallet_transactions", ["wallet_id"])

    op.create_table(
        "catalog_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("item_type", sa.String(64), nullable=False),
        sa.Column("slug", sa.String(128), nullable=False, unique=True),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("rarity", sa.String(32), nullable=False, server_default="common"),
        sa.Column("price_currency", sa.String(16), nullable=False, server_default="coins"),
        sa.Column("price_amount", sa.Integer, nullable=False, server_default="0"),
        sa.Column("unlock_rules", postgresql.JSONB, nullable=True),
        sa.Column("companion_kind_scope", sa.String(16), nullable=False, server_default="all"),
        sa.Column("active", sa.Boolean, nullable=False, server_default="true"),
    )

    op.create_table(
        "user_inventory",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("catalog_item_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("catalog_items.id", ondelete="CASCADE"), nullable=False),
        sa.Column("equipped", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("acquired_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("source", sa.String(32), nullable=False, server_default="purchase"),
    )
    op.create_index("ix_user_inventory_user_id", "user_inventory", ["user_id"])

    op.create_table(
        "notifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("channel", sa.String(32), nullable=False),
        sa.Column("template_key", sa.String(128), nullable=False),
        sa.Column("scheduled_for", sa.DateTime(timezone=True), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delivery_state", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("context", postgresql.JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_notifications_user_id", "notifications", ["user_id"])

    op.create_table(
        "event_log",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("session_id", sa.String(128), nullable=True),
        sa.Column("event_name", sa.String(128), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("props", postgresql.JSONB, nullable=True),
    )
    op.create_index("ix_event_log_user_id", "event_log", ["user_id"])
    op.create_index("ix_event_log_event_name", "event_log", ["event_name"])


def downgrade() -> None:
    op.drop_table("event_log")
    op.drop_table("notifications")
    op.drop_table("user_inventory")
    op.drop_table("catalog_items")
    op.drop_table("wallet_transactions")
    op.drop_table("wallet_accounts")
    op.drop_table("mood_entries")
    op.drop_table("journal_entries")
    op.drop_table("goal_completions")
    op.drop_table("proof_assets")
    op.drop_table("goals")
    op.drop_table("daily_checkins")
    op.drop_table("adventure_sessions")
    op.drop_table("companion_memories")
    op.drop_table("companion_state_snapshots")
    op.drop_table("companions")
    op.drop_table("user_profiles")
    op.drop_table("users")
