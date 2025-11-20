#!/usr/bin/env python3
"""
Static Site Generator for Illinois MakerLab Website

PURPOSE:
  This script was created as a one-time migration tool to convert content from
  Squarespace/WordPress XML export to static HTML files for GitHub Pages.

IMPORTANT NOTES:
  - content_data.json will NOT be updated going forward
  - All content updates should be done directly in HTML files
  - This script overwrites HTML files - use with caution!
  - Pages with manual edits are automatically skipped (see skip_files list)
  - Only run this script if you need to regenerate from content_data.json

USAGE:
  python3 generate_site.py

  The script will:
  1. Read content from content_data.json
  2. Generate HTML pages with consistent header/footer
  3. Generate blog index and individual blog posts
  4. Skip pages that have been manually edited
"""

import json
import os
import re
from pathlib import Path
from html import unescape
from datetime import datetime

# Load content data
with open('content_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

site_info = data['site']
pages = data['pages']
posts = data['posts']

# Sort posts by date in descending order (newest first)
# Handle various date formats and missing dates
def parse_date(date_str):
    """Parse date string and return datetime object for sorting (timezone-naive)"""
    if not date_str:
        return None
    try:
        # Try common date formats - try full string first, then truncated versions
        formats = [
            '%a, %d %b %Y %H:%M:%S %z',  # Wed, 12 Nov 2020 10:00:00 +0000 (with timezone)
            '%a, %d %b %Y %H:%M:%S',      # Wed, 12 Nov 2020 10:00:00 (without timezone)
            '%Y-%m-%d %H:%M:%S',          # 2020-11-12 10:00:00
            '%Y-%m-%d',                   # 2020-11-12
            '%d %b %Y',                    # 12 Nov 2020
            '%b %d, %Y',                   # Nov 12, 2020
            '%a, %d %b %Y',                # Wed, 12 Nov 2020 (date only)
        ]
        for fmt in formats:
            try:
                parsed = datetime.strptime(date_str.strip(), fmt)
                # Convert to timezone-naive for consistent comparison
                if parsed.tzinfo is not None:
                    parsed = parsed.replace(tzinfo=None)
                return parsed
            except:
                continue
        # If no format works, try to extract year and month
        year_match = re.search(r'(\d{4})', date_str)
        month_match = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', date_str, re.IGNORECASE)
        day_match = re.search(r'\b(\d{1,2})\b', date_str)
        if year_match:
            year = int(year_match.group(1))
            # If year is clearly wrong (like 1461), return None to sort to end
            if year < 2000 or year > 2030:
                return None
            month = 1
            day = 1
            if month_match:
                month_names = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
                month = month_names.index(month_match.group(1).lower()) + 1
            if day_match:
                try:
                    day = int(day_match.group(1))
                except:
                    pass
            return datetime(year, month, day)
    except Exception as e:
        pass
    return None

# Sort posts: newest first, posts with invalid/missing dates go to end
posts_sorted = sorted(
    posts,
    key=lambda p: (
        parse_date(p.get('pubDate', '')) or datetime(1900, 1, 1)
    ),
    reverse=True
)
posts = posts_sorted

# Navigation items (main pages) - using relative paths from root
nav_items_base = [
    {'title': 'Home', 'url': 'index.html'},
    {'title': 'About', 'url': 'about-us.html'},
    {'title': 'What We Offer', 'url': 'pricingservices.html'},
    {'title': 'Courses', 'url': 'courses.html'},
    {'title': 'Blog', 'url': 'blog/index.html'},
    {'title': 'Resources', 'url': 'resources.html'},
    {'title': 'Contact', 'url': 'contact.html'}
]

def create_html_template(title, content, current_page='', file_path='index.html'):
    """Create full HTML page with navigation and footer using relative paths"""
    # Calculate relative paths for navigation
    nav_html = '<ul>\n'
    for item in nav_items_base:
        rel_url = get_relative_path(file_path, item['url'])
        active_class = ' class="active"' if current_page and (current_page in item['url'] or item['url'] in current_page) else ''
        nav_html += f'        <li><a href="{rel_url}"{active_class}>{item["title"]}</a></li>\n'
    nav_html += '      </ul>'
    
    # Calculate relative paths for assets
    css_path = get_asset_path(file_path, 'css')
    js_path = get_asset_path(file_path, 'js')
    home_path = get_relative_path(file_path, 'index.html')
    
    # Calculate relative paths for footer links
    footer_about = get_relative_path(file_path, 'about-us.html')
    footer_services = get_relative_path(file_path, 'pricingservices.html')
    footer_courses = get_relative_path(file_path, 'courses.html')
    footer_hours = get_relative_path(file_path, 'lab-hours.html')
    footer_resources = get_relative_path(file_path, 'resources.html')
    footer_lab_staff = get_relative_path(file_path, 'lab-staff.html')
    footer_faq = get_relative_path(file_path, 'faq.html')
    footer_blog = get_relative_path(file_path, 'blog/index.html')
    footer_contact = get_relative_path(file_path, 'contact.html')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{site_info['description']}">
  <title>{title} - {site_info['title']}</title>
  <link rel="stylesheet" href="{css_path}">
</head>
<body>
  <header class="site-header">
    <div class="container">
      <div class="header-content">
        <div class="site-branding">
          <a href="{home_path}" class="site-logo">{site_info['title']}</a>
          <div class="site-tagline">{site_info['description']}</div>
        </div>
        <button class="mobile-menu-toggle" aria-label="Toggle menu" aria-expanded="false">&#9776;</button>
        <nav class="main-nav">
          {nav_html}
        </nav>
      </div>
    </div>
  </header>

  <main>
    {content}
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-section">
          <h3>Illinois MakerLab</h3>
          <p>Business Instructional Facility<br>
          Room 3030<br>
          515 East Gregory Drive<br>
          Champaign, IL 61820</p>
        </div>
        <div class="footer-section">
          <h3>Quick Links</h3>
          <a href="{footer_about}">About Us</a>
          <a href="{footer_services}">What We Offer</a>
          <a href="{footer_courses}">Courses</a>
          <a href="{footer_hours}">Lab Hours</a>
        </div>
        <div class="footer-section">
          <h3>Resources</h3>
          <a href="{footer_resources}">Resources</a>
          <a href="{footer_lab_staff}">Lab Staff</a>
          <a href="{footer_faq}">FAQ</a>
          <a href="{footer_blog}">Blog</a>
        </div>
        <div class="footer-section">
          <h3>Connect</h3>
          <a href="https://www.instagram.com/uimakerlab/" target="_blank">Instagram</a>
          <a href="https://www.facebook.com/uimakerlab/" target="_blank">Facebook</a>
          <a href="{footer_contact}">Contact Us</a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2025 Illinois MakerLab. All rights reserved.</p>
      </div>
    </div>
  </footer>

  <script src="{js_path}"></script>
</body>
</html>"""

def clean_content(content):
    """Clean and prepare content HTML"""
    if not content:
        return '<p>Content coming soon.</p>'

    # Remove CDATA tags
    content = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', content, flags=re.DOTALL)

    # Fix image paths - keep them pointing to Squarespace CDN
    # In production, you'd want to download these and host them locally

    return content

def get_relative_path(from_path, to_path):
    """Calculate relative path from one file to another"""
    from_dir = os.path.dirname(from_path) if os.path.dirname(from_path) else '.'
    to_dir = os.path.dirname(to_path) if os.path.dirname(to_path) else '.'
    
    # Normalize paths
    from_parts = from_dir.split(os.sep) if from_dir != '.' else []
    to_parts = to_dir.split(os.sep) if to_dir != '.' else []
    
    # Find common prefix
    common_len = 0
    for i in range(min(len(from_parts), len(to_parts))):
        if from_parts[i] == to_parts[i]:
            common_len += 1
        else:
            break
    
    # Calculate relative path
    up_levels = len(from_parts) - common_len
    down_path = os.sep.join(to_parts[common_len:])
    
    if up_levels == 0 and not down_path:
        # Same directory
        rel_path = os.path.basename(to_path)
    else:
        # Go up and then down
        rel_path = os.sep.join(['..'] * up_levels + ([down_path] if down_path else []) + [os.path.basename(to_path)])
    
    # Normalize separators for web (use forward slashes)
    return rel_path.replace(os.sep, '/')

def get_asset_path(file_path, asset_type='css'):
    """Get relative path to CSS or JS assets based on file location"""
    if asset_type == 'css':
        asset_path = 'css/style.css'
    elif asset_type == 'js':
        asset_path = 'js/main.js'
    else:
        return asset_path
    
    # If file is in root, use direct path
    if os.path.dirname(file_path) == '' or os.path.dirname(file_path) == '.':
        return asset_path
    
    # If file is in subdirectory, go up one level
    depth = len(os.path.dirname(file_path).split(os.sep))
    return '/'.join(['..'] * depth + [asset_path])

def slugify(text):
    """Create URL-friendly slug from text"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def create_page_filename(link):
    """Convert link to filename"""
    if link == '/home' or link == '/':
        return 'index.html'

    # Remove leading/trailing slashes
    link = link.strip('/')

    # Replace slashes with directory structure
    if '/' in link:
        parts = link.split('/')
        # Create directory if needed
        if len(parts) > 1:
            dir_path = '/'.join(parts[:-1])
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            return f"{link}.html"

    return f"{link}.html"

# Generate all pages
# NOTE: This script was used for one-time migration from Squarespace to GitHub Pages.
# content_data.json will NOT be updated going forward. All content updates should be
# done directly in the HTML files. This script is kept for reference/historical purposes.
# Most pages have been manually edited and should not be regenerated.

print("Generating pages...")
print("⚠️  WARNING: This script overwrites HTML files. Most pages have manual edits.")
print("⚠️  Only run this if you need to regenerate from content_data.json.\n")

for page in pages:
    title = page['title']
    content = clean_content(page['content'])
    link = page['link']

    filename = create_page_filename(link)
    
    # Skip files with custom designs or manual edits that should not be regenerated
    # These pages have been manually edited and should be preserved
    # NOTE: Since content_data.json will never be updated, all content changes
    # are done directly in HTML files. These pages should never be regenerated.
    skip_files = [
        # Custom designs
        'index.html',                    # Custom homepage design (hero, CTA cards, news grid, Instagram)
        
        # Major redesigns
        'pricingservices.html',          # Manual redesign with pricing tables, removed images
        'online-ordering.html',          # Manual redesign with Podio form, improved layout
        'lab-staff.html',                # Manual edits (Gurus section, removed Advisory Board)
        
        # Content updates
        'courses.html',                  # Removed 3DPrintingProfs, marked Digital Making as discontinued, removed video/iframe
        'about-us.html',                 # Updated links (Gies profiles, lab-hours), added lab-staff link
        'lab-hours.html',                 # Updated content (removed specific dates, made generic)
        'volunteer.html',                # Updated application dates to "rolling basis"
        'faq.html',                      # Fixed free print days (Fridays → Wednesdays), updated links
        'contact.html',                  # Updated lab-hours link
        'online-ordering-1.html',        # Updated order form status message
        'online-courses.html',           # Updated links (Gies profiles)
        'hackillinois.html',             # Updated links
        
        # Archived pages (have archive notices)
        'summer.html',                   # Archived with notice (2024 content)
        'workshops.html',                # Archived with notice (outdated workshop info)
        'online-summer-camps-2021.html', # Archived with notice (2021 content)
        'makerlab-wrapped.html',         # Archived with notice (2020 content)
        
        # Course pages (may have manual edits)
        'courses/digital-making.html',   # May reference discontinued course
        'courses/making-things.html',    # Course-specific content
    ]
    if filename in skip_files:
        print(f"  ⊘ {filename} (skipped - has manual edits)")
        continue

    # Wrap content in container
    page_content = f"""
    <div class="section">
      <div class="container">
        <div class="content-area">
          <h1>{title}</h1>
          {content}
        </div>
      </div>
    </div>
    """

    html = create_html_template(title, page_content, link, filename)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  ✓ {filename}")

# Generate blog index page
print("\nGenerating blog index...")
Path('blog').mkdir(exist_ok=True)

blog_list_html = '<div class="blog-posts">\n'
blog_index_path = 'blog/index.html'
for post in posts:
    post_slug = post['slug']
    post_filename = f"blog/{post_slug}.html"
    post_url = get_relative_path(blog_index_path, post_filename)

    # Extract excerpt (first 200 chars of content without HTML)
    content_text = re.sub(r'<[^>]+>', '', post['content'] or '')
    excerpt = content_text[:200].strip() + '...' if len(content_text) > 200 else content_text
    if not excerpt.strip():
        excerpt = 'Read more...'

    blog_list_html += f"""
  <article class="blog-post">
    <h2 class="blog-post-title"><a href="{post_url}">{post['title']}</a></h2>
    <div class="blog-post-meta">
      Published on {post['pubDate'][:16] if post['pubDate'] else 'Unknown date'}
      {f" by {post['author']}" if post['author'] else ""}
    </div>
    <p class="blog-post-excerpt">{excerpt}</p>
    <a href="{post_url}" class="btn btn-outline">Read More →</a>
  </article>
"""

blog_list_html += '</div>'

blog_index_content = f"""
    <div class="section">
      <div class="container">
        <h1 class="text-center">MakerLab Blog</h1>
        <p class="text-center mb-2">News, updates, and stories from the Illinois MakerLab</p>
        {blog_list_html}
      </div>
    </div>
"""

html = create_html_template('Blog', blog_index_content, '/blog/', blog_index_path)
with open(blog_index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("  ✓ blog/index.html")

# Generate individual blog posts
print("\nGenerating blog posts...")
for post in posts:
    title = post['title']
    content = clean_content(post['content'])
    slug = post['slug']

    filename = f"blog/{slug}.html"
    blog_index_rel = get_relative_path(filename, 'blog/index.html')
    
    post_content = f"""
    <div class="section">
      <div class="container">
        <div class="content-wrapper">
          <article class="content-area">
            <h1>{title}</h1>
            <div class="blog-post-meta mb-2">
              Published on {post['pubDate'][:16] if post['pubDate'] else 'Unknown date'}
              {f" by {post['author']}" if post['author'] else ""}
            </div>
            {content}
            <div class="mt-3">
              <a href="{blog_index_rel}" class="btn btn-secondary">← Back to Blog</a>
            </div>
          </article>
        </div>
      </div>
    </div>
    """

    html = create_html_template(title, post_content, '/blog/', filename)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

    # Print progress every 20 posts
    if (posts.index(post) + 1) % 20 == 0:
        print(f"  ✓ {posts.index(post) + 1}/{len(posts)} posts generated...")

print(f"  ✓ All {len(posts)} blog posts generated")

print("\n" + "="*60)
print("✓ Site generation complete!")
print(f"✓ Generated {len(pages)} pages")
print(f"✓ Generated {len(posts)} blog posts")
print(f"✓ Generated 1 blog index")
print("="*60)
