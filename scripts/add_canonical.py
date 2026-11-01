#!/usr/bin/env python3
"""
Add a self-referencing canonical link to every HTML page.

The homepage canonical is https://makerlab.illinois.edu/ .
Every other page uses its .html URL on that host, which is also the URL
listed in sitemap.xml.

The same pass inserts a noscript rule so the mobile menu stays available
when JavaScript is off. css/style.css hides that menu on small screens
until it is opened, which keeps the first paint from shifting.

Idempotent. Run after adding a page:

    python3 scripts/add_canonical.py
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = "https://makerlab.illinois.edu"
GLOBS = (
    "*.html",
    "blog/*.html",
    "courses/*.html",
    "summer/*.html",
    "archive/pages/*.html",
    "articles/*.html",
)

NOSCRIPT = (
    '<noscript><style>@media (max-width: 768px){'
    '.main-nav{display:block !important}'
    '}</style></noscript>'
)
CANONICAL_RE = re.compile(
    r'[ \t]*<link\s+rel=["\']canonical["\']\s+href=["\'][^"\']*["\']\s*/?>\s*',
    re.I,
)


def canonical_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return ORIGIN + "/"
    return ORIGIN + "/" + rel


def html_files():
    found = []
    for pattern in GLOBS:
        found.extend(ROOT.glob(pattern))
    return sorted(set(found))


def update(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if "</head>" not in text:
        return "skipped"
    url = canonical_url(path)
    tag = f'  <link rel="canonical" href="{url}">'
    current = CANONICAL_RE.search(text)
    has_tag = current is not None and url in current.group(0)
    has_noscript = NOSCRIPT in text
    if has_tag and has_noscript:
        return "unchanged"
    original = text
    text = CANONICAL_RE.sub("", text)
    if NOSCRIPT not in text:
        text = text.replace("</head>", "  " + NOSCRIPT + "\n</head>", 1)
    text = text.replace("</head>", tag + "\n</head>", 1)
    if text == original:
        return "unchanged"
    path.write_text(text, encoding="utf-8")
    return "updated"


def main():
    counts = {"updated": 0, "unchanged": 0, "skipped": 0}
    for path in html_files():
        result = update(path)
        counts[result] += 1
    print(
        f"Canonical tags: updated {counts['updated']}, "
        f"already current {counts['unchanged']}, "
        f"skipped {counts['skipped']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
