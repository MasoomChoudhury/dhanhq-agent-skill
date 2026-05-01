# Market Quote (Data APIs)

Snapshot market data for up to **1000 instruments per request**. Three levels of detail available.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/marketfeed/ltp` | LTP (Last Traded Price) only |
| `POST` | `/marketfeed/ohlc` | LTP + OHLC (Open/High/Low/Close) |
| `POST` | `/marketfeed/quote` | Full quote — LTP, OHLC, market depth, OI, volume, circuit limits |

> **Rate limit:** Up to **1000 instruments** per request, **1 request/second**.
> **Data plan required** for Data APIs — check subscription via [User Profile](AUTHENTICATION.md#user-profile-token-validation).

---

## Required Headers

> ⚠️ **Data APIs require BOTH headers** — unlike Trading APIs which only need `access-token`:

| Header | Description |
|---|---|
| `access-token` *(required)* | JWT access token |
| `client-id` *(required)* | Your Dhan Client ID |

---

## Request Format

All three endpoints share the same request body format:

```json
{
    "NSE_EQ": [11536],
    "NSE_FNO": [49081, 49082]
}
```

- Keys are **exchange segment ENUMs** (e.g., `NSE_EQ`, `NSE_FNO`, `BSE_EQ`)
- Values are **arrays of integer security IDs**
- Security IDs are found in the [Instrument List](reference/INSTRUMENTS.md)

---

## Ticker Data (LTP)

`POST https://api.dhan.co/v2/marketfeed/ltp`

```bash
curl --request POST \
  --url https://api.dhan.co/v2/marketfeed/ltp \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT' \
  --header 'client-id: 1000000001' \
  --data '{"NSE_EQ":[11536],"NSE_FNO":[49081,49082]}'
```

**Response:**

```json
{
    "data": {
        "NSE_EQ": {
            "11536": {
                "last_price": 4520
            }
        },
        "NSE_FNO": {
            "49081": { "last_price": 368.15 },
            "49082": { "last_price": 694.35 }
        }
    },
    "status": "success"
}
```

Response is nested: `data → {segment} → {securityId} → fields`

| Field | Type | Description |
|---|---|---|
| `last_price` | float | Last traded price |

---

## OHLC Data

`POST https://api.dhan.co/v2/marketfeed/ohlc`

```bash
curl --request POST \
  --url https://api.dhan.co/v2/marketfeed/ohlc \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT' \
  --header 'client-id: 1000000001' \
  --data '{"NSE_EQ":[11536],"NSE_FNO":[49081,49082]}'
```

**Response:**

```json
{
    "data": {
        "NSE_EQ": {
            "11536": {
                "last_price": 4525.55,
                "ohlc": {
                    "open": 4521.45,
                    "close": 4507.85,
                    "high": 4530,
                    "low": 4500
                }
            }
        }
    },
    "status": "success"
}
```

| Field | Type | Description |
|---|---|---|
| `last_price` | float | Last traded price |
| `ohlc.open` | float | Day open price |
| `ohlc.close` | float | Previous day close price |
| `ohlc.high` | float | Day high price |
| `ohlc.low` | float | Day low price |

---

## Market Depth Data (Full Quote)

`POST https://api.dhan.co/v2/marketfeed/quote`

Returns the richest snapshot — LTP, OHLC, 5-level bid/ask depth, OI, volume, and circuit limits.

```bash
curl --request POST \
  --url https://api.dhan.co/v2/marketfeed/quote \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT' \
  --header 'client-id: 1000000001' \
  --data '{"NSE_FNO":[49081]}'
```

**Response:**

```json
{
    "data": {
        "NSE_FNO": {
            "49081": {
                "average_price": 0,
                "buy_quantity": 1825,
                "sell_quantity": 0,
                "last_price": 368.15,
                "last_quantity": 0,
                "last_trade_time": "01/01/1980 00:00:00",
                "lower_circuit_limit": 48.25,
                "upper_circuit_limit": 510.85,
                "net_change": 0,
                "volume": 0,
                "oi": 0,
                "oi_day_high": 0,
                "oi_day_low": 0,
                "ohlc": {
                    "open": 0,
                    "close": 368.15,
                    "high": 0,
                    "low": 0
                },
                "depth": {
                    "buy": [
                        { "quantity": 1800, "orders": 1, "price": 77 },
                        { "quantity": 25, "orders": 1, "price": 50 },
                        { "quantity": 0, "orders": 0, "price": 0 },
                        { "quantity": 0, "orders": 0, "price": 0 },
                        { "quantity": 0, "orders": 0, "price": 0 }
                    ],
                    "sell": [
                        { "quantity": 0, "orders": 0, "price": 0 },
                        { "quantity": 0, "orders": 0, "price": 0 },
                        { "quantity": 0, "orders": 0, "price": 0 },
                        { "quantity": 0, "orders": 0, "price": 0 },
                        { "quantity": 0, "orders": 0, "price": 0 }
                    ]
                }
            }
        }
    },
    "status": "success"
}
```

**Response Fields:**

| Field | Type | Description |
|---|---|---|
| `last_price` | float | Last traded price |
| `last_quantity` | int | Last traded quantity |
| `last_trade_time` | string | Timestamp of last trade |
| `average_price` | float | Volume-weighted average price (VWAP) for the day |
| `buy_quantity` | int | Total buy order quantity pending at exchange |
| `sell_quantity` | int | Total sell order quantity pending at exchange |
| `net_change` | float | Absolute change in LTP from previous day close |
| `volume` | int | Total traded volume for the day |
| `lower_circuit_limit` | float | Current lower circuit limit |
| `upper_circuit_limit` | float | Current upper circuit limit |
| `oi` | int | Open Interest (derivatives only) |
| `oi_day_high` | int | Day high Open Interest *(NSE_FNO only)* |
| `oi_day_low` | int | Day low Open Interest *(NSE_FNO only)* |
| `ohlc.open` | float | Day open price |
| `ohlc.close` | float | Previous day close |
| `ohlc.high` | float | Day high |
| `ohlc.low` | float | Day low |
| `depth.buy[n].price` | float | Price at buy depth level n (0=best bid) |
| `depth.buy[n].quantity` | int | Quantity at this buy depth level |
| `depth.buy[n].orders` | int | Number of open buy orders at this level |
| `depth.sell[n].price` | float | Price at sell depth level n (0=best ask) |
| `depth.sell[n].quantity` | int | Quantity at this sell depth level |
| `depth.sell[n].orders` | int | Number of open sell orders at this level |

> **Depth array:** Always 5 levels for both buy and sell. Unused levels return `quantity: 0, orders: 0, price: 0`.
