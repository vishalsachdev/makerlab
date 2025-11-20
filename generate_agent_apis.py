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
SITE_DIR = Path("/home/user/makerlab")
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
        return ""

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

def generate_sitemap_xml(num_pages, num_posts):
    """Generate sitemap.xml"""
    print("Generating sitemap.xml...")

    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    # Add homepage
    sitemap_lines.extend([
        '  <url>',
        f'    <loc>{BASE_URL}/index.html</loc>',
        f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>'
    ])

    # Add all pages
    html_files = [f for f in SITE_DIR.glob("*.html")]
    for html_file in sorted(html_files):
        filename = html_file.name
        if filename == 'index.html' or filename.startswith('.'):
            continue

        # Determine change frequency and priority
        changefreq = 'monthly'
        priority = '0.8'

        if 'blog' in filename:
            changefreq = 'weekly'
            priority = '0.9'
        elif any(x in filename for x in ['about', 'contact', 'course']):
            priority = '0.9'

        sitemap_lines.extend([
            '  <url>',
            f'    <loc>{BASE_URL}/{filename}</loc>',
            f'    <lastmod>{get_file_modified_date(html_file)}</lastmod>',
            f'    <changefreq>{changefreq}</changefreq>',
            f'    <priority>{priority}</priority>',
            '  </url>'
        ])

    # Add blog posts
    if BLOG_DIR.exists():
        blog_files = [f for f in BLOG_DIR.glob("*.html")]
        for blog_file in sorted(blog_files):
            filename = blog_file.name
            if filename == 'index.html':
                continue

            sitemap_lines.extend([
                '  <url>',
                f'    <loc>{BASE_URL}/blog/{filename}</loc>',
                f'    <lastmod>{get_file_modified_date(blog_file)}</lastmod>',
                '    <changefreq>yearly</changefreq>',
                '    <priority>0.7</priority>',
                '  </url>'
            ])

    # Add API endpoints for agents
    sitemap_lines.extend([
        '  <url>',
        f'    <loc>{BASE_URL}/api/site-info.json</loc>',
        f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>0.8</priority>',
        '  </url>',
        '  <url>',
        f'    <loc>{BASE_URL}/api/pages.json</loc>',
        f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>0.8</priority>',
        '  </url>',
        '  <url>',
        f'    <loc>{BASE_URL}/api/blog/posts.json</loc>',
        f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>',
        '    <changefreq>daily</changefreq>',
        '    <priority>0.8</priority>',
        '  </url>',
        '  <url>',
        f'    <loc>{BASE_URL}/agent-guide.json</loc>',
        f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>',
        '    <changefreq>monthly</changefreq>',
        '    <priority>0.8</priority>',
        '  </url>'
    ])

    sitemap_lines.append('</urlset>')

    # Write sitemap
    sitemap_file = SITE_DIR / "sitemap.xml"
    with open(sitemap_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sitemap_lines))

    print(f"✓ Generated sitemap.xml with {num_pages + num_posts + 4} URLs")

def main():
    """Main execution"""
    print("=" * 60)
    print("Illinois MakerLab - Agent API Generator")
    print("=" * 60)
    print()

    # Generate API files
    num_pages = generate_pages_json()
    num_posts = generate_blog_posts_json()
    generate_sitemap_xml(num_pages, num_posts)

    print()
    print("=" * 60)
    print("✓ All agent API files generated successfully!")
    print("=" * 60)
    print()
    print("Generated files:")
    print(f"  - /api/site-info.json (site metadata)")
    print(f"  - /api/pages.json ({num_pages} pages)")
    print(f"  - /api/blog/posts.json ({num_posts} posts)")
    print(f"  - /sitemap.xml ({num_pages + num_posts + 4} URLs)")
    print()

if __name__ == "__main__":
    main()
