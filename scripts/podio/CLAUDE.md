# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python scripts for interacting with the Podio API to manage Illinois MakerLab operations. Primary use case is extracting order data and images from the "Orders" app for blog content generation on the MakerLab website.

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

## Podio API Notes

- Comments endpoint: `/comment/item/{item_id}/`
- File download: `/file/{file_id}/raw` with OAuth2 header
- GlobiMail integration adds email threads as comments (filter out "GlobiMail Activated" messages)
- Item fields have varying structures - check for `value`, `file`, or `embed` keys
