#!/usr/bin/env python3
"""
Script to migrate Squarespace CDN images to local hosting
"""
import os
import re
import json
import hashlib
import urllib.request
import urllib.parse
from pathlib import Path
from collections import defaultdict
import time

def extract_squarespace_urls(file_path):
    """Extract all Squarespace CDN URLs from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        # Find all Squarespace CDN URLs
        pattern = r'https://images\.squarespace-cdn\.com[^"\'\s<>]*'
        urls = re.findall(pattern, content)
        return urls
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def categorize_image(file_path, url):
    """Determine which category folder an image should go into"""
    file_path = str(file_path).lower()

    if 'blog/' in file_path:
        return 'blog'
    elif 'courses/' in file_path:
        return 'courses'
    elif 'summer/' in file_path or 'summer' in file_path:
        return 'summer'
    elif 'staff' in file_path or 'staff' in url.lower():
        return 'staff'
    elif 'workshop' in file_path or 'birthday' in file_path or 'event' in file_path or 'party' in file_path:
        return 'events'
    else:
        return 'general'

def get_filename_from_url(url):
    """Extract a clean filename from Squarespace URL"""
    # Parse URL
    parsed = urllib.parse.urlparse(url)
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
            # Remove query parameters for cleaner URLs, but keep the original URL for downloading
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            req = urllib.request.Request(url, headers=headers)

            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()

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

def scan_all_files():
    """Scan all HTML and CSS files for Squarespace URLs"""
    print("Scanning files for Squarespace CDN URLs...")

    url_map = {}  # url -> {category, filename, files_used_in[]}

    # Scan HTML files
    for html_file in Path('.').rglob('*.html'):
        if '.git' in str(html_file):
            continue

        urls = extract_squarespace_urls(html_file)
        for url in urls:
            # Normalize URL (remove format parameters)
            base_url = url.split('?')[0]

            if base_url not in url_map:
                category = categorize_image(html_file, url)
                filename = get_filename_from_url(url)
                url_map[base_url] = {
                    'category': category,
                    'filename': filename,
                    'files': set(),
                    'original_urls': set()
                }

            url_map[base_url]['files'].add(str(html_file))
            url_map[base_url]['original_urls'].add(url)

    # Scan CSS files
    for css_file in Path('.').rglob('*.css'):
        if '.git' in str(css_file):
            continue

        urls = extract_squarespace_urls(css_file)
        for url in urls:
            base_url = url.split('?')[0]

            if base_url not in url_map:
                category = 'general'
                filename = get_filename_from_url(url)
                url_map[base_url] = {
                    'category': category,
                    'filename': filename,
                    'files': set(),
                    'original_urls': set()
                }

            url_map[base_url]['files'].add(str(css_file))
            url_map[base_url]['original_urls'].add(url)

    # Scan content_data.json
    content_json = Path('content_data.json')
    if content_json.exists():
        urls = extract_squarespace_urls(content_json)
        for url in urls:
            base_url = url.split('?')[0]

            if base_url not in url_map:
                category = 'general'
                filename = get_filename_from_url(url)
                url_map[base_url] = {
                    'category': category,
                    'filename': filename,
                    'files': set(),
                    'original_urls': set()
                }

            url_map[base_url]['files'].add(str(content_json))
            url_map[base_url]['original_urls'].add(url)

    print(f"Found {len(url_map)} unique images to download")

    # Print category breakdown
    category_count = defaultdict(int)
    for info in url_map.values():
        category_count[info['category']] += 1

    print("\nCategory breakdown:")
    for cat, count in sorted(category_count.items()):
        print(f"  {cat}: {count} images")

    return url_map

def download_all_images(url_map):
    """Download all images to their categorized folders"""
    print("\nDownloading images...")

    success_count = 0
    fail_count = 0

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

        # Use the first original URL (with parameters) for downloading
        download_url = list(info['original_urls'])[0]

        print(f"[{i}/{len(url_map)}] Downloading to images/{category}/{filename}")

        if download_image(download_url, dest_path):
            success_count += 1
        else:
            fail_count += 1

        # Small delay to be respectful to the server
        if i % 10 == 0:
            time.sleep(1)

    print(f"\nDownload complete: {success_count} successful, {fail_count} failed")
    return success_count, fail_count

def replace_urls_in_file(file_path, url_map):
    """Replace Squarespace URLs with local paths in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        original_content = content
        replacements = 0

        # Build replacement map - map all URL variants to the local path
        replacement_map = {}
        for base_url, info in url_map.items():
            local_path = f"/images/{info['category']}/{info['filename']}"

            # Map all original URLs (with different parameters) to the same local path
            for original_url in info['original_urls']:
                replacement_map[original_url] = local_path

        # Sort by length (longest first) to avoid partial replacements
        for url in sorted(replacement_map.keys(), key=len, reverse=True):
            local_path = replacement_map[url]
            if url in content:
                content = content.replace(url, local_path)
                replacements += 1

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return replacements

        return 0
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return 0

def update_all_files(url_map):
    """Update all files to use local image paths"""
    print("\nUpdating file references...")

    files_to_update = set()
    for info in url_map.values():
        files_to_update.update(info['files'])

    total_replacements = 0
    for file_path in sorted(files_to_update):
        replacements = replace_urls_in_file(file_path, url_map)
        if replacements > 0:
            print(f"  {file_path}: {replacements} replacements")
            total_replacements += replacements

    print(f"\nTotal replacements: {total_replacements}")
    return total_replacements

def verify_migration():
    """Verify that no Squarespace CDN URLs remain"""
    print("\nVerifying migration...")

    remaining_urls = []

    for html_file in Path('.').rglob('*.html'):
        if '.git' in str(html_file):
            continue
        urls = extract_squarespace_urls(html_file)
        if urls:
            remaining_urls.append((str(html_file), len(urls)))

    for css_file in Path('.').rglob('*.css'):
        if '.git' in str(css_file):
            continue
        urls = extract_squarespace_urls(css_file)
        if urls:
            remaining_urls.append((str(css_file), len(urls)))

    if Path('content_data.json').exists():
        urls = extract_squarespace_urls('content_data.json')
        if urls:
            remaining_urls.append(('content_data.json', len(urls)))

    if remaining_urls:
        print("WARNING: Squarespace URLs still found in:")
        for file_path, count in remaining_urls:
            print(f"  {file_path}: {count} URLs")
        return False
    else:
        print("✓ All Squarespace CDN URLs successfully replaced!")
        return True

def main():
    print("=" * 60)
    print("Squarespace CDN Image Migration Script")
    print("=" * 60)

    # Step 1: Scan all files
    url_map = scan_all_files()

    if not url_map:
        print("No Squarespace URLs found!")
        return

    # Step 2: Download all images
    success, failed = download_all_images(url_map)

    if failed > 0:
        print(f"\nWarning: {failed} images failed to download")
        response = input("Continue with URL replacement anyway? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return

    # Step 3: Update all file references
    update_all_files(url_map)

    # Step 4: Verify
    verify_migration()

    print("\n" + "=" * 60)
    print("Migration complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review the changes")
    print("2. Test the website locally")
    print("3. Commit and push the changes")

if __name__ == '__main__':
    main()
