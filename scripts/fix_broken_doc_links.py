#!/usr/bin/env python3
"""Corrige links quebrados onde 'api/' foi perdido pelo slice href[7:]."""

from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def fix_file(md_path: Path) -> None:
    text = md_path.read_text(encoding="utf-8")

    def replace_link(match: re.Match[str]) -> str:
        label, inner = match.group(1), match.group(2)
        prefixes = ("pi/v2/", "api/v2/", "/docs/api/v2/")
        tail = None
        for pref in prefixes:
            if pref in inner:
                tail = inner.split(pref, 1)[1]
                break
        if tail is None:
            return match.group(0)
        anchor = ""
        if "#" in tail:
            path_part, frag = tail.split("#", 1)
            tail = path_part
            anchor = "#" + frag
        target = (DOCS / "api" / "v2" / tail.strip("/")).resolve()
        try:
            rel = Path(os.path.relpath(target, md_path.parent)).as_posix()
        except ValueError:
            rel = target.as_posix()
        return f"[{label}]({rel}{anchor})"

    new_text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_link, text)
    if new_text != text:
        md_path.write_text(new_text, encoding="utf-8")
        print("fixed", md_path.relative_to(ROOT))


def main() -> None:
    for md in sorted(DOCS.rglob("*.md")):
        fix_file(md)


if __name__ == "__main__":
    main()
