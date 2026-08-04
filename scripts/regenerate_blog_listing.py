#!/usr/bin/env python3
"""
Rebuild the post listing inside blog/index.html from api/blog/posts.json.

blog/index.html holds a hand-maintained list of <article class="blog-post">
entries that drifts out of sync whenever a post is added or retitled. This
script regenerates that list (everything inside #blog-posts-container) and
leaves the rest of the page untouched.

Run AFTER scripts/regenerate_blog_index.py, which rebuilds posts.json from
the blog HTML files (the source of truth):

    python3 scripts/regenerate_blog_index.py
    python3 scripts/regenerate_blog_listing.py
"""

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_JSON = ROOT / "api" / "blog" / "posts.json"
INDEX_HTML = ROOT / "blog" / "index.html"

CONTAINER_OPEN = '<div id="blog-posts-container" class="blog-posts">'


def build_entry(post):
    """Render a single <article> listing entry."""
    slug = post["url"].split("/")[-1]
    title = html.escape(post["title"])
    excerpt = html.escape(post.get("excerpt") or post.get("description") or "")

    try:
        pretty_date = datetime.strptime(post["pubDate"], "%Y-%m-%d").strftime(
            "%a, %d %b %Y"
        )
    except (ValueError, KeyError):
        pretty_date = post.get("pubDate", "")

    return f"""  <article class="blog-post">
    <h2 class="blog-post-title"><a href="{slug}">{title}</a></h2>
    <div class="blog-post-meta">
      Published on {pretty_date}
       by Illinois MakerLab
    </div>
    <p class="blog-post-excerpt">{excerpt}</p>
    <a href="{slug}" class="btn btn-outline">Read More &rarr;</a>
  </article>
"""


def main():
    posts = json.loads(POSTS_JSON.read_text(encoding="utf-8"))["posts"]
    posts = sorted(posts, key=lambda p: p.get("pubDate", ""), reverse=True)

    source = INDEX_HTML.read_text(encoding="utf-8")

    start = source.find(CONTAINER_OPEN)
    if start == -1:
        raise SystemExit(f"Could not find {CONTAINER_OPEN} in {INDEX_HTML}")
    body_start = start + len(CONTAINER_OPEN)

    # Walk forward balancing <div> tags so we close the right container.
    depth = 1
    pos = body_start
    tag = re.compile(r"<(/?)div\b", re.IGNORECASE)
    while depth:
        match = tag.search(source, pos)
        if not match:
            raise SystemExit("Unbalanced <div> tags; container end not found")
        depth += -1 if match.group(1) else 1
        pos = match.end()
    body_end = source.rfind("<", body_start, pos)

    previous = len(re.findall(r'<article class="blog-post">', source[body_start:body_end]))

    entries = "\n" + "\n".join(build_entry(p) for p in posts)
    INDEX_HTML.write_text(
        source[:body_start] + entries + source[body_end:], encoding="utf-8"
    )

    print(f"Rebuilt {INDEX_HTML.relative_to(ROOT)}")
    print(f"  entries before: {previous}")
    print(f"  entries after:  {len(posts)}")
    if posts:
        print(f"  newest:         {posts[0]['pubDate']}  {posts[0]['title']}")


if __name__ == "__main__":
    main()
