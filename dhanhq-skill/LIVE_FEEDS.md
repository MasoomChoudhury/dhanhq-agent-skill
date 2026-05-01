# Live Market Feed (WebSocket)

Real-time tick-by-tick market data via persistent WebSocket connections. All Dhan platforms use these same feeds.

> **Requests** → JSON | **Responses** → **Binary** (Little Endian) — requires a binary parser.

## Connection Limits

| Limit | Value |
|---|---|
| Max WebSocket connections per user | **5** |
| Max instruments per connection | **5000** |
| Max instruments per subscribe message | **100** |

---

## Establishing Connection

Connect via WebSocket with credentials in the **URL query parameters** (not headers):

```
wss://api-feed.dhan.co?version=2&token={JWT}&clientId={ClientId}&authType=2
```

| Parameter | Description |
|---|---|
| `version` *(required)* | Always `2` for DhanHQ v2 |
| `token` *(required)* | JWT access token |
| `clientId` *(required)* | Your Dhan Client ID |
| `authType` *(required)* | Always `2` |

---

## Subscribing to Instruments

Send a JSON message over the WebSocket connection after connecting. Max 100 instruments per message — send multiple messages to reach 5000.

```json
{
    "RequestCode": 15,
    "InstrumentCount": 2,
    "InstrumentList": [
        {
            "ExchangeSegment": "NSE_EQ",
            "SecurityId": "1333"
        },
        {
            "ExchangeSegment": "BSE_EQ",
            "SecurityId": "532540"
        }
    ]
}
```

| Field | Type | Description |
|---|---|---|
| `RequestCode` *(required)* | int | Data mode to subscribe (see Feed Request Codes below) |
| `InstrumentCount` *(required)* | int | Number of instruments in this message |
| `InstrumentList[].ExchangeSegment` *(required)* | enum | Exchange segment (see Annexure) |
| `InstrumentList[].SecurityId` *(required)* | string | Exchange security ID |

### Feed Request Codes

| Code | Data Mode | Packets Received |
|---|---|---|
| `15` | Ticker | Ticker + Prev Close |
| `17` | Quote | Quote + OI + Prev Close |
| `21` | Full | Full Packet (Quote + Depth + OI) + Prev Close |

---

## Keepalive (Ping-Pong)

- Server sends a **ping every 10 seconds**
- WebSocket library auto-responds with pong
- If no response for **40 seconds** → server closes the connection
- On disconnect, re-establish connection and re-subscribe

---

## Disconnecting

Send this JSON to gracefully disconnect:

```json
{
    "RequestCode": 12
}
```

> **Max connections:** If a 6th WebSocket is opened, the **first** (oldest) connection is forcibly closed with disconnect code **805**.

---

## Binary Response Format

All responses are **binary, Little Endian**. Every message starts with an 8-byte **Response Header**, followed by a payload that varies by packet type.

> **Endianness:** DhanHQ uses **Little Endian** — least significant byte first. If your system is Big Endian, specify endianness when reading the WebSocket.

### Response Header (8 bytes — same for all packets)

| Bytes | Type | Size | Description |
|---|---|---|---|
| 1 | `byte` | 1 | **Feed Response Code** — identifies packet type (see below) |
| 2–3 | `int16` | 2 | Total message length (header + payload) |
| 4 | `byte` | 1 | Exchange Segment (see Annexure) |
| 5–8 | `int32` | 4 | Security ID |

---

## Packet Structures

### Ticker Packet (Response Code: `2`)

Sent for each price tick. Also triggers a Prev Close packet on first subscription.

| Bytes | Type | Size | Description |
|---|---|---|---|
| 0–8 | header | 8 | Response Header (code `2`) |
| 9–12 | `float32` | 4 | Last Traded Price (LTP) |
| 13–16 | `int32` | 4 | Last Trade Time (LTT) — UNIX epoch |

---

### Prev Close Packet (Response Code: `6`)

Sent once when an instrument is first subscribed (any mode). Provides previous day baseline data.

