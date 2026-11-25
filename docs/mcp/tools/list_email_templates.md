# list_email_templates

*List the email templates of the account, with the variables each one needs.*

| | |
| --- | --- |
| **Permission** | `gmail` |
| **REST equivalent** | *(none — templates are managed in the Velip portal)* |

Returns the email templates of the account (up to 200, by name). `template_id` is the value [send_email](send_email.md) takes to send by template, and `variables` lists the values `send_email` needs in its `variables` parameter. `EMAIL` and `UNSUB_LINK` are filled by Velip and never need a value.

## Parameters

None.

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
      "name": "list_email_templates",
      "arguments": {}
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
      "template_id": 42,
      "name": "Order confirmation",
      "subject": "Your order {{EXTRA1}}",
      "variables": ["NOME", "EXTRA1"]
    }
  ],
  "total": 1,
  "note": "EMAIL and UNSUB_LINK are filled automatically by the platform. Provide values for the other listed variables via the 'variables' parameter of send_email."
}
```

Standard variables are `NOME`, `COD_CLI` and `EXTRA1` to `EXTRA8`, plus the automatic `EMAIL` and `UNSUB_LINK`.
