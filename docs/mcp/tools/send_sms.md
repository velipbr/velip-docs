# send_sms

*Send a single SMS message via the Velip platform.*

| | |
| --- | --- |
| **Permission** | `sms` |
| **REST equivalent** | [MakeSMS](../../api/v2/sms/MakeSMS.md) |

Sends an SMS to one destination. Messages are limited to 160 characters per segment; set `cut_text=true` to truncate instead of erroring.

## Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `dest` | string | Yes | Destination with area code (DDD), digits only. Example: `11999999999` |
| `text` | string | Yes | Message body (max 160 chars unless `cut_text=true`) |
| `from_number` | string | No | Sender ID if authorized for the account |
| `cut_text` | boolean | No | If `true`, truncates text over 160 chars. Default: `false` |

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
      "name": "send_sms",
      "arguments": {
        "dest": "11999999999",
        "text": "Your verification code is 4321"
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
  "cdls_id": "123456",
  "message": "SMS enviado para 11999999999"
}
```

**Error:**

```json
{
  "success": false,
  "status": "error",
  "status_code": 5,
  "error": "Saldo insuficiente"
}
```

See [REST error codes](../../api/v2/errors.md) for `status_code` values.
