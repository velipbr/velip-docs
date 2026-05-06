# Send Instagram Direct message

*Send an Instagram Direct message via the Meta Graph API using the customer's PAT.*


**Endpoint:** `POST https://<base>/api/v2/MakeInstagram.php`

Sends an Instagram Direct message through the Meta Graph API (`POST /me/messages`) using the page access token (PAT) bound to the Instagram-class line (`cd_v8_line` with `v8l_class='instagram'`). Supports text, image, audio, and video.

The endpoint shares the underlying call with [`MakeMessenger`](../messenger/MakeMessenger.md), but resolves to the Instagram business account (`v8l_ig_account_id`) and applies the Instagram-specific 24-hour messaging window.

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Request

#### `tsid` — type: *string* — **required**

Token for the account.


#### `app_id` — type: *integer* — **required**

ID of the Instagram line (`cd_v8_line.v8l_id`). Legacy alias `v8l_id` is accepted.


#### `dest` — type: *string* — **required**

Recipient IGSID (Instagram-Scoped User ID) returned by Meta when the user starts the conversation.


#### `mtype` — type: *string* — default: `text`

Message type. One of `text`, `image`, `audio`, `video`.


#### `mdata` — type: *string* — **required**

For `text`, the body. For media types, the public URL of the asset.


#### `msg_id` — type: *string*

Optional reference id stored in the log.


## Request example
```bash curl
curl -X POST 'https://<base>/api/v2/MakeInstagram.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "app_id": 1234,
    "dest": "<igsid>",
    "mtype": "text",
    "mdata": "Thanks for reaching out — how can we help?"
  }'
```
## Response
```json 200 OK
{
  "return": {
    "status": "OK",
    "status_code": 200,
    "messageId": "m_xyz",
    "cdls_id": 9876547
  }
}
```
## Error codes

| Code | `status` | Cause |
| --- | --- | --- |
| `210` | `No app_id` | Missing `app_id`. |
| `220` | `No dest` | Missing IGSID. |
| `225` | `No mdata` | Missing body / media URL. |
| `230` | `Instagram line not found` | Line missing, inactive, or `v8l_class` is not `instagram`. |
| `233` | `No page access token` | `v8l_wa_api_key` empty for the line. |

> **Note**
> Instagram enforces a 24-hour messaging window (Meta error codes `10` / `551`). Outside the window, only message tags or human-agent labels are allowed; this endpoint sends `messaging_type: RESPONSE` only and will fail outside the window.
