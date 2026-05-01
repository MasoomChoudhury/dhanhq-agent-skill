# Funds & Margin

Check margin requirements before placing orders and retrieve available fund limits.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/margincalculator` | Calculate margin for a single order |
| `POST` | `/margincalculator/multi` | Calculate margin for multiple orders |
| `GET` | `/fundlimit` | Retrieve available fund limits |

---

## Margin Calculator — Single Order

`POST https://api.dhan.co/v2/margincalculator`

Calculate SPAN, exposure, VAR margin, brokerage, and leverage for any order before placing it.

```bash
curl --request POST \
  --url https://api.dhan.co/v2/margincalculator \
  --header 'Content-Type: application/json' \
  --header 'access-token: {JWT}' \
  --data '{Request JSON}'
```

**Request Body:**

```json
{
    "dhanClientId": "1000000132",
    "exchangeSegment": "NSE_EQ",
    "transactionType": "BUY",
    "quantity": 5,
    "productType": "CNC",
    "securityId": "1333",
    "price": 1428,
    "triggerPrice": 1427
}
```

| Field | Type | Description |
|---|---|---|
| `dhanClientId` *(required)* | string | Your Dhan Client ID |
| `exchangeSegment` *(required)* | enum | `NSE_EQ` / `NSE_FNO` / `BSE_EQ` / `BSE_FNO` / `MCX_COMM` |
| `transactionType` *(required)* | enum | `BUY` / `SELL` |
| `quantity` *(required)* | int | Number of shares |
| `productType` *(required)* | enum | `CNC` / `INTRADAY` / `MARGIN` / `MTF` |
| `securityId` *(required)* | string | Exchange security ID |
| `price` *(required)* | float | Order price |
| `triggerPrice` *(cond. required)* | float | Trigger price for SL / SL-M orders |

**Response:**

```json
{
    "totalMargin": 2800.00,
    "spanMargin": 1200.00,
    "exposureMargin": 1003.00,
    "availableBalance": 10500.00,
    "variableMargin": 1000.00,
    "insufficientBalance": 0.00,
    "brokerage": 20.00,
    "leverage": "4.00"
}
```

| Field | Type | Description |
|---|---|---|
| `totalMargin` | float | Total margin required to place the order |
| `spanMargin` | float | SPAN margin component |
| `exposureMargin` | float | Exposure margin component |
| `availableBalance` | float | Available funds in trading account |
| `variableMargin` | float | VAR (Variable/Value-at-Risk) margin |
| `insufficientBalance` | float | Shortfall amount (`availableBalance - totalMargin`; `0` if sufficient) |
| `brokerage` | float | Brokerage charges for the order |
| `leverage` | string | Margin leverage ratio for the product type |

---

## Margin Calculator — Multi Order

`POST https://api.dhan.co/v2/margincalculator/multi`

Calculate combined margin requirements for multiple instruments in one request. Includes portfolio-level netting with existing positions and open orders.

> **Note:** Margin values returned are **indicative** and valid only for the current trading session.

```bash
curl --request POST \
  --url https://api.dhan.co/v2/margincalculator/multi \
  --header 'Content-Type: application/json' \
  --header 'access-token: {JWT}' \
  --data '{Request JSON}'
```

**Request Body:**

```json
{
    "includePosition": true,
    "includeOrders": true,
    "scripts": [
        {
            "exchangeSegment": "NSE_EQ",
            "transactionType": "BUY",
            "quantity": 100,
            "productType": "CNC",
            "securityId": "12345",
            "price": 250.50,
            "triggerPrice": 0
        }
    ]
}
```

| Field | Type | Description |
|---|---|---|
| `includePosition` | boolean | Include existing open positions in margin netting |
| `includeOrders` | boolean | Include open pending orders in margin calculation |
| `scripts` | array | List of orders to calculate margin for |
| `scripts[].exchangeSegment` | string | Exchange segment (e.g. `NSE_EQ`, `NSE_FNO`) |
| `scripts[].transactionType` | string | `BUY` / `SELL` |
| `scripts[].quantity` | int | Order quantity |
| `scripts[].productType` | string | `CNC` / `INTRADAY` / `MARGIN` / `MTF` |
| `scripts[].securityId` | string | Exchange security ID |
| `scripts[].price` | float | Order price |
| `scripts[].triggerPrice` | float | Trigger price (if applicable) |

**Response:**

```json
{
    "total_margin": "150000.00",
    "span_margin": "50000.00",
    "exposure_margin": "30000.00",
    "equity_margin": "70000.00",
    "fo_margin": "0.00",
    "commodity_margin": "0.00",
    "currency": "INR",
    "hedge_benefit": ""
}
```

| Field | Type | Description |
|---|---|---|
| `total_margin` | string | Combined total margin required |
| `span_margin` | string | Combined SPAN margin |
| `exposure_margin` | string | Combined exposure margin |
| `equity_margin` | string | Equity-specific margin |
| `fo_margin` | string | F&O-specific margin |
| `commodity_margin` | string | Commodity-specific margin |
| `currency` | string | Currency of margin values (e.g. `INR`) |
| `hedge_benefit` | string | Hedge benefit offset applied |

> **⚠️ Field name note:** The multi-order request uses `scripts` (not `scripList` as shown in some API doc examples). Use `scripts` for the correct field name.

---

## Fund Limit

`GET https://api.dhan.co/v2/fundlimit`

Retrieve complete fund details — balance, margin used, collateral, receivables, and withdrawable amount.

```bash
curl --request GET \
  --url https://api.dhan.co/v2/fundlimit \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT'
```

**Response:**

```json
{
    "dhanClientId": "1000000009",
    "availabelBalance": 98440.0,
    "sodLimit": 113642,
    "collateralAmount": 0.0,
    "receiveableAmount": 0.0,
    "utilizedAmount": 15202.0,
    "blockedPayoutAmount": 0.0,
    "withdrawableBalance": 98310.0
}
```

| Field | Type | Description |
|---|---|---|
| `dhanClientId` | string | Your Dhan Client ID |
| `availabelBalance` | float | Available amount to trade ⚠️ *Note: API returns `availabelBalance` (typo in API — not `availableBalance`)* |
| `sodLimit` | float | Start-of-day balance |
| `collateralAmount` | float | Amount received against collateral pledge |
| `receiveableAmount` | float | Amount available from pending delivery sales |
| `utilizedAmount` | float | Margin utilised so far today |
| `blockedPayoutAmount` | float | Amount blocked against a payout request |
| `withdrawableBalance` | float | Amount available to withdraw to bank |
