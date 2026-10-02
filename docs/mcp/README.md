# Velip MCP server — documentation index

The Velip MCP server exposes Velip APIs (SMS, voice, WhatsApp, email, campaigns) as **Model Context Protocol (MCP) tools** for AI clients such as Cursor, Claude Desktop, and custom agents.

## Core

| Topic | File |
| --- | --- |
| Overview | [overview.md](overview.md) |
| Getting started | [getting-started.md](getting-started.md) |
| Authentication | [authentication.md](authentication.md) |
| Permissions | [permissions.md](permissions.md) |

## Connect a client

| Client | File |
| --- | --- |
| Cursor IDE | [clients/cursor.md](clients/cursor.md) |
| Claude Desktop | [clients/claude-desktop.md](clients/claude-desktop.md) |
| curl (HTTP) | [clients/curl.md](clients/curl.md) |
| Custom MCP client | [clients/custom.md](clients/custom.md) |

## Tools reference

| Channel | Tools |
| --- | --- |
| SMS | [send_sms](tools/send_sms.md) |
| Telephony | [make_tts_call](tools/make_tts_call.md), [get_tts_voices](tools/get_tts_voices.md), [get_call_status](tools/get_call_status.md), [get_campaigns_list](tools/get_campaigns_list.md), [get_campaign_groups](tools/get_campaign_groups.md), [create_campaign](tools/create_campaign.md), [clone_campaign](tools/clone_campaign.md), [change_campaign](tools/change_campaign.md) |
| Destination bases | [create_destination_base](tools/create_destination_base.md), [get_destination_bases](tools/get_destination_bases.md) |
| WhatsApp | [send_whatsapp](tools/send_whatsapp.md), [get_wa_templates](tools/get_wa_templates.md), [get_wa_lines](tools/get_wa_lines.md) |
| Gmail | [send_gmail_oauth](tools/send_gmail_oauth.md) |

Full tool index: [tools/README.md](tools/README.md)

## Related

- [REST API v2 index](../api/v2/README.md) — same capabilities via HTTP endpoints
- [REST Authentication](../api/v2/authentication.md) — token issuance (`tsid`)

## Production endpoints

| Endpoint | URL |
| --- | --- |
| MCP (Streamable HTTP) | `https://vox20.velip.com.br/mcpserver/velip` |
| Health check | `https://vox20.velip.com.br/mcpserver/velip/health` |
