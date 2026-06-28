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
**Full ops runbook** (FormBuilder refunds/cancellations, token renewal, capacity gotchas, business-office refund memos): [docs/operations/summer-camp-operations.md](docs/operations/summer-camp-operations.md).

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

Summer camp operations (camps running Jun–Jul): cancellation/refund + transfer handling, waitlist backfill outreach, abandoned-cart cleanup, FormBuilder trigger/UX tuning. Mail status: **mailcorpus is current again** (indexed 6/27) — use it for reply-tracking. Still blocked: **desktop Outlook frozen at 6/14** (Outlook MCP reads stale cache + can't target the delegate uimakerlab mailbox); restart Outlook to unfreeze. Note refund confirmations split across vishal + uimakerlab mailboxes (see memory `feedback-refund-confirmation-mailbox-split`).

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
- [x] Email auto-reply GitHub Action (Podio → OpenAI → SendGrid pipeline) — **deactivated 2026-05-12** (workflow file removed; recover from git history if revisited)
- [x] 3D Print Quote Calculator (STL/OBJ upload, Three.js preview, real-time pricing)
- [x] MakerLab Teams Bot POC — Power Automate "orders" keyword flow (SharePoint → Teams group chat)
- [x] Registration data pipeline: FormBuilder API → availability badges on website
- [x] Daily availability updates — now a GitHub Actions cron (`.github/workflows/update-availability.yml`, 14:00 UTC); needs repo secret `FORMBUILDER_TOKEN`. (History: Cloudflare Worker → local launchd → GitHub Actions, 2026-05-12. Local launchd plist renamed `.disabled`; `scripts/daily_availability_cron.sh` kept as fallback.)
- [x] Summer camp instructor job postings + staff schedule + hiring landing page
- [x] Renew FormBuilder token (renewed 2026-05-08, expires 11/08/2026)

## Session Log

### 2026-06-29
- Completed: **Lena Hutchens cancellation (end-to-end) + full refund-txn reconciliation.** (All PII in gitignored `data/cancellations.csv` / `data/refund-memo-*.md` / `data/parent-emails/`.) (1) Processed the latest Podio cancellation — **Lena Hutchens, Adventures in 3D Modeling Jul 6–10 AM**, ref `pgpn-eyyy-yyyy-y`, $225 paid; 9 days out → 8–20 tier → **$112.50** (50% flat). FormBuilder Cancel Registration done (status Cancelled, seat freed 7/8, no phantom); CSV logged; **Kip memo + Burgener waitlist offer both staged in GlobiMail and SENT** (offer holds seat until midnight Mon 6/29; first-dibs Burgener → Frahm → Mirica). (2) 🔵 **Resolved the open GlobiMail caveat**: the Kip memo (no incoming thread) CAN go via GlobiMail — open the reply-compose on the parent's cancellation Podio item, then swap the To chip to Kip; committed to the skill ref (`482569e`, pushed). (3) **Reconciled every "pending" refund txn id in cancellations.csv** via mailcorpus + the uimakerlab mailbox: Sandholm `6863959551105` (6/3), Huang `6046929547826` (6/23), Reid+Heidi Molitor `3152679557974`/`5152689557024` (4/21 — email prose was reversed; ref-number match was the clincher; refund predated the 5/12 form-edit), Liam Davis `6586419550968` (Adventures) + `5623999563211` (GenAI), ~5/13. (4) 🔵 Wrote memory `feedback-refund-confirmation-mailbox-split.md` — refund confirmations split across vishal + **uimakerlab** mailboxes; mailcorpus only indexes vishal's Inbox, so "no confirmation found" isn't conclusive.
- Next: Watch for Burgener's reply by midnight Mon 6/29 (else offer Frahm → Mirica). Only genuinely-open refund: **Lena Hutchens $112.50** awaiting Kip's confirmation. ⚠️ **Desktop Outlook still frozen at 6/14** (Outlook MCP reads stale cache + targets vishal's inbox, not the delegate uimakerlab account) — restart Outlook to unfreeze; mailcorpus IS current (indexed 6/27). Carryover: GenAI silent-fallback form-UX fix; ChambanaMoms images; re-enable Podio order form.

*Older entries archived to `docs/session-archive.md`.*
