# Create campaign

*Create a voice campaign — simple TTS, IVR Q&A, or confirmation+validation flow.*


**Endpoint:** `POST https://<base>/api/v2/CreateCampaign.php`

Creates a voice campaign that batch-dials a destination list (`cd_lista_cadastro`). Supports four flavors via `cp_type`:

- `0` (default) — **Simple TTS / audio playback**.
- `4` — **Q&A IVR** (collects DTMF digits with branched audio per digit).
- `6` — **Confirmation + validation** (callee confirms identity by entering a digit-coded value).
- Cloning from another campaign (`cp_id`) reuses an existing model and just changes scheduling / list.

The endpoint can also generate the destination list and the audio assets in a single call by accepting CSV/JSON content and TTS text.

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Common parameters

#### `tsid` — type: *string* — **required**

Token for the account.


#### `name` — type: *string*

Campaign name (`cp_nome`). When cloning, defaults to the name of the source destination list.


#### `detail` — type: *string*

Free-text description (`cp_descritivo`).


#### `cdlc_id` — type: *integer*

ID of an existing destination list. Required unless you upload a list inline (see "Inline list" below).


#### `cp_id` — type: *integer*

Source campaign id when cloning. When set, most schedule/audio parameters are copied from the source.


#### `cp_type` — type: *string*

Campaign type: empty / `0` (simple), `4` (Q&A), `6` (confirmation+validation).


#### `cp_ctid` — type: *string*

Customer-side campaign id, useful for analytics and downstream filtering.


#### `content` — type: *string*

Existing audio file id (`cd_wav.cdw_file`) for the main message.


#### `text` — type: *string*

TTS text — when supplied, the endpoint generates the audio internally and uses it instead of `content`.


#### `voice` — type: *string*

TTS voice (`provider|VoiceName`).


#### `amd` — type: *string*

Audio file id used for answering-machine detection.


#### `urlcontent` — type: *string*

Public URL to fetch an audio file from (`http`/`https`). Use as an alternative to `content`/`text`.


#### `audio64` — type: *string*

Base64-encoded audio. Auto-decoded into the `audio` parameter when `audio` is empty.


#### `date_start` — type: *string*

Start date `YYYY-MM-DD`. Defaults to today.


#### `date_end` — type: *string*

End date `YYYY-MM-DD`. Defaults to `date_start`.


#### `time_start` — type: *string*

Daily start time `HH:MM:SS`. Default `00:00:00`.


#### `time_end` — type: *string*

Daily end time `HH:MM:SS`. Default `23:59:59`.


#### `vel` — type: *string* — default: `max`

Maximum calls per minute. Either an integer (`1`–`100`) or `max` to use the customer's full channel allocation.


#### `resends` — type: *integer* — default: `0`

Number of retries when calls fail. Total attempts = `resends + 1`. Hard cap is `3` retries.


#### `time_resends` — type: *integer* — default: `30`

Minutes between retries (`1`–`240`).


#### `mobile` — type: *integer* — default: `1`

Set `1` to allow mobile numbers, `0` to skip them.


#### `max_answered` — type: *integer*

Stop after this many answered calls.


#### `limit_name` — type: *integer* — default: `1`

Match limit per recipient name (`0`–`2`).


#### `no_block` — type: *integer*

`1` disables the PROCON-style block-list filter (use with care; legal/compliance implications in BR).


#### `group` — type: *integer*

Group id (`cd_group.cdg_id`) for organizing the campaign in dashboards.


#### `queue_id` — type: *integer*

Contact-center queue id (`cc_fila.ccf_id`) to which calls are transferred.


#### `rurl` — type: *string*

Custom callback URL for status updates.


#### `tfix` — type: *string*

Fixed termination route. Multiple values separated by `|`.


#### `xnum` — type: *integer*

Set `1` to allow multiple destination numbers per record.


#### `sms_action` — type: *string*

Trigger an SMS follow-up. One of `ok`, `nae`, `oknae`, `dtmf1`. Only with `cp_type` empty / `0`.


#### `sms_text` — type: *string*

SMS body when `sms_action` is set. Max 160 chars (accents stripped).


#### `cp_ativo` — type: *integer*

`1` activates the campaign immediately, `0` keeps it paused.


### Q&A campaign (`cp_type=4`) — extra parameters

