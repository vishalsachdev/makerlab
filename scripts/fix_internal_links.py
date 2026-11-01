#!/usr/bin/env python3
"""
Repair broken internal links and image paths.

Blog posts often use paths such as images/blog/photo.jpg. From /blog/ that
resolves to /blog/images/blog/photo.jpg, while the file lives at /images/blog/.
Old Squarespace and WordPress URLs are pointed at the current page when one
exists. Links with no equivalent page are unwrapped and the visible text stays.

The script is idempotent. Run it again after adding pages.

    python3 scripts/fix_internal_links.py          # report only
    python3 scripts/fix_internal_links.py --write  # update HTML and CSS
"""

from __future__ import annotations

import os
import re
import sys
from html import escape, unescape
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent

HTML_GLOBS = (
    "*.html",
    "blog/*.html",
    "courses/*.html",
    "summer/*.html",
    "archive/pages/*.html",
    "articles/*.html",
)

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico", ".bmp", ".avif"}
ASSET_EXTS = IMAGE_EXTS | {".css", ".js", ".pdf", ".json", ".xml", ".txt", ".yaml", ".yml", ".woff", ".woff2"}

# Old site paths that have a current page. Values are site paths.
ALIASES = {
    "/services": "/pricingservices.html",
    "/services/": "/pricingservices.html",
    "/volunteer": "/archive/pages/volunteer.html",
    "/volunteer/": "/archive/pages/volunteer.html",
    "/subscribe": "/archive/pages/newsletter.html",
    "/subscribe/": "/archive/pages/newsletter.html",
    "/events": "/workshops.html",
    "/events/": "/workshops.html",
}

SQUARESPACE_SECTION = {
    "feed": "/blog/index.html",
    "workshops": "/workshops.html",
    "birthday-parties": "/birthday-parties.html",
    "contact": "/contact.html",
    "people": "/lab-staff.html",
    "makers": "/blog/index.html",
    "design-stories": "/blog/index.html",
    "media-coverage": "/blog/index.html",
    "makingthingsclass": "/courses/making-things.html",
    "makingthings2015": "/courses/making-things.html",
    "visitors": "/blog/index.html",
    "outreach": "/blog/index.html",
    "events": "/workshops.html",
    "thingswemade": "/blog/index.html",
}

DATED_POST = re.compile(
    r"^/(?:illinois-makerlab|blog)/(?:19|20)\d{2}/\d{1,2}/\d{1,2}/([^/?#]+)/?$",
    re.I,
)
DATED_POST_SHORT = re.compile(
    r"^/(?:illinois-makerlab|blog)/(?:19|20)\d{2}/\d{1,2}/([^/?#]+)/?$",
    re.I,
)

ATTR_RE = re.compile(
    r"(\b(?:href|src|poster)\s*=\s*)([\"'])(.*?)\2",
    re.I | re.S,
)
SRCSET_RE = re.compile(r"(\bsrcset\s*=\s*)([\"'])(.*?)\2", re.I | re.S)
CSS_URL_RE = re.compile(r"url\(\s*([\"']?)([^)\"']+)\1\s*\)", re.I)
ANCHOR_RE = re.compile(r"<a\b([^>]*)>(.*?)</a>", re.I | re.S)
IMG_RE = re.compile(r"<img\b[^>]*>", re.I | re.S)
HREF_RE = re.compile(r"""href\s*=\s*(["'])(.*?)\1""", re.I | re.S)


def html_files():
    found = []
    for pattern in HTML_GLOBS:
        found.extend(ROOT.glob(pattern))
    return sorted(set(found))


def is_inside(path: Path) -> bool:
    try:
        path.resolve().relative_to(ROOT)
        return True
    except ValueError:
        return False


def site_file(site_path: str) -> Path | None:
    """Resolve a root-absolute path the way GitHub Pages does."""
    rel = unquote(site_path).split("?", 1)[0].split("#", 1)[0]
    if rel.endswith("/") and rel != "/":
        rel = rel[:-1]
    rel = rel.lstrip("/")
    if rel == "":
        index = ROOT / "index.html"
        return index if index.is_file() else None
    candidate = (ROOT / rel).resolve()
    if not is_inside(candidate):
        return None
    if candidate.is_file():
        return candidate
    if candidate.is_dir() and (candidate / "index.html").is_file():
        return candidate / "index.html"
    if candidate.suffix == "":
        html = Path(str(candidate) + ".html")
        if html.is_file():
            return html
    return None


def browser_file(url: str, source: Path) -> Path | None:
    """File a browser would request, or None when that request 404s."""
    raw = unescape(url).strip()
    if not raw or raw.startswith(("#", "mailto:", "tel:", "javascript:", "data:", "sms:")):
        return None
    if raw.startswith(("http://", "https://", "//")):
        return None
    path = unquote(urlsplit(raw).path)
    if not path:
        return None
    if path.startswith("/"):
        return site_file(path)
    resolved = (source.parent / path).resolve()
    if not is_inside(resolved):
        return None
    if resolved.is_file():
        return resolved
    if resolved.is_dir() and (resolved / "index.html").is_file():
        return resolved / "index.html"
    if resolved.suffix == "" and Path(str(resolved) + ".html").is_file():
        return Path(str(resolved) + ".html")
    return None


