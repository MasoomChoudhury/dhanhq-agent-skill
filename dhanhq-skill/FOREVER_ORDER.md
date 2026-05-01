# Forever Order (Good Till Triggered)

Forever Orders (GTT) remain active until triggered or manually cancelled. Supports two modes:

| `orderFlag` | Description |
|---|---|
| `SINGLE` | One order triggered when price is hit |
| `OCO` | One Cancels Other — two legs; when one triggers, the other is automatically cancelled |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/forever/orders` | Create a forever order |
| `PUT` | `/forever/orders/{order-id}` | Modify an existing forever order |
| `DELETE` | `/forever/orders/{order-id}` | Cancel a forever order |
| `GET` | `/forever/all` | Retrieve all existing forever orders |

> **⚠️ Static IP whitelisting is required** for placement, modification, and cancellation.

> **Regulatory Notes:**
> - Market orders via API are converted to **limit orders with MPP**
> - Order rate limit: **10 orders/second**

---

## Create Forever Order

`POST https://api.dhan.co/v2/forever/orders`

```bash
curl --request POST \
  --url https://api.dhan.co/v2/forever/orders \
  --header 'Content-Type: application/json' \
  --header 'access-token: {JWT}' \
  --data '{Request JSON}'
```

**Request Body:**

```json
{
    "dhanClientId": "1000000132",
    "correlationId": "",
    "orderFlag": "OCO",
    "transactionType": "BUY",
    "exchangeSegment": "NSE_EQ",
    "productType": "CNC",
    "orderType": "LIMIT",
    "validity": "DAY",
    "securityId": "1333",
    "quantity": 5,
    "disclosedQuantity": 1,
    "price": 1428,
    "triggerPrice": 1427,
    "price1": 1420,
    "triggerPrice1": 1419,
    "quantity1": 10
}
```

**Request Parameters:**

| Field | Type | Description |
|---|---|---|
| `dhanClientId` *(required)* | string | Your Dhan Client ID |
| `correlationId` | string | User-defined tracking ID. Max 30 chars, `[a-zA-Z0-9 _-]` |
| `orderFlag` *(required)* | enum | `SINGLE` / `OCO` |
| `transactionType` *(required)* | enum | `BUY` / `SELL` |
| `exchangeSegment` *(required)* | enum | `NSE_EQ` / `NSE_FNO` / `BSE_EQ` / `MCX_COMM` |
| `productType` *(required)* | enum | `CNC` / `MTF` |
| `orderType` *(required)* | enum | `LIMIT` / `MARKET` |
| `validity` *(required)* | enum | `DAY` / `IOC` |
| `securityId` *(required)* | string | Exchange security ID |
| `quantity` *(required)* | int | Number of shares |
| `disclosedQuantity` | int | Visible quantity (keep > 30% of total) |
| `price` *(required)* | float | Order price |
| `triggerPrice` *(required)* | float | Price at which order is triggered |
| `price1` *(cond. required)* | float | Target price for OCO second leg |
| `triggerPrice1` *(cond. required)* | float | Target trigger price for OCO second leg |
| `quantity1` *(cond. required)* | int | Target quantity for OCO second leg |

> `price1`, `triggerPrice1`, `quantity1` are **required only for OCO orders**.

**Response:**

```json
{
    "orderId": "5132208051112",
    "orderStatus": "PENDING"
}
```

| Field | Type | Description |
|---|---|---|
| `orderId` | string | Dhan-generated order ID |
| `orderStatus` | enum | `TRANSIT` / `PENDING` / `REJECTED` / `CANCELLED` / `TRADED` / `EXPIRED` / `CONFIRM` |

---

## Modify Forever Order

`PUT https://api.dhan.co/v2/forever/orders/{order-id}`

Modifiable fields: price, quantity, order type, disclosed quantity, trigger price, and validity.

```bash
curl --request PUT \
  --url https://api.dhan.co/v2/forever/orders/{order-id} \
  --header 'Content-Type: application/json' \
  --header 'access-token: {JWT}' \
  --data '{Request JSON}'
```

**Request Body:**

