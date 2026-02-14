# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static HTML/CSS/JS website for the Illinois MakerLab (makerlab.illinois.edu) - the world's first business school 3D printing lab at UIUC. Migrated from Squarespace in November 2025. Contains 32 active pages and 300 blog posts.

## Development Commands

```bash
# Local development server
python3 -m http.server 8000

# Add Illinois Brand Toolkit to all HTML files (run after adding new pages)
python3 scripts/add_toolkit.py

# Bulk update navigation across all HTML files (after editing nav templates)
python3 scripts/update_nav.py

# Regenerate blog post index with dates, excerpts, and auto-tags
python3 scripts/regenerate_blog_index.py

# Fix accessibility: add skip-to-content links to all pages
python3 scripts/add_skip_link.py

# Fix accessibility: add alt text to blog images with empty alt=""
python3 scripts/fix_blog_alt_text.py

# Fix accessibility: add alt text to blog images missing alt attribute entirely
python3 scripts/fix_missing_alt.py

# Fix accessibility: add title attributes to iframes
python3 scripts/fix_iframe_titles.py

# Add Schema.org BlogPosting + BreadcrumbList to blog posts
python3 scripts/add_blog_schema.py

# Add Schema.org BreadcrumbList to static pages
python3 scripts/add_breadcrumbs.py
```

## Deployment

Automatically deploys to GitHub Pages on push to `main` via `.github/workflows/static.yml`. No build step required - static files only.

- **Live site**: https://makerlab.illinois.edu (custom domain, verified)
- **GitHub Pages**: https://vishalsachdev.github.io/makerlab/
- **Google Analytics**: G-R2GVFSKNPE

## Architecture

```
makerlab/
├── *.html              # 32 active pages (about-us, courses, contact, etc.)
├── blog/               # 300 blog posts as individual HTML files
├── courses/            # Course-specific pages (making-things active)
├── summer/             # Summer 2026 camp pages (3 camps, pricing on main page)
├── css/style.css       # Single stylesheet with Illinois branding
├── js/main.js          # Vanilla JS (mobile menu, blog search/pagination, keyboard nav, ARIA)
├── images/             # All images organized by category
│   ├── blog/           # Blog post images
│   ├── staff/          # Staff photos
│   ├── birthday-parties/
│   └── partners/
├── api/                # LLM-agent friendly JSON APIs
│   ├── site-info.json  # Site metadata, contact, services
│   ├── pages.json      # Page index with descriptions
│   └── blog/posts.json # Blog post index
├── llms.txt            # Plain text summary for AI agents
├── agent-guide.json    # Detailed AI agent instructions
├── api/openapi.yaml    # OpenAPI 3.0 spec documenting all JSON endpoints
├── scripts/            # Python utilities
│   ├── podio/          # Podio API integration for blog generation
│   ├── update_nav.py   # Bulk update navigation across all HTML files
│   ├── regenerate_blog_index.py  # Rebuild posts.json with dates/tags from HTML
│   ├── add_skip_link.py          # Add skip-to-content links to all pages
│   ├── fix_blog_alt_text.py      # Fix empty alt="" on blog images
│   ├── fix_missing_alt.py        # Fix missing alt attributes on blog images
│   ├── fix_iframe_titles.py      # Add title attributes to iframes
│   ├── add_blog_schema.py        # Add BlogPosting + BreadcrumbList JSON-LD to blog posts
│   └── add_breadcrumbs.py        # Add BreadcrumbList JSON-LD to static pages
└── archive/            # Archived content
    ├── pages/          # Archived HTML pages (newsletter, old camps, etc.)
    └── *.xml           # Original Squarespace export
```

## Navigation

Dropdown navigation with two menus:
- **About** → About Us, Lab Staff, Partners, FAQ
- **What We Offer** → Services & Pricing, Summer Camps, Birthday Parties, Workshops, Courses, Resources

Top-level links: Home, About▾, What We Offer▾, Order Online, Blog, Lab Hours, Contact

To update navigation site-wide, edit the templates in `scripts/update_nav.py` (NAV_ROOT, NAV_SUBDIR, NAV_ARCHIVE for different path depths) and run:
```bash
python3 scripts/update_nav.py
```
Nav templates include ARIA attributes for accessibility. When editing, preserve `aria-haspopup`, `aria-expanded`, `role="menu"`, and `role="menuitem"` attributes.

## Branding

Illinois brand colors defined in CSS variables:
- `--illinois-orange: #FF5F05`
- `--illinois-blue: #13294B`

