# MCP server overview

*Expose Velip communications APIs as MCP tools for AI agents and IDE integrations.*

The **Velip MCP APIs server** is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that wraps the Velip Public API v2. AI clients (Cursor, Claude Desktop, LangGraph agents, etc.) can call Velip without writing HTTP integration code — they discover and invoke **tools** such as `send_sms`, `make_tts_call`, or `send_whatsapp`.

## Architecture

```
AI client (Cursor, Claude, custom agent)
        │  HTTPS + Bearer token
        ▼
https://vox20.velip.com.br/mcpserver/velip
        │  MCP Streamable HTTP (JSON-RPC)
        ▼
Velip MCP APIs server
  • validates token (cd_psid)
  • filters tools by permission (cdpsid_mcp_apis)
  • proxies to Velip PHP API
        ▼
https://vox.velip.com.br/api/v2/
```

## When to use MCP vs REST

| Use MCP when… | Use REST API v2 when… |
| --- | --- |
| Integrating with Cursor, Claude, or an MCP-native agent | Building a traditional backend or mobile app |
| You want the LLM to pick tools dynamically | You need full control over every HTTP call |
| Quick prototyping from an IDE | You need endpoints not yet exposed as MCP tools |

Both interfaces use the **same account token** and enforce the **same business rules** (balance, validation, rate limits).

## What is available

13 MCP tools covering SMS, outbound voice (TTS), WhatsApp, Gmail OAuth, campaigns, destinations, and call status. See the [tools index](tools/README.md).

Tools not listed in your `tools/list` response are hidden because your token lacks permission for that channel — not because they do not exist.

## Transport

- **Protocol:** MCP over **Streamable HTTP** (stateless JSON-RPC)
- **Auth:** `Authorization: Bearer <30-char-token>` on every request
- **Health:** `GET /mcpserver/velip/health` (no auth)

## Next steps

1. [Getting started](getting-started.md) — token, first `tools/list`, first `send_sms`
2. [Authentication](authentication.md) — how tokens work
3. [Permissions](permissions.md) — enable SMS, telephony, WhatsApp, Gmail per token
4. [Connect Cursor](clients/cursor.md) or [Claude Desktop](clients/claude-desktop.md)

## REST equivalent

Every MCP tool maps to one or more [REST API v2](../api/v2/README.md) endpoints. Tool pages include cross-links to the PHP API reference.
