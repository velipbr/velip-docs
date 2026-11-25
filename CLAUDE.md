# velip-docs (CLAUDE.md)

Public documentation of the Velip API v2 and MCP server, published at developers.velip.com.br
(GitHub Pages from `docs/`). A push to `main` publishes.

- Follow `CONTRIBUTING.md`: relative links, English, `curl` examples with `YOUR_TSID`, no real
  token, password or customer data.
- A new or renamed endpoint page goes into **every** list of CONTRIBUTING.md, "Pages that list the
  endpoints" (README.md, docs/index.md, docs/llms.txt, docs/api/v2/README.md, plus overview.md
  and ai-integration when they apply), in the same commit.
- Before committing, run `python3 scripts/check_catalog.py` (the same check runs on GitHub).
- The behavior described comes from the code of the endpoint (`api/v2/<Endpoint>.php` in the
  private application repository): read it before documenting. Never name internal routines,
  servers or tables that a customer does not use.
