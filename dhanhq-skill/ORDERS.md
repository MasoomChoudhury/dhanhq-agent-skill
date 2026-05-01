# Orders

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/orders` | Place a new order |
| `PUT` | `/orders/{order-id}` | Modify a pending order |
| `DELETE` | `/orders/{order-id}` | Cancel a pending order |
| `POST` | `/orders/slicing` | Slice order into multiple legs (over freeze limit) |
| `GET` | `/orders` | Retrieve all orders for the day (Order Book) |
| `GET` | `/orders/{order-id}` | Retrieve status of a specific order |
| `GET` | `/orders/external/{correlation-id}` | Retrieve order status by correlation ID |
| `GET` | `/trades` | Retrieve all trades for the day (Trade Book) |
| `GET` | `/trades/{order-id}` | Retrieve trades for a specific order |

> **⚠️ Static IP is required** for Order Placement, Modification, and Cancellation APIs.

> **Regulatory Notes:**
> - Market orders via API are converted to **limit orders with MPP**
> - Order rate limit: **10 orders/second**
> - All API orders must originate from a **whitelisted static IP**

---

## Order Placement

`POST https://api.dhan.co/v2/orders`

```bash
curl --request POST \
  --url https://api.dhan.co/v2/orders \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT' \
  --data '{Request JSON}'
```

**Request Body:**

```json
{
    "dhanClientId": "1000000003",
    "correlationId": "123abc678",
    "transactionType": "BUY",
    "exchangeSegment": "NSE_EQ",
    "productType": "INTRADAY",
    "orderType": "MARKET",
    "validity": "DAY",
    "securityId": "11536",
    "quantity": "5",
    "disclosedQuantity": "",
    "price": "",
    "triggerPrice": "",
    "afterMarketOrder": false,
    "amoTime": ""
}
```

**Request Parameters:**

| Field | Type | Description |
|---|---|---|
| `dhanClientId` *(required)* | string | Your Dhan Client ID |
| `correlationId` | string | User-defined tracking ID. Max 30 chars. Allowed: `[a-zA-Z0-9 _-]` |
| `transactionType` *(required)* | enum | `BUY` / `SELL` |
| `exchangeSegment` *(required)* | enum | Exchange segment (see Instruments reference) |
| `productType` *(required)* | enum | `CNC` / `INTRADAY` / `MARGIN` / `MTF` |
| `orderType` *(required)* | enum | `LIMIT` / `MARKET` / `STOP_LOSS` / `STOP_LOSS_MARKET` |
| `validity` *(required)* | enum | `DAY` / `IOC` |
| `securityId` | string | Exchange security ID for the instrument |
| `quantity` *(required)* | int | Number of shares |
| `disclosedQuantity` | int | Visible quantity (keep > 30% of total quantity) |
| `price` *(required)* | float | Order price |
| `triggerPrice` *(cond. required)* | float | Trigger price for `STOP_LOSS` / `STOP_LOSS_MARKET` |
| `afterMarketOrder` *(cond. required)* | boolean | `true` for AMO orders |
| `amoTime` *(cond. required)* | enum | AMO timing: `PRE_OPEN` / `OPEN` / `OPEN_30` / `OPEN_60` |

**Response:**

```json
{
    "orderId": "112111182198",
    "orderStatus": "PENDING"
}
```

| Field | Type | Description |
|---|---|---|
| `orderId` | string | Dhan-generated order ID |
| `orderStatus` | enum | `TRANSIT` / `PENDING` / `REJECTED` / `CANCELLED` / `TRADED` / `EXPIRED` |

---

## Order Modification

`PUT https://api.dhan.co/v2/orders/{order-id}`

Modifiable fields: price, quantity, order type, and validity. Only pending orders can be modified.

```bash
curl --request PUT \
  --url https://api.dhan.co/v2/orders/{order-id} \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT' \
  --data '{Request JSON}'
```

**Request Body:**

```json
{
    "dhanClientId": "1000000009",
    "orderId": "112111182045",
    "orderType": "LIMIT",
    "quantity": "40",
    "price": "3345.8",
    "disclosedQuantity": "10",
    "triggerPrice": "",
    "validity": "DAY"
}
```

