#!/usr/bin/env python3
"""
Update blog index.html to use correct authors from individual blog post files.
"""

import re
from pathlib import Path

BLOG_DIR = Path('blog')
INDEX_FILE = BLOG_DIR / 'index.html'

def extract_author_from_post(html_file):
    """Extract author name from a blog post HTML file"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for "Published on ... by AuthorName" pattern
        pattern = r'Published on[^<]*?\s+by\s+([^<\n]+)'
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            author = match.group(1).strip()
            # Clean up any trailing whitespace or punctuation
            author = re.sub(r'\s+', ' ', author).strip()
            return author
    except Exception as e:
        print(f"  Error reading {html_file}: {e}")
    
    return None

def main():
    print("Reading blog index...")
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    original_content = index_content
    
    # Find all blog post entries in index
    # Pattern: <article>...</article> with link to post
    article_pattern = r'(<article class="blog-post">.*?<a href="([^"]+\.html)">.*?</article>)'
    articles = re.findall(article_pattern, index_content, re.DOTALL)
    
    print(f"Found {len(articles)} blog post entries in index\n")
    
    updated_count = 0
    
    for full_article, post_filename in articles:
        post_file = BLOG_DIR / post_filename
        
        if not post_file.exists():
            continue
        
        # Extract author from individual post
        author = extract_author_from_post(post_file)
        
        if not author:
            continue
        
        # Check if index entry has GuestUser
        if 'GuestUser' in full_article or 'Guest User' in full_article:
            # Replace GuestUser with real author
            new_article = re.sub(
                r'(\s+by\s+)(?:GuestUser|Guest User|guest user)',
                rf'\1{author}',
                full_article,
                flags=re.IGNORECASE
            )
            
            if new_article != full_article:
                index_content = index_content.replace(full_article, new_article)
                updated_count += 1
                print(f"  ✓ Updated {post_filename}: {author}")
    
    if index_content != original_content:
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(index_content)
        print(f"\n{'='*60}")
        print(f"✓ Updated {updated_count} entries in blog index")
        print(f"{'='*60}")
    else:
        print("\nNo updates needed in blog index")

if __name__ == '__main__':
    main()
