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

**Post-season (site flipped 2026-08-03; lab closed until week of Aug 31).** Active: parent feedback campaign **LAUNCHED 2026-08-03** — email sent From vishal@illinois.edu to 65 families (BCC; 3 lookup-needed families skipped per Vishal), live Google Form survey (link + settings in gitignored `data/parent-emails/feedback-campaign-plan.md`); replies land in vishal's inbox (mailcorpus indexes them); reminder nudge ~Aug 10, leadership one-pager ~Aug 20; season-recap blog post (public gist draft out to Bayu/Ling for media, Aric CC'd); five site-review housekeeping decisions (see 8/03 session log archive). **PRIORITY: executive summary for Associate Dean Mark Peecher, due EOD Friday 2026-08-07** — he will use it to decide whether to reappoint the ML director roles. Draft complete (~1,794 words, Word doc in session scratchpad) and sent in-thread to Aric for his BADM 331 section plus a full read; assemble and send once he responds. **Fall staffing schedule 2026-08-04** — three gurus (Bayu, Aldo Villanueva, Sahib Bedi) for the Aug 31 reopen; HTML confirmation email opened for review, grid needs verifying before send. Ops runbook now lives in the private makerlab-camps repo; file cancellation/ops issues there. Mail status: mailcorpus/Thunderbird is the reading source (Outlook desktop still needs re-auth); refund confirmations split across vishal + uimakerlab mailboxes (see memory `feedback-refund-confirmation-mailbox-split`).

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

### 2026-08-04
- Completed, three threads:
  - **(1) Executive summary for the Associate Dean (the session's main work).** Mark Peecher asked 8/04, EOD Friday deadline, for a 1–3 page summary of ML instruction/research/engagement in AY25-26 plus an AY26-27 outlook, explicitly "to decide whether to reappoint your ML roles." Researched via 8 parallel agents across mail, Podio, and the repo, then ~8 revision rounds. Final shape: summary → evolution arc (digital making → entrepreneurship → AR/VR → AI) → "why a business school should teach robotics" (Generative AI + Physical AI) → Instruction/Research/Engagement → priorities mapping table → AY26-27 → the ask. Strongest sourced material: **Dejan's Spatial AI arc** (May 2025 qual exam charge, with Vishal + Aric on committee → two Dlab SOWs Jul/Aug 2025 → "CAD Learning Barriers Research" delivered Dec 1 2025 → VR/AR module taught in BADM 525 March 2026; a closed loop in ten months), and the **distributed LLM inference SOW** with MakerLab as client on ~10 legacy iMacs. Excluded per Vishal: AI for Impact Build-a-thon (not ML-tied), the College-level AI leadership section, agentic AI as a throughline rung, Mark Peecher mentions, NSF AI-Ready Hub. Word doc (appendix stripped, ~1,794 words) sent **in-thread to Aric only, not reply-all**, so a draft containing `[Aric to complete]` did not reach Peecher or the thread's three CCs (Emma Fava, Gopesh Anand, Carlos Torelli).
  - **(2) Eight blog posts from Podio orders, plus two repo bugs fixed** (pushed `163eecf`). Live Podio pull: **119 orders since Aug 1 2025, 85 student / 27 faculty-staff-alumni / 6 other**. Wrote 8 posts from Feb–May 2026 orders, backdated to order dates (BADM 525 prototypes, BADM 331 final prototypes, Vet Med CT materials, watch reverse-engineering, Tau Beta Pi batch, hub caps, SCM keychains, architecture models). Editorial policy applied: no student names on coursework (FERPA-adjacent), no names on personal items, no NetIDs. **Bug 1:** auto-tagger regexes `PPE`, `PLA`, `cad` were unanchored and matched inside ordinary words ("sto**ppe**d", "swa**ppe**d", "dis**pla**y") — 47 of 52 COVID-19 tags were false positives, now 5. **Bug 2:** `blog/index.html` had drifted (7 missing posts, 6 stale titles+dates); added `scripts/regenerate_blog_listing.py` so it rebuilds from posts.json and cannot drift again. Counts synced to 309 posts / 332 sitemap URLs; all 18 doc links verified live.
  - **(3) Fall staffing schedule.** Availability gathered for the three fall gurus: Bayu (Mon–Thu 4–7pm, Fri 1–7pm, ~16–20 hrs/wk, open to remote Podio/email hours), Aldo Villanueva (new third guru, Tue/Thu 2–5pm), Sahib Bedi (~5 hrs/wk MakerLab↔Dlab coordination, Mon 1–5pm proposed). Schedule email **rebuilt as HTML with a real table** and opened for review; Wed 1–4pm still uncovered, and the reconstruction also shows Tue/Thu 1–2pm open (verify against intent).
- **Gotcha found and fixed (global):** thunderbird MCP `sendMail`/`replyToMessage` default to `isHtml: false`, so Thunderbird composes plain text and hard-wraps at its 72-column default, baking narrow ragged line breaks into the sent message. **Always pass `isHtml: true` with raw (not entity-escaped) HTML.** Verified end-to-end. Written to global CLAUDE.md, `~/.claude/references/mail-automation.md`, and memory `feedback-thunderbird-send-html`.
- Next: (1) **Exec summary is the deadline item** — Aric owes the BADM 331 paragraph + a full read (asked for Thursday); then assemble and send to Peecher by EOD Friday 8/07. Optional upgrades: confirm the distributed-inference outcome (currently written as scope, not result) and whether the Tech Arm WebXR platform shipped; decide whether Dean Elliott's "This is really good!!" should return somewhere, since cutting the AI-leadership section removed the only direct Dean quote. (2) **Send the Fall Schedule email** after verifying the grid; get Sahib's Mon 1–5pm confirmation. (3) **Feedback campaign:** reminder nudge ~Mon Aug 10; leadership one-pager ~Aug 20. (4) **Recap post publish** once Bayu/Ling media arrives. (5) **Before Aug 31 reopen:** post fall hours (real OpeningHoursSpecification), reopen order form, verify Guru roster on lab-staff.html (Bayu + Aldo + Sahib), makerlab-camps #14 roster-automation wrap. (6) Watch-cleaner blog post held for Vishal's video interview (Podio order 2210, 99 printed parts, still In Progress). (7) Five pending site-review decisions and other carry-forwards — see `docs/session-archive.md` (2026-08-03 entry).

*Older entries archived to `docs/session-archive.md`.*
