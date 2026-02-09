#!/usr/bin/env python3
"""
Fix <img> tags that have no alt attribute at all in blog posts.
Adds alt="Image from [post title]" for accessibility.
"""

import re
from pathlib import Path


def fix_missing_alt_in_file(file_path):
    """Add alt attributes to img tags that don't have one."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find img tags without alt attribute
    # Match <img that is NOT followed by alt= before the closing >
    pattern = r'<img\b((?![^>]*\balt=)[^>]*)/?\s*>'

    if not re.search(pattern, content):
        return False

    # Extract title from h1
    title_match = re.search(r'<h1>(.*?)</h1>', content, re.DOTALL)
    if title_match:
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
    else:
        title = file_path.stem.replace('-', ' ').title()

    # Escape special characters for alt attribute
    alt_text = f'Image from {title}'.replace('"', '&quot;')

    def add_alt(match):
        tag = match.group(0)
        # Insert alt attribute after <img
        return tag.replace('<img', f'<img alt="{alt_text}"', 1)

    new_content = re.sub(pattern, add_alt, content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True

    return False


def main():
    blog_dir = Path('/Users/vishal/code/makerlab/blog')
    blog_files = sorted(blog_dir.glob('*.html'))

    print(f'Found {len(blog_files)} blog HTML files')

    updated = 0
    skipped = 0

    for file_path in blog_files:
        if file_path.name == 'index.html':
            continue
        if fix_missing_alt_in_file(file_path):
            updated += 1
        else:
            skipped += 1

    print(f'\nUpdated: {updated}, Skipped: {skipped}')


if __name__ == '__main__':
    main()
