# Velip Docs

Public documentation for the **Velip** communications platform.

**Read online:** [https://developers.velip.com.br](https://developers.velip.com.br)

This repository is written in **plain Markdown** so it reads well on [GitHub](https://github.com/velipbr/velip-docs) (file tree, search, and blame). Cross-page links use **relative paths** (e.g. `../authentication.md`) so they work when browsing the repo on github.com.

**Start here:** [`docs/introduction.md`](docs/introduction.md) — product overview and links into the API manual.

## What you find here

- **API v2 manual** — every public endpoint under `https://<base>/api/v2/*.php`: parameters, examples, responses, and endpoint-specific error codes.
- **MCP server** — connect AI clients (Cursor, Claude) to Velip tools via MCP Streamable HTTP.
- **Cross-cutting guides** — [authentication](docs/api/v2/authentication.md), [error codes](docs/api/v2/errors.md), [rate limits](docs/api/v2/rate-limits.md), [getting started](docs/api/v2/getting-started.md).

## Layout

```
docs/
  index.md                     # landing (GitHub Pages home)
  introduction.md              # overview for integrators
  DEPLOY.md                    # GitHub Pages + DNS setup
  api/v2/
    README.md                  # index of all v2 pages
    overview.md
    getting-started.md
    authentication.md
    errors.md
    rate-limits.md
    sms/
    whatsapp/
    voice/
    audio-files/
    campaigns/
    destinations/
    messenger/
    instagram/
    email/
    auth-token/
  mcp/
    README.md                  # MCP section index
    overview.md
    getting-started.md
    authentication.md
    permissions.md
    clients/                   # Cursor, Claude, curl
    tools/                     # 13 MCP tools reference
```

## Publishing

See [`docs/DEPLOY.md`](docs/DEPLOY.md) for GitHub Pages and DNS configuration (`developers.velip.com.br`).

## Editing

1. Edit the relevant `.md` file under `docs/`.
2. Keep internal links **relative** to the file you are editing (same rule as above).
3. Open a PR against `main`.

## Out of scope

- SDKs / client libraries — not maintained in this repo.
- Internal architecture and runbooks — private repos only.

## Contact

Support: `support@velip.com` · Sales: `sales@velip.com`
