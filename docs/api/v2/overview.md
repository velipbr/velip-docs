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

The [credit purchase](credit/CreatePixCharge.md) endpoints also use `403`, `404`, `409`, `422`, `429`, `500`, `502` and `503`; each page lists when. The status and report endpoints ([`GetCallStatus`](voice/GetCallStatus.md), [`GetMessageStatus`](messages/GetMessageStatus.md), [`GetMessageCampaignsList`](messages/GetMessageCampaignsList.md), [`GetChannelSummary`](messages/GetChannelSummary.md)) use `429` for their rate limits and `500` for a temporary failure.

## Endpoint catalogue

- **[SMS](sms/MakeSMS.md)** — Send a single SMS message.
- **[WhatsApp](whatsapp/MakeWhatsapp.md)** — Send WhatsApp text, media, or HSM/templates.
- **[Voice (TTS)](voice/MakeTTSCall.md)** — Place an outbound call with TTS, DTMF/IVR, and optional transfer.
- **[Audio files](audio-files/GetAudiosList.md)** — Manage and play recorded audio assets.
- **[Campaigns](campaigns/CreateCampaign.md)** — Create, edit, and list campaigns and contact-center queues.
- **[Destinations](destinations/CreateDestinationBase.md)** — Manage destination lists used by campaigns.
- **[Messenger / Instagram](messenger/MakeMessenger.md)** — Send messages on Meta channels.
- **[Email (OAuth)](email/SendEmailOAuth.md)** — Send transactional email through customer-owned Gmail or Microsoft 365 mailboxes, with templates and attachments.
- **[Message status and reports](messages/GetMessageStatus.md)** — Status of SMS, WhatsApp and e-mail sends, bulk message campaigns, and totals per channel.
- **[Credit purchase](credit/CreatePixCharge.md)** — Buy credit with PIX and check the charge status and the balance.
- **[Auth helpers](auth-token/GetUserID.md)** — Validate credentials and introspect the current account.

## Read this first

1. [Getting started](getting-started.md) — base URL, request shape, encoding gotchas.
2. [Authentication](authentication.md) — how `tsid` is generated and checked.
3. [Errors](errors.md) — the canonical error code table.
4. [Rate limits](rate-limits.md) — per-IP, per-user, and SMS night cap.
