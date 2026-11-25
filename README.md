# Velip Developers

Public documentation of the **Velip** platform: voice calls, SMS, WhatsApp, Messenger, Instagram and e-mail through one REST API (v2) and one MCP server for AI agents.

**Read online:** [developers.velip.com.br](https://developers.velip.com.br) · **For AI agents:** [`llms.txt`](https://developers.velip.com.br/llms.txt) (index of every page, with links to the raw Markdown)

## Start here

| You are | Start with |
| --- | --- |
| A developer integrating a system | [Getting started](docs/api/v2/getting-started.md), then the page of the task below. |
| An AI agent writing an integration | This page: the essentials, then the page of the task below. With only a URL, read [`llms.txt`](https://developers.velip.com.br/llms.txt). |
| Someone who wants an AI agent to build it | [Build your integration with an AI agent](docs/ai-integration/README.md): ready prompts. |
| Using Claude, Cursor or another MCP client | [MCP server](docs/mcp/README.md): the same capabilities as tools. |

## Essentials for every request

- **URL:** `https://<base>/api/v2/<Endpoint>.php`, where `<base>` is the host of your account (usually `vox.velip.com.br`).
- **Token:** a 30-character API token created in the Velip portal (integrations screen), sent as `Authorization: Bearer <token>` or as the `tsid` parameter. Keep it in your backend, never in the browser. See [Authentication](docs/api/v2/authentication.md).
- **Request:** `POST`, in JSON or form encoding. URL parameters override JSON body keys with the same name.
- **Response:** JSON. `return.status` is `"OK"` or the error message, and `return.status_code` is `"0"` or the numeric error code. Each endpoint page says where the data come (inside `return` or in a sibling key).
- **HTTP:** `200` success, `400` validation, `401` authentication. Some endpoints also use `403`, `404`, `409`, `422`, `429` and `5xx`; their pages list when. See [Error codes](docs/api/v2/errors.md) and [Rate limits](docs/api/v2/rate-limits.md).

```bash
curl -X POST 'https://vox.velip.com.br/api/v2/MakeSMS.php' \
  -H 'Authorization: Bearer YOUR_TSID' \
  -H 'Content-Type: application/json' \
  -d '{ "dest": "5511999999999", "message": "Hello from Velip" }'
```

## I want to…

| Task | Read |
| --- | --- |
| Send an SMS | [MakeSMS](docs/api/v2/sms/MakeSMS.md) |
| Send a WhatsApp message (a template outside the 24-hour window) | [MakeWhatsapp](docs/api/v2/whatsapp/MakeWhatsapp.md), [GetWATemplates](docs/api/v2/whatsapp/GetWATemplates.md) |
| Manage WhatsApp templates or check a number | [CreateWhatsappTemplate](docs/api/v2/whatsapp/CreateWhatsappTemplate.md), [CheckTemplateStatus](docs/api/v2/whatsapp/CheckTemplateStatus.md), [DeleteWhatsappTemplate](docs/api/v2/whatsapp/DeleteWhatsappTemplate.md), [ValidateWhatsAppNumber](docs/api/v2/whatsapp/ValidateWhatsAppNumber.md) |
| Place a voice call with text-to-speech or recorded audio | [MakeTTSCall](docs/api/v2/voice/MakeTTSCall.md), [GetTTSVoices](docs/api/v2/voice/GetTTSVoices.md) |
| Get the result of a call | `rurl` in [MakeTTSCall](docs/api/v2/voice/MakeTTSCall.md) (webhook), or [GetCallStatus](docs/api/v2/voice/GetCallStatus.md) |
| Upload, list or play audio files | [CreateAudioFile](docs/api/v2/audio-files/CreateAudioFile.md), [GetAudiosList](docs/api/v2/audio-files/GetAudiosList.md), [PlayAudioFile](docs/api/v2/voice/PlayAudioFile.md) |
| Make calls from my own agent screen (browser softphone) | [WebRTC softphone guide](docs/api/v2/voice/webrtc-softphone.md), [GetWebRTC](docs/api/v2/voice/GetWebRTC.md) |
| Reach many contacts at once (campaign) | [CreateDestinationBase](docs/api/v2/destinations/CreateDestinationBase.md), [CreateCampaign](docs/api/v2/campaigns/CreateCampaign.md), [GetCampaignsList](docs/api/v2/campaigns/GetCampaignsList.md), [ChangeCampaign](docs/api/v2/campaigns/ChangeCampaign.md), [GetDestinationsList](docs/api/v2/destinations/GetDestinationsList.md) |
| Manage contact-center queues | [CreateCenterQueue](docs/api/v2/campaigns/CreateCenterQueue.md), [GetCenterQueues](docs/api/v2/campaigns/GetCenterQueues.md) |
| Send on Messenger or Instagram | [MakeMessenger](docs/api/v2/messenger/MakeMessenger.md), [MakeInstagram](docs/api/v2/instagram/MakeInstagram.md) |
| Check what happened to an SMS, WhatsApp or e-mail I sent | [GetMessageStatus](docs/api/v2/messages/GetMessageStatus.md) |
| List my SMS, WhatsApp and e-mail campaigns and their results | [GetMessageCampaignsList](docs/api/v2/messages/GetMessageCampaignsList.md) |
| See totals per channel for a period (dashboard, report) | [GetChannelSummary](docs/api/v2/messages/GetChannelSummary.md) |
| Send e-mail from a Gmail or Microsoft 365 account (template, attachments) | [SendEmailOAuth](docs/api/v2/email/SendEmailOAuth.md) |
| Send e-mail from a Gmail account (older, Gmail only) | [SendGmailOAuth](docs/api/v2/email/SendGmailOAuth.md) |
| Buy credit with PIX | [CreatePixCharge](docs/api/v2/credit/CreatePixCharge.md) |
| Check a payment or the balance | [GetChargeStatus](docs/api/v2/credit/GetChargeStatus.md) |
| Check that the token works | [GetUserID](docs/api/v2/auth-token/GetUserID.md) |
| Use Velip from Claude, Cursor or another AI client | [MCP server](docs/mcp/README.md) |

Every endpoint, by area: [API v2 index](docs/api/v2/README.md).

## Out of scope

- SDKs and client libraries: not maintained here.
- Internal architecture and runbooks: private repositories.

Editing these docs: [CONTRIBUTING.md](CONTRIBUTING.md).

## Contact

Support: `support@velip.com` · Sales: `sales@velip.com`
