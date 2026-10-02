# make_tts_call

*Place an outbound call with TTS or pre-recorded audio.*

| | |
| --- | --- |
| **Permission** | `telephony` |
| **REST equivalent** | [MakeTTSCall](../../api/v2/voice/MakeTTSCall.md) |

Places an outbound phone call using synthesized speech (`text`) or a pre-recorded audio ID (`content`). At least one of `text` or `content` is required.

## Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `dest` | string | Yes | Destination with DDD, digits only |
| `text` | string | Conditional | TTS text — required if `content` is empty |
| `content` | string | Conditional | Audio/voice ID from [get_tts_voices](get_tts_voices.md). Must be an audio of your own account (or a shared Velip/corporate-group audio); otherwise the call is refused with `205 Content not found` |
| `ctid` | string | No | External idempotency key |

The caller ID comes from the account configuration and cannot be chosen through MCP.

## Example

```bash
curl -X POST 'https://vox20.velip.com.br/mcpserver/velip' \
  -H 'Authorization: Bearer YOUR_TOKEN_30_CHARS' \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "make_tts_call",
      "arguments": {
        "dest": "11999999999",
        "text": "Olá, esta é uma ligação de teste da Velip."
      }
    }
  }'
```

## Responses

**Success:**

```json
{
  "success": true,
  "status": "OK",
  "cd_id": "42_123456",
  "message": "Call placed"
}
```

Use [get_call_status](get_call_status.md) to track the call outcome.
