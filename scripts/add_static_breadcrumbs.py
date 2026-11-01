#!/usr/bin/env python3
"""
Write breadcrumb navigation into each inner page.

js/main.js used to insert the breadcrumb bar after load, which pushed the
page down. The markup is now in the HTML so the first paint matches the
final layout. The script skips a page that already has <nav class="breadcrumb">.

    python3 scripts/add_static_breadcrumbs.py
"""

from html import escape
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GLOBS = (
    "*.html",
    "blog/*.html",
    "courses/*.html",
    "summer/*.html",
    "archive/pages/*.html",
    "articles/*.html",
)

SECTION_LINKS = {
    "blog": ("Blog", "blog/index.html"),
    "courses": ("Courses", "courses.html"),
    "summer": ("Summer Camps", "summer.html"),
}


def html_files():
    found = []
    for pattern in GLOBS:
        found.extend(ROOT.glob(pattern))
    return sorted(set(found))


def page_name(text: str, fallback: str) -> str:
    h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", text, re.I | re.S)
    if h1:
        name = re.sub(r"<[^>]+>", "", h1.group(1))
        name = re.sub(r"\s+", " ", name).strip()
        if name:
            return name
    title = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
    if title:
        name = re.sub(r"\s*-\s*Illinois MakerLab\s*$", "", title.group(1).strip())
        if name:
            return name
    return fallback


def relative(from_file: Path, site_path: str) -> str:
    target = ROOT / site_path
    rel = Path(os_relpath(target, from_file.parent)).as_posix()
    return rel


def os_relpath(target: Path, start: Path) -> str:
    import os
    return os.path.relpath(target, start)


def crumbs_for(path: Path, text: str):
    rel = path.relative_to(ROOT).as_posix()
    if rel in {"index.html", "summer/index.html"}:
        return None
    if re.search(r'<meta\s+http-equiv=["\']refresh["\']', text, re.I):
        return None
    parts = rel.split("/")
    name = page_name(text, Path(parts[-1]).stem.replace("-", " ").title())
    items = [("Home", relative(path, "index.html"))]
    if len(parts) > 1 and parts[0] in SECTION_LINKS:
        label, target = SECTION_LINKS[parts[0]]
        if rel != target:
            items.append((label, relative(path, target)))
    items.append((name, None))
    return items


def render(items) -> str:
    lines = [
        '  <nav class="breadcrumb" aria-label="Breadcrumb">',
        '    <div class="container">',
        '      <ol class="breadcrumb-list">',
    ]
    for label, href in items:
        safe = escape(label)
        if href:
            lines.append(
                f'        <li class="breadcrumb-item"><a href="{escape(href, quote=True)}">{safe}</a></li>'
            )
        else:
            lines.append(
                f'        <li class="breadcrumb-item active" aria-current="page">{safe}</li>'
            )
    lines.extend([
        "      </ol>",
        "    </div>",
        "  </nav>",
        "",
    ])
    return "\n".join(lines)


def update(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if 'class="breadcrumb"' in text or "<main" not in text:
        return "unchanged"
    items = crumbs_for(path, text)
    if not items:
        return "unchanged"
    markup = render(items)
    text = text.replace("<main", markup + "<main", 1)
    path.write_text(text, encoding="utf-8")
    return "updated"


def main():
    updated = unchanged = 0
    for path in html_files():
        if update(path) == "updated":
            updated += 1
        else:
            unchanged += 1
    print(f"Breadcrumbs: added {updated}, left in place {unchanged}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
