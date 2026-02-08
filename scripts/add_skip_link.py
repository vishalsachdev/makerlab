#!/usr/bin/env python3
"""
Add skip-to-content link and main-content ID to all HTML pages.
"""

import re
from pathlib import Path


def add_skip_link_to_file(file_path):
    """Add skip-to-content link after <body> and id='main-content' on <main>."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # Add skip link after <body> if not already present
    if 'skip-link' not in content:
        content = content.replace(
            '<body>',
            '<body>\n  <a href="#main-content" class="skip-link">Skip to main content</a>',
            1
        )
        modified = True

    # Add id="main-content" to <main> if not already present
    if 'id="main-content"' not in content and '<main>' in content:
        content = content.replace('<main>', '<main id="main-content">', 1)
        modified = True

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False


def main():
    base_dir = Path('/Users/vishal/code/makerlab')

    # Find all HTML files
    html_files = []
    for pattern in ['*.html', 'blog/*.html', 'courses/*.html', 'summer/*.html', 'archive/pages/*.html']:
        html_files.extend(base_dir.glob(pattern))

    print(f'Found {len(html_files)} HTML files')

    updated = 0
    skipped = 0

    for file_path in sorted(html_files):
        if add_skip_link_to_file(file_path):
            updated += 1
        else:
            skipped += 1

    print(f'\nUpdated: {updated}, Skipped: {skipped}')


if __name__ == '__main__':
    main()
