# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static HTML/CSS/JS website for the Illinois MakerLab (makerlab.illinois.edu) - the world's first business school 3D printing lab at UIUC. Migrated from Squarespace in November 2025. Contains 32 active pages and 301 blog posts.

## Development Commands

Local server: `python3 -m http.server 8000`. Validate before push: `python3 scripts/validate_agent_data.py`.
**Full script reference** (toolkit/nav/blog-index/accessibility/schema/availability/GA helpers): [docs/development/commands.md](docs/development/commands.md).

## Deployment

Automatically deploys to GitHub Pages on push to `main` (legacy branch mode — no Actions workflow needed). No build step required - static files only. Run `python3 scripts/validate_agent_data.py` locally before pushing.

- **Live site**: https://makerlab.illinois.edu (custom domain, verified)
- **GitHub Pages**: https://vishalsachdev.github.io/makerlab/
- **Google Analytics**: G-R2GVFSKNPE (all active pages — run `scripts/add_ga_tracking.py` after adding new pages)

## Data & Privacy (PII) — this repo is PUBLIC

**Never commit or push PII.** The repo is public (GitHub Pages, Free plan — can't go private without taking the live site down). PII = parent/camper names+emails+phones, addresses, minor DOBs, and IPay/payment data (transaction IDs, payment reference IDs).

- Registration dumps, cancellation logs, refund memos, and recipient lists are **local-only** and gitignored: `data/cancellations.csv`, `data/early-bird-registrations.csv`, `data/refund-memo-*.md`, `data/registrations-*`, `data/*ReportDump*`, `data/*.xlsx`, `data/*recipients*`.
- FormBuilder report exports (`Registrations_ReportDump_*.xlsx`, `ReportDump_*.csv`) contain payment data — keep them **out of the repo** (store in `~/Downloads` or a non-repo folder), never under `data/`.
- Before any commit touching `data/`, run `git status` and confirm no PII file is staged. `data/summer-camps-2026.json` (camp config) is the only safe-to-commit file in `data/`.
- **History was purged** of previously-committed PII on 2026-05-30 (git-filter-repo + force-push). Anything public before then is already exposed — treat those emails/IPay IDs as compromised.

## Architecture

Static site: `*.html` pages at root, `blog/` (301 posts), `courses/`, `summer/`, `css/`, `js/`, `images/`, `api/` (LLM-agent JSON), `scripts/` (Python utilities), `archive/`.
**Full directory map**: [docs/development/architecture.md](docs/development/architecture.md).

⚠️ **Never run `archive/generate_site.py`** — it's the archived one-time Squarespace migration generator and will overwrite current HTML files from stale JSON. All content is edited directly in HTML now.

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
| `/api/pages.json` | 31 active pages with unique descriptions + archived pages list |
| `/api/blog/posts.json` | Searchable blog index (301 posts, 2012-2026) |
| `/api/openapi.yaml` | OpenAPI 3.0 spec for all JSON endpoints |
| `/sitemap.xml` | Complete URL inventory (318 URLs) |
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

Source of truth for camp operations data is `data/summer-camps-2026.json` — do not hand-edit duplicated camp facts. Regenerate + validate:
```bash
python3 scripts/sync_summer_data.py
python3 scripts/validate_agent_data.py
```
**Full ops runbook** (FormBuilder refunds/cancellations, token renewal, capacity gotchas, business-office refund memos): moved to the **private makerlab-camps repo** — `docs/operations/summer-camp-operations.md` in `vishalsachdev/makerlab-camps` (local: `~/admin/makerlab-camps`). A pointer stub remains at [docs/operations/summer-camp-operations.md](docs/operations/summer-camp-operations.md). File future cancellation/ops issues in makerlab-camps, not here.

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

**Fall 2026, lab open since Mon Aug 31.** Hours Mon/Fri 1–7, Tue/Thu 2–7, Wed 4–7 PM; gurus Bayu (ops lead, Mon–Thu 4–7, Fri 1–7), Aldo Villanueva (Tue/Thu 2–5), Sahib Bedi (Mon 1–5). Hours are hand-edited in five places (see 2026-09-01 log) and carry dated notices via `specialOpeningHoursSpecification` + `hours.notices[]`; update all five together and bump the freshness stamps. Open operational items: the **Thera-Solutions client job** (mini redesign quote + 25 originals) is with Bayu/Sahib, and several Aug 4 threads (exec summary, feedback campaign, recap post) have not been re-verified since. Ops runbook lives in the private makerlab-camps repo; file cancellation/ops issues there.

## Roadmap

- [x] Squarespace migration (Nov 2025)
- [x] SEO: Schema.org JSON-LD on key pages, breadcrumbs, BlogPosting on all posts
- [x] Accessibility: skip links, ARIA nav, keyboard nav, heading hierarchy, alt text, iframe titles
- [x] LLM agent support: llms.txt, agent-guide.json, OpenAPI spec, posts.json with real dates/tags
- [x] ChambanaMoms campaign text deliverables
- [x] ChambanaMoms campaign images (2 social posts, round-up thumbnail, Facebook album photo)
- [ ] Podio migration: drop GlobiMail, evaluate full migration to Microsoft stack
- [ ] Monthly blog generation workflow from Podio orders
- [x] Commit Podio audit/automation scripts
- [x] Email auto-reply GitHub Action (Podio → OpenAI → SendGrid pipeline) — **deactivated 2026-05-12** (workflow file removed; recover from git history if revisited)
- [x] 3D Print Quote Calculator (STL/OBJ upload, Three.js preview, real-time pricing)
- [x] MakerLab Teams Bot POC — Power Automate "orders" keyword flow (SharePoint → Teams group chat)
- [x] Registration data pipeline: FormBuilder API → availability badges on website
- [x] Daily availability updates — now a GitHub Actions cron (`.github/workflows/update-availability.yml`, 14:00 UTC); needs repo secret `FORMBUILDER_TOKEN`. (History: Cloudflare Worker → local launchd → GitHub Actions, 2026-05-12. Local launchd plist renamed `.disabled`; `scripts/daily_availability_cron.sh` kept as fallback.)
- [x] Summer camp instructor job postings + staff schedule + hiring landing page
- [x] Renew FormBuilder token (renewed 2026-05-08, expires 11/08/2026)

## Session Log

### 2026-09-01
- **Hours check dispatched from control, then fixed (pushed `62306de`, `89eca05`, both verified live).** Live site byte-matched main on every hours surface, but three things were stale: the homepage tile still said "OPEN MON, AUG 31" the day after reopening (now "NOW OPEN"), no Labor Day note anywhere (positive control: "thanksgiving" hit lab-hours.html), and Tue/Thu were posted as 1:00–7:00 although coverage starts at 2:00 (Aldo 2–5, Bayu 4–7). Now: Mon/Fri 1–7, **Tue/Thu 2–7**, Wed 4–7; notices Thu Sep 3 opens at 4 PM (Aldo out for a Nucor capstone trip), Mon Sep 7 closed. Hours live in **five hand-edited places** that must move together: `lab-hours.html` (table + JSON-LD, now with `specialOpeningHoursSpecification` for dated notices), `api/site-info.json` (`hours.note`, `currentStatus`, new `hours.notices[]`), `agent-guide.json` sample response, `llms.txt` (two lines), `free-print-wednesday.html`. Vishal told the gurus about the Tue/Thu 2 PM start in person at tonight's kickoff (Sep 1, 6:30 PM, pizza by Aric).
- **Mail state read at open (mailcorpus):** Sahib and Bayu started Aug 31; Aldo's hourly hire approved Aug 27. **Celine Skertich (Thera-Solutions / functionalhand.com) asked Aug 31** for status + cost on the "mini" redesign and whether the 25 originals were printed and assembled; Aric dropped her materials in the lab Aug 31 afternoon for Bayu and Sahib. Adjacent: Melissa Graebner introduced Vishal to Dries Faems (WHU, AI in entrepreneurship) and floated the mHUB urban-manufacturing challenge; Geoffrey Challen's conversational-programming course reply mentions the AI hub + MakerLab space; David Charles wants to reconnect.
- **Housekeeping:** archived the 08-04 log entry (its uncommitted Aug 5 Gopesh addition preserved there); `.mcp.json` (google-analytics MCP, machine-specific credential path) gitignored rather than committed; Current Focus rewritten for the reopened lab. Two Aug 26 reopening commits were authored by a Codex session (no surviving deferrals).
- **Order form reactivated late in the session (`20052ee`, verified live):** Vishal confirmed the Podio webform is active again; `online-ordering.html` embeds it once more and the "currently unavailable" callout is gone. The repo pre-commit PII hook flags `uimakerlab@illinois.edu` (the lab's public mailbox) in that file; it is a false positive, bypassed with `--no-verify` after confirming it was the only hit.
- **Site sweep after the order form came back (`6f14a98`, verified live):** 17 broken internal links fixed (online-courses.html course links lacked `.html`; about-us + courses/making-things carried 15 Squarespace date-path blog URLs, all re-pointed at `blog/<slug>.html`); workshops.html note now says no sessions scheduled for Fall 2026; sitemap lastmod bumped for the seven pages touched today; GA added to summer/camp-instructor-schedule.html (summer/index.html is a redirect stub, left alone). Season text everywhere else checked and left as is.
- Next: (1) Podio embed confirmed rendering by Vishal in a browser (Sep 1 evening); nothing further on the order form. (2) **Thera-Solutions job:** Bayu/Sahib to quote the mini redesign and confirm the 25-unit build; reply to Celine. (3) **Thursday Sep 3 door notice** (4 PM open) is a physical task. (4) Unverified since Aug 4, check before assuming done: exec summary to Peecher (due Aug 7), parent feedback nudge/one-pager, recap post publish, watch-cleaner post (Podio order 2210). (5) Roadmap: Podio migration (drop GlobiMail first), monthly blog workflow from Podio orders. (6) Site-review decisions from the 08-03 archive entry.

*Older entries archived to `docs/session-archive.md`.*
