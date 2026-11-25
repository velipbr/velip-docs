# get_message_campaigns

*Bulk SMS, WhatsApp and e-mail campaigns, with optional delivery stats.*

| | |
| --- | --- |
| **Permission** | the channel asked: `sms`, `whatsapp` or `gmail` (for `email`) |
| **REST equivalent** | [GetMessageCampaignsList](../../api/v2/messages/GetMessageCampaignsList.md) |

The message counterpart of [get_campaigns_list](get_campaigns_list.md), which covers voice campaigns. One channel per call. Lists the bulk campaigns of the account, newest first (default 50 per page, maximum 200), or returns one campaign with its stats. To list the messages of a campaign, use [get_message_status](get_message_status.md) with `campaign_id`.

The tool is listed when the token has any of the three channels; each call checks the channel asked.

`state` is `scheduled`, `running`, `paused` or `finished`; `pause_reason` is filled only while the campaign is paused.

## Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `channel` | string | Yes | `sms`, `whatsapp` or `email` |
| `campaign_id` | string | No | One campaign, always with stats |
| `active_only` | boolean | No | Only active campaigns that are not finished |
| `date_start` | string | No | Campaigns created from this date (`YYYY-MM-DD`). Maximum period 366 days |
| `date_end` | string | No | Campaigns created until this date (`YYYY-MM-DD`) |
| `search` | string | No | Part of the campaign name |
| `max_records` | integer | No | Campaigns per page. Default 50, maximum 200 |
| `last_id` | string | No | Pagination cursor: `pagination.next_id` of the previous response |
| `with_stats` | boolean | No | Adds stats per campaign (first 10 campaigns of the page) |

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
      "name": "get_message_campaigns",
      "arguments": {
        "channel": "sms",
        "active_only": true,
        "with_stats": true
      }
    }
  }'
```

## Responses

**Success:**

```json
{
  "success": true,
  "channel": "sms",
  "campaigns": [
    {
      "campaign_id": 3456,
      "name": "November promo",
      "state": "running",
      "active": true,
      "pause_reason": null,
      "created_at": "2026-11-06 18:02:11",
      "window": { "date_start": "2026-11-07", "date_end": "2026-11-10", "time_start": "09:00", "time_end": "18:00" },
      "list_id": 4248439,
      "counters": { "queued": 12000, "sent": 8450 },
      "text": "Hi {{NOME}}, ...",
      "stats": {
        "total": 12000, "pending": 3550, "sent": 610, "delivered": 7720, "failed": 120,
        "value": 422.5, "replies": 85, "replied": 80, "conversation_replies": 85
      }
    }
  ],
  "total": 1,
  "pagination": { "has_more": false, "next_id": null }
}
```

The `stats` buckets (`pending`, `sent`, `delivered`, `read` on WhatsApp, `failed`; e-mail: `pending`, `sent`, `failed`, `skipped`) are mutually exclusive and add up to `total`. SMS stats also carry `replies`, `replied` and `conversation_replies`; e-mail stats carry `optout`. Every field is described in [GetMessageCampaignsList](../../api/v2/messages/GetMessageCampaignsList.md).

Limit: 200 calls per hour per account (`status_code` 429).
