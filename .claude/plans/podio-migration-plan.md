# Plan: Migrate Off Podio + GlobiMail

**Created**: 2026-02-19
**Updated**: 2026-02-24 (access verification complete)
**Status**: Access verified, ready to execute
**Savings**: ~$290/year (Podio Plus $14/mo + GlobiMail $15/mo)

---

## Current State

### What We Pay
- **Podio Plus**: ~$14/month
- **GlobiMail Core**: $15/month (3-app limit for email integration)
- **Total**: ~$29/month ($348/year)

### What We Actually Use (10 of 45 apps)

| App | Items | Monthly Volume | Complexity |
|-----|------:|----------------|------------|
| UIMakerLab Emails | 3,716 | ~18/mo | Simple (7 fields) |
| Transactions | 3,199 | High | Medium |
| Orders | 2,049 | ~9/mo | Complex (35 fields, calculations, app refs) |
| Closing Notes | 1,827 | High | Simple |
| Events | 906 | Seasonal | Complex (31 fields, app refs) |
| Timesheets | 486 | Slowing | Medium |
| Payments | 147 | Low | Medium |
| EventMaster | 52 | Templates only | Simple (8 fields) |
| Checklists | 49 | Active | Simple |
| CommonPrints | 9 | Low | Simple |

### What's Dead (can delete)
- 35 dormant apps across 7 workspaces
- 4 empty workspaces (Coursera-Analytics, Employee Network, iMBA-SocialMediaProject, MakersUIUC-Summer)
- 3 fully dormant workspaces (CTA Social Media, 3dp MOOC, iMBA-TechStars — 2016-2018 era)
- Attendees app (returns 410 Gone)
- Volunteers (last real activity 2020), Private Events (last 2022), Certificates, Feedback

### Email App Issues
- 64% of emails (2,390) stuck in "open" status — untriaged backlog
- GlobiMail only needed for compose/reply; Outlook shared mailbox already receives the emails

---

## Available Tools (Already Licensed, $0 Extra)

UIUC is a Microsoft E3/E5 shop:
- **Outlook / Exchange** — shared mailboxes, native email
- **Microsoft Teams** — channels, chat, integrations
- **SharePoint Lists** — lightweight database (replaces Podio apps)
- **Power Automate** — workflow automation (basic flows with O365)
- ~~**PowerApps** — custom apps on SharePoint/Dataverse~~ **NOT AVAILABLE** (see below)
- **Microsoft Forms** — intake forms
- **Asana** — project/task management (already licensed)
- **UIUC SMTP Relay** — Cloud Email Delivery for campus apps

### Access Verification (2026-02-24)

Verified via browser automation against `vishal@illinois.edu`:

| Service | URL | Status | Notes |
|---------|-----|--------|-------|
| **SharePoint** | `uillinoisedu.sharepoint.com` | Full access | Can create sites + lists. "Create site" button available. Existing sites visible (Gies Grad Programs, ALA Accreditation, etc.) |
| **Power Automate** | `make.powerautomate.com` | Full access | University of Illinois environment (`Default-44467e6f-462c-4ea2-823f-7800de5434e3`). Can create flows, templates, approvals, solutions. |
| **Power Apps** | `make.powerapps.com` | **No license** | "Sorry, you'll need to sign up" — not included in UIUC license. Redirects to `/error/nobaptenant`. |
| **M365 Copilot** | `m365.cloud.microsoft` | Available | Copilot Chat (Basic) tier. |
| **Microsoft Teams** | `teams.microsoft.com` | Full access | Multiple teams, Apps store, Workflows, Agents. Copilot added by org. |

**Key finding**: SharePoint domain is `uillinoisedu.sharepoint.com` (not `illinois.sharepoint.com`).

**Impact of no Power Apps**: Power Apps was planned for custom UI on the Orders app (35 fields). Without it, the alternatives are:
1. **SharePoint List built-in forms** — adequate for most apps, supports custom views and conditional formatting
2. **SharePoint List + custom formatting (JSON)** — column/view formatting for richer UI without Power Apps
3. **Microsoft Forms → Power Automate → SharePoint List** — for intake workflows (e.g., new orders)
4. **Direct Graph API access** — for script-based automation (blog generation, bulk operations)

SharePoint Lists alone cover all 10 Podio apps. Power Apps would have been nice-to-have for the Orders app but is not a blocker.

### Teams Bot & Data Interaction (2026-02-24)

Verified via Teams Apps store (`teams.microsoft.com`):

**Available bot/workflow capabilities:**
- **Workflows (Power Automate in Teams)** — full access to workflow templates:
  - "Notify a team of new SharePoint list items" — post to channel when new SP list item created
  - "Send webhook alerts to a channel/chat" — external systems → Teams via webhook
  - "Start an approval when a response is submitted in Forms" — Forms → Approval → Teams
  - "Notify the chat when a new Forms response is submitted"
  - "Create a task in Planner from Microsoft Forms and post message in Teams"
  - Categories: Approval, Calendar, Data collection, Notifications, Productivity
