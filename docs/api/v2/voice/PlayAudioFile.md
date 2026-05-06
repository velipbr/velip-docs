# Stream audio file

*Download or stream a stored TTS audio or call recording.*


**Endpoint:** `POST https://<base>/api/v2/PlayAudioFile.php`

Streams the binary content of an audio asset over HTTP. Two modes:

- **TTS / uploaded audio** — pass `cdw_id` (or legacy `cdw_file`) to retrieve a file from `cd_wav`.
- **Call recording** — pass `recid` (the `cd_id` of a call) to retrieve the recording from `cd_rec` (Google Cloud Storage or local disk, depending on `cdr_storage`).

The endpoint supports HTTP `Range` requests for partial downloads (used by browsers for seekable audio playback).

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Request

#### `tsid` — type: *string* — **required**

Token for the account.


#### `cdw_id` — type: *integer*

ID of the audio asset (`cd_wav.cdw_id`). Aliases: `cdw_file` (numeric portion of the file name) and `cdw_file_test`.


#### `recid` — type: *integer*

Call id whose recording you want (`cd_rec.cdr_cd_id`). When provided, `cdw_id` is ignored.


#### `noheader` — type: *string*

Pass `yes` to skip HTTP audio headers (useful when proxying from another backend that adds its own headers).


## Request example
```bash curl (TTS asset)
curl -X POST 'https://<base>/api/v2/PlayAudioFile.php' \
  -d 'tsid=YOUR_TSID&cdw_id=12345' \
  --output audio.mp3
```

```bash curl (recording)
curl -X POST 'https://<base>/api/v2/PlayAudioFile.php' \
  -d 'tsid=YOUR_TSID&recid=9876545' \
  --output recording.mp3
```

```html HTML5 audio
<audio controls
       src="https://<base>/api/v2/PlayAudioFile.php?tsid=YOUR_TSID&cdw_id=12345">
</audio>
```
## Response

On success, the response body is the audio binary (typically `audio/mpeg`). Headers depend on whether `Range` was sent:

| Header | Description |
| --- | --- |
| `Content-Type` | `audio/mpeg` for MP3, `audio/x-wav` for WAV. |
| `Content-Length` | Number of bytes in the (range) response. |
| `Accept-Ranges: bytes` | Range requests supported. |
| `Content-Range` | Sent on `206 Partial Content` responses. |
| `Content-Disposition` | `inline; filename="<file>.mp3"`. |

On failure, the response is JSON with the standard `return` envelope.

## Error codes

| Code | `status` | Cause |
| --- | --- | --- |
| `220` | `No audio ID` | None of `cdw_id`, `cdw_file`, `cdw_file_test`, or `recid` provided. |
| `230` | `Audio id is not valid` | The asset does not belong to the customer. |
| `240` | `Audio out of date` | The asset was deleted (`cdw_del_date` set). |
| `250` | `No audio file` | Recording row exists but the file content is unavailable. |
| `260` | `Fail get audio` | The upstream TTS server returned an error or the file fetch failed (incl. SSRF protections refusing the URL). |

## Notes

- Recordings stored on Google Cloud Storage are fetched via the GCS SDK using the bucket configured per recording (`cdr_bucket`). Local-storage recordings are fetched over HTTP from the per-environment `ip_tts_server` parameter.
- The endpoint applies SSRF protection: only `http`/`https` schemes are allowed, hosts must match `[a-z0-9._-]`, and well-known internal hosts (GCE metadata, loopback, `169.254.0.0/16`) are blocked.
- The maximum download size is `50 MB`. Uploads larger than that are aborted mid-stream.
