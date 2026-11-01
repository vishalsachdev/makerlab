#!/usr/bin/env python3
"""
Generate LLM Agent-Friendly API files for Illinois MakerLab
This script creates JSON APIs, sitemaps, and other agent-discovery files
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime
from html.parser import HTMLParser
from html import unescape

# Configuration
BASE_URL = "https://vishalsachdev.github.io/makerlab"
CANONICAL_ORIGIN = "https://makerlab.illinois.edu"
SITE_DIR = Path(os.environ.get("MAKERLAB_SITE_DIR", "./makerlab"))
API_DIR = SITE_DIR / "api"
BLOG_DIR = SITE_DIR / "blog"

class HTMLMetaExtractor(HTMLParser):
    """Extract title and meta description from HTML"""
    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            attrs_dict = dict(attrs)
            if attrs_dict.get("name") == "description":
                self.description = attrs_dict.get("content", "")

    def handle_data(self, data):
        if self.in_title:
            self.title += data

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

def extract_html_metadata(html_path):
    """Extract title and description from HTML file"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        parser = HTMLMetaExtractor()
        parser.feed(content)

        # Clean title - remove " - Illinois MakerLab" suffix if present
        title = parser.title.strip()
        title = re.sub(r'\s*-\s*Illinois MakerLab\s*$', '', title)

        return {
            'title': title or os.path.basename(html_path).replace('.html', '').replace('-', ' ').title(),
            'description': parser.description or ''
        }
    except Exception as e:
        print(f"Warning: Could not extract metadata from {html_path}: {e}")
        return {
            'title': os.path.basename(html_path).replace('.html', '').replace('-', ' ').title(),
            'description': ''
        }

def get_file_modified_date(file_path):
    """Get file modification date in ISO format"""
    try:
        timestamp = os.path.getmtime(file_path)
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except OSError:
        return datetime.now().strftime('%Y-%m-%d')

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

def generate_pages_json():
    """Generate pages.json API file"""
    print("Generating pages.json...")

    pages = []

    # Get all HTML files in root (excluding blog directory)
    html_files = [f for f in SITE_DIR.glob("*.html")]

    for html_file in sorted(html_files):
        filename = html_file.name

        # Skip certain files
        if filename.startswith('.') or filename == 'agent-docs.html':
            continue

        metadata = extract_html_metadata(html_file)
        slug = filename.replace('.html', '')

        # Categorize pages
        category = "information"
        if 'course' in filename or 'digital-making' in filename or 'making-things' in filename:
            category = "education"
        elif 'blog' in filename:
            category = "blog"
        elif 'summer' in filename or 'camp' in filename:
            category = "programs"
        elif 'pricing' in filename or 'service' in filename:
            category = "services"
        elif 'contact' in filename or 'about' in filename:
            category = "about"
        elif 'resource' in filename:
            category = "resources"

        pages.append({
            "title": metadata['title'],
            "slug": slug,
            "url": f"/makerlab/{filename}",
            "description": metadata['description'],
            "category": category,
            "lastModified": get_file_modified_date(html_file)
        })

    # Create API output
    output = {
        "total": len(pages),
        "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
        "pages": pages
    }

    # Write to file
    API_DIR.mkdir(parents=True, exist_ok=True)
    output_file = API_DIR / "pages.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✓ Generated pages.json with {len(pages)} pages")
    return len(pages)

