# List campaigns

*Search and list campaigns belonging to the authenticated account.*


**Endpoint:** `POST https://<base>/api/v2/GetCampaignsList.php`

Returns up to `maxreg` campaigns sorted by descending id, with current schedule, throughput, and progress counters. Filters let you scope by group, ctid, single id, model templates, end-date floor, or free-text search.

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Request

#### `tsid` — type: *string* — **required**

Token for the account.


#### `cp_id` — type: *integer*

Single campaign id.


#### `cp_ctid` — type: *string*

Customer-side campaign id (`cp_ctid`).


#### `group` — type: *integer*

Group id (`cp_cdg_id`).


#### `type` — type: *string*

Pass `on` to return only currently active campaigns (`cp_ativo = 1`).


#### `model` — type: *string*

Pass `1` to return only campaigns flagged as model templates (`cp_model_show = 1`).


#### `date` — type: *string*

Filter by end date. `1` = today onward; otherwise a `YYYY-MM-DD` to floor `cp_data_fim`.


#### `search` — type: *string*

Free-text search across `cp_nome`, `cp_descritivo`, `cp_id`, and `cm_vmc_audio`.


#### `maxreg` — type: *integer* — default: `500`

Maximum number of records to return.


## Request example
```bash curl
curl -X POST 'https://<base>/api/v2/GetCampaignsList.php' \
  -H 'Content-Type: application/json' \
  -d '{ "tsid": "YOUR_TSID", "type": "on", "maxreg": 50 }'
```
## Response
```json 200 OK
{
  "return": { "status": "OK", "status_code": "0" },
  "campaigns": [
    {
      "cp_id": 987654,
      "cp_name": "Welcome 2026",
      "cp_ctid": "lote-A",
      "cp_group ": "marketing",
      "cp_active ": "1",
      "cp_ontime ": "1",
      "cp_date_start": "2026-05-08",
      "cp_date_end": "2026-05-09",
      "cp_time_start": "09:00",
      "cp_time_end": "18:00",
      "cp_destinations": 4500,
      "cp_lig_min": "max",
      "cp_pas": "null",
      "cp_made": 1230,
      "cp_answered": 870,
      "cp_transfered": "null",
      "cp_model": 0,
      "cp_max_answered": "0",
      "cp_group_id": "12",
      "cp_status_txt": "Inseridos: 4500 destinos (2s)"
    }
  ]
}
```
- **`campaigns[].cp_active `** (*string*) — `1` active, `0` inactive, `2` still loading destinations (creation is asynchronous; see [CreateCampaign](CreateCampaign.md)).
- **`campaigns[].cp_ontime `** (*string*) — `1` when the campaign is active **and** the current date/time is inside its schedule window.
- **`campaigns[].cp_max_answered`** (*string*) — Answered-call limit (`0` = no limit).
- **`campaigns[].cp_group_id`** (*string*) — Group id (`0` = no group).
- **`campaigns[].cp_status_txt`** (*string*) — Destination loading status, e.g. `-Gerando: 20000 destinos (8s)` while loading and `Inseridos: 4500 destinos (2s)` when done. When loading died, the campaign is set to `cp_active` `0` with a text starting `Falha na geração` (after about 30 minutes without progress): nothing is dialed, it cannot be activated again ([ChangeCampaign](ChangeCampaign.md) error `234`), and a new campaign with the same list, date and time can be created.


- **`campaigns[].cp_pas`** (*string*) — Concurrency limit for transferred calls (`cp_cdtrf_emcurso_lim`). `null` for campaigns whose model is not transfer-based.


- **`campaigns[].cp_transfered`** (*string*) — Number of calls that requested transfer. `null` for non-transfer campaigns.


## Error codes

| Code | `status` | Cause |
| --- | --- | --- |
| `500` | `internal error` | Database error preparing/running the query. |
