#!/usr/bin/env python3
"""Apply fairpari v2 template to all HTML pages."""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://fairpari-casino-bonuses.com"
ASSET_V = "20260618v2"
TODAY = "2026-06-18"
LEGAL_FRAGMENTS = (
    "cookie", "politika", "maxfiylik", "foydalanish", "masuliyat",
    "usloviya", "terms-of-use", "privacy-policy", "responsible-gaming",
    "cookie-policy", "otvetstvennaya",
)


def css_prefix(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parts) - 1
    return "../" * depth if depth else ""


def patch_html(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    prefix = css_prefix(path)

    if 'data-template="v2"' not in text:
        text = text.replace("<html ", '<html data-template="v2" ', 1)

    if "fairpari-light-theme.css" not in text:
        text = re.sub(
            rf'(<link rel="stylesheet" href="{re.escape(prefix)}css/style\.css\?v=[^"]+" />\n)',
            rf'\1    <link rel="stylesheet" href="{prefix}css/fairpari-light-theme.css?v={ASSET_V}" />\n',
            text,
            count=1,
        )

    if "fairpari-v2.css" not in text:
        text = re.sub(
            rf'(<link rel="stylesheet" href="{re.escape(prefix)}css/fairpari-light-theme\.css\?v=[^"]+" />\n)',
            rf'\1    <link rel="stylesheet" href="{prefix}css/fairpari-v2.css?v={ASSET_V}" />\n',
            text,
            count=1,
        )
        if "fairpari-v2.css" not in text:
            text = re.sub(
                rf'(<link rel="stylesheet" href="{re.escape(prefix)}css/multipage\.css\?v=[^"]+" />\n)',
                rf'\1    <link rel="stylesheet" href="{prefix}css/fairpari-v2.css?v={ASSET_V}" />\n',
                text,
                count=1,
            )

    text = re.sub(r"\?v=202606\d{2}[a-z0-9]*", f"?v={ASSET_V}", text)
    text = re.sub(r'"dateModified": "2026-06-\d{2}"', f'"dateModified": "{TODAY}"', text)
    text = text.replace('<a href="">Главная</a>', '<a href="/">Главная</a>')

    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def update_sitemap():
    sm = ROOT / "sitemap.xml"
    if not sm.exists():
        return
    urls = re.findall(r"<loc>([^<]+)</loc>", sm.read_text(encoding="utf-8"))
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc in urls:
        rel = loc.replace(DOMAIN, "").rstrip("/")
        if not rel:
            fp = ROOT / "index.html"
        elif rel == "/ru":
            fp = ROOT / "ru" / "index.html"
        elif rel.startswith("/ru/"):
            fp = ROOT / rel.lstrip("/")
            fp = fp if fp.suffix else Path(str(fp) + ".html")
        elif rel.startswith("/en/"):
            fp = ROOT / rel.lstrip("/")
            fp = fp if fp.suffix else Path(str(fp) + "/index.html")
        else:
            fp = ROOT / (rel.lstrip("/") + ".html")
            if not fp.exists():
                fp = ROOT / rel.lstrip("/") / "index.html"
        lm = TODAY
        if fp.exists():
            lm = datetime.fromtimestamp(fp.stat().st_mtime).strftime("%Y-%m-%d")
        pri = "1.0" if rel in ("", "/ru", "/en") else "0.3" if any(x in rel for x in LEGAL_FRAGMENTS) else "0.8"
        lines.append(f"  <url><loc>{loc}</loc><lastmod>{lm}</lastmod><priority>{pri}</priority></url>")
    lines.append("</urlset>")
    sm.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    n = 0
    for html in sorted(ROOT.rglob("*.html")):
        if any(x in str(html) for x in LEGAL_FRAGMENTS):
            continue
        if patch_html(html):
            n += 1
    for html in sorted(ROOT.rglob("*.html")):
        if any(x in str(html) for x in LEGAL_FRAGMENTS):
            if patch_html(html):
                n += 1
    update_sitemap()
    print(f"Patched HTML files, asset v={ASSET_V}")


if __name__ == "__main__":
    main()
