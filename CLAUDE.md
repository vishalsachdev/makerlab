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

# Fetch registration data and update session availability on website
python3 scripts/update_availability.py          # fetch + update
python3 scripts/update_availability.py --dry-run # show counts only

# Add Google Analytics tracking to all active pages (run after adding new pages)
python3 scripts/add_ga_tracking.py
```

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

```
makerlab/
├── *.html              # 32 active pages (about-us, courses, contact, etc.)
├── blog/               # 301 blog posts as individual HTML files
├── courses/            # Course-specific pages (making-things active)
├── summer/             # Summer 2026 camp pages (5 camps, pricing on main page)
├── css/style.css       # Single stylesheet with Illinois branding
├── js/main.js          # Vanilla JS (mobile menu, blog search/pagination, keyboard nav, ARIA)
├── js/quote.js         # 3D Print Quote Calculator (STL/OBJ parsing, Three.js preview, pricing)
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

Source of truth for camp operations data is:

- `data/summer-camps-2026.json`

Do not hand-edit duplicated camp facts across pages. Use:

```bash
python3 scripts/sync_summer_data.py
python3 scripts/validate_agent_data.py
```

`sync_summer_data.py` updates duplicated summer data in:
- `summer.html` (pricing, robot-capacity guideline, camp card age/max/session summary)
- `summer/*.html` camp detail blocks (ages, max campers, price line, session tables, register link)
- `faq.html`
- `api/site-info.json`
- `api/pages.json`
- `llms.txt`

`validate_agent_data.py` now also checks:
- no two camps share the same date/time slot
- detail-page sessions and capacities match canonical JSON
- registration URL consistency across summer detail pages

Current 2026 snapshot:
- 5 camps across Jun 1–Jul 31 (no camp week of Jun 29–Jul 3)
- Robot camps (Build Your Own Robot Arm, Reachy Mini) max 6 campers/session
- Reachy Mini has 3 sessions including Jul 6–10 (1:00 PM – 4:00 PM)
- Pricing: $250/week (early bird $225 ended March 15, 2026)
- Registration URL: `https://appserv7.admin.uillinois.edu/FormBuilderSurvey/Survey/gies_college_of_business/illinois_makerlab/summer_2026/`

### Camp Operations (FormBuilder)

**Refund policy** (per `summer.html`): 21+ days before camp = full minus $20 deposit; 8–20 days = **50% flat** (no deposit deduction); ≤7 days = no refund.

**Token renewal** (`FORMBUILDER_TOKEN` in `data/.env`, expires every 6mo). Test with `python3 scripts/update_availability.py --dry-run` — HTTP 403 = expired. To renew: FormBuilder Admin → Form Group → 2026 Summer Camp Registration → DataEndpoints → Edit `makerlab-summer-2026` → "Add Another Access Token" → 6 Months → click visibility icon to reveal → paste into `data/.env`. Endpoint UUID `d182387d-ce09-4fbd-b114-b40f011cdd90` (in script).

**Cancellations**: In FormBuilder admin, Form Responses → DETAILS for the response → click **"Cancel Registration"** (NOT "Delete Form Response" — preserves payment record). Then append row to `data/cancellations.csv` and run `python3 scripts/update_availability.py` to refresh the badge. IPay refund is processed separately by the user — not through FormBuilder.

**Refund-authorization memo to the business office**: After logging a cancellation, send an Outlook memo to **Kip Mecum (kmecu01s@illinois.edu)** authorizing the refund. State the **date of the family's original cancellation request** — this is what determines the refund tier (21+ days before camp = full minus $20 deposit/camp; 8–20 days = 50% flat; ≤7 days = none). If the request came in within the window but was actioned later, the *request date* governs, not the action date — call this out explicitly in the memo. List each camp + amount + total. Kip replies with the IPay transaction IDs once processed. Use the `compose-outlook-email` skill with a `data/refund-memo-<name>.md` draft.

**Critical: Data endpoint must filter cancelled responses.** Configured 2026-05-08 via "Additional Filtering" → Level 1 Condition Type = "Form Cancelled State" → "not cancelled". Without this filter, the API returns cancelled responses and the script overcounts. If a fresh data endpoint is created in future periods (e.g., Summer 2027), reapply this filter.

