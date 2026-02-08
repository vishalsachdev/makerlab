#!/usr/bin/env python3
"""
Regenerate blog/posts.json from blog HTML files.
Extracts real dates, clean excerpts, and auto-tags.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from html.parser import HTMLParser


class HTMLTextExtractor(HTMLParser):
    """Extract visible text from HTML, ignoring tags."""
    def __init__(self):
        super().__init__()
        self.result = []
        self.skip = False
    
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'):
            self.skip = True
    
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'):
            self.skip = False
    
    def handle_data(self, data):
        if not self.skip:
            self.result.append(data)
    
    def get_text(self):
        return ' '.join(self.result)


def strip_html(html_str):
    """Remove HTML tags and return plain text."""
    extractor = HTMLTextExtractor()
    try:
        extractor.feed(html_str)
    except Exception:
        # Fallback: simple regex strip
        return re.sub(r'<[^>]+>', '', html_str)
    return extractor.get_text()


def clean_text(text, max_length=200):
    """Clean and truncate text for excerpts."""
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove common boilerplate
    text = re.sub(r'Illinois MakerLab\s*Learn\.\s*Make\.\s*Share\.?', '', text).strip()
    
    if len(text) > max_length:
        # Truncate at word boundary
        text = text[:max_length].rsplit(' ', 1)[0] + '...'
    
    return text


TAG_KEYWORDS = {
    '3D Printing': [r'3d print', r'3d-print', r'printer', r'filament', r'PLA', r'ultimaker', r'makerbot'],
    'COVID-19': [r'covid', r'pandemic', r'PPE', r'face shield', r'mask buckle'],
    'Education': [r'course', r'class', r'student', r'learning', r'teaching', r'curriculum'],
    'Making Things': [r'making things', r'BADM 331', r'badm331'],
    'Digital Making': [r'digital making', r'BADM 357', r'badm357'],
    'Summer Camp': [r'summer camp', r'summer program', r'youth camp'],
    'Birthday Party': [r'birthday part', r'birthday celebrat'],
    'Workshop': [r'workshop'],
    'Design': [r'design think', r'prototype', r'prototyping', r'3d model', r'tinkercad', r'fusion 360', r'cad'],
    'Volunteer': [r'volunteer', r'guru spotlight', r'guru interview'],
    'Community': [r'community', r'outreach', r'partnership', r'partner'],
    'Research': [r'research', r'study', r'experiment'],
    'Events': [r'maker faire', r'makeathon', r'hackathon', r'hackillinois', r'open house'],
    'Staff': [r'meet the maker', r'employee spotlight', r'featured maker', r'staff'],
    'Scanning': [r'3d scan', r'scanning', r'digitizer'],
}


def auto_tag(title, content_text):
    """Generate tags based on keyword analysis of title and content."""
    tags = set()
    combined = (title + ' ' + content_text).lower()
    
    for tag, keywords in TAG_KEYWORDS.items():
        for kw in keywords:
            if re.search(kw, combined, re.IGNORECASE):
                tags.add(tag)
                break
    
    return sorted(tags)


def parse_blog_post(file_path):
    """Parse a single blog HTML file and extract metadata."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slug = file_path.stem
    
    # Skip index.html
    if slug == 'index':
        return None
    
    # Extract title from <h1>
    title_match = re.search(r'<h1>(.*?)</h1>', content, re.DOTALL)
    title = strip_html(title_match.group(1)).strip() if title_match else slug.replace('-', ' ').title()
    
    # Extract date from "Published on Day, DD Mon YYYY"
    date_match = re.search(r'Published on\s+\w+,\s+(\d{1,2}\s+\w+\s+\d{4})', content)
    pub_date = None
    year = None
    if date_match:
        date_str = date_match.group(1)
        try:
            dt = datetime.strptime(date_str, '%d %b %Y')
            pub_date = dt.strftime('%Y-%m-%d')
            year = dt.year
        except ValueError:
            pass
    
    # If no date found, use a fallback
    if not pub_date:
        pub_date = '2025-11-18'
    
    # Extract author from "by AuthorName"
    author = 'MakerLab Team'
    author_match = re.search(r'Published on.*?\n\s*by\s+(.*?)(?:\n|<)', content, re.DOTALL)
    if author_match:
        author = author_match.group(1).strip()
        if not author:
            author = 'MakerLab Team'
    
    # Extract content from sqs-html-content div
    content_match = re.search(
        r'<div class="sqs-html-content"[^>]*>(.*?)</div>\s*(?:<div class="mt-3">|$)',
        content, re.DOTALL
    )
    
    if content_match:
        article_html = content_match.group(1)
    else:
        # Fallback: get content from article tag
        article_match = re.search(r'<article[^>]*>(.*?)</article>', content, re.DOTALL)
        article_html = article_match.group(1) if article_match else ''
    
    content_text = strip_html(article_html).strip()
    content_text = re.sub(r'\s+', ' ', content_text)
    
    # Generate clean excerpt
    excerpt = clean_text(content_text, 200)
    if not excerpt or excerpt == '...':
        excerpt = title
    
    # Auto-tag
    tags = auto_tag(title, content_text)
    
    return {
        'title': title,
        'slug': slug,
        'url': f'/blog/{slug}.html',
        'excerpt': excerpt,
        'description': excerpt,
        'pubDate': pub_date,
        'year': year,
        'tags': tags,
        'author': author,
    }


def main():
    base_dir = Path('/Users/vishal/code/makerlab')
    blog_dir = base_dir / 'blog'
    output_file = base_dir / 'api' / 'blog' / 'posts.json'
    
    # Find all blog HTML files (exclude index.html)
    blog_files = sorted(blog_dir.glob('*.html'))
    
    print(f'Found {len(blog_files)} HTML files in blog/')
    
    posts = []
    errors = []
    
    for file_path in blog_files:
        if file_path.name == 'index.html':
            continue
        
        try:
            post = parse_blog_post(file_path)
            if post:
                posts.append(post)
        except Exception as e:
            errors.append(f'{file_path.name}: {e}')
            print(f'  Error: {file_path.name}: {e}')
    
    # Sort by date (newest first)
    posts.sort(key=lambda p: p['pubDate'], reverse=True)
    
    # Build output
    output = {
        'total': len(posts),
        'lastUpdated': datetime.now().strftime('%Y-%m-%d'),
        'posts': posts,
    }
    
    # Write JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f'\nGenerated {output_file} with {len(posts)} posts')
    
    # Stats
    with_dates = sum(1 for p in posts if p['year'] is not None)
    with_tags = sum(1 for p in posts if len(p['tags']) > 0)
    print(f'  Posts with real dates: {with_dates}/{len(posts)}')
    print(f'  Posts with tags: {with_tags}/{len(posts)}')
    
    if errors:
        print(f'\n  Errors: {len(errors)}')
        for e in errors:
            print(f'    {e}')


if __name__ == '__main__':
    main()
