#!/usr/bin/env python3
"""
Replace 'Courses' navigation link with 'Order Online' linking to online-ordering.html
"""

import re
from pathlib import Path

def replace_courses_nav(html_file):
    """Replace Courses link with Order Online in navigation"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern 1: <li><a href="courses.html">Courses</a></li> (root level)
    content = re.sub(
        r'<li><a href="courses\.html">Courses</a></li>',
        r'<li><a href="online-ordering.html">Order Online</a></li>',
        content
    )
    
    # Pattern 2: <li><a href="../courses.html">Courses</a></li> (subdirectory)
    content = re.sub(
        r'<li><a href="\.\./courses\.html">Courses</a></li>',
        r'<li><a href="../online-ordering.html">Order Online</a></li>',
        content
    )
    
    # Pattern 3: Handle any whitespace variations
    content = re.sub(
        r'<li>\s*<a\s+href=["\']courses\.html["\']>\s*Courses\s*</a>\s*</li>',
        r'<li><a href="online-ordering.html">Order Online</a></li>',
        content,
        flags=re.IGNORECASE
    )
    
    content = re.sub(
        r'<li>\s*<a\s+href=["\']\.\./courses\.html["\']>\s*Courses\s*</a>\s*</li>',
        r'<li><a href="../online-ordering.html">Order Online</a></li>',
        content,
        flags=re.IGNORECASE
    )
    
    if content != original_content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    print("Finding HTML files with Courses navigation...")
    
    # Find all HTML files
    html_files = []
    for html_file in Path('.').rglob('*.html'):
        # Skip archive directory
        if 'archive' not in str(html_file):
            html_files.append(html_file)
    
    print(f"Found {len(html_files)} HTML files\n")
    
    updated_count = 0
    for html_file in html_files:
        if replace_courses_nav(html_file):
            print(f"  ✓ Updated {html_file}")
            updated_count += 1
    
    print(f"\n{'='*60}")
    print(f"✓ Updated {updated_count} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
