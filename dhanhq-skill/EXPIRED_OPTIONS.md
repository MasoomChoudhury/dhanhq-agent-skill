# Expired Options Data

Pre-processed historical data for expired options contracts, stored on a rolling ATM-relative basis. Ideal for backtesting IV-based and OI-based strategies.

## API Endpoint

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/charts/rollingoption` | Expired options contract data (rolling, ATM-relative) |

---

## Key Concepts

| Concept | Detail |
|---|---|
| **Rolling basis** | Data is indexed by **ATM-relative strike** (e.g., ATM, ATM+1, ATM-3) — not absolute strike price |
| **Data granularity** | Minute-level (1, 5, 15, 25, 60 min intervals) |
| **Max range per request** | **30 days** |
| **History depth** | Last **5 years** |
| **Strike range (Index near expiry)** | ATM ± 10 |
| **Strike range (all other contracts)** | ATM ± 3 |
| **Available data** | OHLC, IV, Volume, OI, Spot |

---

## Request

`POST https://api.dhan.co/v2/charts/rollingoption`

```bash
curl --request POST \
  --url https://api.dhan.co/v2/charts/rollingoption \
  --header 'Content-Type: application/json' \
  --header 'access-token: {JWT}' \
  --data '{}'
```

**Request Body:**

```json
{
    "exchangeSegment": "NSE_FNO",
    "interval": "1",
    "securityId": 13,
    "instrument": "OPTIDX",
    "expiryFlag": "MONTH",
    "expiryCode": 1,
    "strike": "ATM",
    "drvOptionType": "CALL",
    "requiredData": [
        "open",
        "high",
        "low",
        "close",
        "volume"
    ],
    "fromDate": "2021-08-01",
    "toDate": "2021-09-01"
}
```

| Field | Type | Description |
|---|---|---|
| `exchangeSegment` *(required)* | enum | Exchange & segment (e.g., `NSE_FNO`) |
| `interval` *(required)* | enum int | Candle interval in minutes: `1`, `5`, `15`, `25`, `60` |
| `securityId` *(required)* | string | Underlying instrument's security ID (e.g., `13` for Nifty) |
| `instrument` *(required)* | enum | Instrument type (e.g., `OPTIDX`, `OPTSTK`) |
| `expiryFlag` *(required)* | enum | `WEEK` or `MONTH` |
| `expiryCode` *(required)* | enum int | Expiry number — see Annexure |
| `strike` *(required)* | enum string | ATM-relative strike: `ATM`, `ATM+1`, `ATM-1`, `ATM+2`, etc. |
| `drvOptionType` *(required)* | enum | `CALL` or `PUT` |
| `requiredData` *(required)* | array | Fields to include in response — choose from: `open` `high` `low` `close` `iv` `volume` `strike` `oi` `spot` |
| `fromDate` *(required)* | string | Start date — `YYYY-MM-DD` |
| `toDate` *(required)* | string | End date — `YYYY-MM-DD` (**non-inclusive**) |

> **`requiredData` is selective:** Only fields listed here are populated in the response. Unlisted fields return as empty arrays `[]`. Include only what you need to reduce payload size.

---

## Response

```json
{
    "data": {
        "ce": {
            "iv": [],
            "oi": [],
            "strike": [],
            "spot": [],
            "open": [354, 360.3],
            "high": [],
            "low": [],
            "close": [],
            "volume": [],
            "timestamp": [1756698300, 1756699200]
        },
        "pe": null
    }
}
```

Response is **columnar parallel arrays** — same index `n` across all arrays = same candle.

| Field | Type | Description |
|---|---|---|
| `data.ce` | object | CALL option data (`null` if not requested) |
| `data.pe` | object | PUT option data (`null` if not requested) |
| `open` | float[] | Candle open prices |
| `high` | float[] | Candle high prices |
| `low` | float[] | Candle low prices |
| `close` | float[] | Candle close prices |
| `volume` | int[] | Volume traded per candle |
| `iv` | float[] | Implied Volatility per candle |
| `oi` | int[] | Open Interest per candle |
| `strike` | float[] | Actual strike price for this ATM-relative level per candle |
| `spot` | float[] | Spot (underlying) price per candle |
| `timestamp` | int[] | Candle start time — UNIX epoch |

> **Unrequested fields:** Fields not included in `requiredData` return as `[]` (empty array), not omitted.
> **Opposite leg:** If you request only `CALL`, the `pe` key will be `null` (not missing).
