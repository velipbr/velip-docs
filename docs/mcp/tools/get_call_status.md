# get_call_status

*Retrieve call status and history.*

| | |
| --- | --- |
| **Permission** | `telephony` |
| **REST equivalent** | [GetCallStatus](../../api/v2/voice/GetCallStatus.md) |

Returns call records with status, duration, DTMF responses, and recording URLs. All filter parameters are optional. Default limit: 1000 records (newest first).

For tokens without "full numbers" (all OAuth connectors), phone numbers come masked (`xxxxx` + last 3 digits, `return.numbers_masked=true`) in lists **and** in `cd_id` lookups; only a `ctid` that matches a single call returns the full number.

## Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `cp_id` | string | No | Filter by campaign ID |
| `cpid` | string | No | Filter by campaign external CTID |
| `ctid` | string | No | Filter by call tracking ID. When `ctid` is sent, `cd_id` is ignored; `ctid="null"` or a `ctid` shared by several calls is a list request |
| `cd_id` | string | No | Single call lookup (ignored when `ctid` is given) |
| `date_start` | string | No | Start date `YYYY-MM-DD` (use with `date_end`) |
| `date_end` | string | No | End date `YYYY-MM-DD` |
| `max_records` | integer | No | Max records per page (default 1000; maximum 5000 — `-1` means the maximum) |
| `last_id` | string | No | Pagination cursor from previous `next_id` |
| `only_dtmf` | boolean | No | Only calls with DTMF data |

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
      "name": "get_call_status",
      "arguments": {
        "date_start": "2026-05-01",
        "date_end": "2026-05-26",
        "max_records": 50
      }
    }
  }'
```

## Responses

**Success:**

```json
{
  "success": true,
  "calls": [
    {
      "cd_id": "42_999",
      "cd_status": "OK",
      "dest": "5511999999999",
      "date": "2026-05-26",
      "dur": "45",
      "cdr_url": "https://..."
    }
  ],
  "total": 1,
  "pagination": { "has_more": false, "next_id": "" }
}
```

`cd_status` values: `OK`, `BUSY`, `NOANSWER`, `CANCEL`, `CONGESTION`, `CHANUNAVAIL`.
