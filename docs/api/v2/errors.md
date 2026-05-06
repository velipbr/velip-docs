# Error codes

*Numeric codes returned in the response status_code field.*

The Velip Public API v2 returns a numeric `status_code` in the JSON body and an HTTP status code that signals the broad category. Use the table below to interpret them.

## Response shape

Every error response carries:

```json
{
  "return": {
    "status": "<short message>",
    "status_code": "<numeric code>",
    "cd_id": "0"
  }
}
```

Successful responses use `status: "OK"` and `status_code: "0"`.

## HTTP status mapping

| HTTP | When |
| --- | --- |
| `200` | Operation succeeded. |
| `400` | Business or validation error. The numeric `status_code` is the source of truth. |
| `401` | Authentication / authorization error (codes `100`–`199`). |

## Authentication and access control (1xx)

| Code | `status` | Cause |
| --- | --- | --- |
| `100` | `fail authentication` | Authentication routine did not return a usable account context. Check `tsid`, `sid`, or HTTP Basic. |
| `102` | `SID not found` | The `sid`/`tsid` is unknown or has expired. Excessive `102`s trigger the anti-probe blacklist. |
| `110` | `account inactive` | The customer account is disabled. |
| `123` | `permission denied` | The token has insufficient permissions for this endpoint. |
| `130` | `no user/pass` | Required `username`/`password` not sent on a Basic-only flow. |
| `131` | `IP trials exceeded` | More than 20 attempts in 10 minutes from this IP — temporary block. |
| `132` | `user trials exceeded` | More than 5 attempts in 10 minutes for this user — temporary block. |
| `140` | `invalid user/pass` | Incorrect credentials. |
| `142` | `IP not allowed` | IP is not on the customer allowlist (`cd_ip`). |
| `198` | `tokens blockeds` | The customer flag `cdcs_tokens_blockeds` is set — all tokens are disabled. |
| `199` | `IP blocked` | IP is on the permanent blacklist (`cd_ip_blacklist`). |

## Validation (2xx, 3xx)

These come from individual endpoints. The exact set of codes varies — see each endpoint page for the codes it can produce. The most common ones:

| Code | `status` | Cause |
| --- | --- | --- |
| `201` | `No text` | Voice / TTS call without any text/content provided. |
| `203` | `number invalid` | Destination number could not be normalized. |
| `210` | `TTS provider not permitted` | The selected voice maps to a provider blocked for this operation. |
| `220` | `No sms account` / `Duplicate ctid` | Account not provisioned for the channel, or duplicate `ctid` when uniqueness is enforced. |
| `230` | `No dest` / `block ddd time` | Destination missing, or a regional/holiday block was hit. |
| `231` | `No wa provider` | WhatsApp line lacks an active provider. |
| `232` | `No app name` | WhatsApp line lacks the `v8l_wa_app_name`. |
| `233` | `No key wa` | WhatsApp line lacks the API key. |
| `235` | `No text` / `No from wa number` | Empty SMS text, or WhatsApp line without a sending number. |
| `236` | `No app_id` | WhatsApp call without `app_id` or `v8l_id`. |
| `238` | `Text >160 ch` | SMS text exceeded 160 characters and `cuttext` was not set. |
| `240` | `Mobile is not valid` | Phone number failed the Brazilian mobile-format check (`setbrasil=1`). |
| `244` | `http duplicidade` / `http duplicity` | A request with the same destination was sent within the `httpdup` window. |
| `245` | `night limit` | The customer's nightly SMS cap (22:00–06:00) was reached. |
| `250` | `no credit` / `error sending` | Customer balance insufficient, or the upstream provider returned a hard error. |
| `255` | `no sms tarif` | No SMS tariff configured for the destination. |
| `260` | `number blocked by list` / `error audio file` | Destination is on the customer block list, or audio file insertion failed. |
| `270` | `Blocked text` | SMS content was rejected by the Velip text filter (bank-name impersonation). |
| `290` | `Inform agent ID` / `Agent is not valid` | Required for `type=100` (agent-bound) calls. |
| `300` | `error sms provider` | Upstream SMS provider returned a non-OK response. |
| `301` | `Sms no action` | `MakeTTSCall` requested SMS follow-up without `sms_action`. |
| `302` | `Sms no text` | `MakeTTSCall` requested SMS follow-up without `sms_text`. |
| `304` | `Invalid sms_action` | `sms_action` is not one of `ok`, `nae`, `oknae`, `dtmf1`. |
| `305` | `Sms text 160 characters` | SMS follow-up text longer than 160 characters. |

> **Note**
> Each endpoint page lists only the codes it can return, with the precise message for that path. Use this page as the cross-cutting reference.


## Provider-side codes (`status` field)

Some channel responses pass through the upstream provider's error message in `status` instead of remapping it. Examples:

- WhatsApp Gupshup: `1010`, `submitted`, `enqueued`, etc.
- SMS Wavy/Tww: `OK`, `NA`, `WR`.
- Matrix: HTTP body returned by the provider.

When `status_code` is `0` and `status` is non-OK, the call left Velip but failed downstream. Check the `cdls_id` / `cd_id` returned in the response and consult [`GetCallStatus`](voice/GetCallStatus.md) (for voice) or your delivery report dashboard.
