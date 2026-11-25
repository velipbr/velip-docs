#!/usr/bin/env python3
"""Check that every API v2 page is listed where agents and readers look for it.

Run from anywhere:  python3 scripts/check_catalog.py [path-to-velip-docs]

Checks:
  1. every page under docs/api/v2/<area>/ appears in the four lists of
     CONTRIBUTING.md ("Pages that list the endpoints"): README.md,
     docs/index.md, docs/llms.txt and docs/api/v2/README.md;
  2. every raw link in docs/llms.txt points to a file of this repository;
  3. every relative link in those lists points to a file that exists.

Exit code 0 when all is listed, 1 otherwise (the problems are printed).
"""
import re
import sys
from pathlib import Path

RAW = "https://raw.githubusercontent.com/velipbr/velip-docs/main/"


def main(root: Path) -> int:
    problems = []
    pages = sorted(p.relative_to(root).as_posix() for p in (root / "docs/api/v2").glob("*/*.md"))
    if not pages:
        print(f"no pages found under {root / 'docs/api/v2'}")
        return 1

    lists = {
        "README.md": lambda page: page,                                  # docs/api/v2/sms/MakeSMS.md
        "docs/index.md": lambda page: page[len("docs/"):],              # api/v2/sms/MakeSMS.md
        "docs/llms.txt": lambda page: RAW + page,                       # raw URL
        "docs/api/v2/README.md": lambda page: page[len("docs/api/v2/"):],  # sms/MakeSMS.md
    }
    texts = {name: (root / name).read_text(encoding="utf-8") for name in lists}

    # 1. every page in every list
    for page in pages:
        for name, link in lists.items():
            if f"({link(page)})" not in texts[name]:
                problems.append(f"{page} is missing from {name}")

    # 2. raw links of llms.txt
    for target in re.findall(re.escape(RAW) + r"([^)\s]+)", texts["docs/llms.txt"]):
        if not (root / target).is_file():
            problems.append(f"docs/llms.txt links to {target}, which does not exist")

    # 3. relative links of the lists
    for name in ("README.md", "docs/index.md", "docs/api/v2/README.md"):
        base = (root / name).parent
        for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", texts[name]):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (base / target).resolve().exists():
                problems.append(f"{name} links to {target}, which does not exist")

    for p in problems:
        print("PROBLEM:", p)
    print(f"{len(pages)} API v2 pages checked, {len(problems)} problem(s).")
    if problems:
        print("See CONTRIBUTING.md, section 'Pages that list the endpoints'.")
    return 1 if problems else 0


if __name__ == "__main__":
    repo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    sys.exit(main(repo.resolve()))
