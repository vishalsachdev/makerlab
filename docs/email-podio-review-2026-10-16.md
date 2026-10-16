# MakerLab email and Podio review

Created: 2026-10-16
Last Updated: 2026-10-16
Author: Claude (makerlab session), requested by Vishal via control
Scope: **investigation only.** No Podio setting, webhook, flow, mail rule, export, deletion or subscription was changed. All Podio data came from read-only API calls (GET and item filter).
Supersedes: the app list and email parts of `.claude/plans/podio-migration-plan.md` (2026-02-24), where they disagree.

---

## 0. Podio app inventory (read-only API, 2026-10-16)

Org Illinois MakerLab (528575) has 10 workspaces and 45 apps holding 14,116 items. 4 workspaces are empty: Coursera-Analytics, Employee Network, iMBA-SocialMediaProject and MakersUIUC-MakerLab-Summer. The Attendees app (11369317) no longer exists.

The table sorts apps by their last real activity:

- **In use** means activity in the last 90 days, since 2026-07-18.
- **Seasonal** means a summer-camp app whose last use was the 2026 camp build.
- **Dormant** means activity within the last 2 years but not in the last 90 days.
- **Dead** means nothing real for 2 years or more.

"Last modified" is the newest `last_event_on` among items. "Last comment / email in" is the newest comment on the 5 most recently edited items, plus how the newest item was created.

### In use (5 apps, 11,502 items): map or fix these

| App (id) | Items | Last created | Last modified | Last comment / email in | Flows and webhooks |
|---|---:|---|---|---|---|
| **UIMakerLab Emails** (12703942), Lab Operations | 4,105 | 2026-10-16 (by Mail) | 2026-10-16 | Comment 2026-10-16, GlobiMail. Intake by email-to-app and web form 1010447 on `contact.html` | Flow "set default status to OPEN". 3 GlobiMail hooks (create/update/delete) |
| **Orders** (6976602), Daily Activities | 2,147 | 2026-10-15 (Webform 2) | 2026-10-16 | Comment 2026-10-16, GlobiMail. Intake by web form 537064 on `online-ordering.html` | Flows "Review New Order", "Create Transaction, when Order status changes to PAID". 3 GlobiMail hooks |
| **Transactions** (14037249), Daily Activities | 3,249 | 2026-10-14 (by Flows) | 2026-10-14 | Comment 2026-10-14, GlobiMail; "Activated" stubs only, no email | Created by the Orders flow. 3 GlobiMail hooks (unused) |
| **Payments** (25086402), Daily Activities | 154 | 2026-09-25 (by Mail) | 2026-09-25 | No comments. Intake by email-to-app | Flow "update date when payment created" |
| **Closing Notes** (15127330), Daily Activities | 1,847 | 2026-09-08 | 2026-09-08 | Comment 2026-04-28 | None |

### Seasonal (2 apps, 958 items): decide in January with the camp restore

| App (id) | Items | Last created | Last modified | Last comment | Flows and webhooks |
|---|---:|---|---|---|---|
| **Events** (6701476) | 906 | 2026-02-16 (created by Claude for Summer 2026) | 2026-02-16 | None | Flows "Confirm Availability", "Find a Volunteer" |
| **EventMaster** (9968618) | 52 | 2026-02-16 | 2026-02-27 | 2026-02-27 | None |

Camp registration and payment run on FormBuilder, not Podio. Events and EventMaster held the camp schedule and templates.

### Dormant (5 apps, 689 items): archive

| App (id), Daily Activities | Items | Last created | Last modified | Last comment | Flows and webhooks |
|---|---:|---|---|---|---|
| CommonPrints (29860514) | 10 | 2026-02-27 | 2026-04-17 | None | None |
| Projects (29932376) | 118 | 2026-02-21 | 2026-02-21 | 2025-03-31 | None |
| Checklists (29860516) | 49 | 2026-02-18 | 2026-02-18 | None | None |
| Timesheets (9907051) | 486 | 2025-09-10 | 2025-09-10 | — | None |
| Templates (29860515) | 26 | 2024-09-05 | 2025-01-28 | — | None |

### Dead (33 apps, 967 items): archive

