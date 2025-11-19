#!/usr/bin/env python3
"""
Fix all HTML files to use relative paths instead of /makerlab/ absolute paths
"""
import os
import re
from pathlib import Path

def get_relative_prefix(file_path):
    """Determine the relative path prefix based on file location"""
    # Count directory depth (how many levels deep from root)
    path_parts = Path(file_path).parts
    depth = len(path_parts) - 1  # Subtract 1 for filename
    
    if depth == 0:
        # Root level: no prefix needed
        return ''
    elif depth == 1:
        # One level deep (e.g., blog/, courses/, summer/): go up one level
        return '../'
    elif depth == 2:
        # Two levels deep (e.g., blog/some-post.html, courses/some-course.html): go up two levels
        return '../../'
    else:
        # For deeper nesting, calculate accordingly
        return '../' * depth

def fix_file_paths(file_path):
    """Replace /makerlab/ paths with relative paths in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get the relative prefix for this file
        prefix = get_relative_prefix(file_path)
        
        # Replace /makerlab/ with the appropriate relative prefix
        # But be careful not to replace URLs that are already relative or external
        # Pattern: match /makerlab/ but not //makerlab/ (protocol-relative) or http://makerlab
        new_content = re.sub(r'(?<!:)//makerlab/', prefix, content)
        new_content = re.sub(r'(?<!http)(?<!https)/makerlab/', prefix, new_content)
        
        # Only write if content changed
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Find and fix all HTML files"""
    html_files = []
    
    # Find all HTML files
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and common build/cache directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                html_files.append(file_path)
    
    print(f"Found {len(html_files)} HTML files")
    print("Fixing paths...")
    
    fixed_count = 0
    for file_path in html_files:
        if fix_file_paths(file_path):
            fixed_count += 1
            if fixed_count % 50 == 0:
                print(f"  Fixed {fixed_count} files...")
    
    print(f"\n✓ Fixed {fixed_count} files")
    print("✓ Done!")

if __name__ == '__main__':
    main()

