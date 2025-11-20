#!/usr/bin/env python3
"""
Re-sort blog/index.html by date (newest first)
"""
import re
from datetime import datetime

# Read current blog index
with open('blog/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all blog posts
posts = []
pattern = r'(<article class="blog-post">.*?</article>)'
matches = re.findall(pattern, content, re.DOTALL)

for match in matches:
    # Extract date
    date_match = re.search(r'Published on ([^<\n]+)', match)
    if date_match:
        date_str = date_match.group(1).strip()
        posts.append({'date': date_str, 'html': match})

print(f"Found {len(posts)} posts")

# Sort by date (newest first)
def parse_date(date_str):
    try:
        # Try parsing 'Wed, 12 Nov 2020' or 'Thu, 12 Nov 2020' format
        date_str_clean = date_str.strip()
        # Remove day name and parse
        date_part = date_str_clean.split(',', 1)[1].strip() if ',' in date_str_clean else date_str_clean
        return datetime.strptime(date_part[:12], '%d %b %Y')
    except Exception as e:
        try:
            # Try extracting year
            year_match = re.search(r'(\d{4})', date_str)
            if year_match:
                year = int(year_match.group(1))
                if 2000 <= year <= 2030:
                    return datetime(year, 1, 1)
        except:
            pass
    return datetime(1900, 1, 1)

posts_sorted = sorted(posts, key=lambda p: parse_date(p['date']), reverse=True)

print(f"First 5 dates after sorting:")
for i, p in enumerate(posts_sorted[:5]):
    print(f"  {i+1}. {p['date'][:30]}")

# Rebuild blog list HTML
blog_list_html = '<div class="blog-posts">\n'
for post in posts_sorted:
    blog_list_html += post['html'] + '\n'
blog_list_html += '</div>'

# Replace the blog posts section in the HTML
blog_section_pattern = r'(<div class="blog-posts">.*?</div>)'
new_content = re.sub(blog_section_pattern, blog_list_html, content, flags=re.DOTALL)

# Write back
with open('blog/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\n✓ Re-sorted blog/index.html")
print(f"✓ Posts now sorted newest to oldest (2020 at top)")