| Bytes | Type | Size | Description |
|---|---|---|---|
| 0–8 | header | 8 | Response Header (code `6`) |
| 9–12 | `float32` | 4 | Previous day closing price |
| 13–16 | `int32` | 4 | Open Interest — previous day |

---

### Quote Packet (Response Code: `4`)

Full trade data. Subscribing to Quote mode also triggers OI packets automatically.

| Bytes | Type | Size | Description |
|---|---|---|---|
| 0–8 | header | 8 | Response Header (code `4`) |
| 9–12 | `float32` | 4 | Last Traded Price (LTP) |
| 13–14 | `int16` | 2 | Last Traded Quantity |
| 15–18 | `int32` | 4 | Last Trade Time (LTT) — UNIX epoch |
| 19–22 | `float32` | 4 | Average Trade Price (ATP / VWAP) |
| 23–26 | `int32` | 4 | Total Volume |
| 27–30 | `int32` | 4 | Total Sell Quantity |
| 31–34 | `int32` | 4 | Total Buy Quantity |
| 35–38 | `float32` | 4 | Day Open |
| 39–42 | `float32` | 4 | Day Close *(only sent post market close)* |
| 43–46 | `float32` | 4 | Day High |
| 47–50 | `float32` | 4 | Day Low |

---

### OI Data Packet (Response Code: `5`)

Automatically sent alongside Quote packets. Contains Open Interest for derivative contracts.

| Bytes | Type | Size | Description |
|---|---|---|---|
| 0–8 | header | 8 | Response Header (code `5`) |
| 9–12 | `int32` | 4 | Open Interest |

---

### Full Packet (Response Code: `8`)

The richest packet — includes everything from Quote + OI + 5-level market depth in one message.

| Bytes | Type | Size | Description |
|---|---|---|---|
| 0–8 | header | 8 | Response Header (code `8`) |
| 9–12 | `float32` | 4 | Last Traded Price (LTP) |
| 13–14 | `int16` | 2 | Last Traded Quantity |
| 15–18 | `int32` | 4 | Last Trade Time (LTT) — UNIX epoch |
| 19–22 | `float32` | 4 | Average Trade Price (ATP) |
| 23–26 | `int32` | 4 | Total Volume |
| 27–30 | `int32` | 4 | Total Sell Quantity |
| 31–34 | `int32` | 4 | Total Buy Quantity |
| 35–38 | `int32` | 4 | Open Interest *(derivatives only)* |
| 39–42 | `int32` | 4 | OI Day High *(NSE_FNO only)* |
| 43–46 | `int32` | 4 | OI Day Low *(NSE_FNO only)* |
| 47–50 | `float32` | 4 | Day Open |
| 51–54 | `float32` | 4 | Day Close *(only sent post market close)* |
| 55–58 | `float32` | 4 | Day High |
| 59–62 | `float32` | 4 | Day Low |
| 63–162 | Market Depth | 100 | 5 × 20-byte depth levels (see below) |

**Market Depth Structure (each of 5 levels — 20 bytes):**

| Bytes | Type | Size | Description |
|---|---|---|---|
| 1–4 | `int32` | 4 | Bid Quantity |
| 5–8 | `int32` | 4 | Ask Quantity |
| 9–10 | `int16` | 2 | Number of Bid Orders |
| 11–12 | `int16` | 2 | Number of Ask Orders |
| 13–16 | `float32` | 4 | Bid Price |
| 17–20 | `float32` | 4 | Ask Price |

---

### Disconnect Packet (Response Code: `50`)

Sent by server when it forcibly closes the connection.

| Bytes | Type | Size | Description |
|---|---|---|---|
| 0–8 | header | 8 | Response Header (code `50`) |
| 9–10 | `int16` | 2 | Disconnection reason code (e.g., `805` = max connections exceeded) |

---

## Response Code Summary

| Code | Packet Type | Feed |
|---|---|---|
| `2` | Ticker (LTP + LTT) | Live Market Feed |
| `4` | Quote (full trade data) | Live Market Feed |
| `5` | OI Data | Live Market Feed |
| `6` | Prev Close | Live Market Feed |
| `8` | Full (Quote + Depth + OI) | Live Market Feed |
| `41` | Bid (Buy) Depth | Full Market Depth |
| `51` | Ask (Sell) Depth | Full Market Depth |
| `50` | Disconnect notification | Both |

