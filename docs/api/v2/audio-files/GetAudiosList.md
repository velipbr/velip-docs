# List audio files

*List the audio assets available for the authenticated account.*


**Endpoint:** `POST https://<base>/api/v2/GetAudiosList.php`

Returns the audio assets registered for the customer (`cd_wav.cdw_cdcs_id`) that have not expired (`cdw_expires > today`) and are visible (`cdw_dis = '1'`). You can filter by type (`tts`, `upload`, `rec`, `todas`) and by free-text search across name, file id, and source text.

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Request

#### `tsid` — type: *string* — **required**

Token for the account.


#### `type` — type: *string* — default: `todas`

Filter by asset type. One of `todas` (all), `tts`, `upload`, `rec`.


#### `search` — type: *string*

Free-text search across `cdw_name`, `cdw_file`, `cdw_text` (uses SQL `LIKE %term%`).


#### `maxreg` — type: *integer* — default: `100`

Maximum number of records to return. Hard cap is whatever you pass (the endpoint does not apply its own ceiling).


## Request example
```bash curl
curl -X POST 'https://<base>/api/v2/GetAudiosList.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "type": "tts",
    "search": "welcome",
    "maxreg": 50
  }'
```
## Response
```json 200 OK
{
  "return": {
    "status": "OK",
    "status_code": "0"
  },
  "audios": [
    {
      "cdw_file": "tf12345",
      "cdw_name": "Welcome message",
      "cdw_sec": "8",
      "cdw_date": "2026-04-15",
      "cdw_expires": "2031-04-15",
      "cdw_type": "tts"
    }
  ]
}
```
- **`audios[].cdw_file`** (*string*) — Asset id (e.g., `tf12345`). Pass the numeric portion as `content`/`contentN` in [`MakeTTSCall`](../voice/MakeTTSCall.md).


- **`audios[].cdw_sec`** (*string*) — Duration of the audio in seconds.


- **`audios[].cdw_expires`** (*string*) — Expiration date (`YYYY-MM-DD`). Assets used in calls have their expiration extended automatically.


## Error codes

| Code | `status` | Cause |
| --- | --- | --- |
| `500` | `internal error` | Database error preparing/running the query. |

The endpoint inherits the [global authentication codes](../errors.md).
