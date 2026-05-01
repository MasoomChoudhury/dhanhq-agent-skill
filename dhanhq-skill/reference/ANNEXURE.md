# Annexure — Enum Reference

Master reference for all enum values used across DhanHQ APIs.

---

## Exchange Segment

| Attribute | Exchange | Segment | Numeric Enum |
|---|---|---|---|
| `IDX_I` | Index | Index Value | `0` |
| `NSE_EQ` | NSE | Equity Cash | `1` |
| `NSE_FNO` | NSE | Futures & Options | `2` |
| `NSE_CURRENCY` | NSE | Currency | `3` |
| `BSE_EQ` | BSE | Equity Cash | `4` |
| `MCX_COMM` | MCX | Commodity | `5` |
| `BSE_CURRENCY` | BSE | Currency | `7` |
| `BSE_FNO` | BSE | Futures & Options | `8` |

> **Note:** Numeric enum values are used in WebSocket binary response headers. String attributes are used in REST API and WebSocket JSON messages.

---

## Product Type

| Attribute | Description |
|---|---|
| `CNC` | Cash & Carry — equity delivery trades |
| `INTRADAY` | Intraday — Equity, Futures & Options |
| `MARGIN` | Carry Forward — Futures & Options |
| `MTF` | Margin Trading Facility |

---

## Order Status

| Attribute | Description |
|---|---|
| `TRANSIT` | Did not reach the exchange server |
| `PENDING` | Order placed, awaiting execution |
| `PART_TRADED` | Partial quantity traded successfully |
| `TRADED` | Fully executed successfully |
| `REJECTED` | Rejected by broker or exchange |
| `CANCELLED` | Cancelled by user |
| `CLOSED` | *Super Order only* — both entry and exit legs placed |
| `TRIGGERED` | *Super Order only* — Target or Stop Loss leg triggered |
| `EXPIRED` | Order expired (e.g., end of day for DAY validity) |

---

## After Market Order (AMO) Timing

| Attribute | Description |
|---|---|
| `PRE_OPEN` | Pumped at pre-market session |
| `OPEN` | Pumped at market open |
| `OPEN_30` | Pumped 30 minutes after market open |
| `OPEN_60` | Pumped 60 minutes after market open |

---

## Expiry Code

Used in Historical Data and related derivative endpoints.

| Code | Description |
|---|---|
| `0` | Current / Near Expiry |
| `1` | Next Expiry |
| `2` | Far Expiry |

---

## Instrument Type

| Attribute | Description |
|---|---|
| `INDEX` | Index (cash value) |
| `EQUITY` | Equity / Stock |
| `FUTIDX` | Futures on Index |
| `OPTIDX` | Options on Index |
| `FUTSTK` | Futures on Stock |
| `OPTSTK` | Options on Stock |
| `FUTCOM` | Futures on Commodity |
| `OPTFUT` | Options on Commodity Futures |
| `FUTCUR` | Futures on Currency |
| `OPTCUR` | Options on Currency |

---

## Feed Request Codes (WebSocket)

Used when sending JSON subscription messages over WebSocket connections.

| Code | Action |
|---|---|
| `11` | Connect Feed |
| `12` | Disconnect Feed |
| `15` | Subscribe — Ticker Packet |
| `16` | Unsubscribe — Ticker Packet |
| `17` | Subscribe — Quote Packet |
| `18` | Unsubscribe — Quote Packet |
| `21` | Subscribe — Full Packet |
| `22` | Unsubscribe — Full Packet |
| `23` | Subscribe — Full Market Depth (20-level or 200-level) |
| `25` | Unsubscribe — Full Market Depth |

---

## Feed Response Codes (WebSocket Binary)

Byte 1 of every binary response header identifies the packet type.

| Code | Packet Type |
|---|---|
| `1` | Index Packet |
| `2` | Ticker Packet (LTP + LTT) |
| `4` | Quote Packet |
| `5` | OI Packet |
| `6` | Prev Close Packet |
| `7` | Market Status Packet |
| `8` | Full Packet (Quote + Depth + OI) |
| `41` | Full Market Depth — Bid (Buy) |
| `51` | Full Market Depth — Ask (Sell) |
| `50` | Feed Disconnect |

---

## Conditional Trigger — Comparison Types

| Type | Description | Mandatory Fields |
|---|---|---|
| `TECHNICAL_WITH_VALUE` | Technical indicator vs fixed numeric value | `indicatorName`, `operator`, `timeFrame`, `comparingValue` |
| `TECHNICAL_WITH_INDICATOR` | Technical indicator vs another indicator | `indicatorName`, `operator`, `timeFrame`, `comparingIndicatorName` |
| `TECHNICAL_WITH_CLOSE` | Technical indicator vs closing price | `indicatorName`, `operator`, `timeFrame` |
| `PRICE_WITH_VALUE` | Market price vs fixed value | `operator`, `comparingValue` |

---

## Conditional Trigger — Indicator Names

| Indicator | Description |
|---|---|
| `SMA_5` | Simple Moving Average (5 periods) |
| `SMA_10` | Simple Moving Average (10 periods) |
| `SMA_20` | Simple Moving Average (20 periods) |
| `SMA_50` | Simple Moving Average (50 periods) |
| `SMA_100` | Simple Moving Average (100 periods) |
| `SMA_200` | Simple Moving Average (200 periods) |
| `EMA_5` | Exponential Moving Average (5 periods) |
| `EMA_10` | Exponential Moving Average (10 periods) |
| `EMA_20` | Exponential Moving Average (20 periods) |
| `EMA_50` | Exponential Moving Average (50 periods) |
| `EMA_100` | Exponential Moving Average (100 periods) |
| `EMA_200` | Exponential Moving Average (200 periods) |
| `BB_UPPER` | Upper Bollinger Band |
| `BB_LOWER` | Lower Bollinger Band |
| `RSI_14` | Relative Strength Index (14 periods) |
| `ATR_14` | Average True Range (14 periods) |
| `STOCHASTIC` | Stochastic Oscillator |
| `STOCHRSI_14` | Stochastic RSI (14 periods) |
| `MACD_26` | MACD long-term component (26 periods) |
| `MACD_12` | MACD short-term component (12 periods) |
| `MACD_HIST` | MACD Histogram |

---

## Conditional Trigger — Operators

| Operator | Description |
|---|---|
| `CROSSING_UP` | Crosses above |
| `CROSSING_DOWN` | Crosses below |
| `CROSSING_ANY_SIDE` | Crosses either side |
| `GREATER_THAN` | Greater than |
| `LESS_THAN` | Less than |
| `GREATER_THAN_EQUAL` | Greater than or equal |
| `LESS_THAN_EQUAL` | Less than or equal |
| `EQUAL` | Equal |
| `NOT_EQUAL` | Not equal |

---

## Conditional Trigger — Alert Status

| Status | Description |
|---|---|
| `ACTIVE` | Alert is currently active and monitoring |
| `TRIGGERED` | Alert condition has been met |
| `EXPIRED` | Alert has expired |
| `CANCELLED` | Alert was cancelled |
