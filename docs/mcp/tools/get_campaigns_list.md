# get_campaigns_list

*List campaigns for the authenticated account.*

| | |
| --- | --- |
| **Permission** | `telephony` |
| **REST equivalent** | [GetCampaignsList](../../api/v2/campaigns/GetCampaignsList.md) |

Returns up to 500 campaigns (newest first) with status, schedule, and statistics. All parameters are optional.

## Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `max_records` | integer | No | Max campaigns (default 500) |
| `active_only` | boolean | No | Only active campaigns (`cp_active=1`). `cp_active` is `2` while a new campaign is still loading destinations |
| `group_id` | string | No | Filter by group ([get_campaign_groups](get_campaign_groups.md)) |
| `date_filter` | string | No | `1` = ending today or later, or `YYYY-MM-DD` |
| `cp_ctid` | string | No | External CTID filter |
| `cp_id` | string | No | Single campaign ID |
| `search` | string | No | Free-text search |
| `model_only` | boolean | No | Template/model campaigns only |

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
      "name": "get_campaigns_list",
      "arguments": { "active_only": true }
    }
  }'
```

## Responses

**Success:**

```json
{
  "success": true,
  "campaigns": [
    {
      "cp_id": "100",
      "cp_name": "May outreach",
      "cp_active": "1",
      "cp_ontime": "1",
      "cp_date_start": "2026-05-01",
      "cp_date_end": "2026-05-31",
      "cp_made": "1500",
      "cp_answered": "800",
      "cp_status_txt": "Inseridos: 4500 destinos (2s)"
    }
  ],
  "total": 1
}
```

All values are strings. `cp_active` is `2` while a new campaign is still loading destinations. `cp_status_txt` is the loading status; `cp_active` `0` with `cp_status_txt` starting `Falha na geração` means loading failed: tell the user and create the campaign again.
