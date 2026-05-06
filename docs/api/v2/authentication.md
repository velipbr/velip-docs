# Authentication

*Tokens (tsid), HTTP Basic, IP allowlists, and brute-force protection.*

The Velip Public API v2 supports three authentication modes. Most integrations use **token authentication** (`tsid`) for production, with HTTP Basic reserved for first-time token issuance.

## 1. Token (`tsid`) — recommended

A `tsid` is a long-lived API token bound to a customer account and (optionally) a user. You can obtain one through the Velip web portal or by calling [`GetUserID`](auth-token/GetUserID.md) with a valid `username` and `password`.

Once you have it, send it on every API request:
```bash curl (URL parameter)
curl -X POST 'https://<base>/api/v2/MakeSMS.php' \
  -d 'tsid=YOUR_TSID' \
  -d 'dest=5511999999999' \
  -d 'message=Hello'
```

```bash curl (Bearer header)
curl -X POST 'https://<base>/api/v2/MakeSMS.php' \
  -H 'Authorization: Bearer YOUR_TSID' \
  -d 'dest=5511999999999' \
  -d 'message=Hello'
```
The server checks the token against `cd_psid` and resolves the active customer (`cdcs_id`) for the request.

> **Note**
> Tokens are 10 to 64 characters long. The first 10 characters are used as the token identifier in logs and rate-limit accounting.


## 2. HTTP Basic

Used to authenticate by `username` / `password` directly — typically only when issuing a first token via [`GetUserID`](auth-token/GetUserID.md).

```bash
curl -X POST 'https://<base>/api/v2/GetUserID.php' \
  -u "username:password"
```

## 3. SID (session)

The `sid` parameter is an internal session ID issued during long-running interactive flows (mostly used by Velip's own routines). It is interchangeable with `tsid` in most endpoints — when both are present, `tsid` takes priority.

## IP allowlist

Each customer can restrict API access to a list of allowed IPs (`cd_ip` table, managed in the admin portal). Behaviour:

- If the customer has **zero** allowlisted IPs, requests are accepted from any IP.
- If at least one IP is configured, all requests must originate from that list.

Internal Velip IPs (Google Cloud egress and `10.128.0.0/16`) are always allowed.

## Brute-force protection

The API enforces both temporary rate limiting and permanent IP bans:

| Threshold | Window | Effect |
| --- | --- | --- |
| 100 failed attempts | 60 minutes | IP added permanently to `cd_ip_blacklist` (origin: `log_api_cli`). Returns code `199`. |
| 50 user/password failures | 60 minutes | IP added permanently to blacklist (origin: `auth_brute_force`). Returns code `199`. |
| 15 SID-not-found errors (`102`) | 10 minutes | IP added permanently to blacklist (origin: `anti_probe`). Returns code `199`. |
| 20 attempts | 10 minutes | Temporary block. Returns code `131`. |
| 5 user/password attempts per user | 10 minutes | User-specific temporary block. Returns code `132`. |
| `cdcs_tokens_blockeds = 1` on the account | n/a | All tokens for the customer are disabled. Returns code `198`. |

Permanent blacklist entries are removed only by the admin team via the management UI.

## Security tips

- Treat `tsid` like a password. Store it in a secret manager, never in source code.
- Combine `tsid` with the IP allowlist — the two together stop most leaked-token scenarios.
- If you suspect a token leaked, rotate it from the portal: the old `tsid` becomes invalid immediately.
- Avoid sending tokens in URL query strings on requests to non-Velip domains. Prefer the body or the `Authorization` header.

## Errors related to authentication

See [Error codes](errors.md) for the full table. The most common ones in this context:

| Code | Meaning |
| --- | --- |
| `100` | `fail authentication` — token invalid, account inactive, or required parameters missing. |
| `102` | `SID not found` — `sid`/`tsid` does not exist or expired. |
| `130` | No username or password supplied. |
| `131` | Too many attempts from this IP (temporary). |
| `132` | Too many attempts for this user (temporary). |
| `140` | Username or password invalid. |
| `198` | All tokens blocked for this customer. |
| `199` | IP is on the permanent blacklist. |