- **Copilot (org-deployed)** — available with "Open" button, Copilot Chat (Basic) tier
  - "Copilot Preview - Get my tasks from MS To Do and Planner"
  - "Copilot Preview - List Pending Approvals"
- **Existing org bots**: IT Help Desk Bot, LeaveBot, Calendar BOT, Ivanti Neurons Bot, PharmaBot
- **Agents section** — "Personalize lessons using Agents" featured, "New agent" option visible in M365 Copilot sidebar
- **Lists app** — available to add directly in Teams (SharePoint Lists embedded in Teams channels)
- **SharePoint app** — available to add as a Teams tab

**How staff would interact with MakerLab data via Teams:**

1. **Passive notifications**: Power Automate flow triggers on new SharePoint List items → posts Adaptive Card to a MakerLab Teams channel (e.g., "New order received: [customer] [project]")
2. **Embedded Lists**: Add the Lists app as a tab in a MakerLab Teams channel — staff view/edit/filter SharePoint List data without leaving Teams
3. **Approval workflows**: New order submitted → Power Automate sends approval request in Teams → staff approves/rejects with a click → status updates in SharePoint List
4. **Webhook integration**: Python scripts can POST to Teams Incoming Webhook URLs to send alerts (e.g., auto-reply system notifies when it classifies an email as NEEDS_HUMAN)
5. **Copilot queries** (future): Once SharePoint Lists have data, Copilot may be able to answer natural language queries about orders, events, etc. — depends on Copilot tier and Graph indexing.

**~~Not available without Power Apps:~~** → **RESOLVED via Azure Bot Service + Chat SDK**

### Azure Portal & App Registrations (2026-02-25)

Verified via `portal.azure.com` with `vishal@illinois.edu`:

| Resource | Status | Notes |
|----------|--------|-------|
| **Azure Portal** | Full access | "Create a resource" available |
| **Azure Subscriptions** | 2 active | `urbana-gies-onlineprograms`, `urbana-vcl-citrix` |
| **App Registrations** | Full access | "New registration" available. 5 existing apps owned. |
| **Azure OpenAI** | Available | Listed in top services |
| **Existing Resources** | SQL database + server | `mySampleDatabase`, `badm554fall2025` |

**Existing app registrations (owned by vishal@illinois.edu):**
- `ChatwithMSBAResumes` (9/2023, secrets expired)
- `chatwithmsbaresumes` (9/2023, secrets expired)
- `jbtcchat` (11/2023, secrets expired)
- `Portals-MSBA At Gies` (9/2024, secrets expired)
- `Project Management Mentor (Microsoft Copilot Studio)` (9/2024, active)

**Key finding**: You've already built Teams chat bots and used Copilot Studio before. Full Azure access means we can create an Azure Bot resource + app registration for a custom MakerLab bot.

### Custom MakerLab Bot (Chat SDK + Azure Bot Service)

