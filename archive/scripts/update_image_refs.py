#!/usr/bin/env python3
"""
Update all Squarespace CDN references to local image paths
"""
import os
import re
from pathlib import Path

def get_downloaded_images():
    """Get all downloaded images and their paths"""
    images = {}
    for category_dir in Path('images').iterdir():
        if category_dir.is_dir():
            for img_file in category_dir.iterdir():
                if img_file.is_file():
                    # Store as {filename: local_path}
                    images[img_file.name] = f"/images/{category_dir.name}/{img_file.name}"
    return images

def extract_squarespace_urls(file_path):
    """Extract all Squarespace CDN URLs from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        pattern = r'https://images\.squarespace-cdn\.com[^"\'\s<>]*'
        urls = re.findall(pattern, content)
        return content, urls
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, []

def get_filename_from_url(url):
    """Extract filename from Squarespace URL"""
    # Remove query parameters
    base_url = url.split('?')[0]
    # Get last part of path
    filename = base_url.split('/')[-1]
    # URL decode
    import urllib.parse
    filename = urllib.parse.unquote(filename)
    # Clean filename
    filename = re.sub(r'[^\w\-_.]', '_', filename)
    return filename

def update_file_references():
    """Update all Squarespace URLs to local paths"""
    print("Getting list of downloaded images...")
    downloaded_images = get_downloaded_images()
    print(f"Found {len(downloaded_images)} downloaded images")

    # Build URL to local path mapping
    url_to_local = {}

    print("\nScanning files for Squarespace URLs...")
    # Scan all HTML files
    all_files = list(Path('.').rglob('*.html')) + list(Path('.').rglob('*.css')) + [Path('content_data.json')]

    for file_path in all_files:
        if '.git' in str(file_path) or not file_path.exists():
            continue

        content, urls = extract_squarespace_urls(file_path)
        if not content:
            continue

        for url in urls:
            filename = get_filename_from_url(url)

            # Check if we downloaded this image
            if filename in downloaded_images:
                url_to_local[url] = downloaded_images[filename]
            # Also try with hash-based filename for generic names
            elif filename.startswith('image-asset') or filename.startswith('image_'):
                # For these, we need to match by URL hash
                import hashlib
                url_hash = hashlib.md5(url.split('?')[0].encode()).hexdigest()[:12]
                for dl_filename, local_path in downloaded_images.items():
                    if url_hash in dl_filename:
                        url_to_local[url] = local_path
                        break

    print(f"Mapped {len(url_to_local)} URLs to local images")

    # Now update all files
    print("\nUpdating file references...")
    total_replacements = 0
    files_updated = 0

    for file_path in all_files:
        if '.git' in str(file_path) or not file_path.exists():
            continue

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            original_content = content
            file_replacements = 0

            # Sort URLs by length (longest first) to avoid partial replacements
            for url in sorted(url_to_local.keys(), key=len, reverse=True):
                if url in content:
                    content = content.replace(url, url_to_local[url])
                    file_replacements += 1

            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  {file_path}: {file_replacements} replacements")
                total_replacements += file_replacements
                files_updated += 1

        except Exception as e:
            print(f"Error updating {file_path}: {e}")

    print(f"\nUpdate complete!")
    print(f"  Files updated: {files_updated}")
    print(f"  Total replacements: {total_replacements}")

    # Check for remaining Squarespace URLs
    print("\nChecking for remaining Squarespace URLs...")
    remaining_count = 0
    for file_path in all_files:
        if '.git' in str(file_path) or not file_path.exists():
            continue
        _, urls = extract_squarespace_urls(file_path)
        if urls:
            remaining_count += len(urls)

    if remaining_count > 0:
        print(f"WARNING: {remaining_count} Squarespace URLs still remain (likely from failed downloads)")
    else:
        print("✓ All Squarespace URLs successfully replaced!")

if __name__ == '__main__':
    update_file_references()
