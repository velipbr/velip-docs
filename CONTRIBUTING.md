# Editing the Velip docs

This repository is plain Markdown, so it reads well on GitHub (file tree, search, blame) and AI agents can read it directly. The site [developers.velip.com.br](https://developers.velip.com.br) is GitHub Pages built from the `docs/` folder.

## Rules

1. Edit the `.md` file under `docs/`.
2. Keep internal links **relative** to the file you are editing (e.g. `../authentication.md`), so they work on github.com and on the site.
3. Write in English, with examples in `curl` and the token as `YOUR_TSID`. Never put a real token, password or customer data in an example.
4. Open a PR against `main`. A push to `main` publishes the site.

## Pages that list the endpoints

A new endpoint, or a renamed one, goes into **all** of these in the same commit:

| File | What it holds |
| --- | --- |
| `README.md` | Repository home: the "I want to…" table. |
| `docs/index.md` | Site home: the same table, with links relative to `docs/`. |
| `docs/llms.txt` | Index for AI agents, with absolute links to the raw Markdown (`https://raw.githubusercontent.com/velipbr/velip-docs/main/docs/...`). |
| `docs/api/v2/README.md` | Every endpoint, by area. |
| `docs/api/v2/overview.md` | Endpoint catalogue by area (one line per area). |
| `docs/ai-integration/README.md` | "Key pages for the agent", when the endpoint is part of a common integration. |

New error codes or HTTP statuses that apply across endpoints also go into `docs/api/v2/errors.md`; new limits into `docs/api/v2/rate-limits.md`.

## Layout

```
README.md                      # repository home (essentials + "I want to…")
CONTRIBUTING.md                # this file
docs/
  index.md                     # site home (GitHub Pages)
  introduction.md              # old link, points to index.md
  llms.txt                     # index for AI agents
  ai-integration/              # build the integration with an AI agent (prompts + diagram)
  DEPLOY.md                    # GitHub Pages + DNS setup
  api/v2/
    README.md                  # index of all v2 pages
    overview.md, getting-started.md, authentication.md, errors.md, rate-limits.md
    sms/ whatsapp/ voice/ audio-files/ campaigns/ destinations/
    messenger/ instagram/ email/ credit/ auth-token/
  mcp/
    README.md                  # MCP section index
    overview.md, getting-started.md, authentication.md, permissions.md
    clients/                   # Cursor, Claude, curl, custom client
    tools/                     # one page per MCP tool
```

## Publishing

See [`docs/DEPLOY.md`](docs/DEPLOY.md) for the GitHub Pages and DNS configuration.
