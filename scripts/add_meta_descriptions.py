#!/usr/bin/env python3
"""
Give each placeholder meta description its own text, and separate duplicate titles.

Pages whose description is only "Learn. Make. Share" get a plain-text summary
of about 150 characters taken from the first paragraph in <main>. Descriptions
that are already unique are left alone.

Also retitles the two Welcome Back posts and the two Free Print Wednesday
pages, and turns extra h1 elements into h2 on the pages that had two.

Idempotent.

    python3 scripts/add_meta_descriptions.py
"""

from html import unescape
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
GENERIC = "learn. make. share"
DESC_RE = re.compile(
    r'(<meta\s+name=["\']description["\']\s+content=["\'])(.*?)(["\']\s*/?>)',
    re.I | re.S,
)
# (relative path, old visible title, new visible title, also change the h1)
TITLE_FIXES = {
    "blog/welcome-back.html": ("Welcome Back!", "Welcome Back for Spring 2015", True),
    "blog/welcome-back-2.html": ("Welcome Back!", "Welcome Back for Fall 2017", True),
    "blog/free-print-wednesdays.html": ("Free Print Wednesdays", "Free Print Wednesdays Announced", True),
    "free-print-wednesday.html": ("Free Print Wednesdays", "Free Print Wednesday", False),
}
EXTRA_H1 = {
    "blog/celebrate-your-next-birthday-with-us.html",
    "blog/makerlab-shows-off-new-ultimaker-2.html",
    "blog/makerlab-would-love-to-host-your-next-birthday.html",
    "archive/pages/summer-2020-response.html",
    "archive/pages/scholarships.html",
    "archive/pages/certificate.html",
    "archive/pages/mijireh-secure-checkout.html",
}


def html_files():
    found = []
    for pattern in GLOBS:
        found.extend(ROOT.glob(pattern))
    return sorted(set(found))


def plain(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", " ", fragment)
    text = unescape(text).replace("\xa0", " ")
    text = text.replace("\u2014", ", ").replace("\u2013", ", ")
    return re.sub(r"\s+", " ", text).strip()


def clip(text: str, limit: int = 150) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text[: limit + 1]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    cut = cut.rstrip(" ,;:-")
    if cut and cut[-1] not in ".!?":
        cut += "."
    if len(cut) > 160:
        cut = cut[:157].rsplit(" ", 1)[0].rstrip(" ,;:-") + "."
    return cut


def excerpt(html: str) -> str:
    main = re.search(r"<main\b[^>]*>(.*)</main>", html, re.I | re.S)
    region = main.group(1) if main else html
    region = re.sub(r"<script\b[^>]*>.*?</script>", " ", region, flags=re.I | re.S)
    region = re.sub(r"<style\b[^>]*>.*?</style>", " ", region, flags=re.I | re.S)
    chunks = []
    for fragment in re.findall(r"<p\b[^>]*>(.*?)</p>", region, re.I | re.S):
        text = plain(fragment)
        if len(text) < 40 or text.lower().strip(".") == GENERIC:
            continue
        chunks.append(text)
        if sum(len(part) for part in chunks) > 220:
            break
    if not chunks:
        title = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
        fallback = plain(title.group(1)) if title else "Illinois MakerLab"
        return clip(fallback)
    return clip(" ".join(chunks))


def demote_extra_h1(html: str) -> str:
    parts = re.split(r"(<h1\b[^>]*>.*?</h1>)", html, flags=re.I | re.S)
    seen = 0
    out = []
    for part in parts:
        if re.match(r"<h1\b", part, re.I):
            seen += 1
            if seen > 1:
                part = re.sub(r"^<h1\b", "<h2", part, count=1, flags=re.I)
                part = re.sub(r"</h1>$", "</h2>", part, count=1, flags=re.I)
        out.append(part)
    return "".join(out)


def apply_title(path: Path, html: str) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel not in TITLE_FIXES:
        return html
    old, new, change_h1 = TITLE_FIXES[rel]
    html = html.replace(
        f"<title>{old} - Illinois MakerLab</title>",
        f"<title>{new} - Illinois MakerLab</title>",
    )
    html = html.replace(f'"headline": "{old}"', f'"headline": "{new}"')
    html = html.replace(f'"name": "{old}"', f'"name": "{new}"')
    if change_h1:
        html = html.replace(f"<h1>{old}</h1>", f"<h1>{new}</h1>")
    return html


def main():
    used = {}
    generic_before = 0
    updated = 0
    titled = 0
    headings = 0
    files = html_files()
    prepared = []
    for path in files:
        html = path.read_text(encoding="utf-8")
        match = DESC_RE.search(html)
        current = plain(match.group(2)) if match else ""
        if current.lower().strip(".") == GENERIC:
            generic_before += 1
        elif current:
            used[current.lower()] = path.relative_to(ROOT).as_posix()
        prepared.append((path, html, match, current))

    for path, html, match, current in prepared:
        original = html
        rel = path.relative_to(ROOT).as_posix()
        html = apply_title(path, html)
        if rel in EXTRA_H1:
            html = demote_extra_h1(html)
            if html != original and "<h2" in html:
                headings += 1
        if current.lower().strip(".") == GENERIC or not current:
            summary = excerpt(html)
            base = summary
            if summary.lower() in used and used[summary.lower()] != rel:
                title = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
                label = plain(title.group(1)) if title else path.stem
                label = re.sub(r"\s*-\s*Illinois MakerLab\s*$", "", label)
                summary = clip(f"{label}. {base}", 160)
            used[summary.lower()] = rel
            if match and plain(match.group(2)) != summary:
                safe = summary.replace("&", "&amp;").replace('"', "&quot;")
                html = DESC_RE.sub(
                    lambda m, safe=safe: m.group(1) + safe + m.group(3),
                    html,
                    count=1,
                )
            elif not match and "</head>" in html:
                tag = f'  <meta name="description" content="{summary}">\n'
                html = html.replace("</head>", tag + "</head>", 1)
        if html != original:
            path.write_text(html, encoding="utf-8")
            updated += 1
            if rel in TITLE_FIXES:
                titled += 1

    print(f"Placeholder descriptions before: {generic_before}")
    print(f"Files updated: {updated}")
    print(f"Duplicate titles retitled: {titled}")
    print(f"Pages whose extra h1 was demoted: {headings}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
