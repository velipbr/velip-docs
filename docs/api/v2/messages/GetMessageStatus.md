# Get message status / list messages

*Status of SMS, WhatsApp and e-mail sends: one message, or a paginated list.*


**Endpoint:** `POST https://<base>/api/v2/GetMessageStatus.php`

The message counterpart of [`GetCallStatus`](../voice/GetCallStatus.md). One channel per request. Returns a single message when you pass `id`, `message_id`, or the `ctid` of one send, or a paginated list (newest first) filtered by period, campaign, recipient and status.

The status is normalized across channels, so the same code works for SMS, WhatsApp and e-mail.

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Request

Parameters can be sent as form fields or as a JSON body.

#### `tsid` — type: *string* — **required**

Token for the account.


#### `channel` — type: *string* — **required**

`sms`, `whatsapp` (alias `wa`) or `email`.


#### `id` — type: *integer*

Velip id of the message, for a single lookup: the `cdls_id` returned by [`MakeSMS`](../sms/MakeSMS.md) and [`MakeWhatsapp`](../whatsapp/MakeWhatsapp.md), or the `return.id` returned by [`SendEmailOAuth`](../email/SendEmailOAuth.md). Dates are ignored.


#### `message_id` — type: *string*

Provider id of the message, for a single lookup: the WhatsApp `wamid`, the SMS operator id, or the e-mail `Message-ID`. Dates are ignored.


#### `ctid` — type: *string*

Your own id, sent with the message. Searched in the last **31 days** unless you send `date_start` / `date_end`. A `ctid` that matches a single message is a single lookup; a `ctid` shared by several messages is a list request (rate limit and masking rules of lists apply).


#### `campaign_id` — type: *integer*

Bulk campaign id (from [`GetMessageCampaignsList`](GetMessageCampaignsList.md)). Without dates, lists the whole campaign.


#### `dest` — type: *string*

Recipient: phone number with country and area code (`5511999999999`) for SMS and WhatsApp, or the e-mail address for `email`. A Brazilian number without the country code is also searched with `55`.


#### `status` — type: *string*

Normalized status to filter by. SMS and WhatsApp: `pending`, `sent`, `delivered`, `read`, `failed`. E-mail: `pending`, `sent`, `failed`, `skipped`. On WhatsApp, `delivered` also returns the messages already read (their `status` is `read`).


#### `date_start` — type: *string*

Start date (`YYYY-MM-DD`). Default: 6 days before `date_end` (7 days in all).


#### `date_end` — type: *string*

End date (`YYYY-MM-DD`). Default: today. The period can have at most **31 days**.


#### `maxreg` — type: *integer* — default: `100`

Messages per page, capped at **1000**. A larger value is reduced to 1000 and the response carries `pagination.maxreg_capped: true` with `maxreg_applied`.


#### `last_id` — type: *integer*

Cursor for the next page. Pass the `pagination.next_id` of the previous response.


## Request example
```bash curl
curl -X POST 'https://<base>/api/v2/GetMessageStatus.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "channel": "whatsapp",
    "date_start": "2026-11-01",
    "date_end": "2026-11-07",
    "status": "failed",
    "maxreg": 50
  }'
```

## Response
```json 200 OK (WhatsApp list)
{
  "return": {
    "status": "OK",
    "status_code": "0",
    "channel": "whatsapp",
    "period": { "date_start": "2026-11-01", "date_end": "2026-11-07" },
    "pagination": { "has_more": true, "next_id": 9876501 },
    "numbers_masked": true
  },
  "messages": [
    {
      "id": 9876545,
      "channel": "whatsapp",
      "status": "failed",
      "status_raw": "OK",
      "delivery_status": "failed",
      "delivery_code": 131026,
      "delivery_date": "2026-11-07 10:00:09",
      "date": "2026-11-07",
      "time": "10:00:05",
      "dest": "xxxxx999",
      "from": "5511888888888",
      "line_id": 12,
      "campaign_id": 3456,
      "campaign_name": "November promo",
      "voice_campaign_id": null,
      "ctid": "order-abc-123",
      "message_id": "wamid.HBgN...",
      "origin": "bulk",
      "value": 0.08,
      "error": "delivery: failed (code 131026)"
    }
  ]
}
```

```json 200 OK (e-mail lookup by id)
{
  "return": {
    "status": "OK",
    "status_code": "0",
    "channel": "email",
    "pagination": { "has_more": false, "next_id": null }
  },
  "messages": [
    {
      "id": 55123,
      "channel": "email",
      "status": "sent",
      "status_raw": "sent",
      "date": "2026-11-07",
      "time": "14:21:30",
      "sent_at": "2026-11-07 14:21:31",
      "dest": "lead@example.com",
      "from": "sales@acme.com",
      "from_name": "Acme Sales",
      "subject": "Your order",
      "provider": "gmail",
      "campaign_id": null,
      "ctid": null,
      "message_id": "<CABzXYZ@mail.gmail.com>",
      "origin": "api_v2",
      "value": 0.01,
      "error": null,
      "dest_name": "Lead",
      "body_preview": "Hi Lead, your order ..."
    }
  ]
}
```

