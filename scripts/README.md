# Scripts

This directory contains utility scripts for managing and maintaining the Illinois MakerLab website.

## Image Management Scripts

### `download_squarespace_images.py`
Downloads images from Squarespace CDN and organizes them into the correct folders.

**Usage:**
```bash
# Download images for blog posts
python3 scripts/download_squarespace_images.py blog/

# Download images site-wide
python3 scripts/download_squarespace_images.py

# Dry run (preview what would be downloaded)
python3 scripts/download_squarespace_images.py blog/ --dry-run
```

**Features:**
- Scans HTML files for Squarespace CDN URLs
- Categorizes images based on file location (blog, summer, events, etc.)
- Downloads images to appropriate folders (`images/blog/`, `images/summer/`, etc.)
- Skips images that already exist locally
- Handles duplicate filenames automatically

### `replace_squarespace_images.py`
Replaces Squarespace CDN image URLs with local GitHub paths in HTML files.

**Usage:**
```bash
# Replace images in all blog posts
python3 scripts/replace_squarespace_images.py blog/

# Replace images site-wide
python3 scripts/replace_squarespace_images.py

# Replace images in a specific file
python3 scripts/replace_squarespace_images.py blog/some-post.html
```

**Features:**
- Maps local images by filename
- Handles URL-encoded filenames
- Replaces both `http://` and `https://` Squarespace URLs
- Updates image paths to use local GitHub references

### `fix_remaining_cdn_images.py`
Fixes remaining Squarespace CDN URLs by matching decoded filenames (handles special cases).

**Usage:**
```bash
python3 scripts/fix_remaining_cdn_images.py
```

**Features:**
- Handles URL-encoded filenames (spaces, special characters)
- Matches Chinese character filenames
- Cleans and matches filenames with special characters
- Updates paths to use `../images/` for blog subdirectory

## Content Processing Scripts

### `parse_export.py`
Parses the Squarespace/WordPress XML export file to extract content.

**Usage:**
```bash
python3 scripts/parse_export.py
```

**Features:**
- Parses `Squarespace-Wordpress-Export-11-18-2025.xml`
- Extracts site information, posts, and pages
- Processes content for migration

## Integration Scripts

### `add_toolkit.py`
Adds Illinois Campus Brand Toolkit CDN resources to every HTML file in the project.

**Usage:**
```bash
python3 scripts/add_toolkit.py
```

**Features:**
- Adds Brand Toolkit CSS and JS to all HTML files
- Skips files that already have toolkit resources
- Ensures consistent branding across all pages

**Note:** Run this script whenever you regenerate or add HTML files to ensure every page loads the toolkit CSS/JS before the MakerLab assets.

## Workflow Examples

### Complete Image Migration Workflow

1. **Download images from Squarespace:**
   ```bash
   python3 scripts/download_squarespace_images.py blog/
   ```

2. **Replace CDN URLs with local paths:**
   ```bash
   python3 scripts/replace_squarespace_images.py blog/
   ```

3. **Fix any remaining URLs with special characters:**
   ```bash
   python3 scripts/fix_remaining_cdn_images.py
   ```

### Adding Brand Toolkit to New Pages

```bash
python3 scripts/add_toolkit.py
```

## Script Dependencies

All scripts use Python 3 standard library only:
- `pathlib` - File path handling
- `re` - Regular expressions
- `urllib.parse` - URL parsing and decoding
- `urllib.request` - HTTP requests (download_squarespace_images.py only)

No external dependencies required!

## Notes

- All scripts are designed to be run from the project root directory
- Scripts preserve existing files and skip duplicates when possible
- Image paths use relative paths (`../images/`) for blog posts in subdirectories
- Scripts handle both `http://` and `https://` Squarespace CDN URLs