def to_relative(source: Path, target: Path) -> str:
    rel = Path(os.path.relpath(target, source.parent)).as_posix()
    return rel


def looks_like_asset(url: str) -> bool:
    path = unquote(urlsplit(unescape(url)).path)
    return Path(path).suffix.lower() in ASSET_EXTS


def build_indexes():
    images = {}
    image_root = ROOT / "images"
    if image_root.exists():
        for path in image_root.rglob("*"):
            if path.is_file():
                images.setdefault(path.name, []).append(path)
    pages = {}
    for path in html_files():
        pages.setdefault(path.name, []).append(path)
    return images, pages


IMAGES, PAGES = build_indexes()


def unique_image(name: str) -> Path | None:
    matches = IMAGES.get(name, [])
    if len(matches) == 1:
        return matches[0]
    return None


def relaxed_image(name: str) -> Path | None:
    """Recover names Squarespace duplicated, such as photo.png.07-PM.png."""
    lower = name.lower()
    for ext in (".jpeg", ".jpg", ".png", ".gif", ".webp"):
        idx = lower.find(ext)
        if idx == -1:
            continue
        short = name[: idx + len(ext)]
        if short != name:
            found = unique_image(short)
            if found:
                return found
    return None


def unique_page(name: str) -> Path | None:
    if not name.endswith(".html"):
        name = name + ".html"
    matches = [p for p in PAGES.get(name, []) if "archive" not in p.parts]
    if len(matches) == 1:
        return matches[0]
    matches = PAGES.get(name, [])
    if len(matches) == 1:
        return matches[0]
    return None


def squarespace_target(path: str) -> str | None:
    parts = [part for part in path.split("/") if part and part.lower() != "img"]
    if not parts or parts[0].lower() != "s":
        # /category/design-stories/ and similar
        if parts and parts[0].lower() == "category":
            return "/blog/index.html"
        return None
    parts = parts[1:]
    if not parts:
        return "/blog/index.html"
    if parts[0].lower() == "category":
        slug = re.sub(r"[^a-z0-9]+", "", "".join(parts[1:]).lower())
        for key, target in SQUARESPACE_SECTION.items():
            if key in slug:
                return target
        return "/blog/index.html"
    if "forum" in parts or "community" in parts:
        return None
    key = parts[-1].lower()
    return SQUARESPACE_SECTION.get(key)


def repair_target(url: str) -> Path | None | str:
    """Return a Path, 'unwrap' when the link should be removed, or None to keep a broken asset."""
    raw = unescape(url).strip()
    path = unquote(urlsplit(raw).path)
    if not path.startswith("/"):
        # Root-relative fallback for paths written without ../ from a subdirectory.
        if not path.startswith("../"):
            cleaned = path[2:] if path.startswith("./") else path
            found = site_file("/" + cleaned)
            if found:
                return found
        path_for_alias = "/" + Path(path).name
    else:
        path_for_alias = path if path.endswith("/") else path

    dated = DATED_POST.match(path.rstrip("/")) or DATED_POST_SHORT.match(path.rstrip("/"))
    if dated:
        slug = dated.group(1)
        if not slug.endswith(".html"):
            slug += ".html"
        candidate = ROOT / "blog" / slug
        if candidate.is_file():
            return candidate
        return "unwrap"

    alias = ALIASES.get(path) or ALIASES.get(path.rstrip("/") + "/") or ALIASES.get(path.rstrip("/"))
    if alias:
        found = site_file(alias)
        if found:
            return found

    if path.startswith("/s/") or path.startswith("/category/"):
        target = squarespace_target(path)
        if target:
            found = site_file(target)
            if found:
                return found
        return "unwrap"

    name = Path(path.rstrip("/")).name
    image = unique_image(name) or relaxed_image(name)
    if image:
        return image
    if "images/" in path:
        suffix = path[path.find("images/") :]
        candidate = ROOT / suffix
        if candidate.is_file():
            return candidate

    known_assets = {
        "style.css": ROOT / "css" / "style.css",
        "main.js": ROOT / "js" / "main.js",
    }
    if name in known_assets and known_assets[name].is_file():
        return known_assets[name]

    if name and not looks_like_asset(path):
        page = unique_page(name)
        if page:
            return page
        if path.startswith("/") or not looks_like_asset(url):
            return "unwrap"
    return None


def classify(url: str, source: Path):
    raw = url.strip()
    if not raw or raw.startswith(("#", "mailto:", "tel:", "javascript:", "data:", "sms:")):
        return "keep", None
    if raw.startswith(("http://", "https://", "//")):
        return "keep", None
    current = browser_file(raw, source)
    if current is not None:
        return "keep", None
    repaired = repair_target(raw)
    if isinstance(repaired, Path):
        parts = urlsplit(unescape(raw).strip())
        rebuilt = to_relative(source, repaired)
        if parts.query:
            rebuilt += "?" + parts.query
        if parts.fragment:
            rebuilt += "#" + parts.fragment
        return "replace", rebuilt
    if repaired == "unwrap":
        return "unwrap", None
    return "broken", None


