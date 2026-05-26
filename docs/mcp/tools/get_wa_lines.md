# get_wa_lines

*List active WhatsApp lines for the account.*

| | |
| --- | --- |
| **Permission** | `whatsapp` |
| **REST equivalent** | *(internal DB query — no standalone REST endpoint)* |

Returns WhatsApp sender numbers configured for your account. Use the `number` field as `from_number` in [send_whatsapp](send_whatsapp.md) and [get_wa_templates](get_wa_templates.md).

## Parameters

None.

## Example

```bash
curl -X POST 'https://vox20.velip.com.br/mcpserver/velip' \
  -H 'Authorization: Bearer YOUR_TOKEN_30_CHARS' \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_wa_lines","arguments":{}}}'
```

## Responses

**Success:**

```json
{
  "success": true,
  "lines": [
    {
      "id": "3",
      "number": "5511888888888",
      "name": "Main WA line"
    }
  ],
  "total": 1
}
```

If your account has exactly one line, `from_number` can be omitted in other WhatsApp tools (auto-detected).

## Related REST docs

- [MakeWhatsapp](../../api/v2/whatsapp/MakeWhatsapp.md)
- [GetWATemplates](../../api/v2/whatsapp/GetWATemplates.md)
