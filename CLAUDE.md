# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static HTML/CSS/JS website for the Illinois MakerLab (makerlab.illinois.edu) - the world's first business school 3D printing lab at UIUC. Migrated from Squarespace in November 2025. Contains 45+ pages and 291+ blog posts.

## Development Commands

```bash
# Local development server
python3 -m http.server 8000

# Add Illinois Brand Toolkit to all HTML files (run after adding new pages)
python3 scripts/add_toolkit.py

# Download images from Squarespace CDN
python3 scripts/download_squarespace_images.py blog/

# Replace Squarespace CDN URLs with local paths
python3 scripts/replace_squarespace_images.py blog/

# Fix remaining CDN URLs with special characters
python3 scripts/fix_remaining_cdn_images.py
```

## Deployment

Automatically deploys to GitHub Pages on push to `main` via `.github/workflows/static.yml`. No build step required - static files only.

- **Live site**: https://makerlab.illinois.edu (custom domain)
- **GitHub Pages**: https://vishalsachdev.github.io/makerlab/

## Architecture

```
makerlab/
├── *.html              # 45+ static pages (about-us, courses, contact, etc.)
├── blog/               # 291 blog posts as individual HTML files
├── courses/            # Course-specific pages (digital-making, making-things)
├── summer/             # Summer camp pages
├── css/style.css       # Single stylesheet with Illinois branding
├── js/main.js          # Vanilla JS (mobile menu, blog search/pagination, breadcrumbs)
├── images/             # All images organized by category
│   ├── blog/           # Blog post images
│   ├── staff/          # Staff photos
│   ├── birthday-parties/
│   └── partners/
├── api/                # LLM-agent friendly JSON APIs
│   ├── site-info.json  # Site metadata
│   ├── pages.json      # Page index
│   └── blog/posts.json # Blog post index
├── scripts/            # Python utilities (no external dependencies)
└── archive/            # Original Squarespace export XML
```

## Branding

Illinois brand colors defined in CSS variables:
- `--illinois-orange: #FF5F05`
- `--illinois-blue: #13294B`

Uses Illinois Campus Brand Toolkit CDN:
- CSS: `//cdn.toolkit.illinois.edu/3/toolkit.css`
- JS: `//cdn.toolkit.illinois.edu/3/toolkit.js`

## LLM Agent APIs

The site exposes structured data for AI assistants:
- `/api/site-info.json` - Contact, hours, services
- `/api/pages.json` - All pages with descriptions
- `/api/blog/posts.json` - Searchable blog index
- `/agent-guide.json` - Agent usage instructions
- `/sitemap.xml` - Complete URL inventory

## Known Issues (WEBMASTER-TODO.md)

- Google Analytics ID is placeholder (`GA_MEASUREMENT_ID` in index.html)
- Some blog posts may still reference Squarespace CDN images
- Footer copyright year may need updating

## Key Contacts

- **Director**: Dr. Vishal Sachdev
- **Executive Director**: Dr. Aric Rindfleisch
- **Email**: uimakerlab@illinois.edu
- **Location**: BIF Room 3030, UIUC
