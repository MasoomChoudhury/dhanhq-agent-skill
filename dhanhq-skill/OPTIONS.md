# Option Chain

Real-time option chain data across NSE, BSE, and MCX — OI, Greeks, IV, volume, and top bid/ask for all strikes of any underlying.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/optionchain` | Full option chain for a specific expiry |
| `POST` | `/optionchain/expirylist` | All active expiry dates for an underlying |

> **Rate limit:** **1 request per 3 seconds** — shared across all `/optionchain` calls.
> **Both `access-token` and `client-id` headers required** (same as Market Quote).

---

## Required Headers

| Header | Description |
|---|---|
| `access-token` *(required)* | JWT access token |
| `client-id` *(required)* | Your Dhan Client ID |

---

## Option Chain

`POST https://api.dhan.co/v2/optionchain`

Fetch the complete option chain for a single underlying and expiry. Returns all strikes with CE/PE data.

```bash
curl --request POST \
  --url https://api.dhan.co/v2/optionchain \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT' \
  --header 'client-id: 1000000001' \
  --data '{Request Body}'
```

**Request Body:**

```json
{
    "UnderlyingScrip": 13,
    "UnderlyingSeg": "IDX_I",
    "Expiry": "2024-10-31"
}
```

| Field | Type | Description |
|---|---|---|
| `UnderlyingScrip` *(required)* | int | Security ID of the underlying instrument |
| `UnderlyingSeg` *(required)* | enum | Segment of the underlying — use `IDX_I` for indices |
| `Expiry` *(required)* | string | Expiry date in `YYYY-MM-DD` format — get from Expiry List endpoint |

**Response:**

```json
{
    "data": {
        "last_price": 25642.8,
        "oc": {
            "25650.000000": {
                "ce": {
                    "average_price": 146.99,
                    "greeks": {
                        "delta": 0.53871,
                        "theta": -15.1539,
                        "gamma": 0.00132,
                        "vega": 12.18593
                    },
                    "implied_volatility": 9.789193798280868,
                    "last_price": 134,
                    "oi": 3786445,
                    "previous_close_price": 244.85,
                    "previous_oi": 402220,
                    "previous_volume": 31931705,
                    "security_id": 42528,
                    "top_ask_price": 134,
                    "top_ask_quantity": 1365,
                    "top_bid_price": 133.55,
                    "top_bid_quantity": 1625,
                    "volume": 117567970
                },
                "pe": { "...": "same structure as ce" }
            }
        }
    },
    "status": "success"
}
```

**Top-level response fields:**

| Field | Type | Description |
|---|---|---|
| `data.last_price` | float | LTP of the underlying |
| `data.oc` | object | Strike-keyed map of option data |
| `data.oc.{strike}` | object | Key is strike price as a string (e.g., `"25650.000000"`) |
| `data.oc.{strike}.ce` | object | Call option data for this strike |
| `data.oc.{strike}.pe` | object | Put option data for this strike |

> **Strike keys are strings** formatted as `"XXXXX.000000"` — parse accordingly when iterating.

**CE/PE option fields (identical structure for both):**

| Field | Type | Description |
|---|---|---|
| `last_price` | float | Last traded price |
| `average_price` | float | VWAP for the day |
| `volume` | int | Day volume |
| `oi` | int | Open Interest |
| `previous_close_price` | float | Previous day close |
| `previous_oi` | int | Previous day OI |
| `previous_volume` | int | Previous day volume |
| `security_id` | int | Security ID of this specific option contract |
| `top_bid_price` | float | Best current bid price |
| `top_bid_quantity` | int | Quantity at best bid |
| `top_ask_price` | float | Best current ask price |
| `top_ask_quantity` | int | Quantity at best ask |
| `implied_volatility` | float | IV of the option |
| `greeks.delta` | float | Change in premium per ₹1 move in underlying |
| `greeks.theta` | float | Time decay — how quickly premium decreases per day |
| `greeks.gamma` | float | Rate of change in delta per ₹1 move in underlying |
| `greeks.vega` | float | Change in premium per 1% change in IV |

---

## Expiry List

`POST https://api.dhan.co/v2/optionchain/expirylist`

Retrieve all active expiry dates for an underlying. Use this to get valid `Expiry` values for the Option Chain request.

```bash
curl --request POST \
  --url https://api.dhan.co/v2/optionchain/expirylist \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT' \
  --header 'client-id: 1000000001' \
  --data '{}'
```

**Request Body:**

```json
{
    "UnderlyingScrip": 13,
    "UnderlyingSeg": "IDX_I"
}
```

**Response:**

```json
{
    "data": [
        "2024-10-17",
        "2024-10-24",
        "2024-10-31",
        "2024-11-28",
        "2025-03-27",
        "2025-06-26"
    ],
    "status": "success"
}
```

| Field | Type | Description |
|---|---|---|
| `data[]` | string[] | All active expiry dates in `YYYY-MM-DD` format, ordered chronologically |

> **Recommended workflow:** Always call `/optionchain/expirylist` first to get valid expiry dates, then pass one to `/optionchain`.
