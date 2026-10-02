# create_campaign

*Create a simple single-audio batch campaign.*

| | |
| --- | --- |
| **Permission** | `telephony` |
| **REST equivalent** | [CreateCampaign](../../api/v2/campaigns/CreateCampaign.md) |

Creates a batch voice campaign with one audio/TTS message. Provide destinations via `cdlc_id` (an active base: find it by name with [get_destination_bases](get_destination_bases.md), or create one with [create_destination_base](create_destination_base.md)) or inline `datajson`.

## Required parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `date_start` | string | Start date `YYYY-MM-DD` |
| `date_end` | string | End date `YYYY-MM-DD` |
| `time_start` | string | Start time `HH:MM` |
| `time_end` | string | End time `HH:MM` |

## Audio (one required)

| Parameter | Type | Description |
| --- | --- | --- |
| `content` | string | Pre-recorded audio ID from [get_tts_voices](get_tts_voices.md) |
| `text` | string | TTS text (supports `NOME`, `COD_CLI`, `EXTRA1`–`EXTRA3`) |

## Destinations (one required)

| Parameter | Type | Description |
| --- | --- | --- |
| `cdlc_id` | string | Existing destination base ID |
| `datajson` | string | Inline JSON (same format as `create_destination_base`) |

## Common optional parameters

| Parameter | Description |
| --- | --- |
| `name` | Campaign name (max 50 chars) |
| `detail` | Description (max 256 chars) |
| `vel` | Calls per minute: `1`–`100` or `max` |
| `resends` | Retries for unanswered: `1`–`3` |
| `sms_text` | SMS sent after call (max 160 chars) |
| `max_answered` | Stop after this many answered calls |
| `group` | Group ID from [get_campaign_groups](get_campaign_groups.md); empty or `0` = no group |
| `active` | `1` active after loading (default) or `0` created inactive |

## Asynchronous generation

Success means the campaign was accepted. Its destinations load in the background (seconds, or minutes for large bases), and then the campaign dials in its date/time window, unless `active` is `0`.

- The response includes `settings` (answered-call limit, speed and resends saved on the campaign) and `next_step`.
- To confirm the load, call [get_campaigns_list](get_campaigns_list.md) with `cp_id`: `cp_active` `2` means still loading, then `1` or `0`.
- Do not change `cp_active` while it is `2`: the loader sets the final status when it finishes.
- Do not repeat a call that returned success. After a timeout or connection error, repeating the exact same call (same arguments) within 30 minutes is safe: the server sends an idempotency key built from the arguments, and the platform returns the campaign already created with `duplicate_request: true` instead of a new one. Changing any argument creates a new campaign.
- If loading dies, after about 30 minutes the campaign shows `cp_active` `0` with `cp_status_txt` starting `Falha na geração`: it cannot be activated; create it again.

See [REST CreateCampaign](../../api/v2/campaigns/CreateCampaign.md) for the full parameter list.

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
      "name": "create_campaign",
      "arguments": {
        "date_start": "2026-06-01",
        "date_end": "2026-06-30",
        "time_start": "09:00",
        "time_end": "18:00",
        "text": "Olá NOME, mensagem de teste.",
        "cdlc_id": "789",
        "name": "June campaign"
      }
    }
  }'
```

## Responses

**Success:**

```json
{
  "success": true,
  "cp_id": "200",
  "message": "Campaign created"
}
```

Use [change_campaign](change_campaign.md) to activate (`cp_active=1`).
