# get_tts_voices

*List TTS voices and pre-recorded audio IDs for the account.*

| | |
| --- | --- |
| **Permission** | `telephony` |
| **REST equivalent** | [GetTTSVoices](../../api/v2/voice/GetTTSVoices.md) |

No parameters. Returns voices usable as `content` in [make_tts_call](make_tts_call.md) or campaign creation.

## Parameters

None.

## Example

```bash
curl -X POST 'https://vox20.velip.com.br/mcpserver/velip' \
  -H 'Authorization: Bearer YOUR_TOKEN_30_CHARS' \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_tts_voices","arguments":{}}}'
```

## Responses

**Success:**

```json
{
  "success": true,
  "voices": [
    {
      "id": "12345",
      "name": "pt-br-google-f",
      "title": "Portugues BR - TTS (G)",
      "type": "tts",
      "language": "pt-BR",
      "genre": "female",
      "company": "Google"
    }
  ],
  "total": 1
}
```

Use the `id` field as `content` in `make_tts_call`.
