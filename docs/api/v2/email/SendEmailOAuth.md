# Send email (Gmail or Microsoft 365)

*Send an email through the customer's own Gmail or Microsoft 365 / Outlook mailbox, with free content or a template, and attachments.*


**Endpoint:** `POST https://<base>/api/v2/SendEmailOAuth.php`

Sends an email from a mailbox the customer has connected to Velip with OAuth (Integrations > OAuth authorizations), on Gmail / Google Workspace or Microsoft 365 / Outlook. Velip finds the connection by the sender address, renews the access token and sends through the provider's API, so the email comes from your own identity and reputation.

The content is either given directly (`subject` + `body`) or taken from an email template of the account (`template_id` + `vars`).

[`SendGmailOAuth`](SendGmailOAuth.md) is the older, Gmail-only version; new integrations should use this endpoint.

## Authentication

Token authentication required. See [Authentication](../authentication.md).

The `from_email` must have an active OAuth connection in the account, usable by the user who owns the token: a *Shared* connection can be used by any user of the account, an *Individual* connection only by the user who authorized it (while that user is active). An *Individual* connection of another user is treated as not found (code `207`).

## Request

Parameters can be sent as form fields or as a JSON body.

#### `tsid` — type: *string* — **required**

Token for the account.


#### `from_email` — type: *string* — **required**

Sender address, with an active OAuth connection (see above).


#### `to_email` — type: *string* — **required**

Recipient address. Alias `dest`.


#### `subject` — type: *string*

Subject. Required without `template_id`; with `template_id` it is optional and replaces the template subject.


#### `body` — type: *string*

HTML body, sent as is. Required without `template_id`; not accepted together with `template_id` (code `211`).


#### `template_id` — type: *integer*

Id of an email template of the account. Subject and body come from the template, and its `{{VAR}}` variables are filled with `vars`. The template's CC, BCC and Reply-To are used when you do not send your own.


#### `vars` — type: *string*

**A string** with a JSON object of the template variables, for example `{"NOME":"Maria","EXTRA1":"Order 123"}`. In a JSON body, send it as a string too: `"vars": "{\"NOME\":\"Maria\"}"`. Every variable the template uses must have a value (code `212`), except two filled by Velip:

- `EMAIL` — the recipient address.
- `UNSUB_LINK` — in single sends it points to a demonstration page; the per-recipient unsubscribe link exists only in bulk email campaigns.


#### `provider` — type: *string*

`gmail` or `microsoft`. Needed only when the same `from_email` is connected on both providers.


#### `from_name` — type: *string*

Display name of the sender. Ignored on Microsoft (the mailbox display name is used).


#### `reply_to` — type: *string*

`Reply-To` address.


#### `cc` — type: *string*

CC addresses, separated by `,` or `;`. `cc` and `bcc` together accept at most **10** addresses, counting those inherited from the template (code `214`).


#### `bcc` — type: *string*

BCC addresses. Counts toward the same 10-address limit.


#### `attachments` — type: *array*

Up to **5** files, **2 MB** in total (decoded). A JSON array, or a string with the JSON array. Each item is either:

- `{"filename": "invoice.pdf", "content_base64": "..."}` — the content in base64 (practical for small generated files); or
- `{"url": "https://...", "filename": "optional.pdf"}` — a public `https` URL that Velip downloads (20 seconds in total for all URLs).

`mime_type` is optional on each item. Refused (code `213`): executables (even renamed), the file types Gmail blocks (`.exe`, `.bat`, `.js`, `.msi`, `.iso`…), macro-enabled Office files (`.docm`, `.xlsm`, `.pptm`), password-protected ZIP files and ZIP files that contain a blocked type, and URLs that are not public `https`.


#### `origin` — type: *string* — default: `api_v2`

Free tag stored with the send (`template` by default when `template_id` is used).


#### `cpid` — type: *string*

Your campaign id, stored with the send.


## Request example
```bash curl
curl -X POST 'https://<base>/api/v2/SendEmailOAuth.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "from_email": "sales@acme.com",
    "to_email": "lead@example.com",
    "template_id": 42,
    "vars": "{\"NOME\":\"Maria\",\"EXTRA1\":\"Order 123\"}",
    "attachments": [
      { "url": "https://files.acme.com/invoices/123.pdf" }
    ]
  }'
```

## Response
```json 200 OK
{
  "return": {
    "status": "OK",
    "status_code": "0",
    "message_id": "<CABzXYZ@mail.gmail.com>",
    "provider": "gmail",
    "id": 55123
  }
}
```

```json 400 Validation
{
  "return": {
    "status": "Missing values for template variables: NOME",
    "status_code": "212",
    "message_id": "",
    "provider": "gmail"
  }
}
```
- **`return.message_id`** (*string*) — Id of the email at the provider (Gmail id or `Message-ID`).
- **`return.provider`** (*string*) — `gmail` or `microsoft`: the mailbox used.
- **`return.id`** (*integer*) — Velip id of the send. Pass it to [`GetMessageStatus`](../messages/GetMessageStatus.md) with `channel=email` to check it later.


## Error codes

| Code | `status` | Cause |
| --- | --- | --- |
| `201` | `Parameter 'to_email' or 'dest' (destination email) is required` | Missing recipient. |
| `202` | `Invalid destination email format` | Invalid recipient. |
| `203` | `Parameter 'subject' is required (unless template_id is used)` | Missing `subject`. |
| `204` | `Parameter 'body' is required (unless template_id is used)` | Missing `body`. |
| `205` | `Parameter 'from_email' (authorized OAuth email) is required` | Missing `from_email`. |
| `206` | `Invalid from_email format` | Invalid `from_email`. |
| `207` | `No active e-mail OAuth connection found for this account. ...` | No active connection for `from_email` (and `provider`) usable by this token's user. |
| `208` | `Parameter 'provider' must be one of: gmail, microsoft` | Invalid `provider`. |
| `209` | `Email template #N not found for this account. ...` | `template_id` does not exist in the account. |
| `210` | (provider message) | The provider refused the send (token revoked, missing permission, send error), or the template has no subject. |
| `211` | `Use 'body' OR 'template_id', not both` | Both sent. |
| `212` | `Missing values for template variables: ...` / `Parameter 'vars' must be a JSON object, ...` | A variable of the template has no value, or `vars` is not a JSON object. |
| `213` | (reason) | Invalid attachment: format, size, number of files, blocked type or refused URL. Nothing is sent. |
| `214` | `Too many cc/bcc recipients (max 10)` | `cc` + `bcc` have more than 10 addresses. Nothing is sent. |
| `215` | `Mailbox sending quota exceeded` | The mailbox's rolling sending quota (per minute / hour / day) does not cover `1 + cc + bcc` recipients now. Nothing is sent; retry later. |

Errors use HTTP 400; authentication errors use HTTP 401 with the [global codes](../errors.md).

> **Note**
> Each successful send uses `1 + cc + bcc` units of the mailbox's rolling sending quota, the same quota used by bulk email campaigns. A send refused by the provider does not use quota.

> **Note**
> If the user revokes Velip's access in the Google or Microsoft account, sends return code `210` with the provider's message. Authorize the mailbox again in the Velip portal.
