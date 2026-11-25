# get_channel_summary

*Totals per channel for a period: SMS, WhatsApp, e-mail and voice calls.*

| | |
| --- | --- |
| **Permission** | any of `sms`, `whatsapp`, `gmail` (e-mail), `telephony` (voice) |
| **REST equivalent** | [GetChannelSummary](../../api/v2/messages/GetChannelSummary.md) |

Summarizes the account's sends for a period in one view: messages per status and value on each channel, and calls placed. With no arguments it covers the current month to date. Maximum period 93 days.

Only the channels enabled for the token are included; `channels_not_permitted` lists the channels you asked for that were left out.

## Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `date_start` | string | No | `YYYY-MM-DD`. Default: first day of the current month |
| `date_end` | string | No | `YYYY-MM-DD`. Default: today |
| `channels` | string | No | Comma-separated: `sms,whatsapp,email,voice`. Default: every channel enabled for the token |

## Example

```bash
curl -X POST 'https://vox20.velip.com.br/mcpserver/velip' \
  -H 'Authorization: Bearer YOUR_TOKEN_30_CHARS' \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "get_channel_summary",
      "arguments": {}
    }
  }'
```

## Responses

**Success:**

```json
{
  "success": true,
  "summary": {
    "sms": { "total": 15200, "pending": 0, "sent": 900, "delivered": 14100, "failed": 200, "value": 532.0, "replies": 340 },
    "whatsapp": { "total": 4100, "pending": 12, "sent": 150, "delivered": 1300, "read": 2580, "failed": 58, "value": 328.0 },
    "voice": { "calls": 48000, "answered": 21500, "not_answered": 26500, "value": 1920.0, "closed_until": "2026-11-24", "includes_today": true }
  },
  "period": { "date_start": "2026-11-01", "date_end": "2026-11-25" },
  "channels_not_permitted": ["email"]
}
```

For SMS and WhatsApp the buckets add up to `total`: `sent` = accepted without delivery confirmation, `delivered` = confirmed (on WhatsApp, not read yet), `read` = read (WhatsApp). `replies` counts every SMS received in the period. E-mail has `pending`, `sent`, `failed` and `skipped`. Voice comes from the daily closing up to `closed_until`, plus today's live counters. `value` is `null` (and `value_hidden=true`) when the user has no permission to see values. Every field is described in [GetChannelSummary](../../api/v2/messages/GetChannelSummary.md).

Limit: 200 calls per hour per account (`status_code` 429).
