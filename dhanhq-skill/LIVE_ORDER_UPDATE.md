# Live Order Update (WebSocket)

Real-time order status updates delivered via WebSocket. Once connected and authenticated, all order events stream automatically — no polling needed.

**WebSocket Endpoint:**
```
wss://api-order-update.dhan.co
```

Messages are JSON. Triggered on every order state change: status updates, modifications, partial fills.

---

## Establishing Connection

Connect using any WebSocket library, then immediately send the authorization message.

### For Individual Users

Receives updates for all orders placed across the account, regardless of platform.

```json
{
    "LoginReq": {
        "MsgCode": 42,
        "ClientId": "1000000001",
        "Token": "JWT"
    },
    "UserType": "SELF"
}
```

| Field | Type | Description |
|---|---|---|
| `LoginReq.MsgCode` *(required)* | int | Always `42` for order updates |
| `LoginReq.ClientId` *(required)* | string | Your Dhan Client ID |
| `LoginReq.Token` *(required)* | string | JWT access token |
| `UserType` *(required)* | string | `SELF` for individual users |

---

### For Partners

Receives order updates for **all users** connected to the partner platform. Requires Partner Login module.

```json
{
    "LoginReq": {
        "MsgCode": 42,
        "ClientId": "partner_id"
    },
    "UserType": "PARTNER",
    "Secret": "partner_secret"
}
```

| Field | Type | Description |
|---|---|---|
| `LoginReq.MsgCode` *(required)* | int | Always `42` for order updates |
| `LoginReq.ClientId` *(required)* | string | `partner_id` from Dhan |
| `UserType` *(required)* | string | `PARTNER` for partner platforms |
| `Secret` *(required)* | string | `partner_secret` from Dhan |

> **Note:** Partner auth does **not** include a `Token` field — uses `Secret` instead.

---

## Order Update Payload

Each message arrives in this structure:

```json
{
    "Data": {
        "Exchange": "NSE",
        "Segment": "E",
        "Source": "N",
        "SecurityId": "14366",
        "ClientId": "1000000001",
        "ExchOrderNo": "1400000000404591",
        "OrderNo": "1124091136546",
        "Product": "C",
        "TxnType": "B",
        "OrderType": "LMT",
        "Validity": "DAY",
        "DiscQuantity": 1,
        "DiscQtyRem": 1,
        "RemainingQuantity": 1,
        "Quantity": 1,
        "TradedQty": 0,
        "Price": 13,
        "TriggerPrice": 0,
        "TradedPrice": 0,
        "AvgTradedPrice": 0,
        "AlgoOrdNo": null,
        "OffMktFlag": "0",
        "OrderDateTime": "2024-09-11 14:39:29",
        "ExchOrderTime": "2024-09-11 14:39:29",
        "LastUpdatedTime": "2024-09-11 14:39:29",
        "Remarks": "NR",
        "MktType": "NL",
        "ReasonDescription": "CONFIRMED",
        "LegNo": 1,
        "Instrument": "EQUITY",
        "Symbol": "IDEA",
        "ProductName": "CNC",
        "Status": "Cancelled",
        "LotSize": 1,
        "StrikePrice": null,
        "ExpiryDate": "0001-01-01 00:00:00",
        "OptType": "XX",
        "DisplayName": "Vodafone Idea",
        "Isin": "INE669E01016",
        "Series": "EQ",
        "GoodTillDaysDate": "2024-09-11",
        "RefLtp": 13.21,
        "TickSize": 0.01,
        "AlgoId": "0",
        "Multiplier": 1,
        "CorrelationId": ""
    },
    "Type": "order_alert"
}
```

**Field Reference:**

> ⚠️ **Abbreviated enum values** — WebSocket uses single-letter codes, unlike REST API:

| Abbreviated Field | Code → Meaning |
|---|---|
| `Product` | `C` = CNC, `I` = INTRADAY, `M` = MARGIN, `F` = MTF |
| `TxnType` | `B` = Buy, `S` = Sell |
| `OrderType` | `LMT` = Limit, `MKT` = Market, `SL` = Stop Loss, `SLM` = Stop Loss Market |
| `Source` | `P` = API order, `N` = Normal |
| `MktType` | `NL` = Normal Market, `AU` / `A1` / `A2` = Auction Market |
| `LegNo` | `1` = Entry Leg, `2` = Stop Loss Leg, `3` = Target Leg |
| `OffMktFlag` | `1` = AMO order, `0` = regular |

**All Fields:**

| Field | Type | Description |
|---|---|---|
| `Exchange` | string | Exchange where order is placed |
| `Segment` | string | Segment of the order |
| `Source` | string | Platform: `P` for API orders |
| `SecurityId` | string | Exchange security ID |
| `ClientId` | string | Your Dhan Client ID |
| `ExchOrderNo` | string | Exchange-generated order ID |
| `OrderNo` | string | Dhan-generated order ID |
| `Product` | enum | Abbreviated product type (see table above) |
| `TxnType` | enum | Abbreviated transaction type |
| `OrderType` | enum | Abbreviated order type |
| `Validity` | enum | `DAY` / `IOC` |
| `DiscQuantity` | int | Visible (disclosed) quantity |
| `DiscQtyRem` | int | Disclosed quantity pending execution |
| `RemainingQuantity` | int | Quantity pending execution |
| `Quantity` | int | Total order quantity |
| `TradedQty` | int | Quantity actually executed on exchange |
| `Price` | float | Order price |
| `TriggerPrice` | float | Trigger price (SL / SL-M) |
| `TradedPrice` | float | Price at which the trade executed |
| `AvgTradedPrice` | float | Average trade price (differs from `TradedPrice` on partial fills) |
| `AlgoOrdNo` | float | Entry leg order number — tracks related legs |
| `OffMktFlag` | string | `1` = AMO, `0` = regular |
| `OrderDateTime` | string | Time order was received by Dhan |
| `ExchOrderTime` | string | Time order was placed on exchange |
| `LastUpdatedTime` | string | Time of last modification or trade |
| `Remarks` | string | Remarks attached at order placement; also `"Super Order"` if part of a Super Order |
| `MktType` | string | Market type (see abbreviations above) |
| `ReasonDescription` | string | Order rejection reason or status (e.g., `CONFIRMED`) |
| `LegNo` | int | Leg identifier for Super Orders (1=Entry, 2=SL, 3=Target) |
| `Instrument` | string | Instrument type (e.g., `EQUITY`) |
| `Symbol` | string | Exchange symbol |
| `ProductName` | string | Full product type name (e.g., `CNC`) |
| `Status` | enum | `TRANSIT` / `PENDING` / `REJECTED` / `CANCELLED` / `TRADED` / `EXPIRED` |
| `LotSize` | int | Lot size for derivative instruments |
| `StrikePrice` | float | Option strike price (`null` for non-options) |
| `ExpiryDate` | string | Contract expiry date |
| `OptType` | string | `CE` / `PE` for options; `XX` for non-options |
| `DisplayName` | string | Full display name of the instrument |
| `Isin` | string | ISIN of the instrument |
| `Series` | string | Exchange series (e.g., `EQ`) |
| `GoodTillDaysDate` | string | Order validity for Forever Orders |
| `RefLtp` | float | LTP at the time of this order update |
| `TickSize` | float | Minimum price movement of the instrument |
| `AlgoId` | string | Exchange ID for special order types |
| `Multiplier` | int | Multiplier for commodity and currency contracts |
| `CorrelationId` | string | User-defined tracking ID (max 30 chars) |
