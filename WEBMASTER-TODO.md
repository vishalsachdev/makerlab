# MakerLab Website - Webmaster TODO

**Updated:** February 12, 2026
**Site:** makerlab.illinois.edu

---

## Recently Completed (Feb 2026)

### Schema.org Structured Data
- [x] **LocalBusiness + hours on lab-hours.html** - OpeningHoursSpecification enables Google Knowledge Panel hours display
- [x] **Service pricing on pricingservices.html** - 3D Printing, Design, Tutoring services with per-user-type pricing
- [x] **EducationEvent on summer.html** - 3 summer camps with early bird/regular pricing offers
- [x] **Course schema on courses/making-things.html** - Course + CourseInstance for BADM 331
- [x] **LocalBusiness + ContactPoint on contact.html** - Contact info structured for search results
- [x] **BlogPosting on all 300 blog posts** - Added via `scripts/add_blog_schema.py`
- [x] **BreadcrumbList on all pages** - Static pages via `scripts/add_breadcrumbs.py`, blog via `add_blog_schema.py`

### Accessibility (WCAG 2.1 AA)
- [x] **Skip-to-content link on all 341 HTML files** - `<a href="#main-content" class="skip-link">` via `scripts/add_skip_link.py`
- [x] **ARIA attributes on nav dropdowns** - `aria-haspopup`, `aria-expanded`, `role="menu"`, `role="menuitem"`
- [x] **Keyboard navigation for dropdown menus** - Enter/Space to open, Escape to close, Arrow keys to navigate
- [x] **`aria-current="page"` on active nav link** - Set dynamically in `js/main.js`
- [x] **Fixed heading hierarchy** - lab-hours.html (h3 to h2), faq.html (12x h3 to h2 with CSS sizing)
- [x] **Added `title` to iframes** - 12 files with untitled iframes fixed via `scripts/fix_iframe_titles.py`
- [x] **Added `aria-label` to autoplay video** - pricingservices.html
- [x] **Fixed empty `alt=""` on 57 blog images** - Set to "Image from [post title]" via `scripts/fix_blog_alt_text.py`
- [x] **Fixed missing `alt` on 78 blog images** - Added alt text via `scripts/fix_missing_alt.py`

### API Data Quality
- [x] **Regenerated blog/posts.json with real dates** - Was all showing 2025-11-18 (export date); now shows actual publication dates
- [x] **Clean excerpts in posts.json** - Was containing HTML scaffolding; now plain text summaries
- [x] **Auto-tagged all 300 blog posts** - Using keyword analysis (3D Printing, Education, Community, etc.)
- [x] **Created OpenAPI spec** - `api/openapi.yaml` (OpenAPI 3.0) documenting all JSON endpoints
- [x] **Fixed agent-guide.json** - Page count 41 to 32, Digital Making marked discontinued, removed `/makerlab/` URL prefixes
- [x] **Fixed site-info.json** - Page count 45 to 32, updated course Q&A, added OpenAPI endpoint
- [x] **Updated llms.txt** - Added OpenAPI reference, pricing Q&A, updated date
- [x] **Added OAI-SearchBot to robots.txt** - Now 10 LLM crawlers explicitly welcomed
- [x] **Updated sitemap.xml** - Added openapi.yaml entry, refreshed lastmod dates

### New Utility Scripts
All scripts are in `scripts/` and can be re-run safely (idempotent):

| Script | Purpose | When to Run |
|--------|---------|-------------|
| `regenerate_blog_index.py` | Rebuilds `api/blog/posts.json` from blog HTML | After adding/editing blog posts |
| `add_skip_link.py` | Adds skip-to-content accessibility link | After adding new pages |
| `add_blog_schema.py` | Adds BlogPosting + BreadcrumbList JSON-LD | After adding new blog posts |
| `add_breadcrumbs.py` | Adds BreadcrumbList JSON-LD to static pages | After adding new pages |
| `fix_blog_alt_text.py` | Fixes `alt=""` (empty) on blog images | After adding blog posts with images |
| `fix_missing_alt.py` | Fixes missing `alt` attribute on blog images | After adding blog posts with images |
| `fix_iframe_titles.py` | Adds `title` to untitled iframes | After embedding new iframes |
| `update_nav.py` | Propagates nav changes to all ~341 HTML files | After editing navigation |

