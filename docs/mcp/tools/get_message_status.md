# get_message_status

*Status of SMS, WhatsApp and e-mail messages: one message, or a list.*

| | |
| --- | --- |
| **Permission** | the channel asked: `sms`, `whatsapp` or `gmail` (for `email`) |
| **REST equivalent** | [GetMessageStatus](../../api/v2/messages/GetMessageStatus.md) |

The message counterpart of [get_call_status](get_call_status.md). One channel per call. Looks up a single message by `id`, `message_id` or `ctid`, or lists messages by period (default last 7 days, maximum 31), campaign, recipient and status. Newest first.

The tool is listed when the token has any of the three channels; each call checks the channel asked.

Normalized `status`: `pending` (queued), `sent` (accepted, no delivery confirmation yet), `delivered`, `read` (WhatsApp only), `failed` (`error` has the reason), `skipped` (e-mail to an address that unsubscribed). E-mail has no delivery or read tracking.

For tokens without "full numbers" (all OAuth connectors), phone numbers and e-mails come masked (`return.numbers_masked=true`) in lists **and** in lookups by `id`; only a lookup by `message_id`, or by the `ctid` of a single send, returns them in full. `value` is `null` when the user has no permission to see values.

## Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `channel` | string | Yes | `sms`, `whatsapp` or `email` |
| `id` | string | No | Velip message id, for a single lookup (`id` returned by [send_email](send_email.md), `cdls_id` of the REST sends) |
| `message_id` | string | No | Provider id for a single lookup: WhatsApp `wamid`, SMS operator id or e-mail `Message-ID` |
| `ctid` | string | No | Your tracking id sent with the message. Searched in the last 31 days unless dates are given |
| `campaign_id` | string | No | Bulk campaign id (from [get_message_campaigns](get_message_campaigns.md)). Without dates, lists the whole campaign |
| `dest` | string | No | Phone number with country and area code (`5511999999999`), or e-mail address for `email` |
| `status` | string | No | `pending`, `sent`, `delivered`, `read`, `failed` (e-mail: `pending`, `sent`, `failed`, `skipped`) |
| `date_start` | string | No | `YYYY-MM-DD`. Default: 7 days ago |
| `date_end` | string | No | `YYYY-MM-DD`. Default: today. Maximum period 31 days |
| `max_records` | integer | No | Messages per page. Default 100, maximum 1000 |
| `last_id` | string | No | Pagination cursor: `pagination.next_id` of the previous response |

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
      "name": "get_message_status",
      "arguments": {
        "channel": "whatsapp",
        "campaign_id": "3456",
        "status": "failed"
      }
    }
  }'
```

## Responses

**Success:**

```json
{
  "success": true,
  "channel": "whatsapp",
  "messages": [
    {
      "id": 9876545,
      "channel": "whatsapp",
      "status": "failed",
      "date": "2026-11-07",
      "time": "10:00:05",
      "dest": "xxxxx999",
      "from": "5511888888888",
      "campaign_id": 3456,
      "message_id": "wamid.HBgN...",
      "origin": "bulk",
      "value": 0.08,
      "error": "delivery: failed (code 131026)"
    }
  ],
  "total": 1,
  "pagination": { "has_more": false, "next_id": null },
  "numbers_masked": true
}
```

SMS items also carry `reply {text, date, count}` when the recipient answered; e-mail items carry `subject`, `from_name` and `provider`. Single lookups by `id` or `message_id` also return the content (`text`, or `body_preview` for e-mail). Every field is described in [GetMessageStatus](../../api/v2/messages/GetMessageStatus.md).

**Error (channel not enabled for the token):**

```json
{
  "success": false,
  "error": "Permission denied for channel 'email' (API 'gmail' is not enabled for this token). Channels enabled: sms, whatsapp.",
  "status_code": 403
}
```

Limits: 200 list requests per hour and 5,000 single lookups per day per account (`status_code` 429). Do not poll messages that already reached a final status.
