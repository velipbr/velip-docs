# Custom MCP clients

*Integrate any MCP-compatible agent with the Velip server.*

The Velip MCP server implements the [Model Context Protocol](https://modelcontextprotocol.io/) over **Streamable HTTP**. Any client that supports this transport can connect.

## Connection parameters

| Parameter | Value |
| --- | --- |
| URL | `https://vox20.velip.com.br/mcpserver/velip` |
| Auth | `Authorization: Bearer <30-char-token>` |
| Protocol | JSON-RPC 2.0 (`tools/list`, `tools/call`, …) |

## Official resources

- [MCP specification](https://modelcontextprotocol.io/specification/)
- [MCP SDKs](https://modelcontextprotocol.io/docs/sdk) — Python, TypeScript, etc.

## Typical integration flow

1. Connect to the MCP endpoint with your Bearer token.
2. Call `tools/list` to discover allowed tools (filtered by [permissions](../permissions.md)).
3. Call `tools/call` with `name` and `arguments` matching the [tool reference](../tools/README.md).
4. Parse the `{success, ...}` payload returned by each tool.

## LangGraph / autonomous agents

Velip autonomous agents can attach this MCP server as an external tool source. Configure the same URL and Bearer token in your agent's MCP client settings. The agent runtime handles `tools/list` and routing.

## REST fallback

If your stack does not support MCP yet, use the [REST API v2](../../api/v2/README.md) directly — same account, same tokens, same business logic.

## Related

- [Overview](../overview.md)
- [curl examples](curl.md)
- [Permissions](../permissions.md)
