# Error Codes Reference

All error responses from DhanHQ APIs follow this structure:

```json
{
    "errorType": "Input Exception",
    "errorCode": "DH-905",
    "errorMessage": "Missing required fields, bad values for parameters etc."
}
```

---

## Trading API Errors (DH-9xx)

| Error Type | Code | Description |
|---|---|---|
| Invalid Authentication | `DH-901` | Client ID or access token is invalid or expired |
| Invalid Access | `DH-902` | User has not subscribed to Data APIs or does not have access to Trading APIs |
| User Account | `DH-903` | Account-level error — check if required segments are activated or other requirements are met |
| Rate Limit | `DH-904` | Too many requests — breaching rate limits. Throttle API calls |
| Input Exception | `DH-905` | Missing required fields or bad parameter values |
| Order Error | `DH-906` | Incorrect order request — cannot be processed |
| Data Error | `DH-907` | System unable to fetch data — incorrect parameters or no data present |
| Internal Server Error | `DH-908` | Server could not process request (rare) |
| Network Error | `DH-909` | API unable to communicate with backend system |
| Others | `DH-910` | Error from other reasons |
| Invalid IP | `DH-911` | Request originated from an IP address not whitelisted for this token |

---

## Data API & WebSocket Errors (8xx)

Used in Data APIs and WebSocket disconnect packets.

| Code | Description |
|---|---|
| `800` | Internal Server Error |
| `804` | Requested number of instruments exceeds limit |
| `805` | Too many requests or connections — further requests may result in the user being blocked |
| `806` | Data APIs not subscribed |
| `807` | Access token is expired |
| `808` | Authentication failed — Client ID or access token invalid |
| `809` | Access token is invalid |
| `810` | Client ID is invalid |
| `811` | Invalid expiry date |
| `812` | Invalid date format |
| `813` | Invalid SecurityId |
| `814` | Invalid request |

> **WebSocket note:** Error code `805` is also used as the disconnect reason code when more than 5 WebSocket connections are opened simultaneously.

---

## Rate Limits (Quick Reference)

| API Category | Limit |
|---|---|
| Orders (place/modify/cancel) | 10 requests/second |
| Non-trading APIs | 10 requests/second |
| Market Quote (`/marketfeed/*`) | 1 request/second, 1000 instruments/request |
| Option Chain (`/optionchain`) | 1 request/3 seconds |
| Data APIs (general) | Refer individual endpoint docs |
