# MCP authentication

*Bearer tokens, validation, and relationship to the REST API `tsid`.*

Every MCP request (except the health check) must include an `Authorization` header:

```
Authorization: Bearer YOUR_TOKEN_30_CHARS
```

## Token format

- **Length:** 30 characters total
- **Structure:** 10-character token ID + 20-character bcrypt hash segment
- **Storage:** table `cd_psid` in the Velip SaaS database
- **Same family** as REST API `tsid` tokens — issued and managed from your Velip account portal

To obtain a token, contact your Velip account administrator or use the token management UI in the Velip control panel.

## What the server validates

On each request the MCP server:

1. Parses the Bearer token from the `Authorization` header
2. Looks up `cd_psid` — token must exist and be active
3. Resolves the customer (`cdcs_id`) and user context
4. Checks IP allowlist (same rules as [REST authentication](../api/v2/authentication.md))
5. Loads MCP permissions from `cdpsid_mcp_apis`
6. Forwards the **same token** to the Velip PHP API when executing a tool

## Error responses

| HTTP | Meaning |
| --- | --- |
| `401` | Missing, invalid, or expired token |
| `403` | Token valid but MCP disabled globally, channel not enabled, or IP blocked |

Example:

```json
{
  "success": false,
  "error": "Não autenticado",
  "status_code": 401
}
```

## Rate limiting

Failed authentication attempts share the same brute-force and blacklist policies as the REST API. See [REST authentication](../api/v2/authentication.md#brute-force-protection) and [rate limits](../api/v2/rate-limits.md).

## Security tips

- Store tokens in environment variables or a secret manager — never commit them to git.
- Enable the IP allowlist on your account when using MCP from fixed server IPs.
- Rotate tokens immediately if you suspect a leak.
- Grant only the MCP channels you need ([Permissions](permissions.md)).

## Next

- [Permissions](permissions.md) — configure `cdpsid_mcp_apis`
- [Getting started](getting-started.md) — first authenticated call