def extract_blog_excerpt(html_path, max_length=200):
    """Extract a plain text excerpt from blog post HTML"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', content)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Unescape HTML entities
        text = unescape(text)
        # Clean up
        text = text.strip()

        # Get first N characters
        if len(text) > max_length:
            text = text[:max_length].rsplit(' ', 1)[0] + '...'

        return text
    except Exception as e:
        print(f"Warning: Could not extract blog excerpt from {html_path}: {e}")
        return "Content preview unavailable"

def generate_blog_posts_json():
    """Generate blog/posts.json API file"""
    print("Generating blog/posts.json...")

    posts = []

    # Get all HTML files in blog directory
    if BLOG_DIR.exists():
        html_files = [f for f in BLOG_DIR.glob("*.html") if f.name != "index.html"]

        for html_file in sorted(html_files):
            filename = html_file.name
            slug = filename.replace('.html', '')

            metadata = extract_html_metadata(html_file)
            excerpt = extract_blog_excerpt(html_file)
            modified_date = get_file_modified_date(html_file)

            # Try to extract year from filename or date
            year_match = re.search(r'(19|20)\d{2}', slug)
            year = int(year_match.group(0)) if year_match else None

            # Extract potential tags from title and content
            tags = []
            title_lower = metadata['title'].lower()
            if any(word in title_lower for word in ['covid', 'pandemic', 'ppe']):
                tags.append('COVID-19')
            if any(word in title_lower for word in ['3d print', 'printing', 'printer']):
                tags.append('3D Printing')
            if any(word in title_lower for word in ['student', 'course', 'class']):
                tags.append('Education')
            if any(word in title_lower for word in ['summer', 'camp']):
                tags.append('Summer Camp')
            if any(word in title_lower for word in ['workshop']):
                tags.append('Workshop')
            if any(word in title_lower for word in ['community', 'partnership']):
                tags.append('Community')

            posts.append({
                "title": metadata['title'],
                "slug": slug,
                "url": f"/makerlab/blog/{filename}",
                "excerpt": excerpt,
                "description": metadata['description'],
                "pubDate": modified_date,
                "year": year,
                "tags": tags,
                "author": "MakerLab Team"
            })

    # Sort by date (newest first)
    posts.sort(key=lambda x: x['pubDate'], reverse=True)

    # Create API output
    output = {
        "total": len(posts),
        "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
        "posts": posts
    }

    # Write to file
    blog_api_dir = API_DIR / "blog"
    blog_api_dir.mkdir(parents=True, exist_ok=True)
    output_file = blog_api_dir / "posts.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✓ Generated blog/posts.json with {len(posts)} posts")
    return len(posts)

def canonical_page_files(site_dir):
    """HTML pages that belong in the sitemap. One canonical URL each."""
    files = []
    for pattern in ("*.html", "blog/*.html", "courses/*.html", "summer/*.html"):
        files.extend(site_dir.glob(pattern))
    unique = []
    seen = set()
    for path in files:
        if path.name.startswith("."):
            continue
        key = path.resolve()
        if key in seen:
            continue
        seen.add(key)
        unique.append(path)
    return sorted(unique, key=lambda path: path.relative_to(site_dir).as_posix())


def canonical_loc(site_dir, path):
    rel = path.relative_to(site_dir).as_posix()
    if rel == "index.html":
        return f"{CANONICAL_ORIGIN}/"
    return f"{CANONICAL_ORIGIN}/{rel}"


def git_lastmod_dates(site_dir):
    """Newest commit date for each file, from git history rather than mtime."""
    import subprocess
    dates = {}
    try:
        output = subprocess.check_output(
            ["git", "log", "--name-only", "--pretty=format:COMMIT %cs"],
            cwd=site_dir,
            text=True,
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return dates
    current = None
    for line in output.splitlines():
        if line.startswith("COMMIT "):
            current = line.split(" ", 1)[1].strip()
        elif line.strip() and current:
            dates.setdefault(line.strip(), current)
    return dates


def page_priority(rel):
    if rel == "index.html":
        return "weekly", "1.0"
    if rel == "blog/index.html":
        return "weekly", "0.9"
    if rel.startswith("blog/"):
        return "yearly", "0.7"
    if rel.startswith("summer/") or rel.startswith("courses/"):
        return "monthly", "0.8"
    if any(token in rel for token in ("about", "contact", "course", "pricing", "lab-hours", "summer")):
        return "monthly", "0.9"
    return "monthly", "0.8"


def generate_sitemap_xml(num_pages=0, num_posts=0):
    """Generate sitemap.xml with one canonical URL per HTML page."""
    print("Generating sitemap.xml...")
    site_dir = Path(__file__).resolve().parent
    dates = git_lastmod_dates(site_dir)
    today = datetime.now().strftime("%Y-%m-%d")
    pages = canonical_page_files(site_dir)

    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for html_file in pages:
        rel = html_file.relative_to(site_dir).as_posix()
        changefreq, priority = page_priority(rel)
        lastmod = dates.get(rel, today)
        sitemap_lines.extend([
            '  <url>',
            f'    <loc>{canonical_loc(site_dir, html_file)}</loc>',
            f'    <lastmod>{lastmod}</lastmod>',
            f'    <changefreq>{changefreq}</changefreq>',
            f'    <priority>{priority}</priority>',
            '  </url>'
        ])
    sitemap_lines.append('</urlset>')

    sitemap_file = site_dir / "sitemap.xml"
    sitemap_file.write_text("\n".join(sitemap_lines) + "\n", encoding="utf-8")
    print(f"✓ Generated sitemap.xml with {len(pages)} canonical URLs")

    guide = site_dir / "agent-guide.json"
    if guide.exists():
        text = guide.read_text(encoding="utf-8")
        updated = re.sub(
            r"Complete XML sitemap with \d+ URLs[^\"]*",
            f"Complete XML sitemap with {len(pages)} canonical HTML URLs",
            text,
        )
        if updated != text:
            guide.write_text(updated, encoding="utf-8")
    return len(pages)

def main():
    """Main execution"""
    print("=" * 60)
    print("Illinois MakerLab - Agent API Generator")
    print("=" * 60)
    print()

    # Generate API files
    num_pages = generate_pages_json()
    num_posts = generate_blog_posts_json()
    num_urls = generate_sitemap_xml(num_pages, num_posts)

    print()
    print("=" * 60)
    print("✓ All agent API files generated successfully!")
    print("=" * 60)
    print()
    print("Generated files:")
    print(f"  - /api/site-info.json (site metadata)")
    print(f"  - /api/pages.json ({num_pages} pages)")
    print(f"  - /api/blog/posts.json ({num_posts} posts)")
    print(f"  - /sitemap.xml ({num_urls} canonical URLs)")
    print()

if __name__ == "__main__":
    main()