#### `cont0..cont9` — type: *string*

Audio file ids played per digit pressed (`cont0` for `0`, `cont1` for `1`, ...).


#### `contentno` — type: *string*

Audio for "no digit pressed".


#### `dtmfini` — type: *string*

Digit that replays the initial audio.


#### `nans` — type: *integer* — default: `1`

Number of digits to capture (`1`–`3`).


#### `dtime` — type: *integer* — default: `7`

Seconds to wait for digits (`4`–`15`).


### Confirmation+validation (`cp_type=6`) — extra parameters

#### `content2..content8` — type: *string*

Branch audios (success, failure, follow-up prompts).


#### `contentfail` — type: *string*

Audio played when validation fails.


#### `ndigval` — type: *string*

Number of digits expected for validation.


#### `dtmf2, fdtmf` — type: *string*

Per-digit DTMF rules and filter rule (`fdtmf=<column>|<value>`).


#### `compw` — type: *string*

Column used to validate the digits typed by the callee. One of `cod_cli`, `extra1`, `extra2`, `extra3`.


### Inline list

You can supply the destination list directly instead of pre-creating it via [`CreateDestinationBase`](../destinations/CreateDestinationBase.md):

#### `datajson` — type: *object | string*

JSON array (or stringified JSON) of destinations.


Or send a multipart form with a CSV/JSON file (any field name). The endpoint detects the file extension and routes accordingly.

### FTP report scheduling

#### `relftp` — type: *integer*

ID of an existing FTP delivery profile (`cd_programa_ftp.cpftp_id`) to deliver call results.


## Request example
```bash curl (simple TTS)
curl -X POST 'https://<base>/api/v2/CreateCampaign.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "name": "Welcome 2026",
    "cdlc_id": 12345,
    "text": "Hello <NOME>, welcome to Acme.",
    "voice": "google|pt-BR-Wavenet-A",
    "vel": "max",
    "date_start": "2026-05-08",
    "time_start": "09:00:00",
    "time_end": "18:00:00"
  }'
```

```bash curl (Q&A)
curl -X POST 'https://<base>/api/v2/CreateCampaign.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "name": "NPS 2026",
    "cdlc_id": 12345,
    "cp_type": "4",
    "content": "tf12345",
    "cont1": "tf12001",
    "cont2": "tf12002",
    "cont3": "tf12003",
    "nans": 1,
    "dtime": 7
  }'
```
## Response
```json 200 OK
{
  "return": {
    "status": "OK",
    "status_code": "0",
    "cp_id": "987654"
  }
}
```
- **`return.cp_id`** (*string*) — Newly created campaign id (`cd_programa.cp_id`). Use it with [`ChangeCampaign`](ChangeCampaign.md) and [`GetCampaignsList`](GetCampaignsList.md).


## Error codes

In addition to [global authentication codes](../errors.md), `CreateCampaign` may return:

| Code | Cause |
| --- | --- |
| `200` | FTP profile (`relftp`) does not exist. |
| `205` | Uploaded file rejected (executable). |
| `206`/`207` | `datajson` parameter or uploaded JSON file is not valid JSON. |
| `212`–`227` | Validation errors on individual parameters (`max_answered`, `mobile`, `vel`, `resends`, `time_resends`, `cp_type`, `no_block`, `limit_name`, etc.). |
| `230` | Active campaign already exists with the same name + start date. |
| `240`–`244` | Audio assets referenced (`content`, `contentno`, `contentfail`, `amd`, `content2..content8`) not found. |
| `250`/`251` | Group or destination list invalid. |
| `252` | `compw` not recognized. |
| `260` | DB error inserting the campaign model. |
| `261` | DB error inserting the campaign row. |
| `262` | Campaign id was not generated (parameter validation failed silently). |
| `270`–`275` | Failure generating the destination list from inline data (`datacsv`/`datajson`). |
| `280`/`281` | TTS or audio-URL fetch failed. |
| `282` | Source `cp_id` (clone) does not belong to the customer. |
| `290`/`291` | `nans` / `nans2` out of bounds. |
| `300`–`305` | SMS follow-up parameters invalid. |

> **Note**
> This is the most powerful and most error-prone endpoint of the API. We recommend creating campaigns through the Velip portal until your integration is well-tested, and only switching to programmatic creation for high-volume / repetitive use cases.
