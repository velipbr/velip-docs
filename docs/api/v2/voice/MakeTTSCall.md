# Place voice call (TTS)

*Outbound voice call with TTS, IVR/DTMF, transfer, and recording.*


**Endpoint:** `POST https://<base>/api/v2/MakeTTSCall.php`

Places a single outbound voice call through the Velip telephony stack. The call can carry recorded audio files, dynamic TTS content with placeholders (`<NOME>`, `<EXTRA1>`–`<EXTRA4>`, `<COD_CLI>`), DTMF/IVR navigation, transfer to a contact-center queue (PA), and optional recording.

This is the most flexible endpoint of the Velip API; many parameters are advanced and only relevant for specific call types. The minimal viable call requires `tsid`, `dest`, and either `text` (for TTS) or `content` (for a recorded audio id).

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Core parameters

#### `tsid` — type: *string* — **required**

Token for the account.


#### `dest` — type: *string* — **required**

Destination phone number. With `setbrasil=1` (default) accepts national formats; otherwise pass full E.164 (without `+`).


#### `text` — type: *string*

TTS text spoken to the callee. One of `text`, `text1..text11`, `content`, or any of the placeholders (`nome`, `extra1..4`, `cod_cli`) must be present.


#### `content` — type: *string*

Audio file id from [`GetAudiosList`](../audio-files/GetAudiosList.md). Multiple slots available: `content1..content15`, plus `contentno`, `contentend`, `contentfail`, `contentdtmf`.


#### `voice` — type: *string*

TTS voice in the form `Provider|VoiceName`. Use [`GetTTSVoices`](GetTTSVoices.md) for the list of voices the account is allowed to use. ElevenLabs is **not** allowed in this endpoint.


#### `encoding` — type: *string*

Encoding of the text payload. One of `UTF-8`, `2UTF-8` (double-encoded), `ASCII`. Defaults to `ISO-8859-1` for form requests; `UTF-8` for JSON.


#### `setbrasil` — type: *integer* — default: `1`

When `1`, normalizes Brazilian numbers; when `0`, sends as-is (international).


#### `callerid` — type: *string*

Override the caller id. Subject to your account's allowed caller ids; falls back to the account default when omitted.


#### `ctid` — type: *string*

Customer-side correlation id; can be enforced unique per call when `cdcs_uni_ctid=1`.


#### `cpid` — type: *string*

Optional campaign id, used to group analytics for many calls.


#### `httpdup` — type: *integer* — default: `10`

Duplicate-suppression window (seconds, 1–600). Returns code `244` when triggered. Pass `0` to disable.


## TTS placeholders

When the spoken script contains placeholders, pass them as separate parameters. The system substitutes them at audio-generation time:

| Placeholder | Parameter |
| --- | --- |
| `<NOME>` / `<NAME>` | `nome` |
| `<EXTRA1>` | `extra1` |
| `<EXTRA2>` | `extra2` |
| `<EXTRA3>` | `extra3` |
| `<EXTRA4>` | `extra4` |
| `<COD_CLI>` / `<CODCLI>` | `cod_cli` |

Example: `text=Hello <NOME>, your code is <COD_CLI>` with `nome=John&cod_cli=4321`.

## Call modes (`type`)

Choose how the call is conducted with the `type` parameter:

| `type` | Behaviour |
| --- | --- |
| `0` (default) | Plays the audio/TTS to the callee and hangs up. |
| `2` | Asks for DTMF confirmation (`dtmfconf`) and transfers to a PA when matched. |
| `3` | DTMF prompt without explicit confirmation; first matching digit transfers. |
| `22` | Plays content and records the response (use `rec=<seconds>`). |
| `100` | Bridges directly to a configured agent (`dtmfini=<ccba_id>` is required). |

## DTMF / IVR

Specify the digits to capture and the action per digit:

#### `ndig` — type: *integer*

Number of digits expected in the response.


#### `dtime` — type: *integer*

Seconds to wait for digits.


#### `dtmfconf` — type: *string*

Single digit that confirms the call (transfers to PA in `type=2`).


#### `dtmfini` — type: *string*

Initial DTMF mapping. For `type=100`, this is the `ccba_id` of the agent to bridge to.


#### `dtmf, dtmf2..dtmf11` — type: *string*

Per-digit destinations. Each maps a key press to a follow-up content/text or to a transfer.


## Transfer to PA / second leg

#### `dest2` — type: *string*

Number of the second leg. Special prefixes (`0800`, `300`, `400`, `103`) bypass national normalization.


#### `fifo` — type: *integer*

When set, queues the transfer in a FIFO until a PA is available.


#### `fifolim` — type: *integer*

Maximum seconds to hold the call in the FIFO before giving up.


#### `senddtmf` — type: *string*

Digits to send after the second leg answers (for IVR-to-IVR bridging).


#### `senddtmftime` — type: *integer*

Seconds to wait after answering the second leg before sending `senddtmf`.


## Recording

#### `rec` — type: *integer*

Maximum seconds of recording to keep. Set together with `mrec` for legacy compatibility.


#### `startrec` — type: *string*

When recording starts: `pa` (after PA bridge), `conf` (after conference forms), or `ini` (from the start).


## Scheduling and retries

#### `repeat` — type: *string*

Format `tries|interval_min|until|YYYY-MM-DD HH:MM`. Example `3|30|22:00|2026-05-10 09:00` — first call at 09:00 on 2026-05-10, then up to 2 retries every 30 minutes until 22:00.


