# Validate credentials (GetUserID)

*Check that your token (or username/password) is valid and retrieve your account ids.*


**Endpoint:** `POST https://<base>/api/v2/GetUserID.php`

Validates the caller's credentials and returns the customer / user ids ("whoami"). Use it to test your integration during onboarding and as a periodic health check that your token is still valid and the account is active.

> **Changed in 2026-08:** this endpoint no longer issues session tokens. The former `tsid=1` flow (which returned a 20-character session token) and the `aut_app` / `aut_send` / `aut_camp` response flags were removed. API tokens are permanent (30 characters) and are created and managed in the Velip portal — see [Authentication](../authentication.md).

## Authentication

Two modes are accepted:

- **Token** (30 characters) — the recommended mode for all integrations.
- **HTTP Basic** with username + password.

See [Authentication](../authentication.md).

## Request

No parameters. Send only your credentials.

## Request example
```bash curl (token)
curl -X POST 'https://<base>/api/v2/GetUserID.php' \
  -d 'tsid=YOUR_API_TOKEN'
```

```bash curl (HTTP Basic)
curl -X POST 'https://<base>/api/v2/GetUserID.php' \
  -u "your_user:your_password"
```
## Response
```json 200 OK
{
  "return": {
    "status": "OK",
    "status_code": "0",
    "cdcs_id": "1234",
    "cdcsu_id": "987"
  }
}
```

```json 401 Unauthorized
{
  "return": {
    "status": "fail authentication",
    "status_code": "100",
    "cdcs_id": "0",
    "cdcsu_id": "0"
  }
}
```
- **`return.cdcs_id`** (*string*) — Customer id (multi-tenant key). Persist if you operate on behalf of multiple customers.


- **`return.cdcsu_id`** (*string*) — User id (the specific operator account inside the customer).


## Error codes

This endpoint is gated by [`log_api_v2`](../authentication.md) — most failures come from there:

| Code | `status` | Cause |
| --- | --- | --- |
| `100` | `fail authentication` | Credentials wrong, account inactive, or required input missing. |
| `101` | `Token is not valid` | Token malformed or expired (only 10- and 30-character tokens are accepted). |
| `110` | `Inactive account` | The customer account is disabled. |
| `131` | `IP trials exceeded` | Too many attempts from this IP in 10 minutes. |
| `132` | `user trials exceeded` | Too many failed attempts for this user in 10 minutes. |
| `140` | `invalid user/pass` | Wrong username or password. |
| `199` | `IP blocked` | IP is on the permanent blacklist. |

## Usage tips

- Obtain your permanent API token in the Velip portal (integrations screen) and store it in your secret manager. This endpoint does not issue tokens.
- A daily call is a reasonable health check; don't call it on every request — failed attempts count toward the brute-force counters.
- Tokens do not expire by themselves but can be revoked by the customer (admin sets `cdcs_tokens_blockeds = 1`) or blocked by IP allowlist changes.
