# Conditional Trigger

Place orders automatically when price or technical indicator conditions are met. Supports multiple orders per trigger and indicator combinations.

> **Scope:** Currently supported for **Equities and Indices only** (not F&O or commodities).
> **Postback:** Receive updates when triggered — set a Webhook URL while generating your Access Token.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/alerts/orders` | Create a conditional trigger |
| `PUT` | `/alerts/orders/{alertId}` | Modify a conditional trigger |
| `DELETE` | `/alerts/orders/{alertId}` | Delete a conditional trigger |
| `GET` | `/alerts/orders/{alertId}` | Get a specific trigger by ID |
| `GET` | `/alerts/orders` | Get all conditional triggers |

---

## Condition Object Reference

The `condition` object is used in Create, Modify, and Get responses:

| Field | Type | Description |
|---|---|---|
| `comparisonType` *(required)* | string | Type of comparison — e.g., `TECHNICAL_WITH_VALUE`, `PRICE_WITH_VALUE` (see Annexure) |
| `timeFrame` *(required)* | string | Timeframe for indicator evaluation: `DATE` / `ONE_MIN` / `FIVE_MIN` / `FIFTEEN_MIN` |
| `exchangeSegment` *(required)* | enum | `NSE_EQ` / `BSE_EQ` / `IDX_I` |
| `securityId` *(required)* | string | Exchange security ID |
| `indicatorName` *(cond. required)* | string | Technical indicator — e.g., `SMA_5`, `SMA_10` (see Annexure) |
| `operator` *(required)* | string | Comparison operator — e.g., `CROSSING_UP`, `CROSSING_DOWN` (see Annexure) |
| `comparingValue` *(cond. required)* | number | Value to compare against (used with `TECHNICAL_WITH_VALUE` or `PRICE_WITH_VALUE`) |
| `comparingIndicatorName` *(cond. required)* | string | Second indicator for indicator-vs-indicator comparison |
| `expDate` *(required)* | string (date) | Alert expiry date. Default: 1 year from creation |
| `frequency` *(required)* | string | `ONCE` — trigger fires once then deactivates |
| `userNote` | string | Optional user note for this alert |

---

## Orders Array Reference

The `orders` array defines which orders to place when the condition fires:

| Field | Type | Description |
|---|---|---|
| `transactionType` *(required)* | enum | `BUY` / `SELL` |
| `exchangeSegment` *(required)* | enum | Exchange segment (see Instruments reference) |
| `productType` *(required)* | enum | `CNC` / `INTRADAY` / `MARGIN` / `MTF` |
| `orderType` *(required)* | enum | `LIMIT` / `MARKET` / `STOP_LOSS` / `STOP_LOSS_MARKET` |
| `securityId` *(required)* | string | Exchange security ID |
| `quantity` *(required)* | int | Number of shares |
| `validity` *(required)* | enum | `DAY` / `IOC` |
| `price` *(required)* | string | Order price |
| `discQuantity` | string | Visible quantity (keep > 30%) |
| `triggerPrice` *(cond. required)* | string | Trigger price for SL / SL-M orders |

---

## Place Conditional Trigger

`POST https://api.dhan.co/v2/alerts/orders`

```bash
curl --request POST \
  --url https://api.dhan.co/v2/alerts/orders \
  --header 'Content-Type: application/json' \
  --header 'access-token: {JWT}' \
  --data '{Request Body}'
```

**Request Body:**

```json
{
  "dhanClientId": "123456789",
  "condition": {
    "comparisonType": "TECHNICAL_WITH_VALUE",
    "exchangeSegment": "NSE_EQ",
    "securityId": "12345",
    "indicatorName": "SMA_5",
    "timeFrame": "DAY",
    "operator": "CROSSING_UP",
    "comparingValue": 250,
    "expDate": "2019-08-24",
    "frequency": "ONCE",
    "userNote": "Price crossing SMA"
  },
  "orders": [
    {
      "transactionType": "BUY",
      "exchangeSegment": "NSE_EQ",
      "productType": "CNC",
      "orderType": "LIMIT",
      "securityId": "12345",
      "quantity": 10,
      "validity": "DAY",
      "price": "250.00",
      "discQuantity": "0",
      "triggerPrice": "0"
    }
  ]
}
```

See [Condition Object Reference](#condition-object-reference) and [Orders Array Reference](#orders-array-reference) for field details.

**Response:**

```json
{
  "alertId": "12345",
  "alertStatus": "ACTIVE"
}
```

| Field | Type | Description |
|---|---|---|
| `alertId` | string | Unique ID of the created conditional trigger |
| `alertStatus` | string | `ACTIVE` / `TRIGGERED` / `CANCELLED` / `EXPIRED` (see Annexure) |

---

## Modify Conditional Trigger

`PUT https://api.dhan.co/v2/alerts/orders/{alertId}`

Same request structure as Place — provide full `condition` and `orders` objects with updated values.

```bash
curl --request PUT \
  --url https://api.dhan.co/v2/alerts/orders/{alertId} \
  --header 'Content-Type: application/json' \
  --header 'access-token: {JWT}' \
  --data '{Request Body}'
```

**Request Body:** Same as Place, with `alertId` added at top level:

```json
{
  "dhanClientId": "123456789",
  "alertId": "12345",
  "condition": { ... },
  "orders": [ ... ]
}
```

**Response:** `{ "alertId": "12345", "alertStatus": "ACTIVE" }`

---

## Delete Conditional Trigger

`DELETE https://api.dhan.co/v2/alerts/orders/{alertId}`

No request body.

```bash
curl --request DELETE \
  --url https://api.dhan.co/v2/alerts/orders/{alertId} \
  --header 'access-token: {JWT}'
```

**Response:**

```json
{
  "alertId": "12345",
  "alertStatus": "CANCELLED"
}
```

---

## Get Conditional Trigger by ID

`GET https://api.dhan.co/v2/alerts/orders/{alertId}`

```bash
curl --request GET \
  --url https://api.dhan.co/v2/alerts/orders/{alertId} \
  --header 'access-token: {JWT}'
```

**Response:**

```json
{
  "alertId": "12345",
  "alertStatus": "ACTIVE",
  "createdTime": "2019-08-24T14:15:22Z",
  "triggeredTime": null,
  "lastPrice": "245.50",
  "condition": { ... },
  "orders": [ ... ]
}
```

**Additional Response Fields (beyond condition/orders):**

| Field | Type | Description |
|---|---|---|
| `alertId` | string | Unique trigger identifier |
| `alertStatus` | string | Current status (see Annexure) |
| `createdTime` | string | ISO timestamp when alert was created |
| `triggeredTime` | string | ISO timestamp when alert was triggered (`null` if not yet) |
| `lastPrice` | string | Last traded price of the instrument |

---

## Get All Conditional Triggers

`GET https://api.dhan.co/v2/alerts/orders`

Returns an array of all conditional triggers for the account.

```bash
curl --request GET \
  --url https://api.dhan.co/v2/alerts/orders \
  --header 'access-token: {JWT}'
```

**Response:** Array of objects — same structure as Get by ID above.

```json
[
  {
    "alertId": "12345",
    "alertStatus": "ACTIVE",
    "createdTime": "2019-08-24T14:15:22Z",
    "triggeredTime": null,
    "lastPrice": 245.5,
    "condition": { ... },
    "orders": [ ... ]
  }
]
```
