# List message campaigns

*Bulk SMS, WhatsApp and e-mail campaigns, with optional delivery stats.*


**Endpoint:** `POST https://<base>/api/v2/GetMessageCampaignsList.php`

The message counterpart of [`GetCampaignsList`](../campaigns/GetCampaignsList.md), which covers voice campaigns. One channel per request. Lists the bulk campaigns of the account, newest first, or returns one campaign with its stats. To list the individual messages of a campaign, use [`GetMessageStatus`](GetMessageStatus.md) with `campaign_id`.

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Request

Parameters can be sent as form fields or as a JSON body.

#### `tsid` — type: *string* — **required**

Token for the account.


#### `channel` — type: *string* — **required**

`sms`, `whatsapp` (alias `wa`) or `email`.


#### `campaign_id` — type: *integer*

Returns this campaign only, always with `stats`.


#### `active_only` — type: *boolean*

`1` returns only active campaigns that are not finished.


#### `date_start` — type: *string*

Campaigns **created** on or after this date (`YYYY-MM-DD`).


#### `date_end` — type: *string*

Campaigns **created** up to this date (`YYYY-MM-DD`). The period can have at most **366 days**. Without dates, every campaign of the account is listed.


#### `search` — type: *string*

Part of the campaign name (up to 100 characters).


#### `with_stats` — type: *boolean*

`1` adds `stats` to each campaign, computed from its messages. Computed for the **first 10 campaigns** of the page; the response then carries `return.stats_note`. Query by `campaign_id` for the others.


#### `maxreg` — type: *integer* — default: `50`

Campaigns per page, capped at **200** (`pagination.maxreg_capped: true` with `maxreg_applied` when reduced).


#### `last_id` — type: *integer*

Cursor for the next page. Pass the `pagination.next_id` of the previous response.


## Request example
```bash curl
curl -X POST 'https://<base>/api/v2/GetMessageCampaignsList.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "channel": "sms",
    "active_only": 1,
    "with_stats": 1
  }'
```

## Response
```json 200 OK (SMS)
{
  "return": {
    "status": "OK",
    "status_code": "0",
    "channel": "sms",
    "pagination": { "has_more": false, "next_id": null }
  },
  "campaigns": [
    {
      "campaign_id": 3456,
      "channel": "sms",
      "name": "November promo",
      "state": "running",
      "status_raw": "run",
      "active": true,
      "pause_reason": null,
      "created_at": "2026-11-06 18:02:11",
      "finished_at": null,
      "window": {
        "date_start": "2026-11-07",
        "date_end": "2026-11-10",
        "time_start": "09:00",
        "time_end": "18:00"
      },
      "per_minute": 300,
      "list_id": 4248439,
      "counters": { "queued": 12000, "sent": 8450 },
      "text": "Hi {{NOME}}, ...",
      "ai_agent_id": null,
      "stats": {
        "total": 12000,
        "pending": 3550,
        "sent": 610,
        "delivered": 7720,
        "failed": 120,
        "value": 422.5,
        "replies": 85,
        "replied": 80,
        "conversation_replies": 85
      }
    }
  ]
}
```

### Campaign state

| `state` | Meaning |
| --- | --- |
| `scheduled` | Active, waiting for its window to start sending. |
| `running` | Sending. |
| `paused` | Paused by the user or by the platform; `pause_reason` says why. |
| `finished` | Finished, or cancelled. |

### Fields

- **`campaigns[].pause_reason`** (*string*) — Filled only while the campaign is paused (and, for e-mail, when it was stopped before the end).
- **`campaigns[].window`** — Dates and hours in which the campaign sends. E-mail also has `week_days`.
- **`campaigns[].list_id`** — Destination list of the campaign (see [`GetDestinationsList`](../destinations/GetDestinationsList.md)).
- **`campaigns[].counters`** — Counters kept by the campaign: `queued` and `sent`; e-mail also has `failed` and `optout`.
- **SMS** campaigns carry `text` (first 500 characters), `per_minute` and `ai_agent_id` (the AI agent that answers the replies, or `null`).
- **WhatsApp** campaigns carry `per_minute`, `line_id`, `from` (sending number), `line_name`, `template_id` and `template_name`.
- **E-mail** campaigns carry `from`, `from_name`, `subject` and `limits` (`per_minute`, `per_hour`, `per_day`).

### Stats

`stats` counts the messages of the campaign by [normalized status](GetMessageStatus.md#status). The buckets are mutually exclusive and add up to `total`:

| Channel | Buckets |
| --- | --- |
| SMS | `pending`, `sent` (accepted, no delivery confirmation), `delivered`, `failed` |
| WhatsApp | `pending`, `sent`, `delivered` (not read yet), `read`, `failed` |
| E-mail | `pending`, `sent`, `failed`, `skipped` (address already unsubscribed) |

Besides the buckets:

- **`value`** (*number*) — Price charged for the messages sent. `null` when the user of the token has no permission to see values (`return.value_hidden: true`).
- **SMS:** `replies` (answers to the campaign messages), `replied` (campaign messages with at least one answer) and `conversation_replies` (every message received in the conversations the campaign started, including answers to an AI agent).
- **E-mail:** `optout` — recipients who unsubscribed through the link after receiving the e-mail. Not one of the buckets.

### Rate limit

**200 requests per account per hour.** Above it: **HTTP 429**, `status_code: 429` and a `Retry-After` header (seconds).

## Error codes

| Code | HTTP | `status` | Cause |
| --- | --- | --- | --- |
| `460` | 400 | `Invalid channel: use sms, whatsapp or email` | Missing or unknown `channel`. |
| `461` | 400 | `Invalid date: use YYYY-MM-DD in date_start and date_end` | Date format. |
| `462` | 400 | `Period too long: max 366 days per request (got N). ...` | Period longer than 366 days. |
| `463` | 400 | `date_end must be on or after date_start` | Dates inverted. |
| `465` | 400 | `campaign_id and last_id must be numeric` | Not numeric. |
| `429` | 429 | `Rate limit exceeded: max 200 requests per hour` | See [Rate limit](#rate-limit). |
| `500` | 500 | `internal error` | Temporary failure on the Velip side. Repeat later. |

It also returns the [global authentication codes](../errors.md) (HTTP 401). Filters that match nothing return an empty `campaigns` list.