---

# Full Market Depth (WebSocket)

Extended order book — 20 or 200 levels of bid/ask depth streamed real-time via WebSocket.

> **Scope:** NSE Equity (`NSE_EQ`) and NSE Derivatives (`NSE_FNO`) **only**.
> Same binary Little Endian format as Live Market Feed. Requests = JSON, Responses = Binary.

## Connection Limits

| Level | Endpoint | Max Instruments per Connection |
|---|---|---|
| 20-level | `depth-api-feed.dhan.co` | **50** |
| 200-level | `full-depth-api.dhan.co` | **1** |

---

## Establishing Connection

### 20-Level Depth

```
wss://depth-api-feed.dhan.co/twentydepth?token={JWT}&clientId={ClientId}&authType=2
```

### 200-Level Depth

```
wss://full-depth-api.dhan.co/twohundreddepth?token={JWT}&clientId={ClientId}&authType=2
```

**Query Parameters (both):**

| Parameter | Description |
|---|---|
| `token` *(required)* | JWT access token |
| `clientId` *(required)* | Your Dhan Client ID |
| `authType` *(required)* | Always `2` |

---

## Subscribing to Instruments

Both levels use `RequestCode: 23`. The message structure differs.

### 20-Level Subscribe (up to 50 instruments per message)

```json
{
    "RequestCode": 23,
    "InstrumentCount": 1,
    "InstrumentList": [
        { "ExchangeSegment": "NSE_EQ", "SecurityId": "1333" }
    ]
}
```

### 200-Level Subscribe (1 instrument only per connection)

```json
{
    "RequestCode": 23,
    "ExchangeSegment": "NSE_EQ",
    "SecurityId": "1333"
}
```

> **200-level uses flat fields** — no `InstrumentList` array and no `InstrumentCount`.

---

## Keepalive

Same as Live Market Feed — server pings every 10 seconds, auto-pong within 40 seconds.

---

## Response Header (12 bytes — Full Market Depth)

> **Different from Live Market Feed's 8-byte header!**

**20-Level Header:**

| Bytes | Type | Size | Description |
|---|---|---|---|
| 1–2 | `int16` | 2 | Total message length |
| 3 | `byte` | 1 | Feed Response Code (`41`=Bid, `51`=Ask) |
| 4 | `byte` | 1 | Exchange Segment |
| 5–8 | `int32` | 4 | Security ID |
| 9–12 | `uint32` | 4 | Message Sequence *(ignore)* |

**200-Level Header:**

| Bytes | Type | Size | Description |
|---|---|---|---|
| 1–2 | `int16` | 2 | Total message length |
| 3 | `byte` | 1 | Feed Response Code (`41`=Bid, `51`=Ask) |
| 4 | `byte` | 1 | Exchange Segment |
| 5–8 | `int32` | 4 | Security ID |
| 9–12 | `uint32` | 4 | **Number of rows** — how many depth entries follow |

---

## Depth Packet

Bid (`41`) and Ask (`51`) arrive as **separate packets**.

- **20-level:** 20 entries × 16 bytes = 320 bytes payload (bytes 13–332)
- **200-level:** up to 200 entries × 16 bytes = up to 3200 bytes (bytes 13–3212)

**Each depth entry (16 bytes):**

| Bytes | Type | Size | Description |
|---|---|---|---|
| 1–8 | `float64` | 8 | Price |
| 9–12 | `uint32` | 4 | Quantity |
| 13–16 | `uint32` | 4 | Number of Orders |

> **Multi-instrument stacking (20-level):** Packets are stacked sequentially — Instrument 1 Bid → Instrument 1 Ask → Instrument 2 Bid → Instrument 2 Ask → ... Split by reading `Message Length` from each header.

---

## Disconnecting

Send `{"RequestCode": 12}` to disconnect gracefully. Server disconnect uses Response Code `50` with 2-byte reason code.
