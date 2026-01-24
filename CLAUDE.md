# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static HTML/CSS/JS website for the Illinois MakerLab (makerlab.illinois.edu) - the world's first business school 3D printing lab at UIUC. Migrated from Squarespace in November 2025. Contains 50+ pages and 300+ blog posts.

## Development Commands

```bash
# Local development server
python3 -m http.server 8000

# Add Illinois Brand Toolkit to all HTML files (run after adding new pages)
python3 scripts/add_toolkit.py
```

## Deployment

Automatically deploys to GitHub Pages on push to `main` via `.github/workflows/static.yml`. No build step required - static files only.

- **Live site**: https://makerlab.illinois.edu (custom domain, verified)
- **GitHub Pages**: https://vishalsachdev.github.io/makerlab/
- **Google Analytics**: G-R2GVFSKNPE

## Architecture

```
makerlab/
├── *.html              # 45+ static pages (about-us, courses, contact, etc.)
├── blog/               # 291 blog posts as individual HTML files
├── courses/            # Course-specific pages (digital-making [discontinued], making-things)
├── summer/             # Summer 2026 camp pages (3 camps, pricing on main page)
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
├── scripts/            # Python utilities
│   └── podio/          # Podio API integration for blog generation
└── archive/            # Archived content
    ├── pages/          # Archived HTML pages (newsletter, old camps, etc.)
    └── *.xml           # Original Squarespace export
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

## Blog Generation (Monthly Workflow)

Scripts in `scripts/podio/` extract orders from Podio to generate blog content. Run monthly:

```bash
cd scripts/podio
python extract_orders.py      # Extract recent orders
python fetch_images.py        # Download images for selected orders
```

See `scripts/podio/README.md` for full workflow. Requires `.env` with Podio credentials.

## Summer Camps (Summer 2026)

Three camps available with pricing on `summer.html`:
- **Minecraft + 3D Printing** (Ages 9+)
- **Adventures in 3D Modeling** (Ages 10-17) - Uses Fusion 360
- **Generative AI + 3D Printing** (Ages 12+)

Pricing: $250 regular, $225 early bird (until Feb 28). Schedule: 3 hrs/day, 5 days (9am-12pm or 1pm-4pm).

## Courses

- **Making Things** (BADM 331) - Active, offered every Spring
- **Digital Making** (BADM 357) - Discontinued (last offered Spring 2019)

## Known Issues (WEBMASTER-TODO.md)

- Workshops page: no active workshops scheduled (Eventbrite links removed)
- Some historical blog posts note "images no longer available" (Squarespace CDN expired)

## Key Contacts

- **Director**: Dr. Vishal Sachdev
- **Executive Director**: Dr. Aric Rindfleisch
- **Email**: uimakerlab@illinois.edu
- **Location**: BIF Room 3030, UIUC
