#!/usr/bin/env python3
"""
Replace all Squarespace CDN image URLs with local GitHub paths
"""
import re
import os
from pathlib import Path
from urllib.parse import unquote

def get_local_image_map():
    """Build a map of filename -> local path"""
    image_map = {}
    for category in ['general', 'summer', 'blog', 'events', 'staff']:
        dir_path = Path(f'images/{category}')
        if dir_path.exists():
            for img_file in dir_path.iterdir():
                if img_file.is_file():
                    # Store both original and lowercase versions
                    filename = img_file.name
                    image_map[filename.lower()] = f'images/{category}/{filename}'
                    image_map[filename] = f'images/{category}/{filename}'
    return image_map

def extract_filename_from_url(url):
    """Extract filename from Squarespace URL"""
    # Remove query parameters
    url = url.split('?')[0]
    # Get the last part after the last /
    filename = url.split('/')[-1]
    # URL decode
    filename = unquote(filename)
    return filename

def replace_images_in_file(file_path, image_map):
    """Replace Squarespace URLs with local paths in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        replacements = 0
        
        # Find all Squarespace CDN URLs (both http and https)
        # Match URLs in src, href, and other attributes
        patterns = [
            r'https://images\.squarespace-cdn\.com[^\s"\'<>\)]+',
            r'http://images\.squarespace-cdn\.com[^\s"\'<>\)]+',
        ]
        
        all_urls = set()
        for pattern in patterns:
            urls = re.findall(pattern, content)
            all_urls.update(urls)
        
        # Sort by length (longest first) to avoid partial replacements
        for url in sorted(all_urls, key=len, reverse=True):
            filename = extract_filename_from_url(url)
            local_path = None
            
            # Try exact match first
            if filename in image_map:
                local_path = image_map[filename]
            # Try lowercase match
            elif filename.lower() in image_map:
                local_path = image_map[filename.lower()]
            
            if local_path:
                # Replace all occurrences of this URL
                count = content.count(url)
                content = content.replace(url, local_path)
                replacements += count
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return replacements
        
        return 0
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def main():
    import sys
    
    # Allow targeting specific directory (e.g., blog/)
    target_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print("Building local image map...")
    image_map = get_local_image_map()
    print(f"Found {len(image_map)} local images")
    
    print(f"\nScanning HTML files for Squarespace URLs in {target_dir}...")
    if target_dir == '.':
        html_files = list(Path('.').rglob('*.html'))
    else:
        html_files = list(Path(target_dir).rglob('*.html'))
    
    total_replacements = 0
    files_updated = 0
    
    for file_path in html_files:
        if '.git' in str(file_path) or 'node_modules' in str(file_path):
            continue
        
        replacements = replace_images_in_file(file_path, image_map)
        if replacements > 0:
            files_updated += 1
            total_replacements += replacements
            print(f"  {file_path}: {replacements} replacements")
    
    print(f"\nDone! Updated {files_updated} files with {total_replacements} total replacements")

if __name__ == '__main__':
    main()

