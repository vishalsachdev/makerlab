#!/usr/bin/env python3
"""
Add real width and height, lazy loading, and WebP sources to content images.

The first image in each file stays eager. Later images get loading="lazy".
WebP siblings are written only when they are smaller. The homepage hero and
the private-session photos are always converted. Other referenced images are
converted when the savings are worthwhile, up to a size cap so the repo does
not grow without a reason. Animated GIFs stay GIFs.

Idempotent.

    python3 scripts/add_image_attributes.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import Image, UnidentifiedImageError

ROOT = Path(__file__).resolve().parent.parent
GLOBS = (
    "*.html",
    "blog/*.html",
    "courses/*.html",
    "summer/*.html",
    "archive/pages/*.html",
    "articles/*.html",
)
RASTER = {".jpg", ".jpeg", ".png", ".gif"}
REQUIRED = {
    "images/general/329EC2D6-4605-4429-9C75-272A42347FF5.jpg",
    "images/private-session-1.jpeg",
    "images/private-session-2.jpeg",
    "images/private-session-3.jpeg",
}
# New WebP bytes, not counting files we refuse to keep.
SIZE_CAP = 25 * 1024 * 1024
MIN_SOURCE = 80 * 1024
IMG_RE = re.compile(r"<img\b[^>]*>", re.I | re.S)
SRC_RE = re.compile(r"""\bsrc\s*=\s*(["'])(.*?)\1""", re.I | re.S)
ALT_FIXES = {
    ("archive/pages/summer-2020-response.html", "Screenshot_20200401-103435.png"):
        "Screenshot from the MakerLab summer 2020 COVID-19 response",
    ("archive/pages/summer-2020-response.html", "IMG_2601.jpg"):
        "3D printed masks for the campus N95 initiative",
    ("archive/pages/practicum.html", "Ultimaker3-3.jpg"):
        "Ultimaker 3D printer at the Illinois MakerLab",
    ("archive/pages/makerlab-wrapped.html", "Untitled.jpg"):
        "Wireframe 3D model of a table and chair",
    ("archive/pages/online-summer-camps-2021.html", "3.png"):
        "Illinois MakerLab graphic for 3D Design with Fusion 360",
}


def html_files():
    found = []
    for pattern in GLOBS:
        found.extend(ROOT.glob(pattern))
    return sorted(set(found))


def local_image(source: Path, src: str) -> Path | None:
    src = src.split("#", 1)[0].split("?", 1)[0]
    if not src or src.startswith(("http://", "https://", "data:", "//")):
        return None
    if src.startswith("/"):
        candidate = (ROOT / src.lstrip("/")).resolve()
    else:
        candidate = (source.parent / src).resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError:
        return None
    if candidate.is_file():
        return candidate
    return None


def referenced_images():
    found = set()
    for path in html_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in SRC_RE.finditer(text):
            image = local_image(path, match.group(2))
            if image and image.suffix.lower() in RASTER:
                found.add(image)
    for css in (ROOT / "css").glob("*.css"):
        text = css.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(r"url\(\s*([\"']?)([^)\"']+)\1\s*\)", text):
            image = local_image(css, match.group(2))
            if image and image.suffix.lower() in RASTER:
                found.add(image)
    for rel in REQUIRED:
        image = ROOT / rel
        if image.is_file():
            found.add(image)
    return found


def animated(path: Path) -> bool:
    if path.suffix.lower() != ".gif":
        return False
    with Image.open(path) as image:
        return getattr(image, "n_frames", 1) > 1


def webp_path(path: Path, reserved: dict) -> Path:
    dest = path.with_suffix(".webp")
    owner = reserved.get(dest)
    if owner not in (None, path):
        dest = path.with_name(f"{path.stem}-{path.suffix.lower().lstrip('.')} .webp".replace(" ", ""))
    reserved[dest] = path
    return dest


def convert_webp(path: Path, dest: Path) -> bool:
    if animated(path):
        return False
    with Image.open(path) as image:
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
        image.save(dest, "WEBP", quality=76, method=4)
    return True


def choose_webp(images):
    kept = []
    removed = 0
    candidates = []
    reserved = {}
    for path in sorted(images):
        rel = path.relative_to(ROOT).as_posix()
        required = rel in REQUIRED
        if not required and path.stat().st_size < MIN_SOURCE:
            removed += 1
            continue
        dest = webp_path(path, reserved)
        if dest.exists() and dest.stat().st_size < path.stat().st_size:
            saved = path.stat().st_size - dest.stat().st_size
            useful = saved > 0 and (
                required
                or saved >= max(8 * 1024, int(path.stat().st_size * 0.20))
            )
            if useful:
                candidates.append((saved, dest.stat().st_size, required, dest, path))
                continue
        try:
            created = convert_webp(path, dest)
        except (UnidentifiedImageError, OSError) as exc:
            print(f"  skip {rel}: {exc}")
            continue
        if not created:
            continue
        saved = path.stat().st_size - dest.stat().st_size
        required = rel in REQUIRED
        useful = saved > 0 and (
            required
            or (path.stat().st_size >= MIN_SOURCE and saved >= max(8 * 1024, int(path.stat().st_size * 0.20)))
        )
        if not useful:
            dest.unlink(missing_ok=True)
            removed += 1
            continue
        candidates.append((saved, dest.stat().st_size, required, dest, path))

    required_bytes = sum(size for _saved, size, required, _dest, _path in candidates if required)
    budget = max(0, SIZE_CAP - required_bytes)
    optional = [item for item in candidates if not item[2]]
    optional.sort(key=lambda item: item[0], reverse=True)
    for saved, size, required, dest, path in candidates:
        if required:
            kept.append((path, dest, saved))
    for saved, size, required, dest, path in optional:
        if size <= budget:
            budget -= size
            kept.append((path, dest, saved))
        else:
            dest.unlink()
            removed += 1
    return kept, removed


def set_attr(tag: str, name: str, value: str) -> str:
    pattern = re.compile(rf"""\b{name}\s*=\s*(["']).*?\1""", re.I | re.S)
    if pattern.search(tag):
        return pattern.sub(f'{name}="{value}"', tag, count=1)
    if tag.endswith("/>"):
        return tag[:-2] + f' {name}="{value}"/>'
    return tag[:-1] + f' {name}="{value}">'


def dimensions(path: Path):
    with Image.open(path) as image:
        return image.size


def update_html(webp_for):
    changed = 0
    sized = 0
    lazy = 0
    pictures = 0
    alts = 0
    for path in html_files():
        html = path.read_text(encoding="utf-8")
        original = html
        matches = list(IMG_RE.finditer(html))
        if not matches:
            continue
        first_local = None
        for index, match in enumerate(matches):
            src = SRC_RE.search(match.group(0))
            if src and local_image(path, src.group(2)):
                first_local = index
                break
        pieces = []
        cursor = 0
        for index, match in enumerate(matches):
            pieces.append(html[cursor:match.start()])
            tag = match.group(0)
            src_match = SRC_RE.search(tag)
            image = local_image(path, src_match.group(2)) if src_match else None
            rel = path.relative_to(ROOT).as_posix()
            if image and (rel, image.name) in ALT_FIXES:
                alt = ALT_FIXES[(rel, image.name)]
                if not re.search(r"\balt\s*=", tag, re.I) or re.search(r"""\balt\s*=\s*(["'])\s*\1""", tag, re.I):
                    tag = set_attr(tag, "alt", alt)
                    alts += 1
            if image:
                try:
                    width, height = dimensions(image)
                    tag = set_attr(tag, "width", str(width))
                    tag = set_attr(tag, "height", str(height))
                    sized += 1
                except (UnidentifiedImageError, OSError):
                    pass
            eager = index == first_local or 'fetchpriority="high"' in tag or "fetchpriority='high'" in tag
            if eager:
                tag = set_attr(tag, "loading", "eager")
            else:
                tag = set_attr(tag, "loading", "lazy")
                lazy += 1
            before = html[max(0, match.start() - 400):match.start()].lower()
            in_picture = "<picture" in before and before.rfind("<picture") > before.rfind("</picture")
            webp = webp_for.get(image) if image else None
            if webp and not in_picture:
                webp_src = Path(
                    __import__("os").path.relpath(webp, path.parent)
                ).as_posix()
                classes = "hero-media" if "hero-photo" in tag else ""
                class_attr = f' class="{classes}"' if classes else ""
                tag = (
                    f'<picture{class_attr}>'
                    f'<source srcset="{webp_src}" type="image/webp">'
                    f"{tag}</picture>"
                )
                pictures += 1
            pieces.append(tag)
            cursor = match.end()
        pieces.append(html[cursor:])
        updated = "".join(pieces)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed, sized, lazy, pictures, alts


def main():
    images = referenced_images()
    print(f"Referenced raster images: {len(images)}")
    kept, removed = choose_webp(images)
    webp_for = {source: dest for source, dest, _saved in kept}
    added = sum(dest.stat().st_size for _source, dest, _saved in kept)
    saved = sum(amount for _source, _dest, amount in kept)
    print(f"WebP kept: {len(kept)} ({added / 1_000_000:.1f} MB added, {saved / 1_000_000:.1f} MB smaller than the originals)")
    print(f"WebP skipped or discarded: {removed}")
    changed, sized, lazy, pictures, alts = update_html(webp_for)
    print(f"HTML files updated: {changed}")
    print(f"Images given dimensions: {sized}")
    print(f"Images marked lazy: {lazy}")
    print(f"Picture elements added: {pictures}")
    print(f"Alt text added: {alts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
