# Super Order

Super Orders bundle entry, target, and stop-loss legs into a single order request, with optional trailing stop loss. Available across all exchanges and segments (Intraday, CNC, MTF).

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/super/orders` | Create a new super order |
| `PUT` | `/super/orders/{order-id}` | Modify a pending super order |
| `DELETE` | `/super/orders/{order-id}/{order-leg}` | Cancel a super order leg |
| `GET` | `/super/orders` | Retrieve all super orders for the day |

> **⚠️ Static IP whitelisting is required** for all Super Order placement, modification, and cancellation APIs.

> **Regulatory Notes:**
> - Market orders via API are converted to **limit orders with MPP**
> - Order rate limit: **10 orders/second**

---

## Place Super Order

`POST https://api.dhan.co/v2/super/orders`

```bash
curl --request POST \
  --url https://api.dhan.co/v2/super/orders \
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
    "productType": "CNC",
    "orderType": "LIMIT",
    "securityId": "11536",
    "quantity": 5,
    "price": 1500,
    "targetPrice": 1600,
    "stopLossPrice": 1400,
    "trailingJump": 10
}
```

**Request Parameters:**

| Field | Type | Description |
|---|---|---|
| `dhanClientId` *(required)* | string | Your Dhan Client ID |
| `correlationId` | string | User-defined tracking ID. Max 30 chars, `[a-zA-Z0-9 _-]` |
| `transactionType` *(required)* | enum | `BUY` / `SELL` |
| `exchangeSegment` *(required)* | enum | Exchange segment (see Instruments reference) |
| `productType` *(required)* | enum | `CNC` / `INTRADAY` / `MARGIN` / `MTF` |
| `orderType` *(required)* | enum | `LIMIT` / `MARKET` |
| `securityId` *(required)* | string | Exchange security ID |
| `quantity` *(required)* | int | Number of shares |
| `price` *(required)* | float | Entry price |
| `targetPrice` *(required)* | float | Target exit price |
| `stopLossPrice` *(required)* | float | Stop-loss trigger price |
| `trailingJump` *(required)* | float | Price increment by which stop loss trails |

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
| `orderStatus` | enum | `TRANSIT` / `PENDING` / `REJECTED` |

---

## Modify Super Order

`PUT https://api.dhan.co/v2/super/orders/{order-id}`

Modify any leg of a super order while it is in `PENDING` or `PART_TRADED` state.

**Modification rules by leg:**

| `legName` | What can be modified | Condition |
|---|---|---|
| `ENTRY_LEG` | quantity, price, targetPrice, stopLossPrice, trailingJump, orderType | Only when main order is `PENDING` or `PART_TRADED` |
| `TARGET_LEG` | targetPrice, trailingJump | After entry is `TRADED` |
| `STOP_LOSS_LEG` | stopLossPrice, trailingJump | After entry is `TRADED` |

```bash
curl --request PUT \
  --url https://api.dhan.co/v2/super/orders/{order-id} \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT' \
  --data '{Request JSON}'
```

**Request Body (Entry Leg example):**

```json
{
    "dhanClientId": "1000000009",
    "orderId": "112111182045",
    "orderType": "LIMIT",
    "legName": "ENTRY_LEG",
    "quantity": "40",
    "price": "1300",
    "targetPrice": 1450,
    "stopLossPrice": 1350,
    "trailingJump": 20
}
```

**Request Parameters:**

| Field | Type | Description |
|---|---|---|
| `dhanClientId` *(required)* | string | Your Dhan Client ID |
| `orderId` *(required)* | string | Order ID to modify |
| `legName` *(required)* | enum | `ENTRY_LEG` / `TARGET_LEG` / `STOP_LOSS_LEG` |
| `orderType` *(cond. required)* | enum | `LIMIT` / `MARKET` |
| `quantity` *(cond. required)* | int | New quantity — only for `ENTRY_LEG` |
| `price` *(cond. required)* | float | New price — only for `ENTRY_LEG` |
| `targetPrice` *(cond. required)* | float | New target price — `ENTRY_LEG` or `TARGET_LEG` |
| `stopLossPrice` *(cond. required)* | float | New stop-loss price — `ENTRY_LEG` or `STOP_LOSS_LEG` |
| `trailingJump` *(cond. required)* | float | New trailing jump — `ENTRY_LEG` or `STOP_LOSS_LEG`. Pass `0` to cancel trailing |

**Response:**

```json
{
    "orderId": "112111182045",
    "orderStatus": "TRANSIT"
}
```

---

## Cancel Super Order

`DELETE https://api.dhan.co/v2/super/orders/{order-id}/{order-leg}`

Cancel a specific leg or the entire super order. Returns `202 Accepted` on success.

```bash
curl --request DELETE \
  --url https://api.dhan.co/v2/super/orders/{order-id}/{order-leg} \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT'
```

**Path Parameters:**

