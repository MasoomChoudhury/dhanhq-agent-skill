# DhanHQ Agent Skill — `dhanhq-agent-skill`

A complete, production-ready **Agent Skill** for the [DhanHQ Trading API](https://dhanhq.co) — built for use with Claude, GPT-4, and any LLM platform supporting the open Agent Skills standard.

This skill gives an AI agent full, accurate knowledge of the DhanHQ API v2.0 — order placement, portfolio management, live market data, options chains, WebSocket feeds, and more — without hallucinating endpoints or field names.

---

## ✨ What's Included

### Trading APIs
| File | Coverage |
|---|---|
| `AUTHENTICATION.md` | Token generation, renewal, partners, TOTP, static IP, user profile |
| `ORDERS.md` | Place, modify, cancel, slice, order book, trade book |
| `SUPER_ORDER.md` | Entry + target + stop-loss + trailing SL |
| `FOREVER_ORDER.md` | GTT — Good Till Triggered, SINGLE & OCO modes |
| `CONDITIONAL_TRIGGER.md` | Price & indicator-based auto order placement |
| `PORTFOLIO.md` | Holdings, positions, convert, exit all |
| `EDIS.md` | CDSL eDIS 3-step flow for selling holdings |
| `TRADERS_CONTROL.md` | Kill Switch + P&L-based auto-exit |
| `FUNDS_MARGIN.md` | Single & multi-order margin calculator, fund limits |
| `STATEMENT.md` | Ledger report & paginated trade history |
| `POSTBACK.md` | Webhooks / real-time order push notifications |
| `LIVE_ORDER_UPDATE.md` | WebSocket order update stream |

### Data APIs
| File | Coverage |
|---|---|
| `MARKET_DATA.md` | LTP, OHLC, full market depth snapshots (up to 1000 instruments) |
| `LIVE_FEEDS.md` | Live market feed WebSocket (binary protocol, all packet types) + 20/200 level depth |
| `HISTORICAL_DATA.md` | Daily & intraday OHLCV candles |
| `EXPIRED_OPTIONS.md` | Rolling ATM-relative historical options data (IV, OI, Greeks, spot) |
| `OPTIONS.md` | Real-time option chain with Greeks, IV, OI, bid/ask |

### Reference
| File | Coverage |
|---|---|
| `reference/ANNEXURE.md` | All enum values — exchange segments, product types, instrument types, feed codes, operators |
| `reference/ERROR_CODES.md` | All DH-9xx and 8xx error codes with rate limits |
| `reference/INSTRUMENTS.md` | Instrument CSV schema + DuckDB lookup tool docs |

### Tool
| File | Coverage |
|---|---|
| `tools/instrument_lookup.py` | DuckDB-powered CLI — query 100k+ instrument CSV without loading it into context |

---

## 🚀 Quick Start

### With Claude (Anthropic)

Attach the `dhanhq-skill/` directory as a skill container via the Files API:

```python
import anthropic

client = anthropic.Anthropic()

# Upload SKILL.md as the entry point
with open("dhanhq-skill/SKILL.md", "rb") as f:
    skill = client.beta.files.upload(
        file=("SKILL.md", f, "text/markdown"),
    )

response = client.beta.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Place a buy order for 1 share of TCS"}],
    system=[{
        "type": "text",
        "text": open("dhanhq-skill/SKILL.md").read(),
        "cache_control": {"type": "ephemeral"}
    }],
    betas=["files-api-2025-04-14"],
)
```

### With OpenAI

Attach as a system prompt or assistant context following the [Agent Skills standard](https://agentskills.dev).

---

## 🔍 Instrument Lookup (DuckDB Tool)

The DhanHQ instrument master has 100,000+ rows. This skill includes a DuckDB-powered tool that queries it without loading the full CSV.

```bash
pip install duckdb

# Always refresh first — the CSV changes daily
python dhanhq-skill/tools/instrument_lookup.py refresh

# Find security IDs
python dhanhq-skill/tools/instrument_lookup.py find_equity RELIANCE NSE
python dhanhq-skill/tools/instrument_lookup.py find_options NIFTY 2024-10-31 25000 CE
python dhanhq-skill/tools/instrument_lookup.py list_expiries BANKNIFTY OPTIDX
python dhanhq-skill/tools/instrument_lookup.py find_futures NIFTY M
```

---

## 📁 Directory Structure

```
dhanhq-skill/
├── SKILL.md                    ← Entry point (load this first)
├── AUTHENTICATION.md
├── ORDERS.md
├── SUPER_ORDER.md
├── FOREVER_ORDER.md
├── CONDITIONAL_TRIGGER.md
├── PORTFOLIO.md
├── EDIS.md
├── TRADERS_CONTROL.md
├── FUNDS_MARGIN.md
├── STATEMENT.md
├── POSTBACK.md
├── LIVE_ORDER_UPDATE.md
├── MARKET_DATA.md
├── LIVE_FEEDS.md
├── HISTORICAL_DATA.md
├── EXPIRED_OPTIONS.md
├── OPTIONS.md
├── reference/
│   ├── ANNEXURE.md
│   ├── ERROR_CODES.md
│   └── INSTRUMENTS.md
└── tools/
    └── instrument_lookup.py
```

---

## 🔑 Key Design Decisions

- **Progressive disclosure** — `SKILL.md` is a lightweight index; detailed content is loaded on-demand per domain
- **DRY** — shared objects (Order reference, Trade reference, Condition object) defined once and cross-referenced
- **Gotchas documented** — API field typos (`availabelBalance`), casing inconsistencies (`filled_qty` snake_case in Postback), abbreviated WebSocket enums (`C`=CNC, `B`=Buy), and `scripts` vs `scripList` inconsistency in margin API
- **Binary protocol coverage** — Full byte-level packet structure for all WebSocket feed types (Ticker, Quote, Full, Depth)
- **No stale enums** — all enum values resolved from the Annexure directly in the skill

---

## 🌐 API Coverage

| Category | Endpoints |
|---|---|
| Trading | 30+ REST endpoints |
| Data | 6 REST endpoints + 3 WebSocket connections |
| Rate Limits | Orders: 10/s · Market Quote: 1/s · Option Chain: 1/3s |
| Base URL | `https://api.dhan.co/v2/` |

---

## 📄 License

MIT — free to use, modify, and distribute.

---

## 🔗 Links

- [DhanHQ API Documentation](https://dhanhq.co/docs/v2/)
- [Agent Skills Standard](https://agentskills.dev)
- [DhanHQ Developer Portal](https://dhanhq.co)