**Request Parameters:**

| Field | Type | Description |
|---|---|---|
| `dhanClientId` *(required)* | string | Your Dhan Client ID |
| `orderId` *(required)* | string | Order ID to modify |
| `orderType` *(required)* | enum | `LIMIT` / `MARKET` / `STOP_LOSS` / `STOP_LOSS_MARKET` |
| `quantity` *(cond. required)* | int | New quantity |
| `price` *(cond. required)* | float | New price |
| `disclosedQuantity` | int | Visible quantity (if used, keep > 30% of quantity) |
| `triggerPrice` *(cond. required)* | float | New trigger price for SL / SL-M orders |
| `validity` *(required)* | enum | `DAY` / `IOC` |

**Response:** `{ "orderId": "...", "orderStatus": "TRANSIT" }`

> Capped at **25 modifications per order**.

---

## Order Cancellation

`DELETE https://api.dhan.co/v2/orders/{order-id}`

No request body required. Returns `202 Accepted` on success.

```bash
curl --request DELETE \
  --url https://api.dhan.co/v2/orders/{order-id} \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT'
```

**Response:**

```json
{
    "orderId": "112111182045",
    "orderStatus": "CANCELLED"
}
```

---

## Order Slicing

`POST https://api.dhan.co/v2/orders/slicing`

Splits a large order into multiple smaller orders to place quantities above the F&O freeze limit.

