# Channel summary

*Totals per channel for a period: SMS, WhatsApp, e-mail and voice calls, by status and value.*


**Endpoint:** `POST https://<base>/api/v2/GetChannelSummary.php`

One request returns, for the period, how many messages were sent on each channel and how they ended, plus the calls placed and the value charged. Use it for a dashboard or a daily report instead of listing every message.

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Request

Parameters can be sent as form fields or as a JSON body. All are optional: with only `tsid`, it summarizes the current month to date for every channel.

#### `tsid` — type: *string* — **required**

Token for the account.


#### `date_start` — type: *string*

Start date (`YYYY-MM-DD`). Without both dates, the period is the first day of the current month to today. With `date_end` only, the period starts 29 days before it (30 days in all).


#### `date_end` — type: *string*

End date (`YYYY-MM-DD`). With `date_start` only, the period ends today (or after 93 days, if earlier). The period can have at most **93 days**.


#### `channels` — type: *string*

Comma-separated list of `sms`, `whatsapp`, `email`, `voice`. Default: all four.


## Request example
```bash curl
curl -X POST 'https://<base>/api/v2/GetChannelSummary.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "date_start": "2026-11-01",
    "date_end": "2026-11-25"
  }'
```

## Response
```json 200 OK
{
  "return": {
    "status": "OK",
    "status_code": "0",
    "period": { "date_start": "2026-11-01", "date_end": "2026-11-25" }
  },
  "summary": {
    "sms": {
      "total": 15200, "pending": 0, "sent": 900, "delivered": 14100, "failed": 200,
      "value": 532.0, "replies": 340
    },
    "whatsapp": {
      "total": 4100, "pending": 12, "sent": 150, "delivered": 1300, "read": 2580, "failed": 58,
      "value": 328.0
    },
    "email": {
      "total": 2300, "pending": 0, "sent": 2250, "failed": 30, "skipped": 20,
      "value": 23.0
    },
    "voice": {
      "calls": 48000, "answered": 21500, "not_answered": 26500,
      "value": 1920.0, "closed_until": "2026-11-24", "includes_today": true
    }
  }
}
```

### SMS and WhatsApp

The buckets are mutually exclusive and add up to `total` (see the [normalized status](GetMessageStatus.md#status)):

- **`pending`** — queued.
- **`sent`** — accepted by the operator or Meta, no delivery confirmation.
- **`delivered`** — delivery confirmed. On WhatsApp, delivered and not read yet.
- **`read`** — WhatsApp only: read by the recipient.
- **`failed`** — not sent or not delivered.
- **`replies`** — SMS only: every SMS received in the period (answers to campaigns, to API sends and to AI agent conversations). The SMS sent by AI agents are counted in `total`.

### E-mail

`pending`, `sent`, `failed` and `skipped` (not sent because the address had unsubscribed), adding up to `total`. E-mail has no delivery or read tracking.

### Voice

- **`calls`**, **`answered`**, **`not_answered`** — calls placed in the period.
- **`closed_until`** — last day of the period already in the daily closing. Today's calls come from live counters, and `includes_today` is `true` when the period includes today.

### Value

`value` is the price charged on each channel. When the user of the token has no permission to see values, every `value` is `null` and the response carries `return.value_hidden: true`.

### Rate limit

**200 requests per account per hour.** Above it: **HTTP 429**, `status_code: 429` and a `Retry-After` header (seconds).

## Error codes

| Code | HTTP | `status` | Cause |
| --- | --- | --- | --- |
| `460` | 400 | `Invalid channel '<name>': use sms, whatsapp, email or voice` | Unknown name in `channels`. |
| `461` | 400 | `Invalid date: use YYYY-MM-DD in date_start and date_end` | Date format. |
| `462` | 400 | `Period too long: max 93 days per request (got N). ...` | Period longer than 93 days. |
| `463` | 400 | `date_end must be on or after date_start` | Dates inverted. |
| `429` | 429 | `Rate limit exceeded: max 200 requests per hour` | See [Rate limit](#rate-limit). |
| `500` | 500 | `internal error` | Temporary failure on the Velip side. Repeat later. |

It also returns the [global authentication codes](../errors.md) (HTTP 401).
