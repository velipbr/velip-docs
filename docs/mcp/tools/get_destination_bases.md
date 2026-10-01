# get_destination_bases

*List destination bases and find a base ID by its name.*

| | |
| --- | --- |
| **Permission** | `telephony` |
| **REST equivalent** | [GetDestinationsList](../../api/v2/destinations/GetDestinationsList.md) |

Returns the account's destination bases, newest first. Use it to find the `cdlc_id` of an existing base before calling [create_campaign](create_campaign.md) or [clone_campaign](clone_campaign.md). Read-only.

Only active bases are listed by default, because campaigns reject inactive bases.

## Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `search` | string | No | Part of the base name or imported file name. Case and accents are ignored |
| `cdlc_id` | string | No | One base by ID (digits only) |
| `ctid` | string | No | Bases with this external control ID |
| `status` | string | No | `active` (default), `inactive` or `all` |
| `max_records` | integer | No | Max bases (default 100, max 500) |

Use one filter at a time. If several are given, only one applies, in this order: `ctid`, `cdlc_id`, `search`.

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
      "name": "get_destination_bases",
      "arguments": { "search": "jequie" }
    }
  }'
```

## Responses

**Success:**

```json
{
  "success": true,
  "bases": [
    {
      "cdlc_id": "4248439",
      "cdlc_active": "1",
      "cdlc_deleted": "0",
      "cdlc_ctid": "0",
      "cdlc_name": "JEQUIE",
      "cdlc_file": "up_5912_20261001_170411_JEQUIE.csv",
      "cdlc_date": "2026-10-01",
      "cdlc_num": "76985"
    }
  ],
  "total": 1,
  "truncated": false
}
```

- All values are strings. `cdlc_num` is the number of destinations in the base.
- `cdlc_deleted: "1"` means the destinations were already purged: the base cannot be reactivated, so create a new one.
- `truncated: true` means more bases match than were returned; narrow the `search` or raise `max_records`.
- When nothing matches, the response has an empty `bases` list and a `hint`.
- Several bases can share a name. Pick the newest, or check `cdlc_date` and `cdlc_num`.
