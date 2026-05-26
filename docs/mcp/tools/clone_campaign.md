# clone_campaign

*Clone an existing campaign with new destinations and dates.*

| | |
| --- | --- |
| **Permission** | `telephony` |
| **REST equivalent** | [CreateCampaign](../../api/v2/campaigns/CreateCampaign.md) (clone mode) |

Clones a campaign created in the control panel (including VoiceBot, Q&A, and other complex types). Only destinations and schedule need to be supplied each run.

## Required parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `cp_id` | string | Source campaign ID ([get_campaigns_list](get_campaigns_list.md)) |
| `date_start` | string | New start date `YYYY-MM-DD` |
| `date_end` | string | New end date `YYYY-MM-DD` |

## Destinations (one required)

| Parameter | Type | Description |
| --- | --- | --- |
| `cdlc_id` | string | Destination base ID |
| `datajson` | string | Inline destination JSON |

## Optional parameters

| Parameter | Description |
| --- | --- |
| `time_start`, `time_end` | Inherited from source if omitted |
| `name`, `detail`, `group` | Override metadata |
| `vel`, `resends`, `mobile`, `max_answered` | Dialing behaviour |

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
      "name": "clone_campaign",
      "arguments": {
        "cp_id": "100",
        "date_start": "2026-06-01",
        "date_end": "2026-06-15",
        "cdlc_id": "789"
      }
    }
  }'
```

## Responses

**Success:**

```json
{
  "success": true,
  "cp_id": "201",
  "message": "Campaign cloned"
}
```
