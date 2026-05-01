# Statement

Retrieve historical ledger transactions and trade history for analysis and reconciliation.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/ledger?from-date=&to-date=` | Ledger report (debit/credit transactions) |
| `GET` | `/trades/{from-date}/{to-date}/{page}` | Paginated historical trade data |

> **Note:** These are historical reporting endpoints. For today's live trades, use [Trade Book](ORDERS.md#trade-book) (`GET /trades`).

---

## Ledger Report

`GET https://api.dhan.co/v2/ledger`

Retrieve all debit and credit transactions for a trading account within a date range.

```bash
curl --request GET \
  --url 'https://api.dhan.co/v2/ledger?from-date=2024-01-01&to-date=2024-01-31' \
  --header 'access-token: {JWT}'
```

**Query Parameters:**

| Field | Description |
|---|---|
| `from-date` *(required)* | Start date in `YYYY-MM-DD` format |
| `to-date` *(required)* | End date in `YYYY-MM-DD` format |

**Response:**

```json
{
    "dhanClientId": "1000000001",
    "narration": "FUNDS WITHDRAWAL",
    "voucherdate": "Jun 22, 2022",
    "exchange": "NSE-CAPITAL",
    "voucherdesc": "PAYBNK",
    "vouchernumber": "202200036701",
    "debit": "20000.00",
    "credit": "0.00",
    "runbal": "957.29"
}
```

| Field | Type | Description |
|---|---|---|
| `dhanClientId` | string | Your Dhan Client ID |
| `narration` | string | Description of the transaction (e.g., `FUNDS WITHDRAWAL`) |
| `voucherdate` | string | Transaction date |
| `exchange` | string | Exchange for the transaction (e.g., `NSE-CAPITAL`) |
| `voucherdesc` | string | Nature/type of transaction (e.g., `PAYBNK`) |
| `vouchernumber` | string | System-generated transaction reference number |
| `debit` | string | Debit amount (non-zero when credit is `0.00`) |
| `credit` | string | Credit amount (non-zero when debit is `0.00`) |
| `runbal` | string | Running balance after this transaction |

---

## Trade History

`GET https://api.dhan.co/v2/trades/{from-date}/{to-date}/{page}`

Paginated historical trade data across all orders for a date range.

> **Pagination:** Pass `0` as the default page number. Increment for subsequent pages.

```bash
curl --request GET \
  --url 'https://api.dhan.co/v2/trades/2024-01-01/2024-01-31/0' \
  --header 'access-token: {JWT}'
```

**Path Parameters:**

| Field | Description |
|---|---|
| `from-date` *(required)* | Start date — `YYYY-MM-DD` |
| `to-date` *(required)* | End date — `YYYY-MM-DD` |
| `page` *(required)* | Page number. Pass `0` to start from the first page |

**Response:**

```json
[
    {
        "dhanClientId": "1000000001",
        "orderId": "212212307731",
        "exchangeOrderId": "76036896",
        "exchangeTradeId": "407958",
        "transactionType": "BUY",
        "exchangeSegment": "NSE_EQ",
        "productType": "CNC",
        "orderType": "MARKET",
        "tradingSymbol": null,
        "customSymbol": "Tata Motors",
        "securityId": "3456",
        "tradedQuantity": 1,
        "tradedPrice": 390.9,
        "isin": "INE155A01022",
        "instrument": "EQUITY",
        "sebiTax": 0.0004,
        "stt": 0,
        "brokerageCharges": 0,
        "serviceTax": 0.0025,
        "exchangeTransactionCharges": 0.0135,
        "stampDuty": 0,
        "createTime": "NA",
        "updateTime": "NA",
        "exchangeTime": "2022-12-30 10:00:46",
        "drvExpiryDate": "NA",
        "drvOptionType": "NA",
        "drvStrikePrice": 0
    }
]
```

**Response Parameters:**

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
| `tradingSymbol` | string | Exchange trading symbol (may be `null`) |
| `customSymbol` | string | Dhan's display name for the instrument |
| `securityId` | string | Exchange security ID |
| `tradedQuantity` | int | Shares executed |
| `tradedPrice` | float | Execution price |
| `isin` | string | Universal ISIN code |
| `instrument` | string | `EQUITY` / `DERIVATIVES` |
| `sebiTax` | string | SEBI turnover charges |
| `stt` | string | Securities Transaction Tax |
| `brokerageCharges` | string | Brokerage charges |
| `serviceTax` | string | Applicable service tax |
| `exchangeTransactionCharges` | string | Exchange transaction charge |
| `stampDuty` | string | Stamp duty charges |
| `createTime` | string | Order creation time (`"NA"` for historical records) |
| `updateTime` | string | Last activity time (`"NA"` for historical records) |
| `exchangeTime` | string | Time order reached exchange |
| `drvExpiryDate` | string | F&O expiry date (`"NA"` for non-derivative) |
| `drvOptionType` | enum | `CALL` / `PUT` (`"NA"` for non-option) |
| `drvStrikePrice` | float | Strike price for options (`0` for non-option) |
