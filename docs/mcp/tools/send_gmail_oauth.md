# send_gmail_oauth

*Send email via Gmail OAuth 2.0.*

| | |
| --- | --- |
| **Permission** | `gmail` |
| **REST equivalent** | [SendGmailOAuth](../../api/v2/email/SendGmailOAuth.md) |

Sends HTML email through a Gmail account authorized via OAuth in the Velip control panel.

## Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `dest` | string | Yes | Recipient email |
| `subject` | string | Yes | Subject line |
| `body` | string | Yes | HTML body |
| `from_email` | string | No | Sender — auto-detected if one OAuth Gmail exists |
| `from_name` | string | No | Display name |
| `reply_to` | string | No | Reply-To address |
| `cc` | string | No | CC address |
| `bcc` | string | No | BCC address |

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
      "name": "send_gmail_oauth",
      "arguments": {
        "dest": "recipient@example.com",
        "subject": "Velip MCP test",
        "body": "<h1>Hello</h1><p>Sent via MCP.</p>",
        "from_email": "sender@gmail.com"
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
  "message_id": "18e2a4b3c5d6f789",
  "from_email": "sender@gmail.com",
  "message": "E-mail enviado para recipient@example.com"
}
```

**Error (no OAuth):**

```json
{
  "success": false,
  "error": "No active Gmail OAuth connection for 'email@gmail.com'. Authorize this email at the OAuth management panel first.",
  "status_code": 403
}
```