Same request body as [Order Placement](#order-placement) above.

```bash
curl --request POST \
  --url https://api.dhan.co/v2/orders/slicing \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT' \
  --data '{Request JSON}'
```

---

## Order Book

`GET https://api.dhan.co/v2/orders`

Returns all orders placed during the day with their latest status.

```bash
curl --request GET \
  --url https://api.dhan.co/v2/orders \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT'
```

No request body. Response is an **array of Order Objects** (see [Order Object Reference](#order-object-reference) below).

---

## Get Order by Order ID

`GET https://api.dhan.co/v2/orders/{order-id}`

```bash
curl --request GET \
  --url https://api.dhan.co/v2/orders/{order-id} \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT'
```

No request body. Returns an **array with one Order Object**.

---

## Get Order by Correlation ID

`GET https://api.dhan.co/v2/orders/external/{correlation-id}`

Use when `orderId` is unknown — look up using your own tracking ID.

```bash
curl --request GET \
  --url https://api.dhan.co/v2/orders/external/{correlation-id} \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT'
```

No request body. Returns an **array with one Order Object**.

---

## Order Object Reference

Shared response structure for Order Book, Get Order by ID, and Get Order by Correlation ID:

```json
{
    "dhanClientId": "1000000003",
    "orderId": "112111182198",
    "correlationId": "123abc678",
    "orderStatus": "PENDING",
    "transactionType": "BUY",
    "exchangeSegment": "NSE_EQ",
    "productType": "INTRADAY",
    "orderType": "MARKET",
    "validity": "DAY",
    "tradingSymbol": "",
    "securityId": "11536",
    "quantity": 5,
    "disclosedQuantity": 0,
    "price": 0.0,
    "triggerPrice": 0.0,
    "afterMarketOrder": false,
    "createTime": "2021-11-24 13:33:03",
    "updateTime": "2021-11-24 13:33:03",
    "exchangeTime": "2021-11-24 13:33:03",
    "drvExpiryDate": null,
    "drvOptionType": null,
    "drvStrikePrice": 0.0,
    "omsErrorCode": null,
    "omsErrorDescription": null,
    "algoId": "string",
    "remainingQuantity": 5,
    "averageTradedPrice": 0,
    "filledQty": 0
}
```

| Field | Type | Description |
|---|---|---|
| `dhanClientId` | string | Your Dhan Client ID |
| `orderId` | string | Dhan-generated order ID |
| `correlationId` | string | User-defined tracking ID |
| `orderStatus` | enum | `TRANSIT` / `PENDING` / `REJECTED` / `CANCELLED` / `PART_TRADED` / `TRADED` / `EXPIRED` |
| `transactionType` | enum | `BUY` / `SELL` |
| `exchangeSegment` | enum | Exchange segment (see Instruments reference) |
| `productType` | enum | `CNC` / `INTRADAY` / `MARGIN` / `MTF` |
| `orderType` | enum | `LIMIT` / `MARKET` / `STOP_LOSS` / `STOP_LOSS_MARKET` |
| `validity` | enum | `DAY` / `IOC` |
| `tradingSymbol` | string | Trading symbol of the instrument |
| `securityId` | string | Exchange security ID |
| `quantity` | int | Total ordered quantity |
| `disclosedQuantity` | int | Visible quantity |
| `price` | float | Order price |
| `triggerPrice` | float | Trigger price (for SL / SL-M orders) |
| `afterMarketOrder` | boolean | Whether this is an AMO order |
| `createTime` | string | Order creation time |
| `updateTime` | string | Last activity time |
| `exchangeTime` | string | Time order reached the exchange |
| `drvExpiryDate` | string | F&O contract expiry date |
| `drvOptionType` | enum | `CALL` / `PUT` (for Options) |
| `drvStrikePrice` | float | Strike price (for Options) |
| `omsErrorCode` | string | Error code if order was rejected/failed |
| `omsErrorDescription` | string | Error description if order was rejected/failed |
| `algoId` | string | Exchange Algo ID |
| `remainingQuantity` | int | Pending quantity at exchange (`quantity - filledQty`) |
| `averageTradedPrice` | int | Average execution price |
| `filledQty` | int | Quantity already traded on exchange |

---

## Trade Book

`GET https://api.dhan.co/v2/trades`

Returns all trades executed during the day.

```bash
curl --request GET \
  --url https://api.dhan.co/v2/trades \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT'
```

---

## Trades of an Order

`GET https://api.dhan.co/v2/trades/{order-id}`

Returns all trade legs for a specific order (useful for partial fills).

```bash
curl --request GET \
  --url https://api.dhan.co/v2/trades/{order-id} \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT'
```

---

## Trade Object Reference

Shared response structure for Trade Book and Trades of an Order:

```json
{
    "dhanClientId": "1000000009",
    "orderId": "112111182045",
    "exchangeOrderId": "15112111182045",
    "exchangeTradeId": "15112111182045",
    "transactionType": "BUY",
    "exchangeSegment": "NSE_EQ",
    "productType": "INTRADAY",
    "orderType": "LIMIT",
    "tradingSymbol": "TCS",
    "securityId": "11536",
    "tradedQuantity": 40,
    "tradedPrice": 3345.8,
    "createTime": "2021-03-10 11:20:06",
    "updateTime": "2021-11-25 17:35:12",
    "exchangeTime": "2021-11-25 17:35:12",
    "drvExpiryDate": null,
    "drvOptionType": null,
    "drvStrikePrice": 0.0
}
```

| Field | Type | Description |
|---|---|---|
| `dhanClientId` | string | Your Dhan Client ID |
| `orderId` | string | Dhan-generated order ID |
| `exchangeOrderId` | string | Exchange-generated order ID |
| `exchangeTradeId` | string | Exchange-generated trade ID |
| `transactionType` | enum | `BUY` / `SELL` |
| `exchangeSegment` | enum | Exchange segment |
| `productType` | enum | `CNC` / `INTRADAY` / `MARGIN` / `MTF` |
| `orderType` | enum | `LIMIT` / `MARKET` / `STOP_LOSS` / `STOP_LOSS_MARKET` |
| `tradingSymbol` | string | Trading symbol (e.g., `TCS`) |
| `securityId` | string | Exchange security ID |
| `tradedQuantity` | int | Number of shares executed |
| `tradedPrice` | float | Execution price |
| `createTime` | string | Order creation time |
| `updateTime` | string | Last activity time |
| `exchangeTime` | string | Time order reached the exchange |
| `drvExpiryDate` | string | F&O contract expiry date |
| `drvOptionType` | enum | `CALL` / `PUT` (for Options) |
| `drvStrikePrice` | float | Strike price (for Options) |
