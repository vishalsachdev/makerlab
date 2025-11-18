#!/usr/bin/env python3
import json
import os
import re
from pathlib import Path
from html import unescape

# Load content data
with open('content_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

site_info = data['site']
pages = data['pages']
posts = data['posts']

# Navigation items (main pages)
nav_items = [
    {'title': 'Home', 'url': '/index.html'},
    {'title': 'About', 'url': '/about-us.html'},
    {'title': 'What We Offer', 'url': '/pricingservices.html'},
    {'title': 'Courses', 'url': '/courses.html'},
    {'title': 'Summer', 'url': '/summer.html'},
    {'title': 'Blog', 'url': '/blog/index.html'},
    {'title': 'Resources', 'url': '/resources.html'},
    {'title': 'Contact', 'url': '/contact.html'}
]

def create_html_template(title, content, current_page=''):
    """Create full HTML page with navigation and footer"""
    nav_html = '<ul>\n'
    for item in nav_items:
        active_class = ' class="active"' if current_page in item['url'] else ''
        nav_html += f'        <li><a href="{item["url"]}"{active_class}>{item["title"]}</a></li>\n'
    nav_html += '      </ul>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{site_info['description']}">
  <title>{title} - {site_info['title']}</title>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <header class="site-header">
    <div class="container">
      <div class="header-content">
        <div class="site-branding">
          <a href="/index.html" class="site-logo">{site_info['title']}</a>
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
          <a href="/about-us.html">About Us</a>
          <a href="/pricingservices.html">What We Offer</a>
          <a href="/courses.html">Courses</a>
          <a href="/lab-hours.html">Lab Hours</a>
        </div>
        <div class="footer-section">
          <h3>Resources</h3>
          <a href="/resources.html">Resources</a>
          <a href="/faq.html">FAQ</a>
          <a href="/workshops.html">Workshops</a>
          <a href="/blog/index.html">Blog</a>
        </div>
        <div class="footer-section">
          <h3>Connect</h3>
          <a href="https://www.instagram.com/uimakerlab/" target="_blank">Instagram</a>
          <a href="https://www.facebook.com/uimakerlab/" target="_blank">Facebook</a>
          <a href="/contact.html">Contact Us</a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2025 Illinois MakerLab. All rights reserved.</p>
      </div>
    </div>
  </footer>

  <script src="/js/main.js"></script>
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
print("Generating pages...")
for page in pages:
    title = page['title']
    content = clean_content(page['content'])
    link = page['link']

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

    html = create_html_template(title, page_content, link)
    filename = create_page_filename(link)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  ✓ {filename}")

# Generate blog index page
print("\nGenerating blog index...")
Path('blog').mkdir(exist_ok=True)

blog_list_html = '<div class="blog-posts">\n'
for post in posts:
    post_slug = post['slug']
    post_url = f"/blog/{post_slug}.html"

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

html = create_html_template('Blog', blog_index_content, '/blog/')
with open('blog/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("  ✓ blog/index.html")

# Generate individual blog posts
print("\nGenerating blog posts...")
for post in posts:
    title = post['title']
    content = clean_content(post['content'])
    slug = post['slug']

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
              <a href="/blog/index.html" class="btn btn-secondary">← Back to Blog</a>
            </div>
          </article>
        </div>
      </div>
    </div>
    """

    html = create_html_template(title, post_content, '/blog/')
    filename = f"blog/{slug}.html"

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
