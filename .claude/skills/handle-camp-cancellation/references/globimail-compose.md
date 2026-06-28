# Email with human-in-the-loop (Podio/GlobiMail, Outlook fallback)

All cancellation emails — Kip refund memos and parent waitlist offers — go **from `uimakerlab@illinois.edu`** and are **reviewed by the user before sending**. Prepare the message, then stop. Never click the final send yourself.

## Preferred: Podio / GlobiMail compose (auto-from uimakerlab)

GlobiMail sends from `uimakerlab@illinois.edu` automatically via per-item compose links in the "UIMakerLab Emails" Podio app (App ID 12703942). Best for **replying to a parent's existing email** that's already in Podio (e.g. a waitlist request or a cancellation request), so the reply threads.

Human-in-the-loop flow (browser, claude-in-chrome):
1. Find the Podio email item (the parent's thread) — see `scripts/podio/find_waitlist_requests.py` / `find_unreplied_camp_emails.py` which extract the GlobiMail compose link from item comments (`http://www.globimail.com/l2/NEW.<token>`).
2. Navigate to that compose link (opens the GlobiMail TinyMCE editor, From already set to uimakerlab).
3. Inject the drafted HTML body into the editor, set the subject — but **do NOT click send**. The send button (top-right "Send") is left for the user. Mechanics confirmed 2026-06-28:
   - **Body:** `tinymce.editors[0].setContent(html)` replaces the whole body; to keep the canned signature + quoted original below your text, prepend instead: `const ed=tinymce.editors[0]; ed.setContent(offerHtml + ed.getContent())`.
   - **Subject:** `document.querySelector('input[name="subject"], #subject').value = "…"`.
   - The compose link redirects to `secure.globimail.com/compose/<token>/` and may take ~2s to load — screenshot/`tabs_context_mcp` to confirm before injecting.
   - Harmless gotcha: a `javascript_tool` call whose result string contains an IPay txn id / reference number comes back `[BLOCKED: Cookie/query string data]`. **The script still ran** — screenshot to verify rather than re-running.

**New emails vs replies — the Kip memo CAN go via GlobiMail (resolved 2026-06-28):** compose links are tied to an existing Podio email item, and the Kip refund memo has no incoming thread of its own. Don't fall back to Outlook for it — instead **open the reply-compose link on the parent's cancellation Podio item, then change the recipient to Kip**: click the **×** on the pre-filled To chip, click the To field, type `kmecu01s@illinois.edu`, press Enter. This sends from uimakerlab AND records the memo against the right cancellation thread. (Replying to a UI-MakerLab-sourced item pre-fills To with `uimakerlab@illinois.edu` — that's why the swap is needed.) Run the parent waitlist reply and the Kip memo as two tabs (`tabs_create_mcp`) so both stage at once.

**Note:** GlobiMail ($15/mo) is slated to be dropped per the Podio-migration plan. If it's been removed, use Outlook.

## Fallback: Outlook desktop

Use the **`compose-outlook-email`** skill: it opens a pre-filled Outlook compose window and stops before send. Source the body from the gitignored draft (`data/refund-memo-<name>.md` or `data/parent-emails/<offer>.md`).

**Setting From does NOT work via AppleScript** — `set sender of newMsg to {...}` is silently ignored. So after opening the compose window, **tell the user to set the From to `uimakerlab@illinois.edu` manually** via the compose window's From dropdown before sending. Don't add the `sender` line to the AppleScript.

## Email content conventions
- From: `uimakerlab@illinois.edu` (both Kip memos and parent emails).
- Kip memo recipient: Kip Mecum, `kmecu01s@illinois.edu`.
- Waitlist offer: state camper, exact session, **$250** (regular; early-bird ended 2026-03-15), the registration link, and **hold the seat until midnight the NEXT day** (verify the weekday against the actual date). Registration URL: `https://appserv7.admin.uillinois.edu/FormBuilderSurvey/Survey/gies_college_of_business/illinois_makerlab/summer_2026/`.
- Plain, warm, concise. Sign as "Illinois MakerLab / uimakerlab@illinois.edu".
