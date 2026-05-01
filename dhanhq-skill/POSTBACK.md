# Postback (Webhooks)

Dhan sends real-time order status updates via HTTP POST to a configured Postback URL. Triggered on every order status change: `TRANSIT`, `PENDING`, `REJECTED`, `CANCELLED`, `TRADED`, `EXPIRED`, order modification, or partial fill.

**Scope:** Per access token — all trades from one access token go to one Postback URL.

---

## Setup

1. Go to [web.dhan.co](https://web.dhan.co) → My Profile → Access DhanHQ APIs
2. Enter your Postback URL in the **'Postback URL'** field before generating the token
3. Click **Generate** — the Postback URL is tied to the token

> **⚠️ Localhost blocked:** Postback does **not** work with `localhost` or `127.0.0.1` URLs. Use a publicly accessible URL.

> **Partners:** To receive postbacks for all orders across your user base, use the [Partner Login](AUTHENTICATION.md#partner-authentication--oauth-flow) module.

---

## Postback Payload

Dhan sends a raw JSON POST body to your Postback URL on every order update:

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
    "filled_qty": 1,
    "algoId": null
}
```

**Payload Fields:**

| Field | Type | Description |
|---|---|---|
| `dhanClientId` | string | Your Dhan Client ID |
| `orderId` | string | Dhan-generated order ID |
| `correlationId` | string | User-defined tracking ID |
| `orderStatus` | enum | `TRANSIT` / `PENDING` / `REJECTED` / `CANCELLED` / `TRADED` / `EXPIRED` |
| `transactionType` | enum | `BUY` / `SELL` |
| `exchangeSegment` | enum | `NSE_EQ` / `NSE_FNO` / `NSE_CURRENCY` / `BSE_EQ` / `MCX_COMM` |
| `productType` | enum | `CNC` / `INTRADAY` / `MARGIN` / `MTF` |
| `orderType` | enum | `LIMIT` / `MARKET` / `STOP_LOSS` / `STOP_LOSS_MARKET` |
| `validity` | enum | `DAY` / `IOC` |
| `tradingSymbol` | string | Trading symbol |
| `securityId` | string | Exchange security ID |
| `quantity` | int | Total ordered quantity |
| `disclosedQuantity` | int | Visible quantity |
| `price` | float | Order price |
| `triggerPrice` | float | Trigger price (SL / SL-M) |
| `afterMarketOrder` | boolean | Whether this is an AMO order |
| `createTime` | string | Order creation time |
| `updateTime` | string | Last activity time |
| `exchangeTime` | string | Time order reached exchange |
| `drvExpiryDate` | string | F&O expiry date (`null` for non-derivative) |
| `drvOptionType` | enum | `CALL` / `PUT` (`null` for non-option) |
| `drvStrikePrice` | float | Strike price for options (`0.0` for non-option) |
| `omsErrorCode` | string | Error code if order rejected/failed (`null` otherwise) |
| `omsErrorDescription` | string | Error description if rejected/failed |
| `filled_qty` | int | Quantity already traded ⚠️ *Note: uses `snake_case`, unlike rest of the API* |
| `algoId` | string | Exchange-registered Algo ID (`null` if not an algo order) |

> **⚠️ Casing inconsistency:** `filled_qty` is `snake_case` — all other fields are `camelCase`. Parse accordingly in your webhook handler.
