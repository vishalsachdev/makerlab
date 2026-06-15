# Email with human-in-the-loop (Podio/GlobiMail, Outlook fallback)

All cancellation emails — Kip refund memos and parent waitlist offers — go **from `uimakerlab@illinois.edu`** and are **reviewed by the user before sending**. Prepare the message, then stop. Never click the final send yourself.

## Preferred: Podio / GlobiMail compose (auto-from uimakerlab)

GlobiMail sends from `uimakerlab@illinois.edu` automatically via per-item compose links in the "UIMakerLab Emails" Podio app (App ID 12703942). Best for **replying to a parent's existing email** that's already in Podio (e.g. a waitlist request or a cancellation request), so the reply threads.

Human-in-the-loop flow (browser, claude-in-chrome):
1. Find the Podio email item (the parent's thread) — see `scripts/podio/find_waitlist_requests.py` / `find_unreplied_camp_emails.py` which extract the GlobiMail compose link from item comments (`http://www.globimail.com/l2/NEW.<token>`).
2. Navigate to that compose link (opens the GlobiMail TinyMCE editor, From already set to uimakerlab).
3. Inject the drafted HTML body into the editor body, set the subject — but **do NOT click send**. Mechanics to model on: `scripts/podio/auto_reply_emails.py` and the editor body `tinymce.editors[0].getBody().children[0].innerHTML`. The send button selector is one of `.gm-send-btn, #send-btn, button[onclick*="send"]` — leave it for the user.
4. Tell the user the GlobiMail compose is ready and stop for their review + send.

**Caveat — new emails vs replies:** GlobiMail compose links are tied to an existing Podio email item. The **Kip refund memo has no incoming thread** to reply to, so there may be no compose link for it. Options: (a) compose a fresh GlobiMail message from the Emails app if the integration supports new-compose, or (b) fall back to Outlook (below) for the Kip memo while using GlobiMail for the parent reply. Confirm with the user rather than guessing.

**Note:** GlobiMail ($15/mo) is slated to be dropped per the Podio-migration plan. If it's been removed, use Outlook.

## Fallback: Outlook desktop

Use the **`compose-outlook-email`** skill: it opens a pre-filled Outlook compose window and stops before send. Source the body from the gitignored draft (`data/refund-memo-<name>.md` or `data/parent-emails/<offer>.md`).

**Setting From does NOT work via AppleScript** — `set sender of newMsg to {...}` is silently ignored. So after opening the compose window, **tell the user to set the From to `uimakerlab@illinois.edu` manually** via the compose window's From dropdown before sending. Don't add the `sender` line to the AppleScript.

## Email content conventions
- From: `uimakerlab@illinois.edu` (both Kip memos and parent emails).
- Kip memo recipient: Kip Mecum, `kmecu01s@illinois.edu`.
- Waitlist offer: state camper, exact session, **$250** (regular; early-bird ended 2026-03-15), the registration link, and **hold the seat until midnight the NEXT day** (verify the weekday against the actual date). Registration URL: `https://appserv7.admin.uillinois.edu/FormBuilderSurvey/Survey/gies_college_of_business/illinois_makerlab/summer_2026/`.
- Plain, warm, concise. Sign as "Illinois MakerLab / uimakerlab@illinois.edu".
