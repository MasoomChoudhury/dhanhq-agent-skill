# Trader's Control

Risk management tools built into Dhan — Kill Switch to halt trading instantly, and P&L-based auto-exit to protect profits and limit losses.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/killswitch?killSwitchStatus=ACTIVATE` | Activate or deactivate Kill Switch |
| `GET` | `/killswitch` | Get current Kill Switch status |
| `POST` | `/pnlExit` | Configure P&L based auto-exit |
| `DELETE` | `/pnlExit` | Stop / disable P&L based exit |
| `GET` | `/pnlExit` | Get current P&L exit configuration |

---

## Kill Switch

### Manage Kill Switch

`POST https://api.dhan.co/v2/killswitch?killSwitchStatus={ACTIVATE|DEACTIVATE}`

Activating the Kill Switch disables all trading for the current trading day.

```bash
# Activate
curl --request POST \
  --url 'https://api.dhan.co/v2/killswitch?killSwitchStatus=ACTIVATE' \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT'

# Deactivate
curl --request POST \
  --url 'https://api.dhan.co/v2/killswitch?killSwitchStatus=DEACTIVATE' \
  --header 'Content-Type: application/json' \
  --header 'access-token: JWT'
```

**Query Parameter:**

| Parameter | Values | Description |
|---|---|---|
| `killSwitchStatus` | `ACTIVATE` / `DEACTIVATE` | Action to perform |

> **⚠️ Pre-requisite:** All positions must be **closed** and there must be **no pending orders** before activating the Kill Switch.

**Response:**

```json
{
    "dhanClientId": "1000000009",
    "killSwitchStatus": "Kill Switch has been successfully activated"
}
```

---

### Kill Switch Status

`GET https://api.dhan.co/v2/killswitch`

Check whether Kill Switch is currently active for the account.

```bash
curl --request GET \
  --url https://api.dhan.co/v2/killswitch \
  --header 'access-token: JWT'
```

**Response:**

```json
{
    "dhanClientId": "1000000009",
    "killSwitchStatus": "ACTIVATE"
}
```

| Field | Type | Description |
|---|---|---|
| `dhanClientId` | string | Your Dhan Client ID |
| `killSwitchStatus` | string | `ACTIVATE` / `DEACTIVATE` |

---

## P&L Based Exit

Automatically exit all applicable positions when cumulative profit or loss crosses defined thresholds.

> **Scope:** Resets at end of each trading session — must be reconfigured daily if needed.

### Configure P&L Based Exit

`POST https://api.dhan.co/v2/pnlExit`

```bash
curl --request POST \
  --url https://api.dhan.co/v2/pnlExit \
  --header 'Content-Type: application/json' \
  --header 'access-token: {JWT}' \
  --data '{Request Body}'
```

**Request Body:**

```json
{
    "profitValue": "1500.00",
    "lossValue": "500.00",
    "productType": ["INTRADAY", "DELIVERY"],
    "enableKillSwitch": true
}
```

| Parameter | Type | Description |
|---|---|---|
| `profitValue` | float | Target profit amount — auto-exit triggers when P&L exceeds this |
| `lossValue` | float | Target loss amount — auto-exit triggers when loss exceeds this |
| `productType` | array | Product types to apply exit on: `INTRADAY` / `DELIVERY` |
| `enableKillSwitch` | boolean | If `true`, also activates Kill Switch when P&L exit triggers |

> **⚠️ Immediate trigger warning:**
> - If `profitValue` is set **below** current profit → exit triggers **immediately**
> - If `lossValue` is set **above** current loss → exit triggers **immediately**

**Response:**

```json
{
    "pnlExitStatus": "ACTIVE",
    "message": "P&L based exit configured successfully"
}
```

| Field | Type | Description |
|---|---|---|
| `pnlExitStatus` | string | `ACTIVE` / `INACTIVE` |
| `message` | string | Confirmation message |

---

### Stop P&L Based Exit

`DELETE https://api.dhan.co/v2/pnlExit`

Disables the active P&L based exit configuration.

```bash
curl --request DELETE \
  --url https://api.dhan.co/v2/pnlExit \
  --header 'access-token: {JWT}'
```

**Response:**

```json
{
    "pnlExitStatus": "DISABLED",
    "message": "P&L based exit stopped successfully"
}
```

---

### Get P&L Based Exit

`GET https://api.dhan.co/v2/pnlExit`

Fetch the current P&L exit configuration for the trading day.

```bash
curl --request GET \
  --url https://api.dhan.co/v2/pnlExit \
  --header 'access-token: {JWT}'
```

**Response:**

```json
{
    "pnlExitStatus": "ACTIVE",
    "profit": "1500.00",
    "loss": "500.00",
    "productType": ["INTRADAY", "DELIVERY"],
    "enable_kill_switch": true
}
```

| Field | Type | Description |
|---|---|---|
| `pnlExitStatus` | string | `ACTIVE` / `INACTIVE` |
| `profit` | float | Configured target profit threshold |
| `loss` | float | Configured target loss threshold |
| `productType` | array | Product types under the exit rule |
| `enable_kill_switch` | boolean | Whether Kill Switch is tied to this exit |
