# send_whatsapp

*Send a WhatsApp message via Meta Cloud API.*

| | |
| --- | --- |
| **Permission** | `whatsapp` |
| **REST equivalent** | [MakeWhatsapp](../../api/v2/whatsapp/MakeWhatsapp.md) |

Supports `text`, `template`, `image`, `audio`, `video`, and `document` message types.

> **Important:** The first message to a contact outside the 24-hour window **must** use `mtype=template` with a valid template JSON. Free-form messages are only allowed within the 24h reply window.

## Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `dest` | string | Yes | Destination with country code. Example: `5511999999999` |
| `mtype` | string | Yes | `text`, `template`, `image`, `audio`, `video`, `document` |
| `mdata` | string | Yes | Text content or media URL |
| `from_number` | string | No | Sender line — auto-detected if only one line exists |
| `template` | string | Conditional | Template JSON when `mtype=template` |
| `mcaption` | string | No | Caption for media messages |
| `ctid` | string | No | External idempotency key |

Use [get_wa_lines](get_wa_lines.md) and [get_wa_templates](get_wa_templates.md) before sending templates.

## Example — text message

```bash
curl -X POST 'https://vox20.velip.com.br/mcpserver/velip' \
  -H 'Authorization: Bearer YOUR_TOKEN_30_CHARS' \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "send_whatsapp",
      "arguments": {
        "dest": "5511999999999",
        "mtype": "text",
        "mdata": "Hello from Velip MCP"
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
  "cdls_id": "789",
  "wa_message_id": "wamid.xxx",
  "from_number": "5511888888888",
  "message": "WhatsApp message sent"
}
```
