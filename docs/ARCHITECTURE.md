# BharatIQ architecture (Phase 0)

## Product boundary
BharatIQ is a research and information terminal, not an execution or personalised-advice product. Prices retain provider, entitlement, source URL, observed time, retrieval time and freshness. Missing evidence renders **Data unavailable**; stale input never renders as live.

## System flow
```text
Licensed / official providers → collectors → Redis Streams / queue → validation
→ normalisation → event deduplication + entity extraction → PostgreSQL + pgvector
→ analytics / historical reactions → evidence-bound AI → Redis cache
→ FastAPI v1 + WebSocket gateway → Next.js/React terminal
```
Collectors are isolated adapters. The browser only consumes our API/gateway, never a provider feed. Batch workers handle fundamentals and backfills; streaming workers handle entitled price/news/options updates.

## Core ERD
```text
users ──< watchlists ──< watchlist_items >── instruments ──< ohlcv
  │             └──< alerts                         │       └──< technical_metrics
  ├──< portfolios ──< portfolio_positions            ├──< market_snapshots
  └──< journal_entries                               ├──< option_contracts ──< option_snapshots
companies ──< instruments; companies >── sectors; companies >── industries
news_sources ──< news_items >── news_events ──< event_entities >── entities
news_events ──< event_evidence; entities ──< entity_relationships >── entities
news_events ──< historical_reactions; ai_analyses ──< ai_evidence
```
All time-series tables use `instrument_id, observed_at` indexes; high-volume OHLCV/ticks are monthly partition candidates. `source_record_id` and `retrieved_at` are mandatory for externally derived facts.

## Security and operations
OIDC/session auth with RBAC (viewer, analyst, admin); API rate limiting at reverse proxy and application layers; Pydantic validation; parameterized SQLAlchemy queries; CSP/security headers; audit logs; secret manager in production. Monitor provider and queue failures, ingestion/API/WebSocket latency, freshness, database latency, AI cost/latency and source-verification failures.
