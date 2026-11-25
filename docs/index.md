---
layout: default
title: Velip Developers
---

# Velip Developers

*Voice calls, SMS, WhatsApp, Messenger, Instagram and e-mail through one REST API (v2), and the same capabilities as MCP tools for AI agents.*

Velip is a Brazilian communications platform for contact centers, marketing teams and product apps, with AI agents (autonomous and real-time voice) on top of it. These docs cover what integrators need to connect to the **Velip Public API** and the **Velip MCP server**.

**For AI agents:** [`llms.txt`](https://developers.velip.com.br/llms.txt) is the index of every page, with links to the raw Markdown. The source is on [GitHub](https://github.com/velipbr/velip-docs).

## Start here

| You are | Start with |
| --- | --- |
| A developer integrating a system | [Getting started](api/v2/getting-started.md), then the page of the task below. |
| An AI agent writing an integration | This page: the essentials, then the page of the task below. With only a URL, read [`llms.txt`](https://developers.velip.com.br/llms.txt). |
| Someone who wants an AI agent to build it | [Build your integration with an AI agent](ai-integration/README.md): ready prompts. |
| Using Claude, Cursor or another MCP client | [MCP server](mcp/README.md): the same capabilities as tools, at `https://vox20.velip.com.br/mcpserver/velip`. |

## Essentials for every request

- **URL:** `https://<base>/api/v2/<Endpoint>.php`, where `<base>` is the host of your account (usually `vox.velip.com.br`).
- **Token:** a 30-character API token created in the Velip portal (integrations screen), sent as `Authorization: Bearer <token>` or as the `tsid` parameter. Keep it in your backend, never in the browser. See [Authentication](api/v2/authentication.md).
- **Request:** `POST`, in JSON or form encoding. URL parameters override JSON body keys with the same name.
- **Response:** JSON. `return.status` is `"OK"` or the error message, and `return.status_code` is `"0"` or the numeric error code. Each endpoint page says where the data come (inside `return` or in a sibling key).
- **HTTP:** `200` success, `400` validation, `401` authentication. Some endpoints also use `403`, `404`, `409`, `422`, `429` and `5xx`; their pages list when. See [Error codes](api/v2/errors.md) and [Rate limits](api/v2/rate-limits.md).

```bash
curl -X POST 'https://vox.velip.com.br/api/v2/MakeSMS.php' \
  -H 'Authorization: Bearer YOUR_TSID' \
  -H 'Content-Type: application/json' \
  -d '{ "dest": "5511999999999", "message": "Hello from Velip" }'
```

## I want to…

| Task | Read |
| --- | --- |
| Send an SMS | [MakeSMS](api/v2/sms/MakeSMS.md) |
| Send a WhatsApp message (a template outside the 24-hour window) | [MakeWhatsapp](api/v2/whatsapp/MakeWhatsapp.md), [GetWATemplates](api/v2/whatsapp/GetWATemplates.md) |
| Manage WhatsApp templates or check a number | [CreateWhatsappTemplate](api/v2/whatsapp/CreateWhatsappTemplate.md), [CheckTemplateStatus](api/v2/whatsapp/CheckTemplateStatus.md), [DeleteWhatsappTemplate](api/v2/whatsapp/DeleteWhatsappTemplate.md), [ValidateWhatsAppNumber](api/v2/whatsapp/ValidateWhatsAppNumber.md) |
| Place a voice call with text-to-speech or recorded audio | [MakeTTSCall](api/v2/voice/MakeTTSCall.md), [GetTTSVoices](api/v2/voice/GetTTSVoices.md) |
| Get the result of a call | `rurl` in [MakeTTSCall](api/v2/voice/MakeTTSCall.md) (webhook), or [GetCallStatus](api/v2/voice/GetCallStatus.md) |
| Upload, list or play audio files | [CreateAudioFile](api/v2/audio-files/CreateAudioFile.md), [GetAudiosList](api/v2/audio-files/GetAudiosList.md), [PlayAudioFile](api/v2/voice/PlayAudioFile.md) |
| Make calls from my own agent screen (browser softphone) | [WebRTC softphone guide](api/v2/voice/webrtc-softphone.md), [GetWebRTC](api/v2/voice/GetWebRTC.md) |
| Reach many contacts at once (campaign) | [CreateDestinationBase](api/v2/destinations/CreateDestinationBase.md), [CreateCampaign](api/v2/campaigns/CreateCampaign.md), [GetCampaignsList](api/v2/campaigns/GetCampaignsList.md), [ChangeCampaign](api/v2/campaigns/ChangeCampaign.md), [GetDestinationsList](api/v2/destinations/GetDestinationsList.md) |
| Manage contact-center queues | [CreateCenterQueue](api/v2/campaigns/CreateCenterQueue.md), [GetCenterQueues](api/v2/campaigns/GetCenterQueues.md) |
| Send on Messenger or Instagram | [MakeMessenger](api/v2/messenger/MakeMessenger.md), [MakeInstagram](api/v2/instagram/MakeInstagram.md) |
| Check what happened to an SMS, WhatsApp or e-mail I sent | [GetMessageStatus](api/v2/messages/GetMessageStatus.md) |
| List my SMS, WhatsApp and e-mail campaigns and their results | [GetMessageCampaignsList](api/v2/messages/GetMessageCampaignsList.md) |
| See totals per channel for a period (dashboard, report) | [GetChannelSummary](api/v2/messages/GetChannelSummary.md) |
| Send e-mail from a Gmail or Microsoft 365 account (template, attachments) | [SendEmailOAuth](api/v2/email/SendEmailOAuth.md) |
| Send e-mail from a Gmail account (older, Gmail only) | [SendGmailOAuth](api/v2/email/SendGmailOAuth.md) |
| Buy credit with PIX | [CreatePixCharge](api/v2/credit/CreatePixCharge.md) |
| Check a payment or the balance | [GetChargeStatus](api/v2/credit/GetChargeStatus.md) |
| Check that the token works | [GetUserID](api/v2/auth-token/GetUserID.md) |
| Use Velip from Claude, Cursor or another AI client | [MCP server](mcp/README.md) |

Every endpoint, by area: [API v2 index](api/v2/README.md). Conventions and response shape: [API v2 overview](api/v2/overview.md).
