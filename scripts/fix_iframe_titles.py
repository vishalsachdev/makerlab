#!/usr/bin/env python3
"""
Add title attributes to iframes missing them in blog posts and static pages.
"""

import re
from pathlib import Path


def get_iframe_title(src):
    """Determine appropriate title based on iframe src."""
    if not src:
        return 'Embedded content'
    src_lower = src.lower()
    if 'youtube' in src_lower:
        return 'YouTube video'
    elif 'kaltura' in src_lower:
        return 'Kaltura video player'
    elif 'docs.google' in src_lower or 'gview' in src_lower:
        return 'Google Docs viewer'
    elif 'storify' in src_lower:
        return 'Storify embed'
    elif 'clipsyndicate' in src_lower:
        return 'News video clip'
    elif 'coursera' in src_lower:
        return 'Coursera course widget'
    elif 'podio' in src_lower:
        return 'Order form'
    return 'Embedded content'


def fix_iframes_in_file(file_path):
    """Add title to iframes missing it."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if '<iframe' not in content:
        return False

    modified = False

    def add_title(match):
        nonlocal modified
        tag = match.group(0)
        # Skip if already has title
        if 'title=' in tag.lower():
            return tag
        # Extract src
        src_match = re.search(r'src="([^"]*)"', tag)
        src = src_match.group(1) if src_match else ''
        title = get_iframe_title(src)
        # Insert title after <iframe
        new_tag = tag.replace('<iframe', f'<iframe title="{title}"', 1)
        modified = True
        return new_tag

    new_content = re.sub(r'<iframe[^>]*>', add_title, content, flags=re.IGNORECASE)

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True

    return False


def main():
    base_dir = Path('/Users/vishal/code/makerlab')

    # Find all HTML files with iframes
    html_files = []
    for pattern in ['*.html', 'blog/*.html', 'courses/*.html', 'summer/*.html']:
        html_files.extend(base_dir.glob(pattern))

    print(f'Found {len(html_files)} HTML files')

    updated = 0
    skipped = 0

    for file_path in sorted(html_files):
        if fix_iframes_in_file(file_path):
            updated += 1
        else:
            skipped += 1

    print(f'\nUpdated: {updated}, Skipped: {skipped}')


if __name__ == '__main__':
    main()
