# Portfolio and Positions

Retrieve holdings, open positions, convert between intraday and delivery, and exit all positions.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/holdings` | Retrieve holdings in demat account |
| `GET` | `/positions` | Retrieve all open positions for the day |
| `POST` | `/positions/convert` | Convert intraday ↔ delivery position |
| `DELETE` | `/positions` | Exit all open positions |

---

## Holdings

`GET https://api.dhan.co/v2/holdings`

Returns all holdings from previous trading sessions — both T1 (pending delivery) and fully delivered quantities.

```bash
curl --request GET \
  --url https://api.dhan.co/v2/holdings \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT'
```

**Response:**

```json
[
    {
        "exchange": "ALL",
        "tradingSymbol": "HDFC",
        "securityId": "1330",
        "isin": "INE001A01036",
        "totalQty": 1000,
        "dpQty": 1000,
        "t1Qty": 0,
        "availableQty": 1000,
        "collateralQty": 0,
        "avgCostPrice": 2655.0
    }
]
```

| Field | Type | Description |
|---|---|---|
| `exchange` | enum | Exchange (`ALL` for combined) |
| `tradingSymbol` | string | Trading symbol |
| `securityId` | string | Exchange security ID |
| `isin` | string | Universal standard ID (ISIN) |
| `totalQty` | int | Total quantity held |
| `dpQty` | int | Quantity delivered to demat account |
| `t1Qty` | int | Quantity pending delivery (T+1) |
| `availableQty` | int | Quantity available for transaction |
| `collateralQty` | int | Quantity pledged as collateral with broker |
| `avgCostPrice` | float | Average buy price of total quantity |

---

## Positions

`GET https://api.dhan.co/v2/positions`

Returns all open positions for the day, including F&O carryforward positions.

```bash
curl --request GET \
  --url https://api.dhan.co/v2/positions \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT'
```

**Response:**

```json
[
    {
        "dhanClientId": "1000000009",
        "tradingSymbol": "TCS",
        "securityId": "11536",
        "positionType": "LONG",
        "exchangeSegment": "NSE_EQ",
        "productType": "CNC",
        "buyAvg": 3345.8,
        "buyQty": 40,
        "costPrice": 3215.0,
        "sellAvg": 0.0,
        "sellQty": 0,
        "netQty": 40,
        "realizedProfit": 0.0,
        "unrealizedProfit": 6122.0,
        "rbiReferenceRate": 1.0,
        "multiplier": 1,
        "carryForwardBuyQty": 0,
        "carryForwardSellQty": 0,
        "carryForwardBuyValue": 0.0,
        "carryForwardSellValue": 0.0,
        "dayBuyQty": 40,
        "daySellQty": 0,
        "dayBuyValue": 133832.0,
        "daySellValue": 0.0,
        "drvExpiryDate": "0001-01-01",
        "drvOptionType": null,
        "drvStrikePrice": 0.0,
        "crossCurrency": false
    }
]
```

| Field | Type | Description |
|---|---|---|
| `dhanClientId` | string | Your Dhan Client ID |
| `tradingSymbol` | string | Trading symbol |
| `securityId` | string | Exchange security ID |
| `positionType` | enum | `LONG` / `SHORT` / `CLOSED` |
| `exchangeSegment` | enum | `NSE_EQ` / `NSE_FNO` / `NSE_CURRENCY` / `BSE_EQ` / `BSE_FNO` / `BSE_CURRENCY` / `MCX_COMM` |
| `productType` | enum | `CNC` / `INTRADAY` / `MARGIN` / `MTF` |
| `buyAvg` | float | Average buy price (mark to market) |
| `buyQty` | int | Total quantity bought |
| `costPrice` | int | Actual cost price |
| `sellAvg` | float | Average sell price (mark to market) |
| `sellQty` | int | Total quantities sold |
| `netQty` | int | `buyQty - sellQty` |
| `realizedProfit` | float | Booked profit or loss |
| `unrealizedProfit` | float | P&L on open position (mark to market) |
| `rbiReferenceRate` | float | RBI reference rate for forex pairs |
| `multiplier` | int | Multiplying factor for currency F&O |
| `carryForwardBuyQty` | int | Carryforward F&O long quantity |
| `carryForwardSellQty` | int | Carryforward F&O short quantity |
| `carryForwardBuyValue` | float | Carryforward F&O long value |
| `carryForwardSellValue` | float | Carryforward F&O short value |
| `dayBuyQty` | int | Quantity bought today |
| `daySellQty` | int | Quantity sold today |
| `dayBuyValue` | float | Value of quantity bought today |
| `daySellValue` | float | Value of quantity sold today |
| `drvExpiryDate` | string | F&O contract expiry date |
| `drvOptionType` | enum | `CALL` / `PUT` |
| `drvStrikePrice` | float | Strike price (for Options) |
| `crossCurrency` | boolean | `true` for non-INR currency pairs |

---

## Convert Position

`POST https://api.dhan.co/v2/positions/convert`

Convert an open position between intraday and delivery product types.

```bash
curl --request POST \
  --url https://api.dhan.co/v2/positions/convert \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT' \
  --data '{}'
```

**Request Body:**

```json
{
    "dhanClientId": "1000000009",
    "fromProductType": "INTRADAY",
    "exchangeSegment": "NSE_EQ",
    "positionType": "LONG",
    "securityId": "11536",
    "tradingSymbol": "",
    "convertQty": "40",
    "toProductType": "CNC"
}
```

| Field | Type | Description |
|---|---|---|
| `dhanClientId` | string | Your Dhan Client ID |
| `fromProductType` | enum | Current product type: `CNC` / `INTRADAY` / `MARGIN` |
| `exchangeSegment` | enum | Exchange segment of the position |
| `positionType` | enum | `LONG` / `SHORT` / `CLOSED` |
| `securityId` | string | Exchange security ID |
| `tradingSymbol` | string | Trading symbol |
| `convertQty` | int | Quantity to convert |
| `toProductType` | enum | Target product type: `CNC` / `INTRADAY` / `MARGIN` |

**Response:** `202 Accepted` (no response body)

---

## Exit All Positions

`DELETE https://api.dhan.co/v2/positions`

Squares off all open positions for the current trading day.

> **⚠️ Important:** This only exits **open positions**. It does **not** cancel pending orders.

```bash
curl --request DELETE \
  --url https://api.dhan.co/v2/positions \
  --header 'access-token: {JWT}'
```

**Response:**

```json
{
    "status": "SUCCESS",
    "message": "All orders and positions exited successfully"
}
```

| Field | Type | Description |
|---|---|---|
| `status` | string | `SUCCESS` / `ERROR` |
| `message` | string | Confirmation or error message |
