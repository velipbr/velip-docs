# get_wa_templates

*List approved WhatsApp message templates for a line.*

| | |
| --- | --- |
| **Permission** | `whatsapp` |
| **REST equivalent** | [GetWATemplates](../../api/v2/whatsapp/GetWATemplates.md) |

Templates are required for initiating conversations outside the 24-hour Meta window.

## Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `from_number` | string | No | WhatsApp line number — auto-detected if account has one line |

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
      "name": "get_wa_templates",
      "arguments": { "from_number": "5511888888888" }
    }
  }'
```

## Responses

**Success:**

```json
{
  "success": true,
  "templates": [
    {
      "id": "1",
      "name": "hello_world",
      "category": "MARKETING",
      "language": "pt_BR",
      "status": "APPROVED",
      "body_text": "Olá {{1}}, bem-vindo!"
    }
  ],
  "total": 1,
  "from_number": "5511888888888"
}
```

Use template data in [send_whatsapp](send_whatsapp.md) with `mtype=template`.
