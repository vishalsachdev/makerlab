#!/usr/bin/env python3
"""
Add BlogPosting + BreadcrumbList JSON-LD Schema.org markup to all blog posts.
"""

import json
import re
from datetime import datetime
from pathlib import Path


def parse_date(content):
    """Extract publication date from blog post HTML."""
    date_match = re.search(r'Published on\s+\w+,\s+(\d{1,2}\s+\w+\s+\d{4})', content)
    if date_match:
        try:
            dt = datetime.strptime(date_match.group(1), '%d %b %Y')
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            pass
    return None


def parse_author(content):
    """Extract author from blog post HTML."""
    author_match = re.search(r'Published on.*?\n\s*by\s+(.*?)(?:\n|<)', content, re.DOTALL)
    if author_match:
        author = author_match.group(1).strip()
        if author:
            return author
    return 'MakerLab Team'


def parse_title(content):
    """Extract title from blog post HTML."""
    title_match = re.search(r'<h1>(.*?)</h1>', content, re.DOTALL)
    if title_match:
        # Strip HTML tags from title
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
        return title
    return None


def parse_description(content):
    """Extract meta description from blog post HTML."""
    desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
    if desc_match:
        desc = desc_match.group(1).strip()
        if desc and desc != 'Learn. Make. Share':
            return desc
    return None


def create_schema(title, slug, pub_date, author, description):
    """Create BlogPosting + BreadcrumbList JSON-LD."""
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BlogPosting",
                "headline": title,
                "url": f"https://makerlab.illinois.edu/blog/{slug}.html",
                "datePublished": pub_date,
                "author": {
                    "@type": "Person" if author != "MakerLab Team" and author != "Illinois MakerLab" else "Organization",
                    "name": author
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Illinois MakerLab",
                    "url": "https://makerlab.illinois.edu/"
                },
                "mainEntityOfPage": {
                    "@type": "WebPage",
                    "@id": f"https://makerlab.illinois.edu/blog/{slug}.html"
                }
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": "https://makerlab.illinois.edu/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Blog",
                        "item": "https://makerlab.illinois.edu/blog/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": title
                    }
                ]
            }
        ]
    }

    if description:
        schema["@graph"][0]["description"] = description

    return schema


def add_schema_to_file(file_path):
    """Add JSON-LD schema to a blog post HTML file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    slug = file_path.stem

    # Skip if already has schema
    if 'application/ld+json' in content:
        return False

    title = parse_title(content)
    if not title:
        print(f'  Skipped (no title): {file_path.name}')
        return False

    pub_date = parse_date(content)
    if not pub_date:
        print(f'  Skipped (no date): {file_path.name}')
        return False

    author = parse_author(content)
    description = parse_description(content)

    schema = create_schema(title, slug, pub_date, author, description)
    schema_tag = f'  <script type="application/ld+json">\n  {json.dumps(schema, indent=2, ensure_ascii=False).replace(chr(10), chr(10) + "  ")}\n  </script>'

    # Insert before </head>
    new_content = content.replace('</head>', f'{schema_tag}\n</head>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True


def main():
    blog_dir = Path('/Users/vishal/code/makerlab/blog')
    blog_files = sorted(blog_dir.glob('*.html'))

    print(f'Found {len(blog_files)} HTML files in blog/')

    updated = 0
    skipped = 0

    for file_path in blog_files:
        if file_path.name == 'index.html':
            continue

        if add_schema_to_file(file_path):
            updated += 1
        else:
            skipped += 1

    print(f'\nUpdated: {updated}, Skipped: {skipped}')


if __name__ == '__main__':
    main()