**Gotcha: FormBuilder session CODES are NOT chronological.** The data endpoint returns session *codes* (e.g. `AIROBOTICS_JUL1`), and `update_availability.py`'s `CODE_TO_SESSION` maps each code → a chronological session index. Do not assume the numbering follows date order — for Reachy, `AIROBOTICS_JUL1` is the *later* week (Jul 27–31) and `JUL2` is the earlier (Jul 6–10). A wrong mapping silently swaps two sessions' availability badges (and misleads parents). To verify/rebuild a mapping, **join the live data-endpoint codes to the ReportDump human-readable labels on `Form Response Identifier`** (one clean single-code registrant per code is enough), never trust the code suffix. Found 2026-06-04 — Reachy `JUL1`/`JUL2` were swapped (fixed `5cdf6f5`); the other four camps were correct.

**Gotcha: the form's session-capacity counter counts cancelled responses; the data endpoint does not.** A session can show "full" on the live registration form (refusing new sign-ups) while the data endpoint — and therefore the website badge and `update_availability.py --dry-run` — correctly shows open spots. This is because cancellations (and partial cancellations done via answer-edit) don't decrement the form's own per-session "Number Registered" tally until the response's camp checkbox is actually unchecked in DETAILS view. Tell-tale sign on Form Responses → session-capacity tables: registered > max (e.g. 7/6, 8/9). To unblock a parent immediately, temporarily bump that session's **Max Registrants** (Periods → "EDIT SESSIONS FOR 2026" → session row → Edit) by the number of phantom seats; real cap is still enforced by the data endpoint/badge. Revert Max to true cap as soon as either (a) the open spot fills, or (b) you clean up the phantom by unchecking the cancelled response's camp box (otherwise max stays inflated above real cap and the form could over-register). Found 2026-05-28 debugging Adventures Jun 1–5 showing full at 6/8.

**Abandoned carts (unpaid registrations).** FormBuilder has no auto-cancel action and no "Cancelled" phase, so a response stuck in `PaymentProcessing` with no payment sits there forever and may hold a seat reservation. The data endpoint already excludes unpaid responses (returns only "registered"), so the website badge is unaffected — but the registration form itself could refuse a new sign-up. Routing trigger **"Notify Vishal: response stalled in PaymentProcessing 24h"** (added 2026-05-12, in Form → Routing Triggers) emails vishal@illinois.edu when a response matches `Current Phase is PaymentProcessing AND Form is not cancelled` for 24h; then manually Cancel Registration on it (Form Responses → filter Phase = PaymentProcessing). To cancel a registration that should keep one of two camps, edit the answers in place (clear the camp field) rather than "Cancel Registration" which voids the whole response.

**Gotcha: a partial answer-edit must clear BOTH the `camps_list_1` checkbox AND the per-camp session sub-answer.** The data endpoint (and therefore the website badge / `update_availability.py`) counts the seat by the **per-camp session field** (e.g. `generative_ai_and_3d_printing` = `GENAI3D_JUN1`), NOT the top-level `camps_list_1` checkbox. Unchecking only the camps-list box leaves the session sub-answer populated, so the seat stays occupied and the count does **not** drop. Clear the session sub-answer too, then save — only then does the endpoint free the seat. Confirmed 2026-06-19 (a GenAI Jun 15–19 partial cancel stayed 8/8 until the session field itself was cleared, then went 7/8).

**Gotcha: "wrong GenAI week on the confirmation" is a silent capacity fallback, NOT a config swap.** Families have reported registering for GenAI Jun 15–19 (PM) but receiving a confirmation for GenAI Jul 20–24 (AM). The Event-Session definitions are correct (`GENAI3D_JUN1`→Jun 15–19 PM, `GENAI3D_JUL1`→Jul 20–24 AM; titles/codes/dates all consistent). The real cause: once Jun 15–19 fills to 8/8 (or its registration window closes — Jun sessions close ~the day before camp), the form **silently offers only the still-open July session**, with no "your preferred week is full" warning, so a June-intending parent lands in July and is genuinely *seated* there (not just mis-emailed). Remediation is per-family (move them if a June seat frees); the systemic fix is a form-UX change (warn or hide the alternate week once a session fills). Found 2026-06-19.

