#!/usr/bin/env python3
"""
Converte .mdx (componentes JSX/Mintlify) para .md Markdown puro.

Uso pontual quando migrar sobrou arquivos .mdx — o repo principal usa apenas .md .
"""

from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def parse_frontmatter(
    text: str,
) -> tuple[tuple[str | None, str | None, str | None], str]:
    if not text.startswith("---\n"):
        return (None, None, None), text
    end = text.find("\n---\n", 4)
    if end == -1:
        return (None, None, None), text
    fm_lines = text[4:end].split("\n")
    rest = text[end + 5 :]
    title: str | None = None
    description: str | None = None
    api_endpoint: str | None = None
    for line in fm_lines:
        if line.startswith("title:"):
            title = line.split(":", 1)[1].strip().strip('"').strip("'")
        if line.startswith("description:"):
            description = line.split(":", 1)[1].strip().strip('"').strip("'")
        if line.startswith("api:"):
            api_endpoint = line.split(":", 1)[1].strip().strip('"').strip("'")
    return (title, description, api_endpoint), rest


def rel_link(from_md: Path, href: str) -> str:
    """href sempre /docs/path/sem/arquivo (+ fragmento opcional no caller)."""
    assert href.startswith("/docs/")
    rel = href[len("/docs/") :].strip("/") or "introduction"
    target = DOCS / f"{rel}.md"
    from_dir = from_md.parent
    rp = os.path.relpath(target, start=from_dir).replace("\\", "/")
    return rp


def replace_doc_links(body: str, from_md: Path) -> str:
    """[text](/docs/...fragment) -> [text](../rel.md#fr)"""

    def repl(m):
        txt, target_path, anchor = m.group(1), m.group(2), (m.group(3) or "")
        href = "/docs/" + target_path.strip("/")
        rp = rel_link(from_md, href)
        return f"[{txt}]({rp}{anchor})"

    return re.sub(
        r"\[([^\]]+)\]\(/docs/([^)#]+)(#[^)]*)?\)",
        repl,
        body,
    )


def unwrap_tag(body: str, tag: str) -> str:
    body = re.sub(rf"\s*<{tag}>\s*", "\n", body)
    body = re.sub(rf"\s*</{tag}>\s*", "\n", body)
    return body


def convert_card_group(body: str, from_md: Path) -> str:
    def card_block(m_inner):
        inner = m_inner.group(1)

        def one_card(cm):
            props, content = cm.group(1), cm.group(2).strip()
            title_m = re.search(r'title="([^"]*)"', props)
            href_m = re.search(r'href="(/docs/[^"]*)"', props)
            if not title_m or not href_m:
                return cm.group(0)
            title = title_m.group(1)
            rp = rel_link(from_md, href_m.group(1))
            return f"- **[{title}]({rp})** — {content}"

        return re.sub(
            r"<Card\s+([^>]+)>\s*([\s\S]*?)\s*</Card>",
            one_card,
            inner,
        )

    return re.sub(
        r"<CardGroup[^>]*>\s*([\s\S]*?)\s*</CardGroup>",
        card_block,
        body,
    )


def convert_param_fields(body: str) -> str:
    def one(m):
        props, desc = m.group(1), m.group(2).strip()
        kv = dict(re.findall(r'(\w+)="([^"]*)"', props))
        required = bool(re.search(r"\brequired\b", props))
        loc = kv.get("path") or kv.get("body") or "?"
        typ = kv.get("type", "")
        default = kv.get("default", "")
        bits = [f"`{loc}`"]
        if typ:
            bits.append(f"type: *{typ}*")
        if required:
            bits.append("**required**")
        if default:
            bits.append(f"default: `{default}`")
        head = " — ".join(bits)
        return f"#### {head}\n\n{desc}\n" if desc else f"#### {head}\n"

    return re.sub(
        r"<ParamField\s+([^>]+)>\s*([\s\S]*?)\s*</ParamField>",
        one,
        body,
    )


def convert_response_fields(body: str) -> str:
    def one(m):
        props, desc = m.group(1), m.group(2).strip()
        kv = dict(re.findall(r'(\w+)="([^"]*)"', props))
        nm = kv.get("name", "?")
        typ = kv.get("type", "")
        t = f" (*{typ}*)" if typ else ""
        dash = f" — {desc}" if desc else ""
        return f"- **`{nm}`**{t}{dash}\n"

    return re.sub(
        r"<ResponseField\s+([^>]+)>\s*([\s\S]*?)\s*</ResponseField>",
        one,
        body,
    )


def convert_notes(body: str) -> str:
    def quote(label: str, content: str) -> str:
        content = content.strip()
        lines = content.split("\n") if content else []
        pref = [f"> **{label}**"] + ([f"> {line}" if line else ">" for line in lines])
        return "\n".join(pref) + "\n"

    body = re.sub(
        r"<Note>\s*([\s\S]*?)\s*</Note>",
        lambda m: quote("Note", m.group(1)),
        body,
    )
    body = re.sub(
        r"<Warning>\s*([\s\S]*?)\s*</Warning>",
        lambda m: quote("Warning", m.group(1)),
        body,
    )
    return body


def strip_api_frontmatter_comment(body: str) -> str:
    """
    Frontmatter opcional tipo:
    ---
    api: POST ...
    ---
    já removido na primeira parse; remover linha órfã api: que às vezes fica só no texto
    não necessário se extract title só.
    """
    return body


def convert_file(mdx_path: Path) -> None:
    raw = mdx_path.read_text(encoding="utf-8")
    (title, description, api_endpoint), body = parse_frontmatter(raw)
    body = strip_api_frontmatter_comment(body)

    # Remover frontmatter api: do bloco yaml se ainda presente (alguns arquivos)
    # já coberto por parse_frontmatter

    out_path = mdx_path.with_suffix(".md")
    body = convert_card_group(body, out_path)
    for tag in ("CodeGroup", "RequestExample", "ResponseExample"):
        body = unwrap_tag(body, tag)
    body = convert_param_fields(body)
    body = convert_response_fields(body)
    body = convert_notes(body)
    body = replace_doc_links(body, out_path)

    parts: list[str] = []
    if title:
        parts.append(f"# {title}\n")
    if description:
        parts.append(f"*{description}*\n")
    if api_endpoint:
        parts.append(f"\n**Endpoint:** `{api_endpoint}`\n")
    parts.append(body.lstrip("\n"))

    final = "\n".join(parts).rstrip() + "\n"
    out_path.write_text(final, encoding="utf-8")
    mdx_path.unlink()
    print("OK", out_path.relative_to(ROOT))


def main() -> None:
    for mdx in sorted(DOCS.rglob("*.mdx")):
        convert_file(mdx)


if __name__ == "__main__":
    main()
