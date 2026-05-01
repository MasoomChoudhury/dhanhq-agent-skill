# EDIS (Electronic Delivery Instruction Slip)

To sell holding stocks, CDSL eDIS approval is required. This is a 3-step flow:
1. Generate T-PIN (sent to registered mobile)
2. Render the eDIS HTML form and enter T-PIN to mark stock for approval
3. Verify approval status before placing sell order

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/edis/tpin` | Generate T-PIN on registered mobile |
| `POST` | `/edis/form` | Get CDSL eDIS HTML form to enter T-PIN |
| `GET` | `/edis/inquire/{isin}` | Check eDIS approval status for a stock |

> **ISIN:** Get the ISIN of portfolio stocks from the [Holdings API](PORTFOLIO.md#holdings) response.

---

## Step 1: Generate T-PIN

`GET https://api.dhan.co/v2/edis/tpin`

Sends a T-PIN to the user's registered mobile number.

```bash
curl --request GET \
  --url https://api.dhan.co/v2/edis/tpin \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT'
```

**Response:** `202 Accepted` (no body)

---

## Step 2: Generate eDIS Form

`POST https://api.dhan.co/v2/edis/form`

Returns an escaped HTML form from CDSL. The client must **unescape and render** this form so the user can enter their T-PIN to mark the stock for eDIS approval.

```bash
curl --request POST \
  --url https://api.dhan.co/v2/edis/form \
  --header 'Content-Type: application/json' \
  --header 'access-token: {JWT}' \
  --data '{}'
```

**Request Body:**

```json
{
    "isin": "INE733E01010",
    "qty": 1,
    "exchange": "NSE",
    "segment": "EQ",
    "bulk": true
}
```

| Field | Type | Description |
|---|---|---|
| `isin` | string | ISIN of the stock to mark (get from Holdings API) |
| `qty` | int | Number of shares to mark for eDIS |
| `exchange` | string | `NSE` / `BSE` |
| `segment` | string | `EQ` |
| `bulk` | boolean | `true` to mark all stocks in portfolio at once |

**Response:**

```json
{
    "dhanClientId": "1000000401",
    "edisFormHtml": "<!DOCTYPE html>..."
}
```

| Field | Type | Description |
|---|---|---|
| `dhanClientId` | string | Your Dhan Client ID |
| `edisFormHtml` | string | Escaped HTML form — must be unescaped and rendered on client side |

> **Implementation note:** Unescape the `edisFormHtml` string and render it in a browser/webview. The form auto-submits to CDSL's `edis.cdslindia.com` endpoint and handles T-PIN entry. Once submitted, the stock is marked for eDIS.

---

## Step 3: Check eDIS Status

`GET https://api.dhan.co/v2/edis/inquire/{isin}`

Verify whether a stock is approved and marked for sell action before placing the sell order.

```bash
curl --request GET \
  --url https://api.dhan.co/v2/edis/inquire/{isin} \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT'
```

> **Tip:** Pass `ALL` instead of a specific ISIN to get eDIS status of all holdings in your portfolio.
> ```
> GET /edis/inquire/ALL
> ```

**Response:**

```json
{
    "clientId": "1000000401",
    "isin": "INE00IN01015",
    "totalQty": 10,
    "aprvdQty": 4,
    "status": "SUCCESS",
    "remarks": "eDIS transaction done successfully"
}
```

| Field | Type | Description |
|---|---|---|
| `clientId` | string | Your Dhan Client ID |
| `isin` | string | ISIN of the queried stock |
| `totalQty` | string | Total shares for this stock |
| `aprvdQty` | string | Number of approved shares |
| `status` | string | Status of the eDIS approval |
| `remarks` | string | Description of the status |