**Roster source for parent comms: prefer the LIVE data endpoint over a saved ReportDump.** `update_availability.py`'s endpoint returns one record per *current* registration (cancelled + unpaid already excluded) with Camper First/Last, Parent First/Last, DOB, `FormResponseId`, and per-camp session codes — but **no email**. Join `FormResponseId` → email from the latest `Registrations-ReportDump_*.csv`. A saved dump alone is unsafe for notifications: it includes cancelled responses and misses post-export replacements (caught 2026-06-19 — a dump showed a cancelled family and missed the camper who took the freed seat).

**Gotcha: the cancellation/waitlist scanners do NOT read Podio comments — the real parent thread lives there.** `find_cancellation_requests.py` / `find_waitlist_requests.py` read only the email *body* (first message). GlobiMail threads the subsequent back-and-forth into the item's **comments**. A request can look "open/declined" from the body while the comments show the family re-confirmed (or resolved) days later. Always open the Podio item's comments (`/comment/item/{id}/`) before acting on a stale-looking request.

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

Summer camp operations: Robot Arm camp Jun 8 readiness (build 2nd SO-100 arm for leader-follower — see makerlab-camps checklist), cancellation/reschedule handling, waitlist tracking decision, summer order-form re-enable.

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

### 2026-06-19
- Completed: **Camp-ops marathon + GenAI session-mismatch root-cause.** (All family/camper names + emails live in gitignored `data/cancellations.csv` / `data/walkin-registrations.csv`, not here.) (1) Reconciled a prior Jun 8–12 partial cancellation as **already refunded** (CSV was stale — verified $410 processed via mailcorpus); updated the rows. (2) Logged **2 in-lab walk-ins** (paid by card; settled) to the gitignored walk-in file. (3) Resolved a stale **GenAI Jun 15–19 waitlist** entry in Podio. (4) Processed a **GenAI Jun 15–19 partial cancellation** — caught via reading the Podio/GlobiMail **comment thread** (scanner skips comments) that the family had *re-confirmed* after earlier declining; cleared BOTH the camps_list checkbox AND the session sub-answer (the field the data endpoint counts), freed the seat (8/8→7/8), 50% Kip memo. (5) **Reassigned the freed seat** to a mismatch-victim camper who already had the morning camp that week → full day; verified 8/8 + Jul 20–24 → 5/8. (6) 🔵 **Root-caused the recurring "wrong GenAI week on confirmation"**: not a config swap — when Jun 15–19 fills/closes, the form silently offers only the open Jul 20–24 session (see new Camp-Ops gotcha). (7) Sent a **Jun 15–18 schedule-change notice** (Jun 19 Juneteenth building closure → Mon–Thu, +30 min/day) to all **11** affected families, built from the **live data endpoint** (the 5/30 dump was stale). (8) Drafted Kip refund memos (50% partial; full $250 goodwill for the mismatch family). Added 4 Camp-Ops gotchas to this file (both-fields partial cancel, GenAI silent-fallback, live-endpoint roster source, scanners-skip-Podio-comments).
- Next: ⚠️ **Finish the open full-cancellation/refund** — FormBuilder **Cancel Registration** on the GenAI Jul 20–24 response in the bottom `data/cancellations.csv` row is STILL PENDING (Chrome extension dropped mid-task); camper is still ACTIVE in that session, and the $250 goodwill Kip memo is drafted/opened — confirm sent. Also: **clean up abandoned unpaid duplicate responses** (several families have stray PaymentProcessing/DataCollection rows); **form-UX fix** for the GenAI silent-fallback (warn/hide the alternate week once a session fills); the 3 unverified July GenAI families left as-is per decision; ChambanaMoms images; re-enable Podio order form.

*Older entries archived to `docs/session-archive.md`.*
