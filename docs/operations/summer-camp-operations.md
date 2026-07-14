# Summer Camp Operations (FormBuilder)

> Operational runbook extracted from CLAUDE.md. Camp data source of truth: `data/summer-camps-2026.json`.

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

**Gotcha: a "phantom seat" blocking a parent can be SELF-INFLICTED by that same parent's own abandoned attempt.** Before assuming a third-party cancelled/abandoned response is holding the seat, search Form Responses for the *complaining parent's own* prior attempts. A parent who "can't click" an open session has often already made 2–4 overlapping responses; if one reached `PaymentProcessing` (a reservation is added on the DataCollection→PaymentProcessing transition) but was never paid, **their own unpaid reservation is the 8th seat** — the data endpoint excludes it (badge shows 7/8) while the form counts it (8/8, greys out the checkbox). Fix: KEEP that valid-but-unpaid response (it holds the correct camp + seat for their child), cancel any empty/duplicate attempts, and get the parent to complete payment by logging back into the form with the same account to resume the in-progress registration (don't have them start fresh — a fresh response sees the session as full). Confirmed 2026-07-12 (GenAI Jul 20–24 AM). Diagnostic tell: live `update_availability.py --dry-run` shows the session at 7/8 (a real open seat) while the parent reports the checkbox is disabled.

**Gotcha: "Cancel Registration" is NOT silent on a `$0`/"Paid" response — it re-fires the payment-confirmation email.** Cancelling a response whose Payment Status is "Paid" (which includes a `$0.00` empty submission — no camp selected → $0 total → auto-"Paid") triggers a form-save that re-evaluates routing triggers; `PaymentConfirmationToPaymentComplete` (condition: Payment Status is Paid AND Phase is PaymentProcessing) then fires, **sending the parent a "[Name] Camp Registration Confirmation" email** and flipping the phase to PaymentCompleteCredit even though Registration Status ends up Cancelled. Net effect: the parent gets a misleading confirmation for a camp they aren't actually registered/paid for. Cancellation itself has no email trigger, so cancelling a *normal* unpaid ($ due) response IS silent — the surprise is specific to $0/"Paid" junk duplicates. If you must cancel one, warn the parent (or plan a clarifying follow-up). Found 2026-07-12.

**Silent admin edits: the "EDIT THESE ANSWERS" page has a "Process Routing Triggers" toggle — leave it Off (the default, marked "Recommended") and the save fires no triggers/emails.** This is the safe way to clean camp answers on a cancelled response (e.g. clearing a phantom checkbox) without risking the trigger-refire above. Related mechanics on that page: "DELETE ANSWER" is staged (nothing happens until "Save Changes" at the bottom), a radio-type session answer can only be cleared via DELETE ANSWER (radios can't be unchecked), and the parent "Camps" answer can't be deleted while dependent session-question answers exist (delete those first, or just leave "Camps" — capacity is tied to the *session* answer, not the Camps checkbox). Also: **the response History pane can lag several minutes** — a fresh "reservation deleted" event may not show immediately after Cancel Registration; reload before concluding the seat wasn't released. Found 2026-07-14.

**Gotcha: a partial answer-edit must clear BOTH the `camps_list_1` checkbox AND the per-camp session sub-answer.** The data endpoint (and therefore the website badge / `update_availability.py`) counts the seat by the **per-camp session field** (e.g. `generative_ai_and_3d_printing` = `GENAI3D_JUN1`), NOT the top-level `camps_list_1` checkbox. Unchecking only the camps-list box leaves the session sub-answer populated, so the seat stays occupied and the count does **not** drop. Clear the session sub-answer too, then save — only then does the endpoint free the seat. Confirmed 2026-06-19 (a GenAI Jun 15–19 partial cancel stayed 8/8 until the session field itself was cleared, then went 7/8).

**Gotcha: "wrong GenAI week on the confirmation" is a silent capacity fallback, NOT a config swap.** Families have reported registering for GenAI Jun 15–19 (PM) but receiving a confirmation for GenAI Jul 20–24 (AM). The Event-Session definitions are correct (`GENAI3D_JUN1`→Jun 15–19 PM, `GENAI3D_JUL1`→Jul 20–24 AM; titles/codes/dates all consistent). The real cause: once Jun 15–19 fills to 8/8 (or its registration window closes — Jun sessions close ~the day before camp), the form **silently offers only the still-open July session**, with no "your preferred week is full" warning, so a June-intending parent lands in July and is genuinely *seated* there (not just mis-emailed). Remediation is per-family (move them if a June seat frees); the systemic fix is a form-UX change (warn or hide the alternate week once a session fills). Found 2026-06-19.

**Roster source for parent comms: prefer the LIVE data endpoint over a saved ReportDump.** `update_availability.py`'s endpoint returns one record per *current* registration (cancelled + unpaid already excluded) with Camper First/Last, Parent First/Last, DOB, `FormResponseId`, and per-camp session codes — but **no email**. Join `FormResponseId` → email from the latest `Registrations-ReportDump_*.csv`. A saved dump alone is unsafe for notifications: it includes cancelled responses and misses post-export replacements (caught 2026-06-19 — a dump showed a cancelled family and missed the camper who took the freed seat).

**Gotcha: the cancellation/waitlist scanners do NOT read Podio comments — the real parent thread lives there.** `find_cancellation_requests.py` / `find_waitlist_requests.py` read only the email *body* (first message). GlobiMail threads the subsequent back-and-forth into the item's **comments**. A request can look "open/declined" from the body while the comments show the family re-confirmed (or resolved) days later. Always open the Podio item's comments (`/comment/item/{id}/`) before acting on a stale-looking request.