| Workspace | Apps (items) | Last activity | Live webhooks or flows to switch off |
|---|---|---|---|
| Events | Volunteers (156), Certificates (39), Feedback (35), Venues (26), ClientOrganizations (23), Private Events (15), Payments (0) | Created 2017 to 2023. Volunteers and Certificates show edits on 2026-02-16 and 02-19, which match the API audit and camp sessions, not staff use. | **Volunteers:** 3 GlobiMail hooks and 2 flows. **Private Events:** 2 PodioTools.com hooks and 1 flow |
| Daily Activities | Gurus (36), Certification Exams (10) | 2024-09-05, 2022-10-13 | **Certification Exams:** 2 PodioTools.com hooks |
| 3dp MOOC | 3dpr-tshirt (91), Contacts (62), 3dpp-contactform (60), Timesheet (41), Checklists (2), Course Update Content (1) | 2016 to 2022 | **3dpp-contactform:** 1 PodioTools.com hook and 1 flow |
| CTA - Social Media | 12 apps, 352 items | 2016 to 2018 | None |
| iMBA-TechStars | 6 apps, 18 items | 2017 | None |

**Changes from the February plan.** The plan counted 10 apps in use. Now only 5 are in use. Timesheets, Checklists and CommonPrints have gone quiet. Events and EventMaster are seasonal.

GlobiMail hooks sit on **4 apps**: Emails, Orders, Transactions and Volunteers. Core plans are described as a 3-app limit, so the 2 unused hook sets (Transactions and Volunteers) could be removed.

---

## 1. Answer first

