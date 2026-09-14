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

**Fall 2026, lab open since Mon Aug 31.** Hours Mon/Fri 1–7, Tue/Thu 2–7, Wed 4–7 PM; gurus Bayu (ops lead, Mon–Thu 4–7, Fri 1–7), Aldo Villanueva (Tue/Thu 2–5), Sahib Bedi (Mon 1–5). Hours are hand-edited in five places (see 2026-09-01 log) and carry dated notices via `specialOpeningHoursSpecification` + `hours.notices[]`; update all five together and bump the freshness stamps. Open operational items: the **Thera-Solutions client job** (pricing reply sent 2026-09-14; Bayu ships the 25 Originals this week, then Vishal invoices; details in the private PEOPLE notes), and several Aug 4 threads (exec summary, feedback campaign, recap post) have not been re-verified since. Ops runbook lives in the private makerlab-camps repo; file cancellation/ops issues there.

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
- [x] Daily availability updates — GitHub Actions workflow (`.github/workflows/update-availability.yml`, 14:00 UTC when scheduled); needs repo secret `FORMBUILDER_TOKEN`. **Off-season:** schedule commented out 2026-08-03 and the workflow disabled in GitHub 2026-09-14 (`gh workflow enable 275662132` plus uncomment the cron to restore). (History: Cloudflare Worker → local launchd → GitHub Actions, 2026-05-12. Local launchd plist renamed `.disabled`; `scripts/daily_availability_cron.sh` kept as fallback.)
- [x] Summer camp instructor job postings + staff schedule + hiring landing page
- [x] Renew FormBuilder token (renewed 2026-05-08, expires 11/08/2026)
- [ ] **Jan 2027: restore summer camp tooling** before registration opens: `git mv` the two skills back from `.claude/skills-disabled/` (see its README) and move the camp memories back from `memory/archive/`. Reconcile the `summer.html` refund wording with the 50%-flat tier first.

## Session Log

### 2026-09-14
- **Thera-Solutions pricing reply sent** to the client 10:33 AM CDT (verified in Sent Items), answering the 09-10 Q4 questions and the 09-08 Mini-quote ask: unit prices for Original and Mini (printed, assembled, with cord cutting), material recommendation (Elegoo PLA; the supplied PLA+ needs 240°C/75°C and slow speeds), weekly capacity, materials routing, shipping and invoicing. Figures and their sources are in the private PEOPLE notes (`~/mykai-home/PEOPLE/linda-merry.md`), not here: this repo is public.
- **Summer camp tooling archived for the off-season** (`ff3f622`, `9dae668`, pushed, Pages deploy green 12:28 PM CDT): both camp skills to `.claude/skills-disabled/` (README has restore steps); five camp memories plus ChambanaMoms and EventMaster notes to `memory/archive/`; `update-availability` workflow disabled in GitHub. Its schedule had been commented out since 08-03 (last run 08-02); this file had wrongly called it a daily cron, now fixed. Inventory found nothing else on GitHub or this Mac that touches Podio or FormBuilder; the Podio webform and GlobiMail hooks stay live for Fall orders. Thunderbird reminder task for 2027-01-11 opened (confirm it saved).
- **Found:** `summer.html` posts the 8 to 20 day refund tier as "half refund minus the $20 deposit", but the skill and ops runbook apply 50% flat. Fix before 2027 registration (in the roadmap restore item).
- **PEOPLE (mykai-home, uncommitted):** created bob-merry, lora-brooks; updated linda-merry, celine-skertich, bayu-febriansyah. `PEOPLE/cheng-li.md` has an unrelated uncommitted change.
- Next: (1) **Thera:** Bayu confirms the PLA+ weekly-capacity figure and ships the 25 Originals this week with tracking; then Vishal sends the invoice (amount in PEOPLE/linda-merry.md). (2) FormBuilder token expires 11/08/2026; renew with the Jan 2027 restore. (3) Carried, unverified since Aug 4: exec summary to Peecher, parent feedback nudge, recap post, watch-cleaner post (Podio order 2210). (4) Roadmap: Podio migration (drop GlobiMail first), monthly blog workflow. (5) Site-review decisions from the 08-03 archive entry.

*Older entries archived to `docs/session-archive.md`.*
