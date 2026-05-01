# Instrument List

DhanHQ provides a full instrument master as downloadable CSV. It contains every tradeable scrip — Equity, F&O, Currency, Commodity — with security IDs, lot sizes, expiry dates, and strike prices.

## CSV Sources

| Type | URL |
|---|---|
| **Compact** (for lookups) | `https://images.dhan.co/api-data/api-scrip-master.csv` |
| **Detailed** (with MTF, margin, ASM/GSM flags) | `https://images.dhan.co/api-data/api-scrip-master-detailed.csv` |

> **Segment API:** To get instruments for a single exchange segment:
> ```
> GET https://api.dhan.co/v2/instrument/{exchangeSegment}
> ```
> e.g., `GET /instrument/NSE_EQ`, `GET /instrument/NSE_FNO`

---

## ⚠️ Never Load the Full CSV into an AI Context

The CSV has **100,000+ rows**. Loading it entirely into a model context would overflow tokens and be useless. Use the provided Python tool instead — it queries only what you need via DuckDB.

---

## ⚠️ Always Refresh Before Querying

The instrument master **changes every trading day** — new expiries are added, expired contracts are removed, and new stocks/derivatives are listed. A stale cache will return wrong or missing security IDs.

**Always run this first at the start of any session:**

```bash
python tools/instrument_lookup.py refresh
```

This downloads the latest compact and detailed CSVs from DhanHQ and saves them to the local `.cache/` directory. Only then run lookup queries.

---

## Instrument Lookup Tool

**Location:** `tools/instrument_lookup.py`
**Dependency:** `pip install duckdb`

The tool downloads and caches the CSV locally (6-hour TTL), then uses **DuckDB** to run SQL against it — reading only the specific rows and columns needed. No full-file loading.

### Setup

```bash
pip install duckdb
python tools/instrument_lookup.py find_equity RELIANCE NSE
```

---

## Commands

### `find_by_symbol` — Fuzzy symbol search

```bash
python tools/instrument_lookup.py find_by_symbol NIFTY
```

Returns up to 20 matches across all instruments where symbol or display name contains the term.

---

### `find_equity` — Get equity security ID

```bash
python tools/instrument_lookup.py find_equity TCS NSE
python tools/instrument_lookup.py find_equity RELIANCE BSE
```

Returns the `security_id` for placing equity orders.

**Sample output:**
```json
[{
    "exchange": "NSE",
    "security_id": 11536,
    "display_name": "TCS",
    "symbol_name": "TCS",
    "segment": "E",
    "lot_size": 1.0,
    "tick_size": 0.05
}]
```

---

### `find_futures` — Futures contracts by underlying

```bash
python tools/instrument_lookup.py find_futures NIFTY M
python tools/instrument_lookup.py find_futures NIFTY W
```

`M` = Monthly expiry, `W` = Weekly expiry. Returns all active expiries ordered by date.

---

### `find_options` — Specific option contract

```bash
python tools/instrument_lookup.py find_options NIFTY 2024-10-31 25000 CE
python tools/instrument_lookup.py find_options BANKNIFTY 2024-11-07 51000 PE
```

Arguments: `<underlying> <expiry_date YYYY-MM-DD> <strike> <CE|PE>`

Returns the exact `security_id` to use in order placement or market data APIs.

---

### `get_security_id` — Exact trading symbol lookup

```bash
python tools/instrument_lookup.py get_security_id NIFTY24OCT25000CE
```

Fastest lookup when you already know the exact exchange trading symbol.

---

### `list_expiries` — All expiry dates for an underlying

```bash
python tools/instrument_lookup.py list_expiries NIFTY OPTIDX
python tools/instrument_lookup.py list_expiries BANKNIFTY OPTIDX
```

Returns all active expiry dates in `YYYY-MM-DD` format — same values valid for Option Chain API.

---

### `segment_list` — All instruments in a segment

```bash
python tools/instrument_lookup.py segment_list NSE_EQ
python tools/instrument_lookup.py segment_list NSE_FNO
```

Returns up to 50 instruments. Valid segments: `NSE_EQ`, `NSE_FNO`, `NSE_CURRENCY`, `BSE_EQ`, `BSE_FNO`, `BSE_CURRENCY`, `MCX_COMM`.

---

## Column Reference

### Compact CSV (Primary — use for lookups)

| Compact Column | Description |
|---|---|
| `SEM_EXM_EXCH_ID` | Exchange: `NSE`, `BSE`, `MCX` |
| `SEM_SEGMENT` | Segment: `E`=Equity, `D`=Derivatives, `C`=Currency, `M`=Commodity |
| `SEM_SMST_SECURITY_ID` | **Security ID** — used in all DhanHQ API calls |
| `SEM_INSTRUMENT_NAME` | Instrument type (see Annexure) |
| `SEM_EXPIRY_CODE` | Expiry code (0=current, 1=next, 2=far) |
| `SEM_TRADING_SYMBOL` | Exchange trading symbol |
| `SEM_LOT_UNITS` | Lot size |
| `SEM_CUSTOM_SYMBOL` | Dhan display name |
| `SEM_EXPIRY_DATE` | Expiry datetime |
| `SEM_STRIKE_PRICE` | Strike price (options) |
| `SEM_OPTION_TYPE` | `CE`=Call, `PE`=Put, `XX`=Not applicable |
| `SEM_TICK_SIZE` | Minimum price increment |
| `SEM_EXPIRY_FLAG` | `M`=Monthly, `W`=Weekly |
| `SEM_EXCH_INSTRUMENT_TYPE` | Exchange instrument type |
| `SEM_SERIES` | Exchange series |
| `SM_SYMBOL_NAME` | Symbol name of underlying |

### Detailed CSV (Extra fields)

| Detailed Column | Description |
|---|---|
| `ISIN` | International Securities Identification Number |
| `UNDERLYING_SECURITY_ID` | Security ID of underlying (derivatives) |
| `UNDERLYING_SYMBOL` | Symbol of underlying (derivatives) |
| `DISPLAY_NAME` | Dhan display name |
| `ASM_GSM_FLAG` | `N`=Normal, `Y`=ASM/GSM, `R`=Removed |
| `ASM_GSM_CATEGORY` | Surveillance category (`NA` if normal) |
| `BUY_SELL_INDICATOR` | `A`=Both buy/sell allowed |
| `MTF_LEVERAGE` | MTF leverage multiplier (equity only) |
| `SM_UPPER_LIMIT` | Upper circuit limit |
| `SM_LOWER_LIMIT` | Lower circuit limit |

---

## Common Workflow

```
1. Find security ID:
   python tools/instrument_lookup.py find_equity RELIANCE NSE
   → security_id: 2885

2. Use in API calls:
   POST /marketfeed/ltp  →  {"NSE_EQ": [2885]}
   POST /orders          →  {"securityId": "2885", ...}
```
