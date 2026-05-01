---
name: dhanhq-trading-api
description: Provides complete expertise for the DhanHQ (Dhan) trading API — authentication, order placement, portfolio management, market data, options chains, charts, and live feeds. Use when the user wants to trade, fetch positions, place orders, get market quotes, stream live data, or build trading automations using the Dhan platform.
---

# DhanHQ Trading API Skill

DhanHQ API v2.0 is a REST-based trading platform for Indian markets. It enables order execution, portfolio management, live market data, and trading automation with JSON request/response format and standard HTTP codes.

## Contents

- **Authentication & Setup** → See [AUTHENTICATION.md](AUTHENTICATION.md)
- **Orders** → See [ORDERS.md](ORDERS.md)
- **Super Order** (entry + target + stop-loss + trailing SL) → See [SUPER_ORDER.md](SUPER_ORDER.md)
- **Forever Order** (GTT — Good Till Triggered, SINGLE & OCO) → See [FOREVER_ORDER.md](FOREVER_ORDER.md)
- **Conditional Trigger** (price/indicator-based auto order placement) → See [CONDITIONAL_TRIGGER.md](CONDITIONAL_TRIGGER.md)
- **Portfolio** → See [PORTFOLIO.md](PORTFOLIO.md)
- **EDIS** (CDSL eDIS flow for selling holdings — T-PIN & approval) → See [EDIS.md](EDIS.md)
- **Trader's Control** (Kill Switch & P&L-based auto-exit) → See [TRADERS_CONTROL.md](TRADERS_CONTROL.md)
- **Funds & Margin** (margin calculator, fund limits) → See [FUNDS_MARGIN.md](FUNDS_MARGIN.md)
- **Statement** (ledger report & paginated trade history) → See [STATEMENT.md](STATEMENT.md)
- **Postback / Webhooks** (real-time order update push notifications) → See [POSTBACK.md](POSTBACK.md)
- **Live Order Update** (WebSocket stream for real-time order events) → See [LIVE_ORDER_UPDATE.md](LIVE_ORDER_UPDATE.md)
- **Market Data & Quotes** → See [MARKET_DATA.md](MARKET_DATA.md)
- **Options Chain** → See [OPTIONS.md](OPTIONS.md)
- **Live Feeds (WebSocket)** → See [LIVE_FEEDS.md](LIVE_FEEDS.md)
- **Historical Data** (daily & intraday OHLCV candles) → See [HISTORICAL_DATA.md](HISTORICAL_DATA.md)
- **Expired Options Data** (rolling ATM-relative historical options data) → See [EXPIRED_OPTIONS.md](EXPIRED_OPTIONS.md)
- **Reference: Annexure** (all enum values — segments, product types, instruments, feed codes) → See [reference/ANNEXURE.md](reference/ANNEXURE.md)
- **Reference: Instrument List & Lookup** (security IDs, CSV schema, DuckDB query tool) → See [reference/INSTRUMENTS.md](reference/INSTRUMENTS.md)
- **Reference: Error Codes** → See [reference/ERROR_CODES.md](reference/ERROR_CODES.md)

## Finding Security IDs

Security IDs are required for every order and market data call. Use the instrument lookup tool — **never load the full CSV**.

> ⚠️ **Always refresh first.** The instrument master changes every trading day. Using a stale cache returns wrong or missing security IDs.

```bash
pip install duckdb

# Step 1 — MANDATORY: Download latest instrument master
python dhanhq-skill/tools/instrument_lookup.py refresh

# Step 2 — Run your lookup
python dhanhq-skill/tools/instrument_lookup.py find_equity TCS NSE
python dhanhq-skill/tools/instrument_lookup.py find_options NIFTY 2024-10-31 25000 CE
python dhanhq-skill/tools/instrument_lookup.py list_expiries BANKNIFTY OPTIDX
```

See [reference/INSTRUMENTS.md](reference/INSTRUMENTS.md) for all commands.

## Base URL

```
https://api.dhan.co/v2/
```

## Rate Limits

| Limit Period | Order APIs | Data APIs | Quote APIs | Non-Trading APIs |
|---|---|---|---|---|
| Per second | 10 | 5 | 1 | 20 |
| Per minute | 250 | — | Unlimited | Unlimited |
| Per hour | 1,000 | — | Unlimited | Unlimited |
| Per day | 7,000 | 1,00,000 | Unlimited | Unlimited |

> Order modifications are capped at **25 modifications per order**.
