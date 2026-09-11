# BharatIQ — Indian Market Intelligence

A source-transparent Indian market research terminal. Phase 0 documents the production architecture; Phase 1 delivers the runnable terminal foundation and an API safety contract. It intentionally ships without a market-data provider: **no sample number is represented as live market data**.

## What is implemented
- Responsive Command Center UI with pre-market countdown, compact dashboard widgets, semantic freshness/status labels, AI fact/analysis separation and event-source evidence placeholders.
- FastAPI health and market snapshot contract that returns `UNAVAILABLE` until a licensed adapter exists.
- Docker local dependencies for PostgreSQL + pgvector and Redis.
- Architecture, ERD, API, source-governance and environment specifications under `docs/`.

## Repository map
```text
src/                 React/TypeScript command-center UI
backend/app/         FastAPI versioned API foundation
backend/tests/       API safety tests
docs/                Phase 0 architecture and contracts
docker-compose.yml   PostgreSQL/pgvector, Redis, API local environment
```

## Run the UI
```bash
npm install
npm run dev
```

> A lockfile is not yet committed, so use `npm install` rather than `npm ci`. Direct frontend dependency versions are pinned; GitHub Actions performs this clean-checkout installation. Commit a generated `package-lock.json` once registry access is available to lock transitive dependencies too.

## Run the API
```bash
cd backend
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Validation and CI
```bash
# Frontend (after npm install)
npm run typecheck
npm test
npm run build

# Backend (after dependencies are installed)
cd backend && python -m pip install -r requirements-dev.txt
python -m ruff check app tests
python -m pytest
```

GitHub Actions runs the clean-checkout frontend dependency install, type check, unit test, production build, backend dependency install, Ruff check and API tests on every push and pull request (`.github/workflows/ci.yml`).

## Phase plan
0. Architecture ✅ · 1. Foundation ✅ · 2. Market data · 3. Analytics · 4. News · 5. AI intelligence · 6. Pre-market · 7. Options · 8. Institutional · 9. Corporate data · 10. Scanners · 11. User features · 12. Copilot · 13. Historical intelligence · 14. Research · 15. Production hardening.
