#!/usr/bin/env python3
"""
Add Illinois Campus Brand Toolkit CDN resources to all HTML files.
This script adds the toolkit CSS and JS to the <head> section of each HTML file.
"""

import os
import re
from pathlib import Path

# Toolkit resources
TOOLKIT_CSS = '  <link rel="stylesheet" href="//cdn.toolkit.illinois.edu/3/toolkit.css">\n'
TOOLKIT_JS = '  <script src="//cdn.toolkit.illinois.edu/3/toolkit.js" type="module"></script>\n'

def update_html_file(file_path):
    """Add toolkit resources to an HTML file if not already present."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if toolkit is already added
        if 'cdn.toolkit.illinois.edu' in content:
            print(f"Skipping {file_path} - toolkit already present")
            return False

        # Add toolkit CSS before the first <link> tag or just before </head>
        if '<link rel="stylesheet"' in content:
            # Add toolkit CSS before the first stylesheet link
            content = re.sub(
                r'(\s*)(<link rel="stylesheet")',
                r'\1' + TOOLKIT_CSS + r'\1\2',
                content,
                count=1
            )
        elif '</head>' in content:
            # If no link tags, add before </head>
            content = content.replace('</head>', TOOLKIT_CSS + '</head>')

        # Add toolkit JS before the first <script> tag or just before </body>
        if '<script src=' in content:
            # Add toolkit JS before the first script tag
            content = re.sub(
                r'(\s*)(<script src=)',
                r'\1' + TOOLKIT_JS + r'\1\2',
                content,
                count=1
            )
        elif '</body>' in content:
            # If no script tags, add before </body>
            content = content.replace('</body>', TOOLKIT_JS + '</body>')

        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Updated {file_path}")
        return True

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Find and update all HTML files in the project."""
    # Get the makerlab directory
    base_dir = Path(__file__).parent

    # Find all HTML files
    html_files = list(base_dir.glob('**/*.html'))

    print(f"Found {len(html_files)} HTML files")
    print("=" * 60)

    updated_count = 0
    for html_file in html_files:
        if update_html_file(html_file):
            updated_count += 1

    print("=" * 60)
    print(f"Updated {updated_count} HTML files")
    print(f"Skipped {len(html_files) - updated_count} files")

if __name__ == '__main__':
    main()
