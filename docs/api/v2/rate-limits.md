# Rate limits

*Per-IP, per-user, and per-channel quotas enforced by the API.*

The Velip API enforces several layers of throttling. They are independent — a request may be rejected for hitting any of them.

## 1. Anti brute-force (authentication)

Counted on **failed** attempts only. See [Authentication](authentication.md) for the full table.

| Counter | Window | Result |
| --- | --- | --- |
| 20 failed attempts per IP | 10 minutes | Code `131` until the window passes. |
| 5 failed attempts per user | 10 minutes | Code `132` for that user. |
| 100 failed attempts per IP | 60 minutes | **Permanent** IP blacklist (code `199`). |
| 50 failed credential attempts per IP | 60 minutes | **Permanent** IP blacklist (code `199`). |
| 15 unknown-SID errors (`102`) per IP | 10 minutes | **Permanent** IP blacklist (anti-probe, code `199`). |

## 2. HTTP duplicate suppression

Per-endpoint, opt-in. Most send endpoints accept `httpdup` (seconds, 1–600) and reject a second request to the same destination within the window.

```bash
# Reject duplicates within 60 s
curl -X POST 'https://<base>/api/v2/MakeSMS.php' \
  -d 'tsid=YOUR_TSID' -d 'dest=5511999999999' \
  -d 'message=Hi' -d 'httpdup=60'
```

Pass `httpdup=0` to disable. The default behaviour without `httpdup` is **a 10-second** dedup window in most send endpoints, applied automatically.

When triggered, the API returns code `244` (`http duplicidade` / `http duplicity`).

## 3. Channel quotas

Some channels enforce additional caps independent of authentication and dedup.

### SMS night limit (Brazil)

Between **22:00 and 06:00 (server time)**, every customer has a configurable night cap on outbound SMS (`cdcs_sms_nightlimit`, default **300**). When the cap is hit, the API returns code `245` (`night limit`) and rejects further sends for the night.

The cap counts only successful sends originated by `MakeSMS` for the customer.

### Customer balance

Send endpoints check `cdcs_saldo > cdcs_saldo_limite` before issuing the message and return code `250` (`no credit`) when balance is insufficient. Resellers' children also need their parent's balance to clear the same check.

### Block lists

Each customer maintains a destination block list (`cd_bloqueados_cli`). Sends to a blocked destination return code `260` (`number blocked by list`).

### Per-call regional / holiday block

Voice and SMS endpoints can apply a regional time block (DDD-level) when the customer enables it (`bkddd=1` or `bkddd=2`). Sends outside the configured window return code `230` (`block ddd time`). With `bkddd=2`, the message is queued silently rather than rejected outright.

## 4. Credit purchase

| Endpoint | Limit | Result |
| --- | --- | --- |
| [`CreatePixCharge`](credit/CreatePixCharge.md) | 10 unpaid charges per account created in the last hour (API and portal) | HTTP 429, code `240`. |
| [`CreatePixCharge`](credit/CreatePixCharge.md) | 12 attempts in 6 minutes and 120 per hour per user; 1,000 per account per day. Refused attempts count too | HTTP 429, code `241`. |
| [`CreatePixCharge`](credit/CreatePixCharge.md) | One charge being created at a time per account (waits up to 10 s) | HTTP 429, code `242`, with `Retry-After`. |
| [`GetChargeStatus`](credit/GetChargeStatus.md) | 60 requests per hour per account, balance-only requests included | HTTP 429, code `210`, with `Retry-After`. |

## 5. Status and report queries

| Endpoint | Limit | Result |
| --- | --- | --- |
| [`GetCallStatus`](voice/GetCallStatus.md) | 200 list requests per account per hour; single lookups capped per day in proportion to the call volume | HTTP 429, code `429`, with `Retry-After`. |
| [`GetMessageStatus`](messages/GetMessageStatus.md) | 200 list requests per account per hour; 5,000 single lookups (`id`, `message_id`, `ctid` of one message) per account per day | HTTP 429, code `429`, with `Retry-After`. |
| [`GetMessageCampaignsList`](messages/GetMessageCampaignsList.md) | 200 requests per account per hour | HTTP 429, code `429`, with `Retry-After`. |
| [`GetChannelSummary`](messages/GetChannelSummary.md) | 200 requests per account per hour | HTTP 429, code `429`, with `Retry-After`. |

Requests refused by validation (codes `460`–`466`) do not count. Prefer one list by campaign or period over polling each message or call.

## Recommendations

- For high-volume integrations, batch sends through a queue and respect the duplicate-suppression window — repeated retries amplify the brute-force counters.
- Enable the IP allowlist (`cd_ip`) so leaked tokens cannot be used from foreign hosts; this also means a misconfigured deploy that lacks allowlist entries will return `142` rather than burn quota.
- When integrating from a fleet of servers, route requests from a stable egress IP (or a small allowlisted set) to make rate-limit accounting predictable.
