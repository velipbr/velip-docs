# API v2 overview

*Endpoint catalogue and conventions for the Velip Public API v2.*

The Velip Public API v2 is a REST-style HTTP API. Each endpoint is a single PHP route mounted under the base URL provided to your account (typically `https://vox.velip.com.br/api/v2/`).

## Conventions

- **Method**: POST is the canonical method. Most endpoints also accept GET (parameters in the query string), but POST is required for payloads larger than typical URL limits.
- **Content type**:
  - `application/x-www-form-urlencoded` (default).
  - `application/json` — auto-detected from the `Content-Type` header. URL/query parameters take precedence over JSON body keys with the same name.
- **Encoding**: legacy endpoints return `ISO-8859-1` for some fields; newer ones use UTF-8. When sending text from a UTF-8 client, prefer JSON or set the `encoding` parameter (where supported) to `UTF-8`.
- **Authentication**: every call requires a `tsid` token (or HTTP Basic). See [Authentication](authentication.md).
- **Response shape** — JSON, with the canonical body:

```json
{
  "return": {
    "status": "OK",
    "status_code": "0",
    "cd_id": "..."
  }
}
```

When validation or auth fails, `status` carries the error message and `status_code` carries the numeric code documented in [Error codes](errors.md). HTTP status codes used:

| HTTP | Meaning |
| --- | --- |
| `200` | Success (`status: "OK"`). |
| `400` | Validation / business error. `status_code` carries the precise code. |
| `401` | Authentication failure (token, IP allowlist, or brute-force lockout). |

## Endpoint catalogue

- **[SMS](sms/MakeSMS.md)** — Send a single SMS message.
- **[WhatsApp](whatsapp/MakeWhatsapp.md)** — Send WhatsApp text, media, or HSM/templates.
- **[Voice (TTS)](voice/MakeTTSCall.md)** — Place an outbound call with TTS, DTMF/IVR, and optional transfer.
- **[Audio files](audio-files/GetAudiosList.md)** — Manage and play recorded audio assets.
- **[Campaigns](campaigns/CreateCampaign.md)** — Create, edit, and list campaigns and contact-center queues.
- **[Destinations](destinations/CreateDestinationBase.md)** — Manage destination lists used by campaigns.
- **[Messenger / Instagram](messenger/MakeMessenger.md)** — Send messages on Meta channels.
- **[Email (Gmail OAuth)](email/SendGmailOAuth.md)** — Send transactional email through customer-owned Gmail accounts.
- **[Auth helpers](auth-token/GetUserID.md)** — Issue tokens and introspect the current account.

## Read this first

1. [Getting started](getting-started.md) — base URL, request shape, encoding gotchas.
2. [Authentication](authentication.md) — how `tsid` is generated and checked.
3. [Errors](errors.md) — the canonical error code table.
4. [Rate limits](rate-limits.md) — per-IP, per-user, and SMS night cap.