#### `priority` — type: *integer*

Routing priority. `-20` = generate audio synchronously and dial as soon as ready; `-1` = dial immediately, ignoring queue priority.


#### `block` — type: *string*

Schedule a "do not dial before" timestamp.


#### `ringtime` — type: *integer*

Maximum ring duration in seconds.


#### `timelimit` — type: *integer*

Maximum total call duration in seconds.


#### `answer` — type: *integer*

Seconds before considering the call answered when no media is detected.


## SMS follow-up after the call

The endpoint can trigger an SMS based on the call outcome:

#### `sms_action` — type: *string*

One of `ok`, `nae`, `oknae`, `dtmf1`. Decides which call outcomes trigger the SMS.


#### `sms_text` — type: *string*

Body for the follow-up SMS (max 160 chars). Accents are stripped.


#### `sms_dtmf` — type: *string*

When `sms_action=dtmf1`, the digit that triggers the SMS.


## Other parameters

#### `amd` — type: *string*

Audio id used as Answering-Machine Detection prompt.


#### `moh` — type: *integer*

Music-on-hold mode: `1` = dial tone, `2` = default music, `3` = silence.


#### `rurl` — type: *string*

URL-encoded callback URL for status updates (overrides the per-account default).


#### `numlim` — type: *integer*

When set together with `cpid`, blocks repeated dialing of the same number more than `numlim` times.


#### `audiolim` — type: *integer*

Same as `numlim`, but for the same number AND the same audio.


#### `bkddd` — type: *integer*

`1` rejects calls outside the configured DDD time window. `2` queues them silently.


#### `tfix` — type: *string*

Forces a specific termination route (only when authorized for the account). Multiple routes separated by `|`, e.g., `0|100`.


## Request example
```bash curl (simple TTS)
curl -X POST 'https://<base>/api/v2/MakeTTSCall.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "dest": "5511999999999",
    "text": "Hello <NOME>, your appointment is confirmed.",
    "nome": "John",
    "voice": "google|pt-BR-Wavenet-A",
    "encoding": "UTF-8"
  }'
```

```bash curl (DTMF + transfer)
curl -X POST 'https://<base>/api/v2/MakeTTSCall.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "dest": "5511999999999",
    "text": "Press 1 to talk to an agent, 2 to hang up.",
    "type": 2,
    "ndig": 1,
    "dtime": 10,
    "dtmfconf": "1",
    "dest2": "08001234567",
    "fifo": 60
  }'
```

```bash curl (agent bridge)
curl -X POST 'https://<base>/api/v2/MakeTTSCall.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "dest": "5511999999999",
    "type": 100,
    "dtmfini": "42",
    "rec": 1800,
    "startrec": "ini"
  }'
```
## Response
```json 200 OK
{
  "return": {
    "status": "OK",
    "status_code": "0",
    "cd_id": "abc_1234567"
  }
}
```

```json 400 Validation
{
  "return": {
    "status": "number invalid",
    "status_code": "203",
    "cd_id": "0"
  }
}
```
- **`return.status`** (*string*) — `OK` on success; otherwise the failure message.


- **`return.status_code`** (*string*) — `0` on success; otherwise the numeric error code.


- **`return.cd_id`** (*string*) — Internal call id, prefixed with the customer database alias (`<cdcs_db>_<cd_id>`). Use it with [`GetCallStatus`](GetCallStatus.md) to query progress.


## Error codes

In addition to the [global authentication codes](../errors.md), `MakeTTSCall` may return:

| Code | `status` | Cause |
| --- | --- | --- |
| `201` | `No text` | No `text*`, `content`, `nome`, or `extra*` provided. |
| `203` | `number invalid` | `dest` could not be normalized. |
| `210` | `TTS … not permitted in MakeTTSCall` | Voice provider not allowed for this endpoint (e.g., ElevenLabs). |
| `220` | `DP` | Duplicate `ctid` for the customer (when `cdcs_uni_ctid=1`). |
| `230` | `block ddd time` | Regional or holiday block hit. |
| `244` | `http duplicity` | Duplicate within `httpdup` window. |
| `250` | `<MakeCall status>` | Underlying `MakeCall.php` failed; `errodet` carries the raw response. |
| `260` | `error audio file` | Audio queue insertion failed. |
| `290` | `Inform agent ID` / `Agent is not valid` | `type=100` requires `dtmfini=<ccba_id>` valid for the account. |
| `301` | `Sms no action` | SMS follow-up requested without `sms_action`. |
| `302` | `Sms no text` | SMS follow-up requested without `sms_text`. |
| `304` | `Invalid sms_action` | `sms_action` is not in `[ok, nae, oknae, dtmf1]`. |
| `305` | `Sms text 160 characters` | `sms_text` longer than 160 characters. |

## Notes

- The `cd_id` returned has the form `<cdcs_db>_<numericId>`. Pass it as-is to [`GetCallStatus`](GetCallStatus.md).
- Audio files referenced by `content*` must already exist (`cd_wav`). They auto-renew their expiration when used; assets unused for 180 days may be purged from storage.
- For dynamic TTS, set `priority=-20` to generate audio synchronously before dialing — useful when the call must go out immediately.
- ElevenLabs voices are blocked at this endpoint due to provider TOS. Use Google or Polly voices for `MakeTTSCall`.
