#!/usr/bin/env python3
"""
Fix empty alt="" attributes on images in blog posts.
Sets alt text to 'Image from [post title]' for accessibility.
"""

import re
from pathlib import Path


def fix_alt_text_in_file(file_path):
    """Fix empty alt attributes in a blog post."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if no empty alt attributes
    if 'alt=""' not in content:
        return False

    # Extract title from h1
    title_match = re.search(r'<h1>(.*?)</h1>', content, re.DOTALL)
    if title_match:
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
    else:
        title = file_path.stem.replace('-', ' ').title()

    # Escape special characters for alt attribute
    alt_text = f'Image from {title}'.replace('"', '&quot;')

    # Replace all empty alt="" with descriptive alt text
    new_content = content.replace('alt=""', f'alt="{alt_text}"')

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
        if fix_alt_text_in_file(file_path):
            updated += 1
        else:
            skipped += 1

    print(f'\nUpdated: {updated}, Skipped: {skipped}')


if __name__ == '__main__':
    main()
