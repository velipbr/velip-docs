# List TTS voices

*Return TTS voices the authenticated account is allowed to use.*


**Endpoint:** `POST https://<base>/api/v2/GetTTSVoices.php`

Returns the list of TTS voices available to the authenticated customer. The list is filtered by the `cdwv_aut_cdcs_id` column on `cd_wav_voices` — voices flagged for `0` (universal) or for this specific `cdcs_id` are returned.

Pass `cdwv_short` as it comes (for example `Google|pt-BR-Wavenet-A`) as the `voice` parameter of [`MakeTTSCall`](MakeTTSCall.md), [`CreateCampaign`](../campaigns/CreateCampaign.md) and [`CreateAudioFile`](../audio-files/CreateAudioFile.md). It already carries the provider: do not add `cdwv_company` in front of it, and do not combine the provider of one voice with the name of another. A `voice` that is not in this list is rejected with code `209`.

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
      "cdwv_id": 52,
      "cdwv_name": "Rosana N",
      "cdwv_tit": "Português BR - TTS (G)",
      "cdwv_short": "Google|pt-BR-Wavenet-A",
      "cdwv_type": "tts",
      "cdwv_language": "pt-BR",
      "cdwv_genre": "female",
      "cdwv_company": "Google",
      "cdwv_sample": "tf708861868"
    }
  ]
}
```
- **`voices[].cdwv_short`** (*string*) — Voice id — pass it unchanged as the `voice` parameter in [`MakeTTSCall`](MakeTTSCall.md). Usually `Provider|VoiceName`, but not always: the default voices `fad` and `fel` have no provider, and Polly neural voices carry a third part (`Polly|Camila|neural`). Do not split or rebuild it.


- **`voices[].cdwv_name`** (*string*) — Display name of the voice (e.g. `Rosana N`). Not accepted as `voice`.


- **`voices[].cdwv_sample`** (*string*) — Audio id of a short sample of the voice, useful for previewing.


- **`voices[].cdwv_genre`** (*string*) — Voice gender hint: `female` or `male`.


## Error codes

This endpoint inherits the [global authentication codes](../errors.md). It does not raise endpoint-specific business codes.

> **Note**
> ElevenLabs voices may appear in this list but are blocked by [`MakeTTSCall`](MakeTTSCall.md), [`CreateCampaign`](../campaigns/CreateCampaign.md) and [`CreateAudioFile`](../audio-files/CreateAudioFile.md) — using them returns code `210`.
