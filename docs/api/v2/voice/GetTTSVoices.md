# List TTS voices

*Return TTS voices the authenticated account is allowed to use.*


**Endpoint:** `POST https://<base>/api/v2/GetTTSVoices.php`

Returns the list of TTS voices available to the authenticated customer. The list is filtered by the `cdwv_aut_cdcs_id` column on `cd_wav_voices` — voices flagged for `0` (universal) or for this specific `cdcs_id` are returned.

Use the `cdwv_company` + `cdwv_short` (or `cdwv_name`) values to compose the `voice` parameter for [`MakeTTSCall`](MakeTTSCall.md) and [`CreateAudioFile`](../audio-files/CreateAudioFile.md).

## Authentication

Token authentication required. See [Authentication](../authentication.md).

## Request

#### `tsid` — type: *string* — **required**

Token for the account.


This endpoint takes no other parameters.

## Request example
```bash curl
curl -X POST 'https://<base>/api/v2/GetTTSVoices.php' \
  -H 'Content-Type: application/json' \
  -d '{ "tsid": "YOUR_TSID" }'
```
## Response
```json 200 OK
{
  "return": {
    "status": "OK",
    "status_code": "0"
  },
  "voices": [
    {
      "cdwv_id": 12,
      "cdwv_name": "google|pt-BR-Wavenet-A",
      "cdwv_tit": "Camila",
      "cdwv_short": "pt-BR-Wavenet-A",
      "cdwv_type": "tts",
      "cdwv_language": "pt-BR",
      "cdwv_genre": "F",
      "cdwv_company": "google",
      "cdwv_sample": "https://..."
    }
  ]
}
```
- **`voices[].cdwv_name`** (*string*) — Voice id in the format `provider|VoiceName` — pass it directly as the `voice` parameter in [`MakeTTSCall`](MakeTTSCall.md).


- **`voices[].cdwv_sample`** (*string*) — URL to a short MP3 sample of the voice, useful for previewing.


- **`voices[].cdwv_genre`** (*string*) — Voice gender hint: `F` (female), `M` (male).


## Error codes

This endpoint inherits the [global authentication codes](../errors.md). It does not raise endpoint-specific business codes.

> **Note**
> ElevenLabs voices may appear in this list (they are valid for [`CreateAudioFile`](../audio-files/CreateAudioFile.md)) but are blocked by [`MakeTTSCall`](MakeTTSCall.md) — using them in `MakeTTSCall` returns code `210`.
