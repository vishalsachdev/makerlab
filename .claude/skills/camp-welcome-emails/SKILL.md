---
name: camp-welcome-emails
description: >-
  Weekly (normally Wednesday) preparation of welcome emails to parents of
  campers whose Illinois MakerLab summer camp starts the following Monday.
  Use when the user says "camp welcome emails", "send welcome emails",
  "welcome email for next week's camps", "prep Monday camp emails", or it's
  Wednesday during camp season and next week's camps need parent emails.
  Covers: refreshing FormBuilder registration data, building cross-verified
  per-session rosters (via the authoritative CODE_TO_SESSION mapping — never
  raw session-code inference), detecting all-day campers, resolving parent
  emails, drafting per-camp + combined all-day emails from canonical
  templates, and opening Outlook compose windows for human review/send.
  Project-specific to the makerlab repo.
---

# Camp Welcome Emails

Every Wednesday during camp season: prepare and compose welcome emails to parents of campers whose camp starts the **following Monday** (camps run Mon–Fri). The user reviews and sends manually from the Outlook compose windows — nothing here ever auto-sends.

## Non-negotiable safety rules

- **This repo is PUBLIC. Never commit PII.** Rosters, drafts, and recipient lists live only in gitignored `data/parent-emails/`. Before any commit, `git status` and confirm nothing under `data/` (except `summer-camps-2026.json`) is staged.
- **FormBuilder session codes are NOT chronological — never infer a session from the code text.** For the "reachy" camp, `AIROBOTICS_JUL1` = **Jul 27–31** and `AIROBOTICS_JUL2` = **Jul 6–10**. On 2026-07-05, welcome emails went out with the wrong roster because codes were assumed sequential. The ONLY authoritative mapping is `CODE_TO_SESSION` (+ `FIELD_TO_CAMP`) in `scripts/update_availability.py` — `build_rosters.py` imports it directly; the skill must never bypass that.
- **Never send email.** `compose_emails.py` only opens compose windows (`open newMsg`, never `send`). The user reviews, switches the From account, and sends.
- **Hard-fail on roster disagreement.** If the API snapshot and the dated registrations CSV disagree, stop and resolve in FormBuilder before drafting anything.

## Workflow

Work the steps in order. Use TodoWrite to track them.

### 1. Refresh registration data

```bash
python3 scripts/update_availability.py
```

Needs `FORMBUILDER_TOKEN` (env or `data/.env`). Writes `data/registrations-snapshot.json` (the FormBuilder data endpoint already excludes cancelled/unpaid — live seats only) and `data/session-availability.json`. If this dirties `summer.html`/detail pages, that's the normal badge refresh — commit or leave per the user's call (no PII in those).

### 2. Confirm the target Monday

Target = next Monday from today. The skill normally runs Wednesdays (5-day lead). If run another day, `build_rosters.py` still targets the next Monday ≥ 4 days out and prints a warning when the lead time is off — surface that warning to the user and confirm the week before proceeding (use `--monday YYYY-MM-DD` to override). Sessions for the week are whatever entries in `data/summer-camps-2026.json` have a `dates` string starting on that Monday (e.g. `"Jul 13–17"` — note the **en-dash**); `time` tells AM (9:00 AM – 12:00 PM) vs PM (1:00 PM – 4:00 PM).

### 3. Build cross-verified rosters

```bash
python3 .claude/skills/camp-welcome-emails/scripts/build_rosters.py --monday YYYY-MM-DD
```

This script:
- imports `FIELD_TO_CAMP` + `CODE_TO_SESSION` from `scripts/update_availability.py` (no copied mapping to drift);
- builds per-session rosters (camper, parent, FormResponseId) from the snapshot;
- **cross-asserts** each roster against the dated registrations CSV (`data/registrations-*.csv` with `camp,session,camper,dob,parent` columns and labels like `Jul 13–17 (1:00 PM – 4:00 PM)`) — **hard-fails with a diff** on any mismatch; loud warning if no CSV covers the week (single-source roster — consider refreshing the CSV);
- cross-checks `data/cancellations.csv` and warns if any rostered camper appears fully cancelled for that session (defense in depth);
- detects **all-day campers** (same camper in an AM and a PM session that week) — their families get ONE combined email and are excluded from the per-camp BCC lists;
- resolves parent emails from the newest `data/*ReportDump*.csv` (`first_name`/`last_name` → `email` + `email2`) with `data/cancellations.csv` (`parent_email`) as fallback;
- prints a **MISSING EMAIL** list — typically families who registered after the last ReportDump export. Fix: pull the address from FormBuilder admin (response DETAILS view) or the uimakerlab OWA mailbox, then either hand-add it to the compose window or append the family to the rosters JSON and re-run compose for that group. Consider exporting a fresh ReportDump (store it in `~/Downloads`, NOT under `data/` — it contains payment data; only move a payment-stripped copy in);
- writes `data/parent-emails/<slug>-rosters.json` (e.g. `jul-13-17-rosters.json`) + a human-readable summary.

