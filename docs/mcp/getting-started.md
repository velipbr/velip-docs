# MCP getting started

*Obtain a token, verify connectivity, and send your first SMS via MCP.*

## Prerequisites

- A Velip account with API access enabled.
- A **30-character Bearer token** with MCP permissions configured (see [Authentication](authentication.md) and [Permissions](permissions.md)).
- At least the `sms` channel enabled on your token for this walkthrough.

## Step 1 — Health check

No authentication required:

```bash
curl https://vox20.velip.com.br/mcpserver/velip/health
```

Expected: HTTP `200` with a JSON body indicating the service is up.

## Step 2 — List available tools

Replace `YOUR_TOKEN_30_CHARS` with your token:

```bash
curl -X POST 'https://vox20.velip.com.br/mcpserver/velip' \
  -H 'Authorization: Bearer YOUR_TOKEN_30_CHARS' \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

You should see only tools your token is allowed to use (e.g. `send_sms` if SMS is enabled).

## Step 3 — Send an SMS

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
        "text": "Hello from Velip MCP"
      }
    }
  }'
```

**Success example:**

```json
{
  "success": true,
  "status": "OK",
  "cdls_id": "123456",
  "message": "SMS enviado para 11999999999"
}
```

**Error example (permission denied):**

```json
{
  "success": false,
  "error": "Permissão negada para API SMS. Verifique cdpsid_mcp_apis no token.",
  "status_code": 403
}
```

## Step 4 — Connect Cursor (recommended)

For day-to-day use with an AI assistant, configure Cursor once:

1. Open Cursor MCP settings (`mcp.json`).
2. Add the Velip server — see [Cursor client guide](clients/cursor.md).
3. Restart Cursor and ask: *"List my Velip MCP tools"* or *"Send a test SMS to …"*.

## What to read next

- [Authentication](authentication.md) — token format and IP checks
- [Permissions](permissions.md) — enable telephony, WhatsApp, Gmail
- [Tool reference: send_sms](tools/send_sms.md)
- [REST API getting started](../api/v2/getting-started.md) — if you prefer direct HTTP
