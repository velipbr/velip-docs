# MCP via curl

*Call the Velip MCP server directly with JSON-RPC over HTTP.*

Endpoint:

```
POST https://vox20.velip.com.br/mcpserver/velip
Authorization: Bearer YOUR_TOKEN_30_CHARS
Content-Type: application/json
```

## Health check (no auth)

```bash
curl https://vox20.velip.com.br/mcpserver/velip/health
```

## List tools

```bash
curl -X POST 'https://vox20.velip.com.br/mcpserver/velip' \
  -H 'Authorization: Bearer YOUR_TOKEN_30_CHARS' \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Call a tool

```bash
curl -X POST 'https://vox20.velip.com.br/mcpserver/velip' \
  -H 'Authorization: Bearer YOUR_TOKEN_30_CHARS' \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "send_sms",
      "arguments": {
        "dest": "11999999999",
        "text": "Test via curl"
      }
    }
  }'
```

## Protocol notes

- Transport: **MCP Streamable HTTP** (JSON-RPC 2.0)
- Methods used: `tools/list`, `tools/call`
- Responses wrap tool output in the MCP result envelope; tool implementations return Velip-style `{success, status, ...}` objects

## More examples

See individual tool pages under [tools/](../tools/README.md) — each includes a ready-to-run `tools/call` payload.

## Related

- [Getting started](../getting-started.md)
- [Authentication](../authentication.md)
- [REST API v2](../../api/v2/getting-started.md) — direct HTTP alternative
