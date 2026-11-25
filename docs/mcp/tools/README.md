# MCP tools reference

All tools require `Authorization: Bearer YOUR_TOKEN_30_CHARS` and the matching [permission channel](../permissions.md).

## SMS

| Tool | Permission | REST equivalent |
| --- | --- | --- |
| [send_sms](send_sms.md) | `sms` | [MakeSMS](../../api/v2/sms/MakeSMS.md) |

## Telephony

| Tool | Permission | REST equivalent |
| --- | --- | --- |
| [make_tts_call](make_tts_call.md) | `telephony` | [MakeTTSCall](../../api/v2/voice/MakeTTSCall.md) |
| [get_tts_voices](get_tts_voices.md) | `telephony` | [GetTTSVoices](../../api/v2/voice/GetTTSVoices.md) |
| [get_call_status](get_call_status.md) | `telephony` | [GetCallStatus](../../api/v2/voice/GetCallStatus.md) |
| [get_campaigns_list](get_campaigns_list.md) | `telephony` | [GetCampaignsList](../../api/v2/campaigns/GetCampaignsList.md) |
| [get_campaign_groups](get_campaign_groups.md) | `telephony` | *(Velip DB — no standalone REST page)* |
| [create_campaign](create_campaign.md) | `telephony` | [CreateCampaign](../../api/v2/campaigns/CreateCampaign.md) |
| [clone_campaign](clone_campaign.md) | `telephony` | [CreateCampaign](../../api/v2/campaigns/CreateCampaign.md) (clone mode) |
| [change_campaign](change_campaign.md) | `telephony` | [ChangeCampaign](../../api/v2/campaigns/ChangeCampaign.md) |

## Destination bases

| Tool | Permission | REST equivalent |
| --- | --- | --- |
| [create_destination_base](create_destination_base.md) | `destinations` | [CreateDestinationBase](../../api/v2/destinations/CreateDestinationBase.md) |
| [get_destination_bases](get_destination_bases.md) | `destinations` | [GetDestinationsList](../../api/v2/destinations/GetDestinationsList.md) |

## WhatsApp

| Tool | Permission | REST equivalent |
| --- | --- | --- |
| [send_whatsapp](send_whatsapp.md) | `whatsapp` | [MakeWhatsapp](../../api/v2/whatsapp/MakeWhatsapp.md) |
| [get_wa_templates](get_wa_templates.md) | `whatsapp` | [GetWATemplates](../../api/v2/whatsapp/GetWATemplates.md) |
| [get_wa_lines](get_wa_lines.md) | `whatsapp` | *(Velip DB — no standalone REST page)* |

## E-mail (Gmail and Microsoft 365)

| Tool | Permission | REST equivalent |
| --- | --- | --- |
| [send_email](send_email.md) | `gmail` | [SendEmailOAuth](../../api/v2/email/SendEmailOAuth.md) |
| [list_email_templates](list_email_templates.md) | `gmail` | *(none — templates are managed in the Velip portal)* |
| [send_gmail_oauth](send_gmail_oauth.md) | `gmail` | [SendGmailOAuth](../../api/v2/email/SendGmailOAuth.md) |

## Message status and reports

| Tool | Permission | REST equivalent |
| --- | --- | --- |
| [get_message_status](get_message_status.md) | the channel asked: `sms`, `whatsapp` or `gmail` | [GetMessageStatus](../../api/v2/messages/GetMessageStatus.md) |
| [get_message_campaigns](get_message_campaigns.md) | the channel asked: `sms`, `whatsapp` or `gmail` | [GetMessageCampaignsList](../../api/v2/messages/GetMessageCampaignsList.md) |
| [get_channel_summary](get_channel_summary.md) | any of `sms`, `whatsapp`, `gmail`, `telephony` | [GetChannelSummary](../../api/v2/messages/GetChannelSummary.md) |

## Calling a tool

```bash
curl -X POST 'https://vox20.velip.com.br/mcpserver/velip' \
  -H 'Authorization: Bearer YOUR_TOKEN_30_CHARS' \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "TOOL_NAME",
      "arguments": { }
    }
  }'
```

See [curl client guide](../clients/curl.md) for more examples.