def html_escape_url(url: str) -> str:
    return escape(url, quote=True)


class Stats:
    def __init__(self):
        self.rewritten = 0
        self.unwrapped = 0
        self.dropped_images = 0
        self.files = 0
        self.broken = []
        self.dropped_urls = set()

    def add_broken(self, source: Path, url: str, kind: str):
        self.broken.append((source.relative_to(ROOT).as_posix(), kind, unescape(url).strip()))


def rewrite_file(path: Path, text: str, stats: Stats, write: bool) -> str:
    original = text

    def rewrite_one(raw, attr):
        action, new = classify(raw, path)
        if action == "replace" and attr in {"src", "poster", "srcset"}:
            if Path(new).suffix.lower() not in ASSET_EXTS:
                stats.add_broken(path, raw, attr)
                return raw
        if action == "replace":
            stats.rewritten += 1
            return html_escape_url(new)
        if action == "broken":
            stats.add_broken(path, raw, attr)
        return raw

    def attr_repl(match):
        prefix, quote, raw = match.group(1), match.group(2), match.group(3)
        attr = prefix.strip().split("=")[0].lower()
        updated = rewrite_one(raw, attr)
        if updated == raw:
            return match.group(0)
        return f"{prefix}{quote}{updated}{quote}"

    text = ATTR_RE.sub(attr_repl, text)

    def srcset_repl(match):
        prefix, quote, raw = match.group(1), match.group(2), match.group(3)
        pieces = []
        changed = False
        for chunk in raw.split(","):
            bits = chunk.strip().split()
            if not bits:
                continue
            updated = rewrite_one(bits[0], "srcset")
            if updated and updated != bits[0]:
                bits[0] = updated
                changed = True
            pieces.append(" ".join(bits))
        if not changed:
            return match.group(0)
        return f"{prefix}{quote}{', '.join(pieces)}{quote}"

    text = SRCSET_RE.sub(srcset_repl, text)

    def css_repl(match):
        quote, raw = match.group(1), match.group(2)
        updated = rewrite_one(raw, "url")
        if not updated or updated == unescape(raw):
            return match.group(0)
        return f"url({quote}{updated}{quote})"

    text = CSS_URL_RE.sub(css_repl, text)

    def anchor_repl(match):
        href = HREF_RE.search(match.group(1))
        if not href:
            return match.group(0)
        action, new = classify(href.group(2), path)
        if action == "keep":
            return match.group(0)
        if action == "replace":
            new_attrs = HREF_RE.sub(
                lambda m: f"href={m.group(1)}{html_escape_url(new)}{m.group(1)}",
                match.group(1),
                count=1,
            )
            return f"<a{new_attrs}>{match.group(2)}</a>"
        if action == "unwrap":
            stats.unwrapped += 1
            return match.group(2)
        stats.add_broken(path, href.group(2), "href")
        return match.group(0)

    text = ANCHOR_RE.sub(anchor_repl, text)

    def img_repl(match):
        tag = match.group(0)
        src = re.search(r"""\bsrc\s*=\s*(["'])(.*?)\1""", tag, re.I | re.S)
        if not src:
            return tag
        action, _new = classify(src.group(2), path)
        raw_path = unquote(urlsplit(unescape(src.group(2))).path)
        fake = "/s/" in raw_path or (raw_path.rstrip("/").endswith("/img") and Path(raw_path).suffix.lower() not in IMAGE_EXTS)
        if fake and action != "keep":
            stats.dropped_images += 1
            stats.dropped_urls.add(unescape(src.group(2)).strip())
            return ""
        return tag

    text = IMG_RE.sub(img_repl, text)

    if write and text != original:
        path.write_text(text, encoding="utf-8")
        stats.files += 1
    elif text != original:
        stats.files += 1
    return text


def main():
    write = "--write" in sys.argv
    stats = Stats()
    targets = html_files()
    for css in (ROOT / "css").glob("*.css"):
        targets.append(css)
    for path in targets:
        text = path.read_text(encoding="utf-8")
        rewrite_file(path, text, stats, write)

    # Unique broken URLs that remain.
    unique = sorted(
        item for item in set(stats.broken)
        if unescape(item[2]).strip() not in stats.dropped_urls
    )
    print(f"Mode: {'write' if write else 'check'}")
    print(f"Files that would change: {stats.files}")
    print(f"URLs rewritten: {stats.rewritten}")
    print(f"Links unwrapped: {stats.unwrapped}")
    print(f"Placeholder images removed: {stats.dropped_images}")
    print(f"Remaining broken references: {len(unique)}")
    for rel, kind, url in unique:
        print(f"  {kind}\t{rel}\t{url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