Using [Chat SDK Teams adapter](https://www.chat-sdk.dev/docs/adapters/teams) — **no Power Apps or Copilot Studio license needed**.

**Architecture:**
```
Staff in Teams → @MakerLabBot "show recent orders"
       ↓
Azure Bot Service → Chat SDK bot (Node.js on Vercel)
       ↓
Microsoft Graph API → SharePoint Lists (Orders, Events, etc.)
       ↓
Bot responds with Adaptive Card showing data
```

**Setup required:**
1. Azure AD app registration (new, with client secret) — you have access
2. Azure Bot resource (free tier) under `urbana-gies-onlineprograms` subscription
3. Node.js webhook endpoint hosted on Vercel (free)
4. Graph API permissions: `Sites.ReadWrite.All`, `Lists.ReadWrite.All`
5. Teams app package (manifest.json + icons) uploaded to Teams

**Bot capabilities:**
- Natural language queries: "show orders this week", "any new emails?"
- Adaptive Card responses with formatted data
- Create/update SharePoint List items from Teams chat
- File upload support (e.g., attach STL files to orders)
- Can be added to any Teams channel or used in DM

**Cost: $0** — Azure Bot Service free tier (10K messages/mo), Vercel free tier, existing Azure subscription

---

## Recommended Migration: Option A (Microsoft-Native)

### Phase 1: Drop GlobiMail Immediately (saves $15/mo)
**Effort: 1 day**

The email workflow doesn't need GlobiMail at all:
1. uimakerlab@illinois.edu is already an Outlook shared mailbox
2. Staff can reply directly from Outlook (no compose links needed)
3. Build a simple Python script (`email_reply.py`) for bulk replies via UIUC SMTP
4. Optionally: Power Automate rule to post new emails to a Teams channel

What we built today (Chrome automation to reply via GlobiMail) proves we can automate replies. The SMTP version would be simpler and faster.

### Phase 2: Migrate Email Tracking to SharePoint List or Asana (saves nothing, improves workflow)
**Effort: 2-3 days**

Replace Podio Emails app with:
- **Option A**: SharePoint List "Email Inbox" — Power Automate creates rows from new emails
- **Option B**: Asana project "Email Inbox" — Power Automate creates tasks from new emails
- **Option C**: Just use Outlook categories/folders + Teams channel (simplest)

### Phase 3: Migrate Daily Activities Apps (biggest migration)
**Effort: 1-2 weeks**

| Podio App | Migrate To | Notes |
|-----------|-----------|-------|
| Orders | SharePoint List + custom JSON formatting | Most complex (35 fields, calculations). Consider simplifying. No Power Apps available — use built-in forms + JSON column formatting. |
| Transactions | SharePoint List | High volume, need Power Automate for notifications |
| Closing Notes | SharePoint List or Teams channel | Simple text entries |
| Timesheets | SharePoint List or existing HR system | Usage declining, may not need |
| Payments | SharePoint List | Low volume |
| Checklists | SharePoint List or Planner | Simple |
| CommonPrints | SharePoint List | Tiny |

**Key challenge**: Orders app has 35 fields with calculations and app references. May want to simplify during migration rather than replicate 1:1. Without Power Apps, use SharePoint List built-in forms + JSON column/view formatting for richer UI.

**Blog generation scripts**: Update `podio_client.py` → `graph_client.py` using Microsoft Graph API + `msal` Python library. SharePoint Lists are accessible via Graph API.

**API access**: Requires an Azure AD app registration with Graph API permissions (Sites.ReadWrite.All, Lists.ReadWrite.All). Note: UIUC admin has disabled GCP project creation — Azure AD app registration access needs to be verified separately.

### Phase 4: Migrate Events Apps
**Effort: 3-5 days**

| Podio App | Migrate To | Notes |
|-----------|-----------|-------|
| EventMaster | SharePoint List "Event Templates" | 52 templates, simple |
| Events | SharePoint List "Events" with lookup to Templates | 906 items, 31 fields |
| Venues | Drop or merge into Events | Only 1 active venue |
| Delete | Attendees, Volunteers, Private Events, Certificates, Feedback | All dormant |

### Phase 5: Cancel Podio (saves $14/mo)
- Export all data via API first (we have full access)
- Archive to JSON/CSV in the makerlab repo
- Cancel subscription

---

## Alternative Options Considered

### Option B: Asana-Centered
- Use Asana for all tracking, Power Automate as glue
- **Pro**: Single tool, great UI/mobile
- **Con**: Asana isn't a database — no calculations, relational data, or app references

### Option C: Hybrid (Teams + SharePoint + Asana)
- SharePoint Lists = database, Asana = tasks, Teams = communication
- **Pro**: Best of each tool
- **Con**: More complex, staff learns 3 tools

### Option D: Custom Python Scripts Only
- Keep Podio as read-only archive, build Python scripts for everything
- **Pro**: Full control, $0 cost
- **Con**: No UI for staff, maintenance burden

### Option E: Just Drop GlobiMail, Keep Podio
- Replace GlobiMail with Python SMTP scripts
- Keep Podio for everything else
- **Pro**: Minimal disruption, saves $15/mo
- **Con**: Still paying $14/mo for Podio

---

## Data Export Plan (Before Canceling Anything)

Before canceling Podio, export everything:
```bash
# Scripts to build:
python export_all_items.py --app orders --output exports/orders.json
python export_all_items.py --app emails --output exports/emails.json
python export_all_items.py --app events --output exports/events.json
python export_all_items.py --app eventmaster --output exports/eventmaster.json
# etc.
```

Already have `extract_orders.py` and `fetch_images.py` as starting points.

---

## Decision Matrix

| Option | Monthly Savings | Effort | Risk | Staff Impact |
|--------|:--------------:|:------:|:----:|:------------:|
| Drop GlobiMail only | $15 | 1 day | Low | Minimal |
| Drop GlobiMail + Podio → Microsoft | $29 | 2-3 weeks | Medium | Training needed |
| Drop GlobiMail + Podio → Asana | $29 | 1-2 weeks | Medium | Training needed |
| Keep everything | $0 | 0 | None | None |

---

## Next Steps

1. **Decision**: Which option to pursue? (Can start with Phase 1 regardless)
2. **Phase 1**: Build SMTP reply script, test, then cancel GlobiMail
3. **If migrating**: Pick target platform, build export scripts, set up new system
4. **Timeline**: Phase 1 can happen this week. Full migration is a spring project.

---

## Audit Scripts (for re-running)

All in `/Users/vishal/code/makerlab/scripts/podio/`:
- `inventory_org.py` — full org inventory
- `audit_orders.py` — Orders app deep dive
- `audit_emails_app.py` — Emails app deep dive
- `audit_events_apps.py` — Events workspace audit
- `check_email_app.py` — GlobiMail/email integration investigation
- `find_unreplied_camp_emails.py` — find unreplied emails (reusable)