---

## Completed (Jan 25, 2026)

### AI Agent Readiness
- [x] **Created llms.txt** - Plain text summary for AI agents at root
- [x] **Updated all URLs to custom domain** - agent-guide.json, site-info.json, robots.txt, sitemap.xml now use makerlab.illinois.edu
- [x] **Added meaningful descriptions to pages.json** - All 32 active pages now have unique, descriptive summaries
- [x] **Added FAQPage schema to faq.html** - Schema.org structured data for search engines and AI
- [x] **Expanded FAQ content** - Added 5 new common questions (ordering, summer camps, birthday parties, courses, contact)
- [x] **Updated robots.txt** - Added llms.txt to allowed paths for agents
- [x] **Updated agent-guide.json** - Added llms.txt endpoint documentation

### Content & Data Accuracy
- [x] **Fixed Digital Making course status** - Removed discontinued BADM 357 from active courses, updated to Making Things (BADM 331) only
- [x] **Cleaned up pages.json** - Separated active (32), archived (4), and legacy (8) pages
- [x] **Updated homepage structured data** - Fixed URL, corrected course info in JSON-LD
- [x] **Added main.js to index.html** - Was missing script include

### Code Quality
- [x] **Consolidated CSS duplication** - Merged 4 duplicate .reviews-grid definitions into single clean section (~120 lines removed)

---

## Previously Fixed

- [x] **Missing `</script>` tag in index.html** - Fixed broken HTML
- [x] **Lab hours updated** - Spring 2026 hours: Mon 2-5pm, Tue/Thu/Fri 2-7pm, Wed CLOSED
- [x] **Sitemap cleaned** - Removed 19 orphaned page entries (now 317 valid URLs)
- [x] **Custom domain verified** - makerlab.illinois.edu DNS verified with GitHub Pages
- [x] **Footer years updated** - Main site pages updated to 2026
- [x] **Squarespace CDN removed** - All external CDN dependencies removed
- [x] **Newsletter page archived** - No longer sending newsletters
- [x] **Google Analytics configured** - `G-R2GVFSKNPE` (Jan 23, 2026)

---

## Seasonal Maintenance

### Each Semester
- [ ] **Update lab hours** in `lab-hours.html` (both visible content AND the JSON-LD `OpeningHoursSpecification` `validFrom`/`validThrough` dates)
- [ ] **Update `api/site-info.json`** hours reference if needed

### Each Month (if new blog posts added)
- [ ] Run `python3 scripts/regenerate_blog_index.py` to rebuild `api/blog/posts.json`
- [ ] Run `python3 scripts/add_blog_schema.py` to add Schema.org markup to new posts

### When Adding New Pages
- [ ] Run `python3 scripts/update_nav.py` to propagate navigation
- [ ] Run `python3 scripts/add_skip_link.py` to add accessibility link
- [ ] Run `python3 scripts/add_breadcrumbs.py` to add breadcrumb schema
- [ ] Add the page to `api/pages.json` and `sitemap.xml`

---

## Site Structure Reference

```
makerlab/
├── index.html          # Homepage (Organization schema)
├── 32 page files       # Main content pages
├── blog/               # 300 blog posts (BlogPosting + BreadcrumbList schema)
├── courses/            # Course pages (Making Things active, Digital Making archived)
├── summer/             # Summer 2026 camp pages (EducationEvent schema)
├── api/                # JSON APIs for LLM agents
│   ├── site-info.json  # Contact, hours, services, leadership
│   ├── pages.json      # Page index with descriptions
│   ├── blog/posts.json # 300 blog posts with dates, tags, excerpts
│   └── openapi.yaml    # OpenAPI 3.0 spec for all endpoints
├── css/style.css       # Main stylesheet (Illinois branding)
├── js/main.js          # Vanilla JS (mobile menu, search, keyboard nav, ARIA)
├── images/             # All images organized by category
├── scripts/            # Python utility scripts (see table above)
├── llms.txt            # Plain text summary for AI agents
├── agent-guide.json    # Detailed AI agent instructions
├── sitemap.xml         # 317 URLs
└── robots.txt          # Allows 10 LLM crawlers
```

---

## Contact

Questions? Reach out to Vishal Sachdev or check the repository at:
https://github.com/vishalsachdev/makerlab