Uses Illinois Campus Brand Toolkit CDN:
- CSS: `//cdn.toolkit.illinois.edu/3/toolkit.css`
- JS: `//cdn.toolkit.illinois.edu/3/toolkit.js`

## LLM Agent Support

The site is optimized for AI agents (ChatGPT, Claude, Perplexity, etc.):

| Endpoint | Purpose |
|----------|---------|
| `/llms.txt` | Plain text summary - quick site overview for agents |
| `/agent-guide.json` | Detailed usage instructions, common queries, response guidelines |
| `/api/site-info.json` | Contact, hours, services, leadership |
| `/api/pages.json` | 32 active pages with unique descriptions + archived pages list |
| `/api/blog/posts.json` | Searchable blog index (300 posts, 2012-2025) |
| `/api/openapi.yaml` | OpenAPI 3.0 spec for all JSON endpoints |
| `/sitemap.xml` | Complete URL inventory (317 URLs) |
| `/robots.txt` | Explicitly allows all LLM crawlers (GPTBot, Claude-Web, PerplexityBot, etc.) |

Schema.org JSON-LD structured data on key pages:
- `index.html`: Organization with services
- `faq.html`: FAQPage for rich results
- `lab-hours.html`: LocalBusiness + OpeningHoursSpecification
- `pricingservices.html`: Service @graph (3D Printing, Design, Tutoring) with Offer pricing
- `summer.html`: EducationEvent @graph (3 camps) with Offer pricing
- `contact.html`: LocalBusiness + ContactPoint
- `courses/making-things.html`: Course + CourseInstance
- All pages: BreadcrumbList
- All blog posts: BlogPosting

## Blog Generation (Monthly Workflow)

Scripts in `scripts/podio/` extract orders from Podio to generate blog content. Run monthly:

```bash
cd scripts/podio
python extract_orders.py      # Extract recent orders
python fetch_images.py        # Download images for selected orders
```

See `scripts/podio/README.md` for full workflow. Requires `.env` with Podio credentials.

## Summer Camps (Summer 2026)

Five camps available across 8 weeks (Jun 1 – Jul 31, no camp week of Jun 29–Jul 3). Pricing on `summer.html`:
- **Minecraft + 3D Printing** (Ages 10+) — flagship, 8 sessions
- **Adventures in 3D Modeling** (Ages 10-17) - Uses Fusion 360, 2 sessions
- **Generative AI + 3D Printing** (Ages 12+) — 2 sessions
- **Build Your Own Robot Arm** (Ages 12+) — NEW, SO-ARM100, max 5 campers, 2 sessions
- **AI Robotics with Reachy Mini** (Ages 12+) — NEW, Reachy Mini Lite, max 5 campers, 2 sessions

Pricing: $250 regular, $225 early bird (until March 15). Schedule: 3 hrs/day, 5 days (9am-12pm or 1pm-4pm).

Registration: https://appserv7.admin.uillinois.edu/FormBuilderSurvey/Survey/gies_college_of_business/gies_fab_lab/summer_2026/

Refund Policy: All camps have a $20 non-refundable deposit. Up to 21 days before camp: full refund minus deposit. 20-8 days before: half refund minus deposit. 7 days or less: no refund. Campers may switch sessions at no cost if seats available.

## Courses

- **Making Things** (BADM 331) - Active, offered every Spring
- **Digital Making** (BADM 357) - Discontinued (last offered Spring 2019)

## Accessibility

The site follows WCAG 2.1 AA practices:
- Skip-to-content link on all pages (`<a href="#main-content" class="skip-link">`)
- ARIA attributes on nav dropdowns (`aria-haspopup`, `aria-expanded`, `role="menu"`, `role="menuitem"`)
- Keyboard navigation for dropdown menus (Enter/Space/Escape/Arrow keys) in `js/main.js`
- `aria-current="page"` set dynamically on active nav link
- All blog images have `alt` text (either original or generated from post title)
- All iframes have `title` attributes
- Proper heading hierarchy (h1 → h2, no gaps) on all pages

## Known Issues (WEBMASTER-TODO.md)

- Workshops page: no active workshops scheduled (Eventbrite links removed)
- Some historical blog posts note "images no longer available" (Squarespace CDN expired)

## Key Contacts

- **Director**: Dr. Vishal Sachdev
- **Executive Director**: Dr. Aric Rindfleisch
- **Email**: uimakerlab@illinois.edu
- **Location**: BIF Room 3030, UIUC
