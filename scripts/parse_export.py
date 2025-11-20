#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import re

# Parse the XML file
tree = ET.parse('Squarespace-Wordpress-Export-11-18-2025.xml')
root = tree.getroot()

# Define namespaces
namespaces = {
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'wp': 'http://wordpress.org/export/1.2/',
    'dc': 'http://purl.org/dc/elements/1.1/'
}

# Extract site info
channel = root.find('.//channel')
site_title = channel.find('title').text if channel.find('title') is not None else 'N/A'
site_description = channel.find('description').text if channel.find('description') is not None else 'N/A'

print(f"Site Title: {site_title}")
print(f"Description: {site_description}")
print("\n" + "="*80 + "\n")

# Extract all items (pages and posts)
items = root.findall('.//item')

pages = []
posts = []

for item in items:
    title_elem = item.find('title')
    link_elem = item.find('link')
    content_elem = item.find('content:encoded', namespaces)

    if title_elem is not None and link_elem is not None:
        title = title_elem.text or 'Untitled'
        link = link_elem.text or ''
        content = content_elem.text if content_elem is not None else ''

        # Skip attachments
        if 'attachment-' in title.lower():
            continue

        item_data = {
            'title': title,
            'link': link,
            'content': content,
            'content_length': len(content) if content else 0
        }

        # Categorize as page or post
        if '/blog/' in link:
            posts.append(item_data)
        else:
            pages.append(item_data)

print(f"PAGES FOUND: {len(pages)}")
print("-" * 80)
for page in pages:
    print(f"\nTitle: {page['title']}")
    print(f"Link: {page['link']}")
    print(f"Content Length: {page['content_length']} characters")
    if page['content']:
        # Show first 200 chars of content (cleaned)
        preview = re.sub(r'<[^>]+>', '', page['content'][:500]).strip()
        preview = ' '.join(preview.split())[:200]
        print(f"Preview: {preview}...")

print("\n" + "="*80 + "\n")
print(f"BLOG POSTS FOUND: {len(posts)}")
print(f"(Showing first 10)")
print("-" * 80)
for post in posts[:10]:
    print(f"\nTitle: {post['title']}")
    print(f"Link: {post['link']}")
    print(f"Content Length: {post['content_length']} characters")
