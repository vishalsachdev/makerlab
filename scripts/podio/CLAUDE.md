# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python scripts for interacting with the Podio API to manage Illinois MakerLab operations. We have full API access (read/write/delete) to all Podio workspaces and apps. Primary use cases:
- Extracting order data and images from the "Orders" app for blog content generation
- Managing EventMaster templates and Events for summer camps and other programming

## Key Configuration

**Environment variables** (`.env`):
- `PODIO_CLIENT_ID` - OAuth client ID from developers.podio.com
- `PODIO_CLIENT_SECRET` - OAuth client secret
- `PODIO_USERNAME` - Podio account email
- `PODIO_PASSWORD` - Podio account password

**Important IDs**:
- Organization: Illinois MakerLab (528575)
- Workspace: Daily Activities (1801600)
  - Orders App: 6976602
- Workspace: Events (1801593)
  - EventMaster App: 9968618 (event type templates — camps, workshops, birthdays, etc.)
  - Events App: 6701476 (individual scheduled events with dates, linked to EventMaster)
  - Venues App: 6790713 (Illinois Makerlab venue ID: 2603449486)
  - Attendees App: 11369317
  - Volunteers App: 12648457
  - Private Events App: 14134963

## Commands

```bash
# Test Podio connection and list all orgs/workspaces/apps
python podio_client.py

# Extract recent orders with full details to orders_extract.json
python extract_orders.py

# Inspect a single order by item ID
python inspect_order.py <item_id>

# Download images from specific orders to makerlab blog folder
python fetch_images.py
```

## Architecture

```
podio_client.py      # Core API client - all other scripts import get_client()
├── extract_orders.py    # Bulk export orders to JSON
├── inspect_order.py     # Single order deep-dive with comments
├── fetch_images.py      # Download images from orders
└── scan_orders.py       # Keyword-based blog opportunity search
```

**PodioClient** handles OAuth2 password-flow authentication. Access tokens are valid for 8 hours. The client provides convenience methods for common operations:
- `get_organizations()`, `get_workspaces(org_id)`, `get_apps(space_id)`
- `get_items(app_id, limit, offset)` - uses filter endpoint
- `get_item(item_id)` - single item with all fields
- Raw `get(endpoint)` and `post(endpoint, data)` for direct API calls

## Related Repository

Downloaded images go to `/Users/vishal/code/makerlab/images/blog/` for the MakerLab website. Blog posts generated from order data are created in `/Users/vishal/code/makerlab/blog/`.

## EventMaster / Events Management

**EventMaster** (app 9968618) stores event type templates. Key fields:
- `title` (text) — event type name
- `short-description` (text) — HTML description
- `signups-enabled` (category) — YES/NO
- `event-instructions` (text), `sample-outputsimages` (image), `link-to-resources` (embed)

**Events** (app 6701476) stores individual scheduled events. Key fields:
- `event-name` (text) — event name
- `date` (date) — `{"start": "YYYY-MM-DD HH:MM:SS", "end": "YYYY-MM-DD HH:MM:SS"}`
- `eventtype` (app ref) — links to EventMaster item ID
- `venue-2` (app ref) — links to Venues item ID (Illinois Makerlab = 2603449486)
- `event-signup-status` (category) — 1=Open, 2=Closed, 3=Pending, 4=Attending
- `category` (category) — 1=Paid, 2=Free, 3=Private
- `status` (category) — 2=Scheduled, 1=Cancelled
- `event-description` (text), `guru-incharge` (contact), `number-of-attendeesfor-makergirl` (number)

**API operations**:
- Create item: `POST /item/app/{app_id}/` with `{"fields": {...}}`
- Update item: `PUT /item/{item_id}` with `{"fields": {...}}`
- Delete item: `DELETE /item/{item_id}`
- Use `?silent=true&hook=false` on deletes to avoid triggering webhooks

**Summer 2026 EventMaster IDs**:
- Minecraft + 3D Printing: 3086747010
- Adventures in 3D Modeling and Printing: 3086793565
- Generative AI + 3D Printing: 3124317517
- Build Your Own Robot Arm: 3253950597
- AI Robotics with Reachy Mini: 3253950609

## Podio API Notes

- Comments endpoint: `/comment/item/{item_id}/`
- File download: `/file/{file_id}/raw` with OAuth2 header
- GlobiMail integration adds email threads as comments (filter out "GlobiMail Activated" messages)
- Item fields have varying structures - check for `value`, `file`, or `embed` keys
- **Rate limits**: ~200 requests before 1-hour cooldown. Use `time.sleep(0.5-1)` between bulk operations. Rate limit is per-account, not per-token.
