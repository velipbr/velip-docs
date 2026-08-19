---
layout: default
title: Velip Developers
---

# Welcome to Velip

*Multichannel communications and AI agents for contact centers — voice, SMS, WhatsApp, Messenger, Instagram, and email under a single API.*

Velip is a Brazilian communications platform that powers contact centers, marketing teams, and product apps with a single backend for **voice, SMS, WhatsApp, Messenger, Instagram, and email**, plus AI agents (autonomous and real-time voice) on top of it.

These docs cover what integrators need to connect to the **Velip Public API** and the **Velip MCP server**. Internal product manuals (call center UI, agent design tools) live elsewhere.

## What is here

- **[API v2 index](api/v2/README.md)** — table of contents for every documented endpoint.
- **[MCP server index](mcp/README.md)** — connect AI clients (Cursor, Claude) to Velip tools.
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
| **Auth / utilities** | `GetUserID` | Credential validation and account introspection. |
| **Audio files** | `CreateAudioFile`, `GetAudiosList` | Upload / list audio assets used by voice campaigns. |
| **MCP (AI agents)** | `send_sms`, `make_tts_call`, `send_whatsapp`, … | Same capabilities exposed as MCP tools for Cursor, Claude, and custom agents. See [MCP overview](mcp/overview.md). |

> **Note**
> All REST endpoints are POST-by-default and accept `application/json` or `application/x-www-form-urlencoded`. URL parameters override JSON body keys.

## Conventions used in these docs

- Sample base URL: `https://<base>` — replace with the host provided to your account (typically `https://vox.velip.com.br`).
- MCP endpoint: `https://vox20.velip.com.br/mcpserver/velip`
- Examples use `curl`. Most endpoints work the same with any HTTP client.
- Token placeholder: `YOUR_TSID` (REST) or `YOUR_TOKEN_30_CHARS` (MCP Bearer). Get one via [Authentication](api/v2/authentication.md) or your account administrator.
- Parameters marked **required** must be sent; otherwise the endpoint returns an error code listed under each endpoint page.

Also available as [introduction.md](introduction.md) for direct links from the repository.