### Status

| `status` | Meaning |
| --- | --- |
| `pending` | Queued, not handed to the operator, Meta or mail provider yet. |
| `sent` | Accepted by the operator, Meta or mail provider; no delivery confirmation (yet). |
| `delivered` | Delivery confirmed (SMS and WhatsApp). |
| `read` | Read by the recipient (WhatsApp only). |
| `failed` | Not sent or not delivered; `error` carries the reason. |
| `skipped` | E-mail not sent because the address had unsubscribed. |

E-mail has no delivery or read tracking: a delivered e-mail stays `sent`.

### Fields

- **`messages[].id`** (*integer*) — Velip id of the message. Also the pagination key.
- **`messages[].status_raw`** (*string*) — Status as recorded by the platform, before normalization.
- **`messages[].delivery_status`**, **`delivery_code`**, **`delivery_date`** — SMS and WhatsApp: the delivery report from the operator or Meta, when there is one.
- **`messages[].from`** — WhatsApp: the sending number (`line_id` is the line). E-mail: the sender address. `null` for SMS.
- **`messages[].campaign_id`**, **`campaign_name`** — Bulk campaign of the message, or `null`. `voice_campaign_id` is set when the message was sent by a voice campaign.
- **`messages[].origin`** — `api`, `bulk` (bulk campaign) or another source (for example an AI agent).
- **`messages[].value`** (*number*) — Price charged. `null` when the user of the token has no permission to see values; the response then carries `return.value_hidden: true`.
- **`messages[].error`** (*string*) — Reason of a `failed` (or `skipped`) message, from the provider.
- **`messages[].reply`** (*object*) — SMS only: `{ "text", "date", "count" }` of the answers received to this message, or `null`. `text` and `date` are those of the last answer.
- **Single lookups** (`id` or `message_id`) also return the content: `text` for SMS and WhatsApp (for a template, `template <name>: <variables>`), and `dest_name` and `body_preview` (first 1,000 characters, without HTML) for e-mail.

### Masked numbers

For tokens without the option **Full numbers in list responses** (Integrations > API tokens), lists **and lookups by `id`** return `dest` masked (`xxxxx999` for phones, `le***@example.com` for e-mails), mask sequences of 8 or more digits in `error`, `reply.text` and `text`, omit `dest_name`, and carry `return.numbers_masked: true`. Message ids are sequential, so a lookup by `id` is masked like a list. A lookup by `message_id`, or by a `ctid` that matches a single message, returns the full data: these are keys you kept from your own send. Requests authenticated with user and password are not masked.

### Rate limit

- **List requests** (by period, campaign, recipient or status, or a `ctid` shared by several messages): **200 per account per hour**.
- **Single lookups** (`id`, `message_id`, or a `ctid` of one message): **5,000 per account per day**, reset at midnight.

Above either limit the endpoint answers **HTTP 429** with `status_code: 429` and a `Retry-After` header (seconds). Requests refused by validation do not count. Do not poll messages that reached a final status; list by campaign or period and page with `last_id`.

## Error codes

| Code | HTTP | `status` | Cause |
| --- | --- | --- | --- |
| `460` | 400 | `Invalid channel: use sms, whatsapp or email` | Missing or unknown `channel`. |
| `461` | 400 | `Invalid date: use YYYY-MM-DD in date_start and date_end` | Date format. |
| `462` | 400 | `Period too long: max 31 days per request (got N). Split the period into smaller windows` | Period longer than 31 days. |
| `463` | 400 | `date_end must be on or after date_start` | Dates inverted. |
| `464` | 400 | `Invalid status: ...` | `status` not valid for the channel. |
| `465` | 400 | `id must be the numeric Velip message id` (and similar) | `id`, `campaign_id` or `last_id` not numeric; `message_id` or `ctid` too long. |
| `466` | 400 | `Invalid dest: ...` | `dest` is not a phone number (SMS, WhatsApp) or an e-mail address (`email`). |
| `429` | 429 | `Rate limit exceeded: ...` / `Daily limit of 5000 message status lookups reached. ...` | See [Rate limit](#rate-limit). |
| `500` | 500 | `internal error` | Temporary failure on the Velip side. Repeat later. |

It also returns the [global authentication codes](../errors.md) (HTTP 401). Filters that match nothing return an empty `messages` list.
