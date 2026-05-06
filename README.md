# Velip Docs

Public documentation for the **Velip** communications platform.

This repository is written in **plain Markdown** so it reads well on [GitHub](https://github.com/velipbr/velip-docs) (file tree, search, and blame). Cross-page links use **relative paths** (e.g. `../authentication.md`) so they work when browsing the repo on github.com.

**Start here:** [`docs/introduction.md`](docs/introduction.md) — product overview and links into the API manual.

## What you find here

- **API v2 manual** — every public endpoint under `https://<base>/api/v2/*.php`: parameters, examples, responses, and endpoint-specific error codes.
- **Cross-cutting guides** — [authentication](docs/api/v2/authentication.md), [error codes](docs/api/v2/errors.md), [rate limits](docs/api/v2/rate-limits.md), [getting started](docs/api/v2/getting-started.md).

## Layout

```
docs/
  introduction.md              # landing / overview for integrators
  api/v2/
    README.md                  # index of all v2 pages (GitHub-friendly)
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
scripts/
  convert_mdx_to_md.py         # one-off MDX → MD (reference)
  fix_broken_doc_links.py      # repair relative links if needed
```

## Editing

1. Edit the relevant `.md` file under `docs/`.
2. Keep internal links **relative** to the file you are editing (same rule as above).
3. Open a PR against `main`.

## Out of scope

- SDKs / client libraries — not maintained in this repo.
- Internal architecture and runbooks — private repos only.

## Contact

Support: `support@velip.com` · Sales: `sales@velip.com`