```json
{
    "dhanClientId": "1000000132",
    "orderId": "5132208051112",
    "orderFlag": "SINGLE",
    "orderType": "LIMIT",
    "legName": "TARGET_LEG",
    "quantity": 15,
    "price": 1421,
    "disclosedQuantity": 1,
    "triggerPrice": 1420,
    "validity": "DAY"
}
```

**Request Parameters:**

| Field | Type | Description |
|---|---|---|
| `dhanClientId` *(required)* | string | Your Dhan Client ID |
| `orderId` *(required)* | string | Order ID to modify |
| `orderFlag` *(required)* | enum | `SINGLE` / `OCO` |
| `orderType` *(required)* | enum | `LIMIT` / `MARKET` / `STOP_LOSS` / `STOP_LOSS_MARKET` |
| `legName` *(required)* | enum | `TARGET_LEG` (single or first OCO leg) / `STOP_LOSS_LEG` (second OCO leg) |
| `quantity` *(required)* | int | New quantity |
| `price` *(required)* | float | New price |
| `disclosedQuantity` | int | Visible quantity (keep > 30%) |
| `triggerPrice` *(required)* | float | New trigger price |
| `validity` *(required)* | enum | `DAY` / `IOC` |

**Response:** `{ "orderId": "...", "orderStatus": "PENDING" }`

---

## Delete Forever Order

`DELETE https://api.dhan.co/v2/forever/orders/{order-id}`

No request body. Returns `202 Accepted` on success.

```bash
curl --request DELETE \
  --url https://api.dhan.co/v2/forever/orders/{order-id} \
  --header 'access-token: {JWT}'
```

**Response:**

```json
{
    "orderId": "5132208051112",
    "orderStatus": "CANCELLED"
}
```

---

## All Forever Orders

`GET https://api.dhan.co/v2/forever/all`

> **Note:** The endpoint is `/forever/all`, not `/forever/orders`.

Returns all active forever orders in the account.

```bash
curl --request GET \
  --url https://api.dhan.co/v2/forever/all \
  --header 'access-token: {JWT}'
```

**Response:**

```json
[
    {
        "dhanClientId": "1000000132",
        "orderId": "1132208051115",
        "orderStatus": "CONFIRM",
        "transactionType": "BUY",
        "exchangeSegment": "NSE_EQ",
        "productType": "CNC",
        "orderType": "SINGLE",
        "tradingSymbol": "HDFCBANK",
        "securityId": "1333",
        "quantity": 10,
        "price": 1428,
        "triggerPrice": 1427,
        "legName": "ENTRY_LEG",
        "createTime": "2022-08-05 12:41:19",
        "updateTime": null,
        "exchangeTime": null,
        "drvExpiryDate": null,
        "drvOptionType": null,
        "drvStrikePrice": 0
    }
]
```

**Response Parameters:**

| Field | Type | Description |
|---|---|---|
| `dhanClientId` | string | Your Dhan Client ID |
| `orderId` | string | Dhan-generated order ID |
| `orderStatus` | enum | `TRANSIT` / `PENDING` / `REJECTED` / `CANCELLED` / `TRADED` / `EXPIRED` / `CONFIRM` |
| `transactionType` | enum | `BUY` / `SELL` |
| `exchangeSegment` | enum | `NSE_EQ` / `NSE_FNO` / `BSE_EQ` / `MCX_COMM` |
| `productType` | enum | `CNC` / `INTRADAY` / `MARGIN` |
| `orderType` | enum | `SINGLE` / `OCO` |
| `tradingSymbol` | string | Trading symbol of the instrument |
| `securityId` | string | Exchange security ID |
| `quantity` | int | Number of shares |
| `price` | float | Order price |
| `triggerPrice` | float | Trigger price |
| `legName` | enum | `TARGET_LEG` (single/first OCO leg) / `STOP_LOSS_LEG` (second OCO leg) |
| `createTime` | string | Forever order creation time |
| `updateTime` | string | Last update time |
| `exchangeTime` | string | Time order reached exchange |
| `drvExpiryDate` | string | Expiry date for derivative contracts |
| `drvOptionType` | enum | `CALL` / `PUT` |
| `drvStrikePrice` | float | Strike price for options |

> **`CONFIRM` status** is unique to Forever Orders — it means the order is confirmed and waiting to be triggered.
