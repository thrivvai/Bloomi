# Bloomi Backend

FastAPI backend for **Bloomi** — a compassionate self-care companion app where users raise either a pet or a plant.

## What is included

### Application layer
- `app/main.py` — FastAPI app factory with CORS, error handlers, and all routers registered
- `app/config.py` — Pydantic Settings with `BLOOMI_*` env prefix
- `app/database.py` — async SQLAlchemy engine and session factory
- `app/dependencies.py` — DB session and stub auth dependencies

### Domain modules
| Module | Covers |
|--------|--------|
| `app/models/user.py` | `users`, `user_profiles` |
| `app/models/companion.py` | `companions`, `companion_state_snapshots`, `companion_memories`, `adventure_sessions` |
| `app/models/practice.py` | `daily_checkins`, `goals`, `goal_completions`, `proof_assets`, `journal_entries`, `mood_entries` |
| `app/models/wallet.py` | `wallet_accounts`, `wallet_transactions` |
| `app/models/catalog.py` | `catalog_items`, `user_inventory` |
| `app/models/notifications.py` | `notifications` |
| `app/models/analytics.py` | `event_log` |

### API surface
```
POST /v1/onboarding/complete
GET  /v1/home/state
POST /v1/checkins
POST /v1/goals
GET  /v1/goals
POST /v1/goals/{goal_id}/complete
POST /v1/goals/{goal_id}/proof-assets
GET  /v1/companion/state
POST /v1/companion/chat
POST /v1/journal-entries
GET  /v1/insights/weekly-summary
GET  /v1/shop/catalog
POST /v1/shop/purchase
POST /v1/shop/equip
GET  /healthz
```

### Infrastructure
- `alembic/` — Alembic async migrations; `001_initial_schema.py` creates all tables
- `scripts/seed.py` — seeds starter catalog items (outfits, pots, room items, themes)
- `app/core/events.py` — analytics event taxonomy (`EventName` enum)
- `app/core/errors.py` — typed error classes with JSON error responses
- `app/core/logging.py` — structlog structured logging (pretty in dev, JSON in prod)

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# copy and edit env
cp .env.example .env

# run migrations (requires Postgres)
alembic upgrade head

# seed catalog data
python -m scripts.seed

# start dev server
uvicorn app.main:app --reload
```

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BLOOMI_ENV` | `dev` | `dev`, `staging`, or `prod` |
| `BLOOMI_DATABASE_URL` | `postgresql+psycopg://postgres:postgres@localhost:5432/bloomi` | Async Postgres DSN |
| `BLOOMI_SECRET_KEY` | — | JWT signing key |
| `BLOOMI_LOG_LEVEL` | `INFO` | Logging level |
| `BLOOMI_REDIS_URL` | `redis://localhost:6379/0` | Redis for ephemeral state |
| `BLOOMI_AI_API_KEY` | — | Anthropic API key for companion chat |
| `BLOOMI_CORS_ORIGINS` | `http://localhost:3000,...` | Allowed CORS origins |

## Tests

```bash
pip install -e ".[dev]"
pytest
```

Tests use an in-memory SQLite database via `aiosqlite` and override DB/auth dependencies.

## Architecture decisions

- **Modular monolith** — clean domain boundaries, single deployable for now
- **Async SQLAlchemy 2.x** — all DB access is async; ready for high concurrency
- **No punitive streaks** — reward engine only credits, never penalises absence
- **Proof assets as first-class** — `proof_assets` table and upload flow in schema from day one even though the UI rollout is phased
- **AI chat stub** — `POST /v1/companion/chat` returns a safe placeholder; real orchestration (Phase 5) plugs in at `app/services/companion.py:chat` behind the same contract

## Next build steps (Phase 1+)

1. Replace stub auth in `app/dependencies.py` with real Supabase JWT validation
2. Build `today_home_state` read model with caching
3. Add async reward fanout job (Redis worker or Postgres-backed queue)
4. Wire Supabase Storage for proof asset uploads
5. Implement notification scheduling with timezone + quiet-hour logic
6. Add AI companion orchestration module (Phase 5)