Show the summary to the user and get a nod on the rosters before drafting.

### 4. Draft the emails

Write one markdown draft per session to the `draft_file` paths named in the rosters JSON (`data/parent-emails/<slug>-<camp_id>.md`, plus `<slug>-combined-allday.md` when there are all-day families). **Canonical templates — copy their structure and blocks exactly, adjusting camp name/dates/roster:**

| Template | Use for |
|---|---|
| `data/parent-emails/jul-6-10-adventures.md` | **AM camps** — drop-off 8:45–9:00 AM, pickup 12:00–12:15 PM, "Lunch Hour Supervision" block (12–1 PM, $10/day, nut-free lunch) |
| `data/parent-emails/jul-6-10-reachy.md` | **PM camps** — drop-off 12:45–1:00 PM, pickup 4:00–4:15 PM, "Late Pickup" block (4–5 PM, $10/day) |
| `data/parent-emails/jul-6-10-combined-allday.md` | **All-day families** — one drop-off 8:45–9:00 AM, one pickup 4:00–4:15 PM, supervised lunch 12–1 PM $10/day |

Common blocks (all templates): location BIF Room 3030, 515 East Gregory Drive, Champaign IL; parking on Sixth Street; forms links `https://makerlab.illinois.edu/summer/camp-forms.html` and `https://makerlab.illinois.edu/summer/forms/Summer-Camp-Forms.pdf`; sent from uimakerlab@illinois.edu.

Conventions:
- **Subject:** `Welcome to MakerLab Camp! <Camp Name> (<Dates>) — Drop-off, Pickup & Forms`
- **Header above the `---` separator** (compose script strips it): the recipient list — family names + emails + camper names, who's excluded as all-day, From, and the `**Subject:** ...` line the compose script parses.
- **Timing wording:** sent Wednesday for a Monday start → "next week" / "on Monday" (not "tomorrow" — that's only right for a Sunday send). Fix any lead-time wording the roster script warned about.

### 5. Compose in Outlook (human-in-the-loop)

```bash
python3 .claude/skills/camp-welcome-emails/scripts/compose_emails.py data/parent-emails/<slug>-rosters.json --dry-run   # verify first
python3 .claude/skills/camp-welcome-emails/scripts/compose_emails.py data/parent-emails/<slug>-rosters.json             # open compose windows
```

For each email: pandoc converts the draft body to HTML wrapped in an Aptos 12pt div, then AppleScript `make new outgoing message` with **To = "Illinois MakerLab" <uimakerlab@illinois.edu>** and each family address as a `bcc recipient`, then `open newMsg` — **never send**. `--only <camp_id>`/`--only allday` composes one at a time. Requires desktop Outlook running + Automation permission (same pattern as the user-level `compose-outlook-email` skill).

**Remind the user before they send:** switch the From account to **uimakerlab@illinois.edu** (delegate access, already set up in desktop Outlook), and eyeball the BCC list against the roster summary.

### 6. Post-send checklist

- Verify the sends landed in the **uimakerlab Sent Items** — desktop Outlook's read view can be stale/frozen, and mailcorpus only indexes vishal's mailbox, so check **uimakerlab via OWA** if in doubt.
- Handle any MISSING EMAIL families (send them an individual copy once the address is found) and note it in the draft header for the record.
- Confirm nothing PII-bearing is staged for commit.

## Remaining 2026 send dates

| Send (Wed) | Camp week | Emails |
|---|---|---|
| Jul 8 | Jul 13–17 | Minecraft (PM) + Robot Arm (AM) |
| Jul 15 | Jul 20–24 | Minecraft (PM) + GenAI (AM) |
| Jul 22 | Jul 27–31 | Minecraft (PM) + Reachy (AM) |

Plus a combined all-day email any week the roster script finds AM+PM campers.
