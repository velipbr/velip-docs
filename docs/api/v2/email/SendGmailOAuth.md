# Send email (Gmail OAuth)

*Send a transactional email through the customer's Gmail account via OAuth 2.0.*


**Endpoint:** `POST https://<base>/api/v2/SendGmailOAuth.php`

Sends an email using a Gmail account that the customer has connected via OAuth 2.0 (records in `cd_oauth_connections` + `cd_oauth_providers`). The Velip server refreshes the access token automatically and uses Gmail's REST API to deliver the message.

Use this when you want emails to come from your own Gmail/Google Workspace identity (and inherit your own deliverability reputation) instead of Velip's transactional sender.

## Authentication

Token authentication required. See [Authentication](../authentication.md). Additionally, the `from_email` must already be linked to your customer through the Velip portal's Gmail OAuth onboarding flow (records stored in `cd_oauth_connections` + `cd_oauth_providers`).

## Request

#### `tsid` — type: *string* — **required**

Token for the account.


#### `from_email` — type: *string* — **required**

Email address that owns the OAuth grant. Must be authorized for this customer.


#### `to_email` — type: *string* — **required**

Recipient address. Alias `dest` is accepted.


#### `subject` — type: *string* — **required**

Email subject line.


#### `body` — type: *string* — **required**

Email body. HTML and plain text are accepted; the underlying class detects the type.


#### `from_name` — type: *string*

Display name for the sender (e.g., "Acme Sales").


#### `reply_to` — type: *string*

`Reply-To` address (RFC 5322 format).


#### `cc` — type: *string*

Comma-separated list of CC recipients.


#### `bcc` — type: *string*

Comma-separated list of BCC recipients.


#### `origin` — type: *string* — default: `api_v2`

Free-text origin tag stored with the send log.


#### `cpid` — type: *string*

Optional campaign id stored with the send log.


## Request example
```bash curl
curl -X POST 'https://<base>/api/v2/SendGmailOAuth.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "from_email": "sales@acme.com",
    "from_name": "Acme Sales",
    "to_email": "lead@example.com",
    "subject": "Following up on your demo request",
    "body": "<p>Hi Lead, ...</p>",
    "reply_to": "ana@acme.com"
  }'
```
## Response
```json 200 OK
{
  "return": {
    "status": "OK",
    "status_code": "0",
    "message_id": "<CABzXYZ@mail.gmail.com>"
  }
}
```

```json 400 Validation
{
  "return": {
    "status": "Invalid destination email format",
    "status_code": "202",
    "message_id": ""
  }
}
```
- **`return.message_id`** (*string*) — RFC 5322 `Message-ID` of the email sent. Use it to correlate with delivery dashboards.


## Error codes

| Code | `status` | Cause |
| --- | --- | --- |
| `201` | `Parameter 'to_email' or 'dest' (destination email) is required` | Missing recipient. |
| `202` | `Invalid destination email format` | Recipient failed `FILTER_VALIDATE_EMAIL`. |
| `203` | `Parameter 'subject' is required` | Missing `subject`. |
| `204` | `Parameter 'body' is required` | Missing `body`. |
| `205` | `Parameter 'from_email' (authorized OAuth email) is required` | Missing `from_email`. |
| `206` | `Invalid from_email format` | `from_email` failed `FILTER_VALIDATE_EMAIL`. |
| `210` | (provider message) | Gmail OAuth class returned an error (token revoked, scope insufficient, send failed). |

> **Note**
> The OAuth token is refreshed automatically. If the refresh token has been revoked from the Google account, this endpoint returns code `210` with the upstream error message — re-link the account in the Velip portal to recover.