| Field | Description | Values |
|---|---|---|
| `order-id` *(required)* | Order ID to cancel | e.g., `112111182198` |
| `order-leg` *(required)* | Which leg to cancel | `ENTRY_LEG` / `TARGET_LEG` / `STOP_LOSS_LEG` |

> **Notes:**
> - Cancelling `ENTRY_LEG` cancels **all legs**
> - Once a `TARGET_LEG` or `STOP_LOSS_LEG` is cancelled, it **cannot be re-added**

**Response:**

```json
{
    "orderId": "112111182045",
    "orderStatus": "CANCELLED"
}
```

---

## Super Order List

`GET https://api.dhan.co/v2/super/orders`

Returns all super orders for the day. Each entry order contains nested `legDetails` for its target and stop-loss legs.

```bash
curl --request GET \
  --url https://api.dhan.co/v2/super/orders \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT'
```

**Response Example:**

```json
[
    {
        "dhanClientId": "1100003626",
        "orderId": "5925022734212",
        "correlationId": "string",
        "orderStatus": "PENDING",
        "transactionType": "BUY",
        "exchangeSegment": "NSE_EQ",
        "productType": "CNC",
        "orderType": "LIMIT",
        "validity": "DAY",
        "tradingSymbol": "HDFCBANK",
        "securityId": "1333",
        "quantity": 10,
        "remainingQuantity": 10,
        "ltp": 1660.95,
        "price": 1500,
        "afterMarketOrder": false,
        "legName": "ENTRY_LEG",
        "exchangeOrderId": "11925022734212",
        "createTime": "2025-02-27 19:09:42",
        "updateTime": "2025-02-27 19:09:42",
        "exchangeTime": "2025-02-27 19:09:42",
        "omsErrorDescription": "",
        "averageTradedPrice": 0,
        "filledQty": 0,
        "legDetails": [
            {
                "orderId": "5925022734212",
                "legName": "STOP_LOSS_LEG",
                "transactionType": "SELL",
                "totalQuatity": 0,
                "remainingQuantity": 0,
                "triggeredQuantity": 0,
                "price": 1400,
                "orderStatus": "PENDING",
                "trailingJump": 10
            },
            {
                "orderId": "5925022734212",
                "legName": "TARGET_LEG",
                "transactionType": "SELL",
                "remainingQuantity": 0,
                "triggeredQuantity": 0,
                "price": 1550,
                "orderStatus": "PENDING",
                "trailingJump": 0
            }
        ]
    }
]
```

**Response Parameters (Entry Level):**

| Field | Type | Description |
|---|---|---|
| `dhanClientId` | string | Your Dhan Client ID |
| `orderId` | string | Dhan-generated order ID |
| `correlationId` | string | User-defined tracking ID |
| `orderStatus` | enum | `TRANSIT` / `PENDING` / `CLOSED` / `REJECTED` / `CANCELLED` / `PART_TRADED` / `TRADED` |
| `transactionType` | enum | `BUY` / `SELL` |
| `exchangeSegment` | enum | Exchange segment |
| `productType` | enum | `CNC` / `INTRADAY` / `MARGIN` / `MTF` |
| `orderType` | enum | `LIMIT` / `MARKET` |
| `validity` | enum | `DAY` |
| `tradingSymbol` | string | Trading symbol |
| `securityId` | string | Exchange security ID |
| `quantity` | int | Total ordered quantity |
| `remainingQuantity` | int | Pending quantity |
| `ltp` | float | Last traded price |
| `price` | float | Entry order price |
| `afterMarketOrder` | boolean | Whether this is an AMO order |
| `legName` | enum | Always `ENTRY_LEG` at top level |
| `exchangeOrderId` | string | Exchange-generated order ID |
| `createTime` | string | Order creation time |
| `updateTime` | string | Last updated time |
| `exchangeTime` | string | Time order reached exchange |
| `omsErrorDescription` | string | Error description if rejected |
| `averageTradedPrice` | int | Average execution price |
| `filledQty` | int | Traded quantity |
| `legDetails` | array | Nested array of target and stop-loss legs |

**`legDetails` Object:**

| Field | Type | Description |
|---|---|---|
| `orderId` | string | Order ID (same as parent) |
| `legName` | enum | `TARGET_LEG` / `STOP_LOSS_LEG` |
| `transactionType` | enum | `BUY` / `SELL` |
| `remainingQuantity` | int | Pending quantity for this leg |
| `triggeredQuantity` | int | Quantity placed on exchange for this leg |
| `price` | float | Leg price |
| `orderStatus` | enum | `PENDING` / `TRIGGERED` / `CANCELLED` / `TRADED` |
| `trailingJump` | float | Trailing jump for stop-loss leg (`0` if not trailing) |

> **Special order statuses:**
> - `CLOSED` — Entry leg and one of target/stop-loss leg is fully triggered
> - `TRIGGERED` — Indicates which of target/stop-loss leg was activated; check `triggeredQuantity` for placed quantity
