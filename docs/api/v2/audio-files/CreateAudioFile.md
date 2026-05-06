# Create audio file

*Generate a TTS audio asset or upload an existing audio file.*


**Endpoint:** `POST https://<base>/api/v2/CreateAudioFile.php`

Creates an audio asset in `cd_wav` so it can be referenced by `content*` parameters in [`MakeTTSCall`](../voice/MakeTTSCall.md) and other voice routines. Three input modes:

- **TTS** — pass `text` (and optionally `voice`). The Velip TTS server generates the WAV/MP3 from the text.
- **File upload** — send `multipart/form-data` with a file field named `audio` (or any other name; the first non-empty file is used).
- **Base64** — pass `audio64` (with or without `data:audio/...;base64,` prefix). Useful when you cannot send multipart bodies.

You can also pass raw bytes in the request body (`Content-Type: audio/...`) when you cannot do multipart or base64.

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Request

#### `tsid` — type: *string* — **required**

Token for the account.


#### `text` — type: *string*

Text to synthesize. Required for TTS mode (mutually exclusive with file uploads / base64).


#### `voice` — type: *string*

Voice id `provider|VoiceName` (see [`GetTTSVoices`](../voice/GetTTSVoices.md)). Defaults to `fad` when only `text` is provided.


#### `encoding` — type: *string*

Encoding of `text`: `UTF-8`, `2UTF-8`, `ASCII`. Default is `ISO-8859-1` for form requests, `UTF-8` for JSON.


#### `rate` — type: *integer*

TTS speech rate, range `-6` to `6`.


#### `audio64` — type: *string*

Base64-encoded audio. Accepts `data:audio/<type>;base64,<...>` data-URIs and url-safe base64. Auto-detects the file extension via `finfo`.


#### `audio` — type: *file*

Multipart file field. The endpoint also accepts any other field name and uses the first valid file.


#### `name` — type: *string*

Friendly name for the asset (`cd_wav.cdw_name`).


#### `name_up` — type: *string*

Filename to use when storing the upload. Auto-detected from the data-URI / mime type when omitted. Alias `nome_up` is accepted.


#### `type` — type: *string*

Asset type: `tts`, `upload`, `rec`, or `ttsvar` (TTS template with placeholders). Inferred from the input mode when omitted.


#### `cdg_id` — type: *integer*

Optional asset group id (`cd_wav_group.cdg_id`).


#### `speed` — type: *number* — default: `1`

Speed factor for uploads. `1` = no change, `<1` = slower, `>1` = faster.


#### `delsilence` — type: *integer*

Silence trimming for uploads: `1` strips initial silence, `2` strips trailing silence, `3` strips both.


#### `incsilence` — type: *integer*

Number of milliseconds of silence to insert at the beginning of an upload.


#### `mp3` — type: *string*

Pass `no` to skip MP3 generation (the WAV is always generated). Default produces both.


#### `ttswrt` — type: *string*

Pass `1` to mark the asset as permanent (does not expire after one day). Otherwise the asset expires after one day if it is TTS-generated.


#### `expires` — type: *string*

Override the expiration date (`YYYY-MM-DD`). Default: tomorrow for TTS without `ttswrt=1`; +5 years otherwise.


#### `dis` — type: *string*

Pass `NO` to hide the asset from the audio list dashboard.


## Request example
```bash curl (TTS)
curl -X POST 'https://<base>/api/v2/CreateAudioFile.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "text": "Hello, this is a test message.",
    "voice": "google|pt-BR-Wavenet-A",
    "name": "test message",
    "ttswrt": "1",
    "encoding": "UTF-8"
  }'
```

```bash curl (file upload)
curl -X POST 'https://<base>/api/v2/CreateAudioFile.php' \
  -F 'tsid=YOUR_TSID' \
  -F 'audio=@/path/to/voice.mp3' \
  -F 'name=Welcome message' \
  -F 'ttswrt=1'
```

```bash curl (base64)
curl -X POST 'https://<base>/api/v2/CreateAudioFile.php' \
  -H 'Content-Type: application/json' \
  -d '{
    "tsid": "YOUR_TSID",
    "audio64": "data:audio/mp3;base64,SUQzBAAAAAAAA...",
    "name_up": "voicemail.mp3",
    "name": "Voicemail",
    "ttswrt": "1"
  }'
```
## Response
```json 200 OK
{
  "return": {
    "status": "OK",
    "status_code": "0",
    "cdw_file": "tf12345",
    "cdw_file_test": "",
    "cdw_name": "test message",
    "cdw_sec ": "5",
    "cdw_expires ": "2031-05-06",
    "cdw_type ": "tts"
  }
}
```
- **`return.cdw_file`** (*string*) — Audio id (e.g., `tf12345`). Pass the numeric portion (without `tf`) as `content`/`content1`/... in [`MakeTTSCall`](../voice/MakeTTSCall.md).


- **`return.cdw_file_test`** (*string*) — Test/preview id when the asset was generated provisionally (legacy). Empty for normal flows.


- **`return.cdw_sec`** (*string*) — Duration of the generated audio in seconds.


- **`return.cdw_expires`** (*string*) — Expiration date of the asset. After this date the asset is purged unless renewed by being used in a call.


## Error codes

| Code | `status` | Cause |
| --- | --- | --- |
| `205` | `not allowed executable file` / `Virus infected file` | The uploaded file is rejected (executable / ClamAV positive). |
| `220` | `no audio or text` | None of `text`, file upload, `audio64`, nor raw body provided. |
| `221` | `upload error code=N` | PHP `UPLOAD_ERR_*` — usually `2` (`MAX_FILE_SIZE`) or `7` (cannot write to disk). |
| `222` | `no name_up` | File uploaded without a filename and `name_up` was not provided. |
| `223` | `size up=N` | Upload smaller than 100 bytes. |
| `224` | `invalid base64 in audio64` | The `audio64` payload could not be decoded. |
| `226` | `multipart discarded …` | Multipart body was discarded by PHP — usually `post_max_size` / `upload_max_filesize` exceeded. |
| `281` | `Error creat audio` | The TTS server returned a non-OK response. |

> **Note**
> Files uploaded via this endpoint are scanned with ClamAV before being persisted. Disable scanning is not supported.
