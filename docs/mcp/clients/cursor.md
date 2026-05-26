# Connect Cursor IDE

*Add the Velip MCP server to Cursor and use Velip tools from the AI chat.*

## Configuration

Edit your Cursor MCP configuration file:

- **macOS / Linux:** `~/.cursor/mcp.json`
- **Windows:** `%USERPROFILE%\.cursor\mcp.json`

Add the Velip server:

```json
{
  "mcpServers": {
    "velipai-apis": {
      "url": "https://vox20.velip.com.br/mcpserver/velip",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN_30_CHARS"
      }
    }
  }
}
```

Replace `YOUR_TOKEN_30_CHARS` with your Velip MCP token.

## Restart Cursor

After saving `mcp.json`, restart Cursor (or reload the window) so the MCP server is discovered.

## Verify connection

In Cursor chat, try:

- *"What Velip MCP tools do I have?"*
- *"Send an SMS to 11999999999 with text Hello"*
- *"List my WhatsApp lines"*

Cursor will call `tools/list` and then invoke tools as needed.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| No Velip tools appear | Token missing MCP permissions — see [Permissions](../permissions.md) |
| `401` / authentication error | Token invalid or typo in `Authorization` header |
| Only some tools visible | Expected — only enabled channels appear in `tools/list` |
| Tool call fails with business error | Check [tool reference](../tools/README.md) and [REST error codes](../../api/v2/errors.md) |

## Security

- Do not commit `mcp.json` with real tokens to version control.
- Prefer a machine-local config or environment-specific token with minimal permissions.

## Related

- [Getting started](../getting-started.md)
- [curl client](curl.md) — test the same server without Cursor
- [MCP overview](../overview.md)
