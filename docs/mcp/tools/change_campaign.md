# change_campaign

*Edit parameters of an existing campaign.*

| | |
| --- | --- |
| **Permission** | `telephony` |
| **REST equivalent** | [ChangeCampaign](../../api/v2/campaigns/ChangeCampaign.md) |

Updates campaign settings. At least one field besides `cp_id` must be provided.

## Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `cp_id` | string | Yes | Campaign ID to edit |
| `cp_active` | string | No | `1` activate, `0` deactivate. A campaign whose loading failed (`cp_status_txt` starting `Falha na geração`) cannot be activated: error `234`, create it again |
| `date_start` | string | No | New start date `YYYY-MM-DD` |
| `date_end` | string | No | New end date |
| `time_start` | string | No | New start time `HH:MM` |
| `time_end` | string | No | New end time |
| `vel` | string | No | Calls per minute |
| `cp_pas` | string | No | Transfer positions (PA count) |
| `name` | string | No | New name (max 50 chars) |
| `max_answered` | string | No | Answered-call limit, `0` = no limit. Changing it reopens sending, like the control panel: a campaign that stopped at the limit dials again if the limit goes up |
| `group` | string | No | Group ID from [get_campaign_groups](get_campaign_groups.md); `0` removes the campaign from its group |

## Example — activate campaign

```bash
curl -X POST 'https://vox20.velip.com.br/mcpserver/velip' \
  -H 'Authorization: Bearer YOUR_TOKEN_30_CHARS' \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "change_campaign",
      "arguments": {
        "cp_id": "200",
        "cp_active": "1"
      }
    }
  }'
```

## Responses

**Success:**

```json
{
  "success": true,
  "campaign": {
    "cp_id": "200",
    "cp_name": "June campaign",
    "cp_active": "1",
    "cp_ontime": "1",
    "cp_made": "0",
    "cp_answered": "0"
  }
}
```
