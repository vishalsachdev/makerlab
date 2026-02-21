# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static HTML/CSS/JS website for the Illinois MakerLab (makerlab.illinois.edu) - the world's first business school 3D printing lab at UIUC. Migrated from Squarespace in November 2025. Contains 32 active pages and 301 blog posts.

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

# Validate AI agent files match actual site content (runs in CI on every push)
python3 scripts/validate_agent_data.py

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
├── blog/               # 301 blog posts as individual HTML files
├── courses/            # Course-specific pages (making-things active)
├── summer/             # Summer 2026 camp pages (5 camps, pricing on main page)
├── css/style.css       # Single stylesheet with Illinois branding
├── js/main.js          # Vanilla JS (mobile menu, blog search/pagination, keyboard nav, ARIA)
├── images/             # All images organized by category
│   ├── blog/           # Blog post images
│   ├── staff/          # Staff photos
│   ├── birthday-parties/
│   ├── campaigns/      # Marketing campaign assets (e.g., chambanamoms-2026/)
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
- **Services** → Services & Pricing, Summer Camps, Birthday Parties, Workshops, Courses, Resources

Top-level links: About▾, Services▾, Order, Summer Camps, Lab Hours, Contact

To update navigation site-wide, edit the templates in `scripts/update_nav.py` (NAV_ROOT, NAV_SUBDIR, NAV_ARCHIVE for different path depths) and run:
```bash
python3 scripts/update_nav.py
```
Nav templates include ARIA attributes for accessibility. When editing, preserve `aria-haspopup`, `aria-expanded`, `role="menu"`, and `role="menuitem"` attributes.

Footer has four sections: Illinois MakerLab (address), Services & Pricing (quick links including Summer Camps), Resources, Connect (social + contact). Footer links also updated by `update_nav.py`.

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
| `/api/blog/posts.json` | Searchable blog index (301 posts, 2012-2026) |
| `/api/openapi.yaml` | OpenAPI 3.0 spec for all JSON endpoints |
| `/sitemap.xml` | Complete URL inventory (319 URLs) |
| `/robots.txt` | Explicitly allows all LLM crawlers (GPTBot, Claude-Web, PerplexityBot, etc.) |

Schema.org JSON-LD structured data on key pages:
- `index.html`: Organization with services
- `faq.html`: FAQPage for rich results
- `lab-hours.html`: LocalBusiness + OpeningHoursSpecification
- `pricingservices.html`: Service @graph (3D Printing, Design, Tutoring) with Offer pricing
- `summer.html`: EducationEvent @graph (5 camps) with Offer pricing
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

Registration: https://appserv7.admin.uillinois.edu/FormBuilderSurvey/Survey/gies_college_of_business/illinois_makerlab/summer_2026/

Add-ons: Lunch hour supervision (12:00–1:00 PM) $10/day, late pickup at 5:00 PM $10/day. Computers provided (MakerLab iMacs). Minecraft accounts provided for Minecraft camp.

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

## GitHub Issue Templates

| Template | Purpose |
|----------|---------|
| `website-fix.yml` | General website bug reports and fixes |
| `update-instagram-feed.yml` | Update Instagram embed on homepage |
| `update-staff-profile.yml` | Add or update staff member profiles |
| `new-blog-post.yml` | Employee-submitted blog posts (title, content, images, publish date) |

## Known Issues (WEBMASTER-TODO.md)

- Workshops page: no active workshops scheduled (Eventbrite links removed)
- Some historical blog posts note "images no longer available" (Squarespace CDN expired)

## Key Contacts

- **Director**: Dr. Vishal Sachdev
- **Executive Director**: Dr. Aric Rindfleisch
- **Email**: uimakerlab@illinois.edu
- **Location**: BIF Room 3030, UIUC

## Current Focus

Email auto-reply automation (monitoring draft runs, then enabling send mode).

## Roadmap

- [x] Squarespace migration (Nov 2025)
- [x] SEO: Schema.org JSON-LD on key pages, breadcrumbs, BlogPosting on all posts
- [x] Accessibility: skip links, ARIA nav, keyboard nav, heading hierarchy, alt text, iframe titles
- [x] LLM agent support: llms.txt, agent-guide.json, OpenAPI spec, posts.json with real dates/tags
- [x] ChambanaMoms campaign text deliverables
- [ ] ChambanaMoms campaign images (2 social posts, round-up thumbnail, Facebook album photo)
- [ ] Podio migration: drop GlobiMail, evaluate full migration to Microsoft stack
- [ ] Monthly blog generation workflow from Podio orders
- [x] Commit Podio audit/automation scripts
- [x] Email auto-reply GitHub Action (Podio → OpenAI → SendGrid pipeline)
- [ ] Monitor draft runs, then enable send mode for auto-replies
- [ ] Build approve-then-send flow (optional enhancement)

## Session Log

- **2026-02-20**: Session start. Added roadmap sections to CLAUDE.md.
- **2026-02-21**: Built and deployed email auto-reply automation. GitHub Action (every 6h, draft mode) with manual dispatch (send/dry-run + configurable lookback). Committed 13 files: workflow, auto_reply_emails.py, smtp_sender.py, website_context.py, Podio audit scripts. Set 6 GitHub secrets. Codex review caught 2 bugs (NEEDS_HUMAN mis-tagging, duplicate drafts) — fixed and pushed. Tested dry-run with 30-day lookback: 1 email classified correctly as NEEDS_HUMAN.
