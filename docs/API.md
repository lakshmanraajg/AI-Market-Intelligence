# API contract
All endpoints are versioned below `/api/v1`, JSON, authenticated unless stated otherwise, and support validated pagination (`limit`, `cursor`), filtering and sorting. Responses include `meta` with request ID and freshness.

| Domain | Base endpoint | Phase |
|---|---|---|
| Markets, indices, stocks | `/markets`, `/indices`, `/stocks` | 2 |
| Commodities, currencies | `/commodities`, `/currencies` | 2 |
| News, events, sources | `/news`, `/events`, `/data-sources` | 4 |
| Options | `/options` | 7 |
| FII/DII, investments, deals | `/fii-dii`, `/institutional`, `/bulk-deals`, `/block-deals` | 8 |
| IPO, actions, earnings | `/ipo`, `/corporate-actions`, `/earnings` | 9 |
| Screener | `/screener` | 10 |
| User data | `/watchlists`, `/alerts`, `/portfolio`, `/journal` | 11 |
| Research | `/backtest`, `/ai` | 12–14 |

`GET /health` is public. The Phase 1 `GET /api/v1/markets/snapshots/{symbol}` contract deliberately returns `UNAVAILABLE` until an entitled provider is configured. A snapshot will expose `value`, OHLCV when licensed, `as_of`, `retrieved_at`, `freshness`, provider, attribution and source link.
