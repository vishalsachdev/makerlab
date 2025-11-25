#!/usr/bin/env python3
"""
Fix blog post authors by replacing "GuestUser" / "Guest User" with real names from XML export.

This script:
1. Parses the XML export to extract author mappings (login -> display name)
2. Extracts author information for each blog post from the XML
3. Updates HTML files to replace "GuestUser"/"Guest User" with real author names
"""

import xml.etree.ElementTree as ET
import re
from pathlib import Path
from html import unescape

# Paths
XML_EXPORT = Path('archive/Squarespace-Wordpress-Export-11-18-2025.xml')
BLOG_DIR = Path('blog')

# Define namespaces
namespaces = {
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'wp': 'http://wordpress.org/export/1.2/',
    'dc': 'http://purl.org/dc/elements/1.1/'
}

def parse_xml_authors(root):
    """Extract author login -> display name mapping from XML"""
    author_map = {}
    
    # Find all author definitions
    for author in root.findall('.//wp:author', namespaces):
        login_elem = author.find('wp:author_login', namespaces)
        display_name_elem = author.find('wp:author_display_name', namespaces)
        
        if login_elem is not None and display_name_elem is not None:
            login = login_elem.text
            display_name = display_name_elem.text
            if login and display_name:
                author_map[login] = display_name
    
    return author_map

def extract_blog_post_authors(root):
    """Extract author information for each blog post from XML"""
    post_authors = {}
    
    # Find all items (blog posts)
    items = root.findall('.//item')
    
    for item in items:
        link_elem = item.find('link')
        author_elem = item.find('dc:creator', namespaces)
        
        if link_elem is not None and author_elem is not None:
            link = link_elem.text or ''
            author_login = author_elem.text or ''
            
            # Only process blog posts
            if '/blog/' in link:
                # Extract slug from link
                slug = link.strip('/').split('/')[-1]
                post_authors[slug] = author_login
    
    return post_authors

def update_blog_post_author(html_file, real_author_name):
    """Update the author name in a blog post HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern to match "by GuestUser" or "by Guest User" (case insensitive, multiline)
    # This handles cases where author is on same line or separate line
    content = re.sub(
        r'(\s+by\s+)(?:GuestUser|Guest User|guest user)',
        rf'\1{real_author_name}',
        content,
        flags=re.IGNORECASE | re.MULTILINE
    )
    
    if content != original_content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    print("Parsing XML export...")
    tree = ET.parse(XML_EXPORT)
    root = tree.getroot()
    
    # Build author mapping
    print("Extracting author mappings...")
    author_map = parse_xml_authors(root)
    print(f"Found {len(author_map)} author mappings:")
    for login, display_name in sorted(author_map.items()):
        print(f"  {login} -> {display_name}")
    
    # Extract blog post authors
    print("\nExtracting blog post authors from XML...")
    post_authors = extract_blog_post_authors(root)
    print(f"Found author info for {len(post_authors)} blog posts")
    
    # Process blog HTML files
    print("\nUpdating blog post HTML files...")
    updated_count = 0
    skipped_count = 0
    
    html_files = list(BLOG_DIR.glob("*.html"))
    html_files = [f for f in html_files if f.name != "index.html"]
    
    for html_file in html_files:
        slug = html_file.stem  # filename without .html
        
        # Check if file contains GuestUser
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        has_guest_user = 'GuestUser' in content or 'Guest User' in content or 'guest user' in content.lower()
        
        if not has_guest_user:
            skipped_count += 1
            continue
        
        # Get author login from XML - try multiple slug variations
        author_login = post_authors.get(slug)
        
        # Try alternative slug formats (some posts might have different URL structures)
        if not author_login:
            # Try without date prefix if slug has date-like patterns
            alt_slug = slug
            if any(char.isdigit() for char in slug[:4]):
                # Might have date prefix, try removing it
                parts = slug.split('-')
                if len(parts) > 3 and parts[0].isdigit():
                    alt_slug = '-'.join(parts[3:])
                    author_login = post_authors.get(alt_slug)
        
        if not author_login:
            # No author info in XML for this post
            skipped_count += 1
            continue
        
        # Get display name from author map
        if author_login in author_map:
            real_author_name = author_map[author_login]
            
            # Skip if it's still GuestUser (can't replace with real name if XML says GuestUser)
            if real_author_name.lower() not in ['guest user', 'guestuser']:
                if update_blog_post_author(html_file, real_author_name):
                    print(f"  ✓ Updated {html_file.name}: {author_login} -> {real_author_name}")
                    updated_count += 1
                else:
                    print(f"  ⊘ No change needed for {html_file.name} (author: {author_login})")
                    skipped_count += 1
            else:
                # XML says GuestUser - can't replace without additional info
                skipped_count += 1
        else:
            # Author login not in author map
            skipped_count += 1
    
    print(f"\n{'='*60}")
    print(f"✓ Updated {updated_count} blog posts")
    print(f"⊘ Skipped {skipped_count} blog posts (no changes needed or no author found)")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
