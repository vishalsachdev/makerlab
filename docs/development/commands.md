# Development Commands

> Script reference extracted from CLAUDE.md.

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

# Fetch registration data and update session availability on website
python3 scripts/update_availability.py          # fetch + update
python3 scripts/update_availability.py --dry-run # show counts only

# Add Google Analytics tracking to all active pages (run after adding new pages)
python3 scripts/add_ga_tracking.py

# SEO maintenance (idempotent; run after adding pages)
python3 scripts/fix_internal_links.py --write
python3 scripts/add_canonical.py
python3 scripts/add_static_breadcrumbs.py
python3 scripts/add_meta_descriptions.py
python3 scripts/add_image_attributes.py
python3 -c "from generate_agent_apis import generate_sitemap_xml; generate_sitemap_xml()"
```

## Mobile UX and quote-calculator regressions

Browser tests are development-only; the site still has no build step.

```bash
cd tests
npm ci
npx playwright install chromium
npm test
```

Requires Node.js 22+ and Python 3. Tests start an ephemeral local HTTP server,
block third-party requests, and serve the pinned Three.js dependency locally for
an OBJ-upload/pricing test. No order or contact form is submitted. To use an
existing Chromium executable, set `CHROMIUM_EXECUTABLE_PATH`.

Coverage: touch dropdowns at 360/390/430px; desktop hover/click/keyboard;
Escape, outside dismissal, hidden submenu tab order, breakpoint focus; nested
relative links and JavaScript-disabled navigation; 320–1366px page/table reflow;
quote totals across all published rates, 1/2/10/99 copies, 20%/100% infill,
and the $10 campus-account minimum. This is Chromium emulation, not a physical
Safari/Android or live Podio form acceptance test.
