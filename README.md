Bloomi Backend
FastAPI backend scaffold for Bloomi, a compassionate self-care companion app where users can choose to raise either a pet or a plant.
What is included
FastAPI application shell
SQLAlchemy model layer for Bloomi's core product entities
API route stubs for onboarding, home state, goals, check-ins, companion state, and weekly insights
Schema primitives for key create and read flows
Simple service layer placeholders to keep business logic out of route files
Suggested next build steps
Add Alembic migrations from the model set.
Implement a real database session dependency and repository layer.
Build the home state read model and reward transaction write path first.
Add auth integration and row-level data access strategy.
Add async jobs for reward fanout and notification scheduling.
Run locally
cd /workspace/bloomi-backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
Environment
export BLOOMI_ENV=dev
export BLOOMI_DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/bloomi
