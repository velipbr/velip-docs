# create_destination_base

*Create a phone number list for batch campaigns.*

| | |
| --- | --- |
| **Permission** | `telephony` |
| **REST equivalent** | [CreateDestinationBase](../../api/v2/destinations/CreateDestinationBase.md) |

Imports destinations as JSON. Recommended max: 500,000 numbers per base.

## Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `datajson` | string | Yes | JSON array of destinations (see format below) |
| `name` | string | No | Label for the base |
| `ctid` | string | No | External tracking ID |

**Destination object format:**

```json
[
  {"number": "5511999999999", "name": "Jose", "codcli": "12345678900"}
]
```

Positional arrays are also accepted: `[["5511999999999", "Jose", "12345678900"]]`.

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
      "name": "create_destination_base",
      "arguments": {
        "name": "May campaign list",
        "datajson": "[{\"number\":\"5511999999999\",\"name\":\"Jose\"}]"
      }
    }
  }'
```

## Responses

**Success:**

```json
{
  "success": true,
  "cdlc_id": "789",
  "num_dest": 1,
  "base_size": 42,
  "message": "Base created"
}
```

Use `cdlc_id` in [create_campaign](create_campaign.md) or [clone_campaign](clone_campaign.md).
