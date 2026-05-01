# Historical Data

OHLCV candle data for any instrument — daily or intraday (1, 5, 15, 25, 60 min).

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/charts/historical` | Daily OHLCV candles |
| `POST` | `/charts/intraday` | Intraday OHLCV candles (1, 5, 15, 25, 60 min) |

> **Response format:** Columnar parallel arrays — all fields (`open`, `high`, `low`, `close`, `volume`, `timestamp`) are aligned arrays where index `n` across all arrays represents the same candle.

---

## Daily Historical Data

`POST https://api.dhan.co/v2/charts/historical`

Daily candle data from the instrument's inception date.

```bash
curl --request POST \
  --url https://api.dhan.co/v2/charts/historical \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT' \
  --data '{}'
```

**Request Body:**

```json
{
    "securityId": "1333",
    "exchangeSegment": "NSE_EQ",
    "instrument": "EQUITY",
    "expiryCode": 0,
    "oi": false,
    "fromDate": "2022-01-08",
    "toDate": "2022-02-08"
}
```

| Field | Type | Description |
|---|---|---|
| `securityId` *(required)* | string | Exchange security ID |
| `exchangeSegment` *(required)* | enum | Exchange & segment (see Annexure) |
| `instrument` *(required)* | enum | Instrument type (e.g., `EQUITY`, `FUTIDX`, `OPTIDX`) |
| `expiryCode` *(optional)* | enum int | For derivatives — expiry code (see Annexure). Use `0` for current expiry |
| `oi` *(optional)* | boolean | `true` to include Open Interest data in response (F&O only) |
| `fromDate` *(required)* | string | Start date — `YYYY-MM-DD` |
| `toDate` *(required)* | string | End date — `YYYY-MM-DD` (**non-inclusive**) |

**Response:**

```json
{
    "open":      [3978, 3856, 3925, ...],
    "high":      [3978, 3925, 3929, ...],
    "low":       [3861, 3856, 3836.55, ...],
    "close":     [3879.85, 3915.9, 3859.9, ...],
    "volume":    [3937092, 1906106, 3203744, ...],
    "timestamp": [1326220200, 1326306600, 1326393000, ...],
    "open_interest": [0, 0, 0, ...]
}
```

| Field | Type | Description |
|---|---|---|
| `open` | float[] | Candle open prices |
| `high` | float[] | Candle high prices |
| `low` | float[] | Candle low prices |
| `close` | float[] | Candle close prices |
| `volume` | int[] | Volume traded per candle |
| `timestamp` | int[] | Candle start time — UNIX epoch |
| `open_interest` | int[] | Open Interest (all zeros for non-F&O) |

---

## Intraday Historical Data

`POST https://api.dhan.co/v2/charts/intraday`

Minute-interval candles. Available for all exchanges and segments, for all active instruments, up to **5 years back**.

```bash
curl --request POST \
  --url https://api.dhan.co/v2/charts/intraday \
  --header 'Content-Type: application/json' \
  --header 'access-token: {JWT}' \
  --data '{}'
```

**Request Body:**

```json
{
    "securityId": "1333",
    "exchangeSegment": "NSE_EQ",
    "instrument": "EQUITY",
    "interval": "1",
    "oi": false,
    "fromDate": "2024-09-11 09:30:00",
    "toDate": "2024-09-15 13:00:00"
}
```

| Field | Type | Description |
|---|---|---|
| `securityId` *(required)* | string | Exchange security ID |
| `exchangeSegment` *(required)* | enum | Exchange & segment (see Annexure) |
| `instrument` *(required)* | enum | Instrument type |
| `interval` *(required)* | enum int | Candle interval in minutes: `1`, `5`, `15`, `25`, `60` |
| `oi` *(optional)* | boolean | `true` to include Open Interest data (F&O only) |
| `fromDate` *(required)* | string | Start datetime — `YYYY-MM-DD HH:MM:SS` |
| `toDate` *(required)* | string | End datetime — `YYYY-MM-DD HH:MM:SS` |

> **⚠️ 90-day limit:** Only 90 days of intraday data can be fetched per request for any interval. It is recommended to store this data locally for day-to-day analysis.

> **Date format difference:** Intraday uses datetime `YYYY-MM-DD HH:MM:SS` (not just `YYYY-MM-DD` like daily).

> **toDate is inclusive** for intraday (unlike daily where it is non-inclusive).

**Response:** Same columnar array format as daily — `open`, `high`, `low`, `close`, `volume`, `timestamp`, `open_interest`.

---

## Key Differences: Daily vs Intraday

| Feature | Daily (`/charts/historical`) | Intraday (`/charts/intraday`) |
|---|---|---|
| Timeframe | 1 day per candle | 1, 5, 15, 25, 60 min per candle |
| History depth | Inception date of instrument | Last 5 years |
| Max range per request | No stated limit | **90 days** |
| Date format | `YYYY-MM-DD` | `YYYY-MM-DD HH:MM:SS` |
| `toDate` inclusive? | **Non-inclusive** | Inclusive |
| Derivatives param | `expiryCode` supported | Not applicable |
