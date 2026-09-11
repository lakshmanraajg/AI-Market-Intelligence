# Phase 0 design specification

## Frontend routes and components
The command center is `/`; planned route groups are `/markets`, `/pre-market`, `/live-market`, `/news`, `/analysis`, `/options`, `/fii-dii`, `/institutional`, `/deals`, `/investments`, `/ipo`, `/corporate-actions`, `/earnings`, `/calendar`, `/screener`, `/watchlist`, `/portfolio`, `/journal`, `/backtest`, `/copilot`, `/education`, `/settings`. The shared component layer includes shell/navigation, market-status badge, freshness indicator, price cell, source/evidence drawer, event card, chart panel, scanner table and accessibility primitives. TanStack Query owns server state; Zustand owns local layout/theme/shortcut state.

## AI evidence pipeline
Raw item → validated source record → deduplicated event fingerprint → entity extraction → graph relationships → deterministic analytics + historical lookup → prompt with evidence IDs only → structured response (`facts`, `analysis`, `historical_context`, `confidence`, `sources`) → policy validation. The model cannot query arbitrary SQL, create a price, or label insufficient evidence as a fact.

## Jobs and WebSockets
Collectors publish typed envelopes to Redis Streams. Consumer groups validate and normalize; idempotent workers deduplicate and write PostgreSQL. Scheduled workers produce pre-open refreshes, EOD reports and historical metrics. A gateway emits only authorized, entitlement-filtered updates from cache. Clients reconnect with cursors and display the source freshness state.

## Calendar, authentication, and configuration
A database-driven market-calendar has exchange, segment, timezone, regular sessions, holidays and exceptional sessions; session state is calculated per asset. Auth uses OIDC plus secure HTTP-only sessions, rotating refresh tokens, CSRF defenses for state changes and RBAC. `.env.example` lists local variables; production reads all secrets from a secret manager. Provider credentials are never returned by APIs or logged.

## Verification strategy
Unit tests cover indicator and risk formulas, time/session resolution, validation, parsers, classifiers and event extraction. Integration tests cover API, PostgreSQL, Redis, jobs and provider adapters using fixtures. E2E tests cover sign-in, dashboard, stock detail, screener, watchlist, alert and copilot evidence flow. Data-quality tests reject missing source metadata, stale/live contradictions, duplicate events, invalid values and timestamp regressions. Security CI runs dependency, lint, typecheck and secret scans.

## Data schema conventions
Identifiers use UUIDs. Monetary values use fixed precision decimal; timestamps are UTC; exchange-local times are converted at boundaries. `data_sources` records licensing/redistribution/attribution policy. Every source-derived row includes source/provider/retrieval/freshness metadata. AI rows reference immutable evidence IDs and model/version metadata. Audit logs are append-only.
