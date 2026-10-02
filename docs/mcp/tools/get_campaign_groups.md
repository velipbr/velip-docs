# get_campaign_groups

*List the account's active campaign groups.*

| | |
| --- | --- |
| **Permission** | `telephony` |
| **REST equivalent** | *(Velip DB — no standalone REST page)* |

Returns the active campaign groups (ID and name). Use `group_id` in the `group` parameter of
[create_campaign](create_campaign.md), [clone_campaign](clone_campaign.md) and
[change_campaign](change_campaign.md), or in the `group_id` filter of
[get_campaigns_list](get_campaigns_list.md). Read-only, no parameters.

## Example

```bash
curl -X POST 'https://vox20.velip.com.br/mcpserver/velip' \
  -H 'Authorization: Bearer YOUR_TOKEN_30_CHARS' \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": { "name": "get_campaign_groups", "arguments": {} }
  }'
```

## Responses

**Success:**

```json
{
  "success": true,
  "groups": [
    { "group_id": "15", "name": "Eleições 2026" }
  ],
  "total": 1
}
```
