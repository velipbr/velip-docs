# Connect Claude Desktop

*Use the Velip MCP server from Anthropic Claude Desktop via HTTP transport.*

Claude Desktop supports MCP servers through configuration in its app settings.

## Configuration

Edit the Claude Desktop config file:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add:

```json
{
  "mcpServers": {
    "velipai-apis": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-client-http"],
      "env": {
        "MCP_HTTP_URL": "https://vox20.velip.com.br/mcpserver/velip",
        "MCP_HTTP_HEADERS": "{\"Authorization\": \"Bearer YOUR_TOKEN_30_CHARS\"}"
      }
    }
  }
}
```

Replace `YOUR_TOKEN_30_CHARS` with your Velip MCP token.

> Requires Node.js / `npx` available on your machine for the HTTP bridge.

## Restart Claude Desktop

Quit and reopen Claude Desktop after saving the config.

## Usage

Ask Claude to use Velip tools naturally, for example:

- *"Send a WhatsApp template message to …"*
- *"Place a TTS call with this text …"*
- *"List my active campaigns"*

Claude discovers tools via MCP and calls them on your behalf.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Server not listed | Validate JSON syntax in config file |
| `npx` errors | Install Node.js 18+ |
| Empty tool list | [Permissions](../permissions.md) — enable required channels |
| Auth failures | [Authentication](../authentication.md) — verify token |

## Related

- [Cursor setup](cursor.md)
- [curl setup](curl.md)
- [Getting started](../getting-started.md)
