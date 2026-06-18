#!/usr/bin/env python3
"""Fix relative asset paths by directory depth; ensure fairpari-v2.css on all pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSET_V = "20260618v2"


def prefix_for(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parts) - 1
    return "../" * depth if depth else ""


def fix_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    orig = text
    changes: list[str] = []
    pfx = prefix_for(path)

    # Normalize css/js hrefs to correct depth
    for kind in ("css", "js"):
        text = re.sub(
            rf'href="(?:\.\./)+{kind}/',
            f'href="{pfx}{kind}/',
            text,
        )
        text = re.sub(
            rf'src="(?:\.\./)+{kind}/',
            f'src="{pfx}{kind}/',
            text,
        )

    # Normalize assets/ paths (keep correct depth)
    text = re.sub(r'src="(?:\.\./)+assets/', f'src="{pfx}assets/', text)
    text = re.sub(r'href="(?:\.\./)+assets/', f'href="{pfx}assets/', text)

    if "fairpari-v2.css" not in text and "fairpari-light-theme.css" in text:
        text = text.replace(
            f'href="{pfx}css/fairpari-light-theme.css?v={ASSET_V}" />',
            f'href="{pfx}css/fairpari-light-theme.css?v={ASSET_V}" />\n'
            f'    <link rel="stylesheet" href="{pfx}css/fairpari-v2.css?v={ASSET_V}" />',
            1,
        )
        changes.append("v2-css")
    elif "fairpari-v2.css" not in text and "multipage.css" in text:
        text = text.replace(
            f'href="{pfx}css/multipage.css?v={ASSET_V}" />',
            f'href="{pfx}css/multipage.css?v={ASSET_V}" />\n'
            f'    <link rel="stylesheet" href="{pfx}css/fairpari-v2.css?v={ASSET_V}" />',
            1,
        )
        changes.append("v2-css")

    text = re.sub(r"\?v=202606\d{2}[a-z0-9]*", f"?v={ASSET_V}", text)

    if text != orig:
        path.write_text(text, encoding="utf-8")
    return changes


def main():
    n = 0
    for html in sorted(ROOT.rglob("*.html")):
        ch = fix_file(html)
        if ch:
            n += 1
            print(f"fixed {html.relative_to(ROOT)}: {', '.join(ch)}")
    print(f"Done, {n} files updated")


if __name__ == "__main__":
    main()
