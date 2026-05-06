# Velip Docs

Public documentation for the **Velip** communications platform.

This repository hosts the source content for the Velip developer portal — published with [Mintlify](https://mintlify.com/) and rendered at `docs.velip.com` (Mintlify subdomain in the meantime).

## What you find here

- **API v2 manual** — every endpoint of `https://<base>/api/v2/*.php`, with parameters, request examples, response shapes, and per-endpoint error codes.
- **Cross-cutting guides** — authentication (token-based `tsid`), global error codes, rate limits, brute-force protection.

## Layout

```
docs/
  introduction.mdx               # portal landing
  api/v2/
    overview.mdx
    getting-started.mdx
    authentication.mdx
    errors.mdx
    rate-limits.mdx
    sms/                         # SMS endpoints
    whatsapp/                    # WhatsApp endpoints
    voice/                       # Voice / TTS / WebRTC
    audio-files/                 # Audio file management
    campaigns/                   # Campaigns and queues
    destinations/                # Destination lists
    messenger/                   # Facebook Messenger
    instagram/                   # Instagram Direct
    email/                       # Email via Gmail OAuth
    auth-token/                  # Authentication helpers
    webhooks/                    # Webhook endpoints
    google-risc/                 # Google RISC events
mint.json                        # Mintlify navigation/theme config
openapi/                         # (optional) OpenAPI 3.1 spec for "Try it"
```

Both Mintlify and plain GitHub render this content. MDX components (`<ParamField>`, `<ResponseField>`, `<RequestExample>`, `<Note>`, `<Warning>`) get the rich UI in Mintlify and degrade gracefully on GitHub.

## Editing

1. Clone the repo, edit the relevant `.mdx` file, push to a branch.
2. Mintlify GitHub App auto-builds a preview URL on every PR.
3. Merging to `main` deploys to the production portal.

## Out of scope

- SDKs / client libraries — not yet maintained.
- Internal architecture, deployment guides, runbooks — those live in private repos.

## Contact

Support: `support@velip.com` · Sales: `sales@velip.com`
