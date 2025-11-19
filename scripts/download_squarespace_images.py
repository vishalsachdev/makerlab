#!/usr/bin/env python3
"""
Download Squarespace CDN images and organize them into correct folders
This script:
1. Scans HTML files for Squarespace CDN URLs
2. Categorizes images based on file location (blog, summer, events, etc.)
3. Downloads images to appropriate folders
4. Optionally updates HTML files to use local paths
"""
import os
import re
import hashlib
import urllib.request
import urllib.parse
from pathlib import Path
from collections import defaultdict
import time
import sys

def extract_squarespace_urls(file_path):
    """Extract all Squarespace CDN URLs from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        # Find all Squarespace CDN URLs (both http and https)
        pattern = r'https?://images\.squarespace-cdn\.com[^"\'\s<>\)]+'
        urls = re.findall(pattern, content)
        return urls
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def categorize_image(file_path, url):
    """Determine which category folder an image should go into"""
    file_path = str(file_path).lower()
    url_lower = url.lower()

    if 'blog/' in file_path:
        return 'blog'
    elif 'courses/' in file_path:
        return 'courses'
    elif 'summer/' in file_path or 'summer' in file_path or 'summer' in url_lower:
        return 'summer'
    elif 'staff' in file_path or 'staff' in url_lower:
        return 'staff'
    elif any(word in file_path or word in url_lower for word in ['workshop', 'birthday', 'event', 'party']):
        return 'events'
    else:
        return 'general'

def get_filename_from_url(url):
    """Extract a clean filename from Squarespace URL"""
    # Remove query parameters
    url_clean = url.split('?')[0]
    
    # Parse URL
    parsed = urllib.parse.urlparse(url_clean)
    path = parsed.path

    # Get the last part of the path (filename)
    filename = path.split('/')[-1]

    # Remove URL encoding
    filename = urllib.parse.unquote(filename)

    # Clean up the filename - remove special characters but keep extensions
    filename = re.sub(r'[^\w\-_.]', '_', filename)

    # If filename is too generic or empty, create one from the hash
    if not filename or len(filename) < 5 or filename.startswith('image-asset'):
        # Use hash of full URL to create unique filename
        url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
        # Try to preserve extension
        ext_match = re.search(r'\.(jpg|jpeg|png|gif|webp|svg)', url.lower())
        ext = ext_match.group(0) if ext_match else '.jpg'
        filename = f"image_{url_hash}{ext}"

    return filename

def download_image(url, dest_path, max_retries=3):
    """Download an image from URL to destination path"""
    for attempt in range(max_retries):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            req = urllib.request.Request(url, headers=headers)

            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()
                
                # Verify it's actually an image
                if len(data) < 100:  # Too small to be an image
                    raise ValueError("Downloaded file too small")

            # Ensure directory exists
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(dest_path, 'wb') as f:
                f.write(data)

            return True
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  Retry {attempt + 1}/{max_retries} for {url}")
                time.sleep(2)
            else:
                print(f"  Failed to download {url}: {e}")
                return False
    return False

def scan_all_files(target_dir='.'):
    """Scan all HTML and CSS files for Squarespace URLs"""
    print(f"Scanning files in {target_dir} for Squarespace CDN URLs...")
    
    url_map = {}  # base_url -> {category, filename, original_urls}
    
    # Find all HTML and CSS files
    html_files = list(Path(target_dir).rglob('*.html'))
    css_files = list(Path(target_dir).rglob('*.css'))
    all_files = html_files + css_files
    
    # Filter out git and node_modules
    all_files = [f for f in all_files if '.git' not in str(f) and 'node_modules' not in str(f)]
    
    print(f"Found {len(all_files)} files to scan")
    
    for file_path in all_files:
        urls = extract_squarespace_urls(file_path)
        for url in urls:
            # Create base URL (without query parameters and protocol) for deduplication
            # Normalize http/https to avoid duplicates
            base_url = url.split('?')[0]
            # Remove protocol to treat http and https as same
            base_url_normalized = base_url.replace('http://', '').replace('https://', '')
            
            if base_url_normalized not in url_map:
                category = categorize_image(file_path, url)
                filename = get_filename_from_url(url)
                
                url_map[base_url_normalized] = {
                    'category': category,
                    'filename': filename,
                    'original_urls': set([url]),
                    'source_files': [str(file_path)],
                    'base_url': base_url  # Keep original base URL for downloading
                }
            else:
                # Add this URL variant and source file
                url_map[base_url_normalized]['original_urls'].add(url)
                if str(file_path) not in url_map[base_url_normalized]['source_files']:
                    url_map[base_url_normalized]['source_files'].append(str(file_path))
    
    print(f"Found {len(url_map)} unique images")
    return url_map

def download_all_images(url_map, dry_run=False):
    """Download all images to their categorized folders"""
    if dry_run:
        print("\n[DRY RUN] Would download images...")
    else:
        print("\nDownloading images...")

    success_count = 0
    fail_count = 0
    skipped_count = 0

    # Handle filename conflicts
    used_filenames = defaultdict(dict)  # category -> {filename -> count}

    for i, (base_url, info) in enumerate(url_map.items(), 1):
        category = info['category']
        filename = info['filename']

        # Handle duplicate filenames within same category
        if filename in used_filenames[category]:
            used_filenames[category][filename] += 1
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{used_filenames[category][filename]}{ext}"
        else:
            used_filenames[category][filename] = 1

        # Update filename in map
        info['filename'] = filename

        dest_path = Path(f'images/{category}/{filename}')

        # Skip if file already exists
        if dest_path.exists():
            print(f"[{i}/{len(url_map)}] Skipping (exists): images/{category}/{filename}")
            skipped_count += 1
            continue

        # Prefer https URL, fallback to first available
        download_url = None
        for url in info['original_urls']:
            if url.startswith('https://'):
                download_url = url
                break
        if not download_url:
            download_url = list(info['original_urls'])[0]

        if dry_run:
            print(f"[{i}/{len(url_map)}] Would download to images/{category}/{filename}")
            print(f"  URL: {download_url}")
        else:
            print(f"[{i}/{len(url_map)}] Downloading to images/{category}/{filename}")

            if download_image(download_url, dest_path):
                success_count += 1
            else:
                fail_count += 1

            # Small delay to be respectful to the server
            if i % 10 == 0:
                time.sleep(1)

    if dry_run:
        print(f"\n[DRY RUN] Would download {len(url_map)} images")
    else:
        print(f"\nDownload complete: {success_count} successful, {fail_count} failed, {skipped_count} skipped")
    return success_count, fail_count, skipped_count

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Download Squarespace CDN images and organize them into folders'
    )
    parser.add_argument(
        'target',
        nargs='?',
        default='.',
        help='Target directory to scan (default: current directory)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be downloaded without actually downloading'
    )
    parser.add_argument(
        '--blog-only',
        action='store_true',
        help='Only scan blog/ directory'
    )
    
    args = parser.parse_args()
    
    target_dir = 'blog' if args.blog_only else args.target
    
    # Scan for URLs
    url_map = scan_all_files(target_dir)
    
    if not url_map:
        print("No Squarespace CDN URLs found!")
        return
    
    # Show summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    categories = defaultdict(int)
    for info in url_map.values():
        categories[info['category']] += 1
    
    for category, count in sorted(categories.items()):
        print(f"  {category}: {count} images")
    print("="*60)
    
    # Download images
    success, failed, skipped = download_all_images(url_map, dry_run=args.dry_run)
    
    if not args.dry_run:
        print(f"\nNext step: Run 'python3 replace_squarespace_images.py {target_dir}' to update HTML files")

if __name__ == '__main__':
    main()

