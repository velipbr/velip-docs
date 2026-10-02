# MCP permissions

*Per-token channel access and dynamic tool filtering.*

Each Bearer token carries an optional JSON field **`cdpsid_mcp_apis`** that controls which MCP tools are visible and executable.

## JSON structure

```json
{
  "enabled": true,
  "apis": {
    "sms": { "enabled": true },
    "telephony": { "enabled": true },
    "destinations": { "enabled": true },
    "whatsapp": { "enabled": true },
    "gmail": { "enabled": true }
  }
}
```

| Field | Effect |
| --- | --- |
| `enabled: false` (root) | Blocks all MCP tools |
| `cdpsid_mcp_apis` NULL or empty | Blocks all MCP tools |
| `apis.<channel>.enabled: true` | Tools for that channel appear in `tools/list` and can be called |
| `apis.<channel>.enabled: false` | Tools for that channel are **hidden** from `tools/list` and rejected on call |

Permissions are configured by your account administrator in the Velip token management UI.

## Channel → tools mapping

| Channel | Tools |
| --- | --- |
| `sms` | `send_sms` |
| `telephony` | `make_tts_call`, `get_tts_voices`, `get_call_status`, `get_campaigns_list`, `get_campaign_groups`, `create_campaign`, `clone_campaign`, `change_campaign` |
| `destinations` | `create_destination_base`, `get_destination_bases` |
| `whatsapp` | `send_whatsapp`, `get_wa_templates`, `get_wa_lines` |
| `gmail` | `send_gmail_oauth` |

Destination bases have their own channel because the same base feeds voice, SMS, WhatsApp and e-mail batch campaigns. To create a voice campaign from an existing base, the token needs both `destinations` (to find the base) and `telephony` (to create the campaign).

## Dynamic `tools/list`

The server filters the tool catalog **before** returning it to your client. If WhatsApp is disabled, you will not see `send_whatsapp` — even if you guess the tool name, execution returns `403`.

This is intentional: AI agents should only discover tools they are allowed to use.

## Example scenarios

| Scenario | Result |
| --- | --- |
| Only `sms.enabled: true` | `tools/list` returns `send_sms` only |
| All channels enabled | Full catalog (13 tools) |
| `enabled: false` at root | Empty `tools/list`, all calls rejected |
| Call `make_tts_call` without telephony | `403 Permission denied` |

## Enable all channels (admin SQL example)

```sql
UPDATE cd_psid
SET cdpsid_mcp_apis = '{"enabled":true,"apis":{"sms":{"enabled":true},"telephony":{"enabled":true},"destinations":{"enabled":true},"whatsapp":{"enabled":true},"gmail":{"enabled":true}}}'
WHERE cdpsid_id = YOUR_TOKEN_ID;
```

> Replace `YOUR_TOKEN_ID` with the internal ID. Token management is normally done via the Velip UI, not direct SQL.

## Related

- [Authentication](authentication.md)
- [Tools index](tools/README.md)
- [REST Authentication](../api/v2/authentication.md)
