# Change campaign

*Update schedule, throughput, or status of an existing campaign.*


**Endpoint:** `POST https://<base>/api/v2/ChangeCampaign.php`

Updates one or more fields of an existing campaign without recreating it. Useful for pausing/resuming campaigns, adjusting daily windows, throttling throughput, or renaming.

The endpoint applies all provided fields atomically and returns the resulting campaign in the same shape as [`GetCampaignsList`](GetCampaignsList.md).

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Request

#### `tsid` — type: *string* — **required**

Token for the account.


#### `cp_id` — type: *integer* — **required**

Campaign id (`cd_programa.cp_id`).


#### `active` — type: *integer*

`0` to pause, `1` to activate.


#### `lig_min` — type: *string*

Calls-per-minute throttle. Either a non-negative integer or `max`.


#### `pas` — type: *integer*

Maximum number of concurrent transfers (`cp_cdtrf_emcurso_lim`). Must be `≥ 1`.


#### `date_start` — type: *string*

Start date `YYYY-MM-DD`.


#### `date_end` — type: *string*

End date `YYYY-MM-DD`.


#### `time_start` — type: *string*

Daily start time `HH:MM:SS`.


#### `time_end` — type: *string*

Daily end time `HH:MM:SS`.


#### `name` — type: *string*

Campaign name.


You must supply at least one mutable field besides `cp_id`; otherwise the endpoint returns code `210`.

## Request example
```bash curl
curl -X POST 'https://<base>/api/v2/ChangeCampaign.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "cp_id": 987654,
    "active": 0,
    "time_end": "20:00:00"
  }'
```
## Response
```json 200 OK
{
  "return": { "status": "OK", "status_code": "0" },
  "campaigns": [
    {
      "cp_id": 987654,
      "cp_name": "Welcome 2026",
      "cp_ctid": "null",
      "cp_active ": "0",
      "cp_ontime ": "0",
      "cp_date_start": "2026-05-08",
      "cp_date_end": "2026-05-08",
      "cp_time_start": "09:00",
      "cp_time_end": "20:00",
      "cp_destinations": 4500,
      "cp_lig_min": "max",
      "cp_pas": "null",
      "cp_made": 1230,
      "cp_answered": 870,
      "cp_transfered": "null",
      "cp_model": 0
    }
  ]
}
```
## Error codes

| Code | `status` | Cause |
| --- | --- | --- |
| `200` | `No cp_id` | Missing or empty `cp_id`. |
| `210` | `No new parameters` | None of the mutable fields was supplied. |
| `212` | `cp_id no valid` | Campaign does not belong to the customer. |
| `230` | `Parameters without change` | UPDATE matched no row (the values were identical to the current ones). |

> **Note**
> Field keys with a trailing space (`cp_active `, `cp_group `, `cp_ontime `) are kept for backward compatibility. Don't fix the names client-side — match them exactly when parsing.
