# Send Facebook Messenger message

*Send a Messenger message via the Meta Graph API using the customer's PAT.*


**Endpoint:** `POST https://<base>/api/v2/MakeMessenger.php`

Sends a Messenger message through the Meta Graph API (`POST /me/messages`) using the page access token (PAT) configured for the WhatsApp/Messenger line (`cd_v8_line` with `v8l_class='messenger'`). Supports text, image, audio, video, and file attachments.

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Request

#### `tsid` — type: *string* — **required**

Token for the account.


#### `app_id` — type: *integer* — **required**

ID of the Messenger line (`cd_v8_line.v8l_id`). Legacy alias `v8l_id` is accepted.


#### `dest` — type: *string* — **required**

Recipient PSID (Page-Scoped User ID) returned by Meta when the user starts the conversation.


#### `mtype` — type: *string* — default: `text`

Message type. One of `text`, `image`, `audio`, `video`, `file` / `document`.


#### `mdata` — type: *string* — **required**

For `text`, the body. For media types, the public URL of the asset.


#### `mcaption` — type: *string*

Caption for `image`, `video`, or `file`. (Note: at the time of writing the Messenger Graph API does not honor captions on attachments — kept for parity with WhatsApp.)


#### `msg_id` — type: *string*

Optional reference to a related call/message id (stored in the log).


## Request example
```bash curl (text)
curl -X POST 'https://<base>/api/v2/MakeMessenger.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "app_id": 1234,
    "dest": "<psid>",
    "mtype": "text",
    "mdata": "Hello from Acme"
  }'
```

```bash curl (image)
curl -X POST 'https://<base>/api/v2/MakeMessenger.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "app_id": 1234,
    "dest": "<psid>",
    "mtype": "image",
    "mdata": "https://cdn.example.com/promo.jpg"
  }'
```
## Response
```json 200 OK
{
  "return": {
    "status": "OK",
    "status_code": 200,
    "messageId": "m_xyz",
    "cdls_id": 9876545
  }
}
```

```json 400 Provider error
{
  "return": {
    "status": "ERROR",
    "status_code": 400,
    "messageId": "",
    "cdls_id": 9876546
  }
}
```
- **`return.status_code`** (*integer*) — When `status_code < 200` (typically `0`–`299`) it is the Velip business code; on success/failure from Meta, the HTTP code from Graph API is echoed back.


- **`return.messageId`** (*string*) — Meta message id (`m_...`). Empty on failure.


- **`return.cdls_id`** (*integer*) — Internal log id in the customer's SMS/messages database.


## Error codes

| Code | `status` | Cause |
| --- | --- | --- |
| `210` | `No app_id` | Missing `app_id`. |
| `220` | `No dest` | Missing destination PSID. |
| `225` | `No mdata` | Missing body / media URL. |
| `230` | `Messenger line not found` | Line missing, inactive, or wrong class (must be `messenger`). |
| `233` | `No page access token` | `v8l_wa_api_key` is empty for the line. |
| `234` | `No page ID` | `v8l_fb_page_id` is empty for the line. |

> **Note**
> Messenger requires the user to have messaged the page within the last 24 hours (the "messaging window"). Sending outside that window returns Graph API code `10` and the call is logged as `ERROR`.
