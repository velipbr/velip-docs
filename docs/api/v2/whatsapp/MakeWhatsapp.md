# Send WhatsApp message

*Send a WhatsApp message (text, media, or HSM/template) via Gupshup or Meta Cloud API.*


**Endpoint:** `POST https://<base>/api/v2/MakeWhatsapp.php`

Sends a single WhatsApp message to one destination through the provider configured on the customer's WhatsApp line (`v8l_id`). Supports plain text, media (image, audio, video, file, sticker), and HSM/template messages.

Templates must be pre-approved on the provider side. Use [`CreateWhatsappTemplate`](CreateWhatsappTemplate.md) to register one and [`CheckTemplateStatus`](CheckTemplateStatus.md) to query approval state.

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Request

#### `tsid` — type: *string* — **required**

Token for the account.


#### `dest` — type: *string* — **required**

Destination phone number, in international format (e.g., `5511999999999`). Minimum 6 digits.


#### `app_id` — type: *integer* — **required**

ID of the WhatsApp line on your account (`cd_v8_line.v8l_id`). The legacy `v8l_id` parameter is also accepted.


#### `ctid` — type: *string*

Customer-side correlation id, persisted alongside the message.


#### `mtype` — type: *string* — default: `text`

Message type. One of `text`, `audio`, `image`, `video`, `file`, `sticker`, `wabody`, `wa_template`, `template`.


#### `mdata` — type: *string*

Content for the message. For `text` it is the body. For media types it is the URL of the asset. For templates it is unused — pass the structure in `template`.


#### `mcaption` — type: *string*

Caption for `image`, `video`, or `file` messages. For `file`, used as the filename.


#### `misHSM` — type: *string*

Set to `true` when sending a session-opening template (HSM). Automatically inferred when `mtype` is `wa_template` / `template`.


#### `template` — type: *object*

Full template payload (Meta Cloud API shape). Required when `mtype=wa_template` or `template`. Example:

  ```json
  {
    "name": "shipment_update",
    "language": { "code": "pt_BR" },
    "components": [
      {
        "type": "body",
        "parameters": [
          { "type": "text", "text": "John" },
          { "type": "text", "text": "ABC-123" }
        ]
      }
    ]
  }
  ```


#### `msg_id` — type: *string*

Optional reference to a related voice call (`cd_id`) for analytics.


#### `httpdup` — type: *integer* — default: `10`

Duplicate-suppression window in seconds (1–600). Returns `250` when triggered. `0` disables.


## Provider behaviour

The WhatsApp line configured for the customer (`v8l_wa_provider`) determines the upstream API used:

- **`gupshup`** — calls Gupshup `https://api.gupshup.io/sm/api/v1/msg`. The session window is computed from the last message exchanged with the user; templates are required when outside the 24-hour window.
- **`meta`** (Meta Cloud API) — calls `https://graph.facebook.com/.../messages` directly. Returns the upstream `messages[0].id` as the message id.

The provider response is parsed and the message id is stored in `cdls_return_id`; the readable status is stored in `cdls_status_delivery`.

## Pricing tiers

WhatsApp messages are billed at two tiers configured on the customer (`cd_customer_com`):

- `cdcc_wa_price_1` — non-HSM (within an open user-initiated session).
- `cdcc_wa_price_2` — HSM/templates (or session opens).

The API charges `price_2` whenever `misHSM=true`; otherwise `price_1`.

## Request example
```bash curl (text)
curl -X POST 'https://<base>/api/v2/MakeWhatsapp.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "dest": "5511999999999",
    "app_id": 1234,
    "mtype": "text",
    "mdata": "Hello from Velip",
    "ctid": "order-abc-123"
  }'
```

```bash curl (image)
curl -X POST 'https://<base>/api/v2/MakeWhatsapp.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "dest": "5511999999999",
    "app_id": 1234,
    "mtype": "image",
    "mdata": "https://cdn.example.com/promo.jpg",
    "mcaption": "Check out our latest promo"
  }'
```

```bash curl (template)
curl -X POST 'https://<base>/api/v2/MakeWhatsapp.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "dest": "5511999999999",
    "app_id": 1234,
    "mtype": "wa_template",
    "template": {
      "name": "shipment_update",
      "language": { "code": "pt_BR" },
      "components": [
        {
          "type": "body",
          "parameters": [
            { "type": "text", "text": "John" },
            { "type": "text", "text": "ABC-123" }
          ]
        }
      ]
    }
  }'
```
## Response
```json 200 OK
{
  "return": {
    "status": "OK",
    "status_code": "0",
    "cdls_id": "9876543"
  }
}
```

```json 400 Provider error
{
  "return": {
    "status": "Recipient phone number not in allowed list",
    "status_code": "131000",
    "cdls_id": "9876544"
  }
}
```
- **`return.status`** (*string*) — `OK` on success; otherwise the upstream provider's error message or a Velip code message.


- **`return.status_code`** (*string*) — `0` on success. On failure, either a Velip code (see below) or the provider's numeric error code (e.g., Meta `131000`).


- **`return.cdls_id`** (*string*) — Internal log id (`cd_log_sms_*.cdls_id`). Inspect `cdls_return_log` for the full provider response.


## Error codes

In addition to the [global authentication codes](../errors.md):

| Code | `status` | Cause |
| --- | --- | --- |
| `220` | `No sms account` | Customer is not provisioned for messaging. |
| `230` | `No dest` | `dest` missing or shorter than 6 digits. |
| `231` | `No wa provider` | `v8l_wa_provider` is empty for this line. |
| `232` | `No app name` | `v8l_wa_app_name` is empty for this line. |
| `233` | `No key wa` | `v8l_wa_api_key` is empty for this line. |
| `235` | `No from wa number` | `v8l_wa_number` is empty. |
| `236` | `No app_id` | `app_id` / `v8l_id` missing. |
| `250` | `http duplicidade` | Duplicate within the `httpdup` window. |
| `260` | `WA not submitted <HTTP>` | Upstream returned non-2xx HTTP code. |
| `261+` | Provider's error code | Pass-through from Meta/Gupshup error responses (e.g., `131000`). |

## Notes

- Templates must be approved on the provider side **before** you can use them. The Velip API only acts as a forwarder.
- The `mdata` URL for media must be publicly reachable by the provider's servers (Meta or Gupshup); private storage URLs need a public CDN front.
- For audio/video files, prefer `.mp3`, `.ogg`, `.mp4`, `.webm`. Limits depend on the WhatsApp Cloud API (currently 16 MB for video/audio, 100 MB for documents).
