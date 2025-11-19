#!/usr/bin/env python3
"""
Fix remaining Squarespace CDN URLs in blog posts by matching decoded filenames
"""
import re
import os
from pathlib import Path
from urllib.parse import unquote

def get_local_image_map():
    """Build a map of cleaned filename -> local path"""
    image_map = {}
    for category in ['general', 'summer', 'blog', 'events', 'staff']:
        dir_path = Path(f'images/{category}')
        if dir_path.exists():
            for img_file in dir_path.iterdir():
                if img_file.is_file():
                    filename = img_file.name
                    # Store original
                    image_map[filename.lower()] = f'../images/{category}/{filename}'
                    image_map[filename] = f'../images/{category}/{filename}'
                    # Store cleaned version (replace special chars with _)
                    cleaned = re.sub(r'[^\w\-_.]', '_', filename)
                    if cleaned != filename:
                        image_map[cleaned.lower()] = f'../images/{category}/{filename}'
                        image_map[cleaned] = f'../images/{category}/{filename}'
    return image_map

def extract_and_clean_filename(url):
    """Extract filename from URL and clean it"""
    # Remove query parameters
    url_clean = url.split('?')[0]
    # Get filename
    filename = url_clean.split('/')[-1]
    # URL decode (may need multiple passes)
    decoded = unquote(unquote(filename))  # Handle double encoding
    # Clean special characters
    cleaned = re.sub(r'[^\w\-_.]', '_', decoded)
    return decoded, cleaned

def fix_file(file_path, image_map):
    """Fix Squarespace URLs in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        replacements = 0
        
        # Find all Squarespace CDN URLs
        pattern = r'https?://images\.squarespace-cdn\.com[^\s"\'<>\)]+'
        urls = re.findall(pattern, content)
        
        for url in urls:
            decoded, cleaned = extract_and_clean_filename(url)
            local_path = None
            
            # Try multiple matching strategies
            # 1. Try exact decoded filename
            if decoded in image_map:
                local_path = image_map[decoded]
            # 2. Try cleaned filename
            elif cleaned in image_map:
                local_path = image_map[cleaned]
            # 3. Try lowercase versions
            elif decoded.lower() in image_map:
                local_path = image_map[decoded.lower()]
            elif cleaned.lower() in image_map:
                local_path = image_map[cleaned.lower()]
            # 4. Try partial match (for cases like "Image September 26" -> "Image_September_26")
            else:
                # Remove common patterns and try again
                simplified = re.sub(r'[^\w]', '_', decoded).replace('__', '_').strip('_')
                if simplified.lower() in image_map:
                    local_path = image_map[simplified.lower()]
            
            if local_path:
                content = content.replace(url, local_path)
                replacements += 1
                print(f"  Matched: {decoded[:50]} -> {local_path}")
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return replacements
        
        return 0
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def main():
    print("Building local image map...")
    image_map = get_local_image_map()
    print(f"Found {len(image_map)} local image mappings")
    
    print("\nScanning blog posts for remaining Squarespace URLs...")
    blog_files = list(Path('blog').glob('*.html'))
    
    total_replacements = 0
    files_updated = 0
    
    for file_path in blog_files:
        replacements = fix_file(file_path, image_map)
        if replacements > 0:
            files_updated += 1
            total_replacements += replacements
            print(f"{file_path}: {replacements} replacements")
    
    print(f"\nDone! Updated {files_updated} files with {total_replacements} total replacements")

if __name__ == '__main__':
    main()

