# send_email

*Send email from a Gmail or Microsoft 365 / Outlook mailbox, with free content or a template, and attachments.*

| | |
| --- | --- |
| **Permission** | `gmail` |
| **REST equivalent** | [SendEmailOAuth](../../api/v2/email/SendEmailOAuth.md) |

Sends an email through a mailbox connected to Velip with OAuth (Integrations > OAuth authorizations), on Gmail / Google Workspace or Microsoft 365 / Outlook. Replaces [send_gmail_oauth](send_gmail_oauth.md), which only covers Gmail.

The content is either given directly (`subject` + HTML `body`) or taken from a template (`template_id` from [list_email_templates](list_email_templates.md), plus `variables`). With a template, `subject` optionally replaces the template subject and `body` is not accepted.

If the account has only one sender available to the user (both providers together), `from_email` can be omitted. Only *Shared* connections and the user's own *Individual* connections can be used.

## Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `dest` | string | Yes | Recipient email |
| `subject` | string | No | Subject. Required without `template_id` |
| `body` | string | No | HTML body. Required without `template_id`; not accepted with it |
| `template_id` | integer | No | Template id from [list_email_templates](list_email_templates.md) |
| `variables` | string | No | JSON object as a string with the template variables, e.g. `{"NOME":"Maria","EXTRA1":"Order 123"}`. `EMAIL` and `UNSUB_LINK` are filled by Velip and are not part of it |
| `from_email` | string | No | Sender with an active OAuth connection. Auto-detected when there is only one |
| `provider` | string | No | `gmail` or `microsoft`, only when the same `from_email` is connected on both |
| `from_name` | string | No | Display name (ignored on Microsoft) |
| `reply_to` | string | No | Reply-To address |
| `cc` | string | No | CC addresses. Up to 10 addresses in `cc` + `bcc` together |
| `bcc` | string | No | BCC addresses. Counts toward the same limit |
| `attachments` | string | No | JSON array as a string, up to 5 files and 2 MB in total. Each item is `{"filename", "content_base64"}` or `{"url", "filename"?}` with a public `https` URL; `mime_type` optional |

Attachments refused: executables (even renamed), the file types Gmail blocks, macro-enabled Office files (`.docm`, `.xlsm`, `.pptm`), password-protected ZIP files and ZIP files with a blocked type inside.

In single sends `UNSUB_LINK` points to a demonstration page; the per-recipient unsubscribe link exists only in bulk email campaigns.

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
      "name": "send_email",
      "arguments": {
        "dest": "lead@example.com",
        "template_id": 42,
        "variables": "{\"NOME\":\"Maria\"}"
      }
    }
  }'
```

## Responses

**Success:**

```json
{
  "success": true,
  "status": "OK",
  "message_id": "<CABzXYZ@mail.gmail.com>",
  "from_email": "sales@acme.com",
  "provider": "gmail",
  "message": "E-mail enviado para lead@example.com",
  "id": 55123,
  "template_id": 42
}
```

`id` is the Velip id of the send: call [get_message_status](get_message_status.md) with `channel="email"` and this `id` to check it later. `attachments` (the number of files) is returned when there were attachments.

**Error (template variable missing):**

```json
{
  "success": false,
  "status": "Missing values for template variables: NOME",
  "status_code": 212,
  "http_status": 400,
  "error": "Missing values for template variables: NOME - Call list_email_templates to see which variables this template requires, then resend with ALL values in 'variables'. EMAIL and UNSUB_LINK are automatic - never include them."
}
```

The `status_code` values are those of [SendEmailOAuth](../../api/v2/email/SendEmailOAuth.md#error-codes). When the sender cannot be found (no connection, or several and no `from_email`), the tool answers `status_code` 403 with the senders available.

> **Note**
> If the platform does not confirm the send (timeout or gateway error), the email may have been sent anyway: the error says so. Do not resend automatically; check with the user first.
