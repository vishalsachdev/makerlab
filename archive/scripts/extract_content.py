#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import json
import re
from html import unescape

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
site_info = {
    'title': channel.find('title').text if channel.find('title') is not None else 'Illinois MakerLab',
    'description': channel.find('description').text if channel.find('description') is not None else 'Learn. Make. Share.',
    'link': channel.find('link').text if channel.find('link') is not None else 'https://makerlab.illinois.edu'
}

# Extract all items (pages and posts)
items = root.findall('.//item')

pages = []
posts = []

for item in items:
    title_elem = item.find('title')
    link_elem = item.find('link')
    content_elem = item.find('content:encoded', namespaces)
    pubDate_elem = item.find('pubDate')
    author_elem = item.find('dc:creator', namespaces)

    if title_elem is not None and link_elem is not None:
        title = title_elem.text or 'Untitled'
        link = link_elem.text or ''
        content = content_elem.text if content_elem is not None else ''
        pubDate = pubDate_elem.text if pubDate_elem is not None else ''
        author = author_elem.text if author_elem is not None else ''

        # Skip attachments
        if 'attachment-' in title.lower():
            continue

        item_data = {
            'title': title,
            'link': link,
            'slug': link.strip('/').split('/')[-1] if link else 'home',
            'content': content,
            'pubDate': pubDate,
            'author': author
        }

        # Categorize as page or post
        if '/blog/' in link:
            posts.append(item_data)
        else:
            pages.append(item_data)

# Sort posts by date (newest first)
posts.sort(key=lambda x: x['pubDate'], reverse=True)

# Create data structure
data = {
    'site': site_info,
    'pages': pages,
    'posts': posts
}

# Save to JSON
with open('content_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✓ Extracted site info")
print(f"✓ Extracted {len(pages)} pages")
print(f"✓ Extracted {len(posts)} blog posts")
print(f"✓ Saved to content_data.json")
