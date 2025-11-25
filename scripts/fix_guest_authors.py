#!/usr/bin/env python3
"""
Fix GuestUser authors by inferring from post content or manual mapping.

Since many posts have GuestUser in both XML and HTML, we need to infer
the real author from post content or use manual mappings.
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

# Known author names to look for in content
KNOWN_AUTHORS = {
    'Vishal Sachdev': ['Vishal Sachdev', 'Vishal', 'director', 'Dr. Vishal Sachdev'],
    'Aric Rindfleisch': ['Aric Rindfleisch', 'Aric'],
    'Katie Khau': ['Katie Khau', 'Katie'],
    'Sarah Hampton': ['Sarah Hampton', 'Sarah'],
    'Joon Ryu': ['Joon Ryu', 'Joon'],
    'Illinois MakerLab': ['MakerLab', 'Illinois MakerLab']
}

def infer_author_from_content(content):
    """Try to infer author from post content"""
    content_lower = content.lower()
    
    # Priority 1: Look for first-person mentions with author names
    # Patterns like "our director, Vishal Sachdev" or "I, Vishal" etc.
    for author_name, keywords in KNOWN_AUTHORS.items():
        for keyword in keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in content_lower:
                # Check for first-person context
                # Look for patterns like "our director", "I", "we", "my" near the name
                patterns = [
                    rf'\b(?:our|my)\s+\w+\s*[,.]?\s*{re.escape(keyword_lower)}',
                    rf'\b(?:I|we)\b.*?{re.escape(keyword_lower)}',
                    rf'{re.escape(keyword_lower)}.*?\b(?:I|we|our|my)\b',
                ]
                for pattern in patterns:
                    if re.search(pattern, content_lower, re.IGNORECASE | re.DOTALL):
                        return author_name
    
    # Priority 2: Check for specific author mentions (full names preferred)
    # Full names are more reliable than partial matches
    full_names = ['Vishal Sachdev', 'Aric Rindfleisch', 'Katie Khau', 'Sarah Hampton', 'Joon Ryu']
    for full_name in full_names:
        if full_name.lower() in content_lower:
            return full_name
    
    # Priority 3: Check for "MakerLab" mentions (likely official posts)
    if 'makerlab' in content_lower and content_lower.count('makerlab') >= 3:
        return 'Illinois MakerLab'
    
    return None

def update_blog_post_author(html_file, real_author_name):
    """Update the author name in a blog post HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern to match "by GuestUser" or "by Guest User" (case insensitive)
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
    print("Finding blog posts with GuestUser authors...")
    
    html_files = list(BLOG_DIR.glob("*.html"))
    html_files = [f for f in html_files if f.name != "index.html"]
    
    guest_posts = []
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'GuestUser' in content or 'Guest User' in content or 'guest user' in content.lower():
            guest_posts.append((html_file, content))
    
    print(f"Found {len(guest_posts)} posts with GuestUser\n")
    
    updated_count = 0
    inferred_count = 0
    
    # Parse XML to get post content for inference
    print("Parsing XML export for content analysis...")
    tree = ET.parse(XML_EXPORT)
    root = tree.getroot()
    
    # Build content map
    post_content_map = {}
    items = root.findall('.//item')
    for item in items:
        link_elem = item.find('link')
        content_elem = item.find('content:encoded', namespaces)
        
        if link_elem is not None and content_elem is not None:
            link = link_elem.text or ''
            if '/blog/' in link:
                slug = link.strip('/').split('/')[-1]
                content = content_elem.text or ''
                post_content_map[slug] = content
    
    print(f"Analyzing {len(guest_posts)} posts...\n")
    
    for html_file, html_content in guest_posts:
        slug = html_file.stem
        
        # Try to infer from XML content
        xml_content = post_content_map.get(slug, '')
        inferred_author = infer_author_from_content(xml_content or html_content)
        
        if inferred_author:
            if update_blog_post_author(html_file, inferred_author):
                print(f"  ✓ {html_file.name}: Inferred -> {inferred_author}")
                updated_count += 1
                inferred_count += 1
        else:
            print(f"  ⊘ {html_file.name}: Could not infer author")
    
    print(f"\n{'='*60}")
    print(f"✓ Updated {updated_count} blog posts")
    print(f"  ({inferred_count} inferred from content)")
    print(f"⊘ Could not infer author for {len(guest_posts) - updated_count} posts")
    print(f"{'='*60}")
    print("\nNote: Posts that couldn't be inferred may need manual review.")

if __name__ == '__main__':
    main()
