# Welcome to Velip

*Multichannel communications and AI agents for contact centers — voice, SMS, WhatsApp, Messenger, Instagram, and email under a single API.*

Velip is a Brazilian communications platform that powers contact centers, marketing teams, and product apps with a single backend for **voice, SMS, WhatsApp, Messenger, Instagram, and email**, plus AI agents (autonomous and real-time voice) on top of it.

These docs cover what consumers of the **Velip Public API** need to integrate. Internal product manuals (call center UI, agent design tools) live elsewhere.

## What is here

- **[API v2 index](api/v2/README.md)** — table of contents for every documented endpoint.
- **[API v2 overview](api/v2/overview.md)** — conventions and response shape.
- **[Authentication](api/v2/authentication.md)** — `tsid` token, IP allowlists, brute-force policies.
- **[Rate limits](api/v2/rate-limits.md)** — per-IP, per-user, and channel limits.
- **[Error codes](api/v2/errors.md)** — numeric `status_code` reference.

## Channels at a glance

| Channel | Endpoints | Notes |
| --- | --- | --- |
| **Voice (TTS / call)** | `MakeTTSCall`, `GetCallStatus`, `GetTTSVoices`, `PlayAudioFile`, `GetWebRTC` | Outbound TTS with DTMF/IVR, transfer to PA, recording, WebRTC. |
| **SMS** | `MakeSMS` | 160-char limit (auto-cut available); per-customer providers (Matrix, Wavy/Tww, Flash). |
| **WhatsApp** | `MakeWhatsapp`, `ValidateWhatsAppNumber`, `CreateWhatsappTemplate`, `GetWATemplates`, `DeleteWhatsappTemplate`, `CheckTemplateStatus` | HSM/templates, text/audio/image/file/video, Gupshup or Meta Cloud API providers. |
| **Messenger / Instagram** | `MakeMessenger`, `MakeInstagram` | Meta channels via business accounts. |
| **Email** | `SendGmailOAuth` | Gmail OAuth-backed sender. |
| **Campaigns / queues** | `CreateCampaign`, `ChangeCampaign`, `GetCampaignsList`, `CreateCenterQueue`, `GetCenterQueues` | Campaign lifecycle and contact-center queue management. |
| **Destinations** | `CreateDestinationBase`, `GetDestinationsList` | Manage destination lists used by campaigns. |
| **Auth / utilities** | `GetUserID` | Token issuance and account introspection. |
| **Audio files** | `CreateAudioFile`, `GetAudiosList` | Upload / list audio assets used by voice campaigns. |

> **Note**
> All endpoints are POST-by-default and accept `application/json` or `application/x-www-form-urlencoded`. URL parameters override JSON body keys.


## Conventions used in these docs

- Sample base URL: `https://<base>` — replace with the host provided to your account (typically `https://vox.velip.com.br`).
- Examples use `curl`. Most endpoints work the same with any HTTP client.
- Token placeholder: `YOUR_TSID`. Get one via [Authentication](api/v2/authentication.md).
- Parameters marked **required** must be sent; otherwise the endpoint returns an error code listed under each endpoint page.
