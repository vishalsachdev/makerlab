# Session Archive

Archived session log entries from CLAUDE.md (>30 days old).

## 2026-05

### 2026-05-05
- Completed: Spring semester closure rollout. Added closure banner + paused online orders on `lab-hours.html` and `online-ordering.html`: final open day is Wed May 6 (extended hours 2–7pm), online order intake stopped May 5, existing customers updated by email with pickup arranged via order email/contact form, will reopen for summer-camp season with limited online order capacity. Podio web form on online-ordering page commented out (easy re-enable). Committed AGENTS.md with agent ops rules. Commits: de0d2b0, e054f46, ab6b1b6, 93d8671.
- Next: When summer camps start, re-enable Podio order form (uncomment in `online-ordering.html`) and update both pages with summer hours. Still pending from prior session: confirm FormBuilder token renewed + `update_availability.py --dry-run` works; follow up on parent registration issue from 2026-04-07.

## 2026-02

- **2026-02-20**: Session start. Added roadmap sections to CLAUDE.md.
- **2026-02-21**: Built and deployed email auto-reply automation. GitHub Action (every 6h, draft mode) with manual dispatch (send/dry-run + configurable lookback). Committed 13 files: workflow, auto_reply_emails.py, smtp_sender.py, website_context.py, Podio audit scripts. Set 6 GitHub secrets. Codex review caught 2 bugs (NEEDS_HUMAN mis-tagging, duplicate drafts) — fixed and pushed. Tested dry-run with 30-day lookback: 1 email classified correctly as NEEDS_HUMAN.
- **2026-02-24**: Verified PR #32 merge (3D Print Quote Calculator). Applied 3 missing fixes: blank 3D preview (unhide before render), slider label tracking (absolute-positioned + JS repositioning), $4 base fee display (shared note, online desc → 20% surcharge). Ran full code audit — fixed all P1s (variable naming mm³ vs cm³, 5M triangle OOM cap, single BASE_FEE constant) and P2s (animation pause on tab hide, WebGL dispose on pagehide, OBJ bounds checking, STL heuristic tolerance 100→256, radio inputs visually-hidden for screen readers, aria-live on price total). Deleted merged branch. Added GA tracking to all 331 active pages (329 were missing it). Added quote calculator event tracking (file upload, quote calculated w/ debounce, Place Order click, Full Pricing click). Created `scripts/add_ga_tracking.py` for future pages.
- **2026-02-25**: Built and tested MakerLab Teams Bot POC via Power Automate. Created "MakerLab Chat Orders" flow (ID: 1b3853ae-762f-4bc8-9f1a-22a8213effa8) — triggers on "orders" keyword in "makerlab website" group chat, queries SharePoint Orders list (MakerLab Bot site), posts Title/ProjectName/Material/Status per order via Flow bot. Tested end-to-end: 5 distinct orders returned (John Smith, Sarah Johnson, Mike Chen, Emily Davis, Alex Rivera). Next: build Events lookup flow, aggregate orders into single message, submit bot app for tenant admin approval.

## 2026-04

- **2026-03-16**: Connected FormBuilder registration API — built `scripts/update_availability.py`, deployed Cloudflare Worker with daily Cron Trigger. FormBuilder token expires 2026-04-16.
- **2026-03-26**: Created summer camp instructor hiring package — two JDs, staff schedule, `summer/jobs.html`, "Now Hiring" banner. Application deadline: April 5, 2026.
- **2026-04-04**: Camp availability operations session. Discovered Cloudflare Worker never successfully committed (secrets issue) — site was 19 days stale. Replaced Worker with local launchd cron (`scripts/daily_availability_cron.sh`, 9 AM daily). Processed Mirica cancellation (Robot Arm Jun 8–12, $205 refund). Added "Join Waitlist" mailto links on sold-out sessions. Created `data/cancellations.csv` and `data/early-bird-registrations.csv`.
- **2026-04-07**: Website security audit and link cleanup. Removed 6 compromised domains across 7 blog posts. Replaced 3dprintingprofs.com with Coursera. P2 pass: removed 24 dead links across 19 blog posts. Archived volunteer.html. Fixed SSL cert issue in update_availability.py.
- **2026-04-13**: Updated Monday lab hours to split schedule (1–3pm, 5–7pm) in `lab-hours.html` — both visible list and Schema.org JSON-LD. Updated Minecraft camp availability: Jun 15–19 AM sold out (waitlist link), Jul 27–31 PM down to 2 spots.

### 2026-04-16
- Completed: Updated summer jobs page — extended application deadline to Apr 20 with "still accepting" note, added current UIUC student eligibility requirement. Updated Minecraft camp Jul 27–31 PM availability (2 → 1 spot). FormBuilder token renewal identified but not yet completed (user handling manually).
- Next: Confirm FormBuilder token renewed and `update_availability.py --dry-run` works. Follow up on parent registration issue flagged 2026-04-07.

### 2026-05-08
- Completed: Renewed FormBuilder token via Chrome (6mo, expires 11/08/2026). Processed Tracy Sulkin cancellation (Minecraft Jun 15-19 AM, ref ycqn-kyyy-yyyy-y, $230 refund per 21+ day policy) — cancelled in FormBuilder, logged to `data/cancellations.csv`, refund processed in IPay. **Discovered & fixed data endpoint bug**: API was returning cancelled responses (Sulkin's slot stayed SOLD OUT after cancellation). Configured "Additional Filtering" → Form Cancelled State = "not cancelled" on the data endpoint; endpoint dropped 79→78, badges correct. Processed Admal reschedule (Robot Arm Jun 22-26 AM → Jun 8-12 PM) via in-place answer edit in FormBuilder. Documented camp ops in CLAUDE.md (token renewal, cancellation flow, refund tiers, the cancelled-filter gotcha). Commits: 2ca22e4, 14180f5, aab26e5.
- Next: Decide on a waitlist tracking approach (currently mailto-only → goes to inbox backlog). Still pending: ChambanaMoms campaign images, monthly Podio blog workflow, monitor draft email auto-replies. When summer camps start (Jun 1), re-enable Podio order form on `online-ordering.html` and update both order pages with summer hours.