- **The $15/month is GlobiMail Core.** Globi Corporation bills it through Stripe to Vishal's university inbox on the 26th. The next charge is due about **2026-10-26**.
- **GlobiMail does real work, mostly on Orders.** It is the order-correspondence tool. 41 of the last 60 orders (Apr 22 to Oct 15) have a GlobiMail thread: **84 messages sent and 49 customer replies logged**, about 14 sent a month. On the Emails app it logs threads mainly for web-form items (12 of 22 recent ones).
- **Email intake is badly set up.** 72 of the last 78 mailed-in Emails items show `uimakerlab` as the sender, not the customer. The forward replaces the sender, so GlobiMail cannot reply to those items. Staff answer them in Outlook, and Podio never sees the answer. All 100 recent Emails items are still `open` (2,721 of 4,105 overall), and vendor newsletters go in with real requests.
- **Only 5 apps matter:** Emails, Orders, Transactions, Payments and Closing Notes. Events and EventMaster are seasonal. The other 38 apps get archived as a reference knowledge base, not migrated (Vishal's decision, §7).
- **Recommendation:**
  1. Fix intake now and move general email to the Outlook shared mailbox (Option 2).
  2. Run a 2-week pilot of logging order email without GlobiMail.
  3. Keep GlobiMail until the pilot works, or until Orders moves.
  4. Move the 5 in-use apps to Microsoft 365 in January 2027 (Option 4), after the archive is done.
  5. Do not start Copilot Studio until Technology Services confirms a license.

---

## 2. What the Podio documentation says

Source: https://www.progress.com/podio/documentation/using-podio/files-and-communication/using-email-with-podio. This page is only an index. The details below come from its subpages, "Email to app" and "Email to item".

| Feature | How it works | Limits stated |
|---|---|---|
| **Email to app** | Each app has an address. Find it under the app's wrench icon, then "Email to app". Each mail creates one item. The settings map email parts (sender, subject, body) to fields, and attachments become files. | 20 attachments at most. Signatures and inline images count as files. Body-to-field parsing is "not a fully supported function". Not available in Event apps. |
| **Email to item** | Each item has an address. A mail to it adds a **comment**. A *personal* address posts as you. A *generic* address posts as the app and is safe to share. | Admins cannot edit or delete comments made through the generic address. |
| **Outbound email to external people** | **Not described.** Podio itself only notifies members. Sending to customers needs an add-on: GlobiMail today, or possibly Podio Workflow Automation (Option 3). | — |
| **Plan requirements** | Not stated for any of these features. | — |

The Emails and Payments apps use email-to-app. The live mapping is sender→From contact, subject→Subject, body→Body, with attachments on. Nothing uses email-to-item today.

---

## 3. What we pay for

| Item | Cost | Evidence | Confidence |
|---|---|---|---|
| GlobiMail Core | **$15.00/month** ($180/year) | Stripe receipts "Your receipt from Globi Corporation" to Vishal's university inbox, monthly since at least 2025-12-27. The latest is dated 2026-09-26, for Sep 26 to Oct 26, 2026. | Verified (mailcorpus) |
| Podio | **Unknown, possibly $0** | `GET /org/528575` returns `"type": "sponsored"`, `"tier": "premium"`, `"user_limit": 5`. mailcorpus finds no Podio invoice ("Podio invoice subscription" returns 0 hits), although the same index finds the GlobiMail receipts. The February plan's "Podio Plus ~$14/mo" has no receipt behind it. | Not verified |

**Vishal must check:**
1. Log in to podio.com, open Illinois MakerLab, then *Manage organization* > *Billing / Subscription*. Is it paid? By which card and for how much? "Sponsored" may mean a free education or nonprofit plan.
2. Log in to globimail.com, open the account or billing page. Find the renewal date and the cancel path.

---

## 4. The current flow, end to end

```
GENERAL EMAIL
Customer ──► uimakerlab (Exchange shared mailbox)
               │ rule FORWARDS to Podio, sender becomes uimakerlab          ← UNOBSERVED
               ▼
         Emails app 12703942 (email-to-app) ─► flow sets status OPEN
               ▼ GlobiMail hook ─► "GlobiMail Activated" comment + Compose link
         Reply: Compose has no customer address ─► staff answer in Outlook ─► not logged

WEB FORMS
contact.html ─► Podio web form 1010447 ─► Emails app (real customer in From)
online-ordering.html ─► Podio web form 537064 ─► Orders app 6976602
               ▼ GlobiMail hook ─► Compose link on the item
         Staff "Compose" ─► GlobiMail sends From uimakerlab ("MakerLab Staff")
         Customer replies ─► GlobiMail logs both sides as item comments   (84 out / 49 in, 6 months)
         Order status PAID ─► flow creates a Transactions item

PAYMENTS
Payment notice mail ─► Payments app 25086402 (email-to-app) ─► flow sets the date
```

### Where it breaks

1. **The forward replaces the sender.** 92% of mailed-in Emails items have uimakerlab as "From", so they cannot be answered from Podio.
2. **Two places to answer.** General mail is answered in Outlook and order mail in GlobiMail. Neither tool holds the whole history.
3. **No triage.** Every Emails item stays `open`, and newsletters enter Podio.
4. **Dead apps still have live third-party hooks:** GlobiMail on Volunteers, and PodioTools.com on 3 dead apps. Remove them during the archive.
5. **Low risk:** the GlobiMail webhook URLs use `http`. Podio hook calls carry only IDs.

### Steps I cannot observe, and the check for each

The uimakerlab mailbox is invisible to every agent tool (memory, verified 2026-09-28).

| Step | Vishal's check |
|---|---|
| The mailbox rule to Podio. Is it a forward or a redirect? Is it an Outlook rule or Exchange forwarding? | In desktop Outlook, open the uimakerlab mailbox, then *File* > *Manage Rules & Alerts*. Or go to Outlook on the web, *Settings* > *Mail* > *Rules* and *Forwarding*, in that mailbox. Note the target (it should end in `@podio.com`) and the rule type. If nothing is there, ask Technology Services about mailbox-level forwarding. |
| What sends mail into Payments | Open the newest Payments item in Podio and look at its source mail. Then find the rule or sender (iPay? the business office?). |
| The email-to-app addresses | For each app, click the wrench, then *Email to app*. The addresses are not in the API answer. |
| How customer replies reach GlobiMail | Open one GlobiMail-sent order email and look at its Reply-To and Cc/Bcc headers. |
| Who answers mail and orders (Bayu? student workers?) | Ask Bayu. The PEOPLE note says remote Podio/email hours are "to be settled". |
| Whether general mail gets answered | Compare uimakerlab Sent Items for Oct 1 to 16 with the 25 Emails items from the same dates. |

---

## 5. Options (in-use apps only)

The dormant and dead apps are covered by the archive plan (§6) in every option. Podio's own cost is unknown (§3), so it is listed separately.

### Option 1: Keep GlobiMail and fix the intake

- **Do:**
  - Change the uimakerlab rule from forward to *redirect*, so the customer stays in From.
  - Keep newsletters out with a rule.
  - Set a weekly status sweep.
  - Remove the unused GlobiMail hooks on Transactions and Volunteers.
- **Cost:** $15 plus Podio.
- **Improves:** GlobiMail can then answer every Emails item, and all correspondence is logged in Podio.
- **Effort:** 1 to 2 hours.
- **Risk:** Low. Campus policy may block redirect, so test with one rule.

### Option 2 (recommended now): Outlook-first email, Podio for operations

- **Do:**
  - Answer general email in the uimakerlab shared mailbox, with categories *Open*, *Waiting* and *Done*.
  - Turn off the forward into the Emails app. Keep the app as a read-only archive.
  - Move `contact.html` from Podio web form 1010447 to a Microsoft Form. A standard Power Automate flow sends the form to uimakerlab with Reply-To set to the customer.
  - **Order email pilot (2 weeks):** send order mail from Outlook, and Bcc the order's *generic* email-to-item address, which is native Podio and free. Put the Podio order number in the subject, so a customer's reply can be found by search. Forward a reply to the same address when it matters.
  - Cancel GlobiMail after the pilot shows the logging works.
- **Cost:** **$0 for email** (saves $180/year), plus Podio.
- **Improves:** one place to answer, the real sender on every message, and less noise in Podio.
- **Effort:** about 1 day, plus 2 weeks of staff use. The day covers the Form, the flow, the `contact.html` edit, the rule change and a one-page staff note.
- **Risk:** Medium. Customer replies on orders are no longer logged automatically, so staff must forward them or rely on mailbox search. That habit can decay, which is why the pilot comes first. The flow must be owned by a service account (see Option 4). Bayu needs shared-mailbox access.

### Option 3: Drop GlobiMail with Podio's own automation

- **Lead to verify:** Podio's Premium tier has historically included **Podio Workflow Automation** (formerly Globiflow), which can send email from an item and log it. The org reports `tier: premium`. I did not verify that PWA is included, and the documentation pages do not mention it. Check by opening Orders, then the app menu, then *Workflow automation*. A prompt to upgrade means it is not included.
- **Cost:** $0 for email if included.
- **Improves:** keeps one-click Compose and logging on Orders.
- **Effort:** 1 to 2 days to build send-and-log actions for Orders and Emails.
- **Risk:** Medium. It puts more logic into Podio just before a planned move off it.

### Option 4: Move the in-use apps to UIUC Microsoft 365 (January 2027)

**Mapping (in-use and seasonal apps only)**

| Podio today | Microsoft 365 target |
|---|---|
| UIMakerLab Emails (intake, status) + web form 1010447 | uimakerlab **Exchange shared mailbox** with categories. **Microsoft Forms** for the contact form, then a flow sends mail with Reply-To set to the customer. Optional: a flow logs new mail to a "Requests" List and posts to Teams. |
| Orders (35 fields, calculations, app references) + web form 537064 + flow "Review New Order" | SharePoint List "Orders" with calculated columns and lookups. Use built-in forms and JSON formatting, because Power Apps is not licensed. The Forms "Order request" flow creates the List row and posts the "review new order" card to Teams. That card flow already works in makerlab-bot. |
| GlobiMail order correspondence | Shared mailbox. The flow "Send an email from a shared mailbox (V2)" (standard Office 365 Outlook connector) sends from uimakerlab and stamps `[Order 2147]` in the subject. A second flow files replies with that tag back to the List item as a note or link. |
| Transactions + flow "Create Transaction when PAID" | List "Transactions" with a lookup to Orders. A flow runs when the Order Status changes to Paid. |
| Payments (email-to-app) + flow "update date" | List "Payments". A flow runs on mail to uimakerlab from the payment sender and creates the row. |
| Closing Notes | Microsoft Form "Closing note" feeding a List, or a Teams channel post |
| Events + EventMaster (seasonal) | Decide in January. Either Lists "Event Templates" and "Events" with a lookup, or archive them, if FormBuilder plus a calendar covers camps. **Bookings** could take tour and consult requests; it is not verified. |
| Front-desk agent | **Copilot Studio** agent over the site FAQ, `llms.txt`, and the archive knowledge base (§6, redacted set only). Blocked on licensing. |
| Blog scripts (`scripts/podio/`) | `graph_client.py` with Graph and `msal`. This needs an app registration with `Sites.Selected` and **tenant admin consent**. |

**License status**

| Capability | Status | Source |
|---|---|---|
| Exchange shared mailbox uimakerlab | Exists. Vishal has delegate access. | memory, 2026-09-28 |
| SharePoint Lists, create site | Available | plan, browser check 2026-02-24 |
| Power Automate, standard connectors | Available (University environment). The "orders" Teams flow runs. | plan 2026-02-24; makerlab-bot DEVLOG |
| Microsoft Forms, Teams Workflows | Available | plan 2026-02-24 |
| Power Apps | **Not licensed** ("nobaptenant") | plan 2026-02-24 |
| Dataverse | **Assume not available.** It needs Power Apps or premium. Dataverse for Teams was not checked. | inference |
| Power Automate premium connectors (HTTP, Dataverse, custom) | **Unknown. Confirm with Technology Services.** It is a per-user paid add-on at list price. | not verified |
| Copilot Studio | **Not included.** Vishal's trial ended in April 2026; Microsoft's 2026-04-12 mail said "purchase a license to continue". Ask Technology Services about tenant capacity. | mailcorpus |
| M365 Copilot Chat | Basic tier | plan 2026-02-24 |
| Custom Teams bot | **Blocked.** No sideloading and no Graph admin consent. | makerlab-bot DEVLOG |
| Bookings | Not checked | — |

None of the mapping above needs a premium connector. Every flow uses the Office 365 Outlook, SharePoint, Forms and Teams connectors.

**Questions for Technology Services:**
1. Can a non-person MakerLab service account own the flows and send as uimakerlab?
2. Do we have premium connectors or Copilot Studio capacity, and at what cost?
3. Is Bookings enabled?
4. Will admin consent be given for `Sites.Selected` on one MakerLab site?
5. Can student workers get site and mailbox access on their NetIDs?

**Cost:** $0 extra on standard licenses. It saves $15/month, plus the Podio fee if Podio is paid. Copilot Studio or premium connectors would add cost, quoted by Technology Services.

**Effort (5 in-use apps, down from the 10-app estimate of 2 to 3 weeks):**

| Work | Days |
|---|---|
| Email and contact form (Option 2) | 1 |
| Orders + Transactions + Payments Lists, 4 flows, order form | 4 to 5 |
| Closing Notes form | 0.5 |
| Events/EventMaster, only if kept | 2 |
| Load history (5 apps, 11,502 items, from the archive export) | 1 |
| Staff training and a one-page runbook | 0.5 |
| **Total** | **about 7 to 10 working days** |

**Risks:**
- **Flow ownership:** a flow owned by a person's NetID stops working when that person leaves. Use a service account, or at least 2 co-owners, and list every flow in `docs/`.
- **Tenant limits:** no Power Apps, no sideloading, and admin consent for Graph. DLP policies may block mixing connectors, so test each flow early.
- **Access:** student workers need NetID access to the site, the Lists and the mailbox, and delegation can take days.
- **Orders is complex.** It will not port 1:1, so simplify the fields with Bayu first.
- **Copilot Studio** needs abuse guardrails and a privacy review, and it must read only the redacted knowledge base.
- **Timing:** finish before camp registration opens in January, and not during the fall term.

### Comparison

| | Email cost/month | Fixes sender defect | One place to answer | Order mail logged | Effort | Risk |
|---|---|---|---|---|---|---|
| 1 Keep and fix | $15 | Yes | No | Yes, automatic | 1 to 2 h | Low |
| **2 Outlook-first + pilot** | **$0 after the pilot** | **Yes** | **Yes** | **Sent: Bcc. Replies: manual** | **1 day + pilot** | **Medium** |
| 3 Podio Workflow Automation | $0 if included | Yes | No | Yes, if built | 1 to 2 days | Medium |
| 4 Microsoft 365 (5 apps) | $0 (+Podio, if paid) | Yes | Yes | Yes, by subject-tag flow | 7 to 10 days | Medium |

---

## 6. Archive plan for the dormant and dead apps (plan only; nothing exported yet)

**Scope:** 38 apps and 1,656 items: 5 dormant, 33 dead, plus Events and EventMaster if January decides to archive them. Add the 5 in-use apps as a frozen snapshot on the day each one moves.

**Export method (per app, all read-only):**
1. **Structure:** `GET /app/{id}` gives field definitions, then save `app.json`.
2. **Items:** `POST /item/app/{id}/filter/`, 100 per page. Write `items.jsonl` (raw) and `items.csv` (one column per field, values flattened).
3. **Comments and email history:** `GET /comment/item/{id}/`, only for items with `comment_count > 0`. GlobiMail and email-in messages are comments, so this captures email history. Each item also gets a Markdown file `items/<app_item_id>-<slug>.md` with its fields, then comments in date order.
4. **Files:** `GET /item/{id}` lists attached files, then download them to `files/<item_id>/`. Skip Podio's email-signature icons under 10 KB (known from the blog scripts).
5. **Cross-check:** the Podio UI *Export to Excel* (app menu, then Export) gives an independent field export with no comments or files. Compare its row count with `items.csv`.
6. **Proof:** a `MANIFEST.md` per app records item count, file count, comment count and export date. The archive counts as complete only when its counts match the live counts in §0.

**Layout:** `podio-archive/<workspace>/<app-name>/{app.json, items.csv, items.jsonl, items/*.md, files/, MANIFEST.md}` plus a top `README.md` with this inventory.

**Effort:** 1 day to write and test a resumable `export_app.py` (the inventory script used today is the base). Then about 2 to 3 hours of API time, limited by roughly 1,000 calls an hour; X-Rate-Limit-Remaining read 984 at the start today. In-use apps add more, because 11,502 items with comments means several hours across runs.

**Where it lives (decision for Vishal):**

| Option | Suits | Against |
|---|---|---|
| A. New **private** GitHub repo (`makerlab-podio-archive`) | Diffable and greppable by agents. Good for non-personal data. | Not Illinois-controlled storage for student or payment data. Private repos get shared by mistake, and this site's repo is public, so a slip is costly. |
| B. **Illinois SharePoint** site or folder owned by uimakerlab (or OneDrive) | Illinois-controlled storage with access by NetID. It is the natural source for Copilot Studio and for the Option 4 Lists. Retention can be applied. | Agents cannot read it today. Harder to diff. |
| **C. Both (recommended)** | SharePoint holds the **full** export, including personal data. The private repo holds only the **non-personal and redacted** set: app structures, templates, checklists, CommonPrints, EventMaster templates, the social-media and course plans, and order write-ups without names. | Two copies to keep consistent. The repo copy is generated from SharePoint by a redaction script, never edited by hand. |

**Personal data: never in a repo, full copy in SharePoint only:**

| App | Personal data likely present | Handling |
|---|---|---|
| UIMakerLab Emails, Orders | Customer names, emails, phones, order correspondence, some camp-parent mail | SharePoint only. A redacted Markdown set (names and addresses replaced with role tokens) may go in the repo for the knowledge base. |
| Payments, Transactions | Payment references, amounts tied to people | SharePoint only, never redacted into the repo. Ask the Gies business office about retention before deleting anything in Podio. |
| Volunteers, Private Events, Certificates, Feedback, 3dp MOOC Contacts and contact form, Certification Exams | Names, emails and phones of the public. Certificates and Volunteers may include **minors** from camps or events. | SharePoint only, in a restricted folder. Do not redact these into the knowledge base. |
| Timesheets (both), Gurus | Staff and student-worker hours and details (student records) | SharePoint only, in a restricted folder |
| Events | Camp sessions; check whether attendee names were stored | SharePoint first. Repo only after a check finds no attendee data. |

The redaction script must fail closed. Any email address, phone number or IPay/payment reference left after redaction blocks the repo commit. The check is a grep gate like the outbound one.

**After the archive is verified, with Vishal's approval:**
- Remove the live third-party hooks and flows on dead apps (GlobiMail on Volunteers and Transactions; PodioTools.com on 3 apps).
- Then delete or keep the dead workspaces. Keep the dormant ones read-only in Podio until the cutover.

---

## 7. Decisions

| Date | Decision | By | Status |
|---|---|---|---|
| 2026-10-16 | Dormant and dead Podio apps are **archived as a reference knowledge base, not migrated**. | Vishal (via control) | **Decided** |
| — | Which email option: 1, **2 (recommended)**, 3 or 4 | Vishal | Open |
| — | Cancel GlobiMail now, or after the 2-week order-email pilot (recommended, about $15 more) | Vishal | Open. The next charge is about 2026-10-26. |
| — | Archive location: SharePoint, private repo, or **both (recommended)** | Vishal | Open |
| — | Run the archive export (read-only) | Vishal | Not approved. No export run. |
| — | Send the Technology Services questions (§5, Option 4) | Vishal | Open |
| — | Events and EventMaster: migrate or archive | Vishal | January 2027, with the camp restore |
