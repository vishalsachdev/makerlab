"""
Audit Podio Events workspace apps.
Gets item counts, recent activity, and field definitions for each app.
"""

import time
from datetime import datetime
from podio_client import get_client

APPS = [
    {"name": "EventMaster", "id": 9968618, "desc": "Event type templates"},
    {"name": "Events", "id": 6701476, "desc": "Scheduled event instances"},
    {"name": "Venues", "id": 6790713, "desc": "Venues"},
    {"name": "Attendees", "id": 11369317, "desc": "Attendees"},
    {"name": "Volunteers", "id": 12648457, "desc": "Volunteers"},
    {"name": "Private Events", "id": 14134963, "desc": "Private events"},
]

FIELD_TYPE_MAP = {
    "text": "Text",
    "number": "Number",
    "image": "Image",
    "date": "Date",
    "app": "App Reference",
    "category": "Category",
    "contact": "Contact",
    "embed": "Embed/Link",
    "money": "Money",
    "phone": "Phone",
    "email": "Email",
    "calculation": "Calculation",
    "duration": "Duration",
    "progress": "Progress",
    "location": "Location",
    "question": "Question",
    "member": "Member",
    "video": "Video",
    "tag": "Tag",
}


def audit_app(client, app_info):
    """Audit a single app: item count, recent items, field definitions."""
    app_id = app_info["id"]
    result = {
        "name": app_info["name"],
        "id": app_id,
        "desc": app_info["desc"],
        "total_items": 0,
        "last_activity": None,
        "recent_items": [],
        "fields": [],
        "error": None,
    }

    # 1. Get total item count (filter with limit=1)
    try:
        filter_resp = client.post(f"/item/app/{app_id}/filter/", {
            "limit": 1,
            "sort_by": "created_on",
            "sort_desc": True,
        })
        result["total_items"] = filter_resp.get("total", 0)
        time.sleep(0.5)
    except Exception as e:
        result["error"] = f"Filter failed: {e}"
        return result

    # 2. Get 3 most recent items
    if result["total_items"] > 0:
        try:
            recent_resp = client.post(f"/item/app/{app_id}/filter/", {
                "limit": 3,
                "sort_by": "created_on",
                "sort_desc": True,
            })
            for item in recent_resp.get("items", []):
                item_info = {
                    "item_id": item.get("item_id"),
                    "title": item.get("title", "(no title)"),
                    "created_on": item.get("created_on"),
                    "last_event_on": item.get("last_event_on"),
                }
                result["recent_items"].append(item_info)

            if result["recent_items"]:
                result["last_activity"] = result["recent_items"][0].get("last_event_on") or result["recent_items"][0].get("created_on")
            time.sleep(0.5)
        except Exception as e:
            result["error"] = f"Recent items failed: {e}"

    # 3. Get app details for field definitions
    try:
        app_details = client.get(f"/app/{app_id}")
        for field in app_details.get("fields", []):
            field_type = field.get("type", "unknown")
            field_info = {
                "external_id": field.get("external_id", ""),
                "label": field.get("config", {}).get("label", field.get("label", "")),
                "type": FIELD_TYPE_MAP.get(field_type, field_type),
                "raw_type": field_type,
            }
            # For category fields, get options
            if field_type == "category":
                options = field.get("config", {}).get("settings", {}).get("options", [])
                field_info["options"] = [opt.get("text", "") for opt in options]
            # For app reference fields, get referenced app
            if field_type == "app":
                ref_apps = field.get("config", {}).get("settings", {}).get("referenced_apps", [])
                field_info["references"] = [
                    {"app_id": ra.get("app_id"), "name": ra.get("app", {}).get("name", "?")}
                    for ra in ref_apps
                ]
            result["fields"].append(field_info)
        time.sleep(0.5)
    except Exception as e:
        result["error"] = f"App details failed: {e}"

    return result


def print_app_report(r):
    """Print a formatted report for one app."""
    print(f"\n{'='*70}")
    print(f"  {r['name']} (App ID: {r['id']})")
    print(f"  {r['desc']}")
    print(f"{'='*70}")

    if r["error"]:
        print(f"  ERROR: {r['error']}")

    print(f"\n  Total items: {r['total_items']}")
    print(f"  Last activity: {r['last_activity'] or 'N/A'}")

    if r["recent_items"]:
        print(f"\n  3 Most Recent Items:")
        for i, item in enumerate(r["recent_items"], 1):
            title = item['title'][:60] if item['title'] else "(no title)"
            print(f"    {i}. {title}")
            print(f"       ID: {item['item_id']}  |  Created: {item['created_on']}  |  Last event: {item['last_event_on']}")
    else:
        print("\n  No items found.")

    if r["fields"]:
        print(f"\n  Fields ({len(r['fields'])}):")
        for f in r["fields"]:
            line = f"    - {f['label']} ({f['external_id']}) — {f['type']}"
            if f.get("options"):
                line += f"  [{', '.join(f['options'])}]"
            if f.get("references"):
                refs = ", ".join(f"{ref['name']} ({ref['app_id']})" for ref in f["references"])
                line += f"  -> {refs}"
            print(line)
    print()


def classify_activity(r):
    """Classify app as active, low-activity, or dormant based on last activity."""
    if r["total_items"] == 0:
        return "empty"
    if not r["last_activity"]:
        return "unknown"
    try:
        # Podio dates: "2026-02-18 14:30:00"
        last = datetime.strptime(r["last_activity"][:19], "%Y-%m-%d %H:%M:%S")
        days_ago = (datetime.now() - last).days
        if days_ago <= 30:
            return "active"
        elif days_ago <= 180:
            return "low-activity"
        else:
            return "dormant"
    except (ValueError, TypeError):
        return "unknown"


def main():
    print("Authenticating with Podio...")
    client = get_client()
    print("Authenticated.\n")

    results = []
    for app_info in APPS:
        print(f"Auditing {app_info['name']} (ID: {app_info['id']})...")
        r = audit_app(client, app_info)
        results.append(r)

    # Print individual reports
    for r in results:
        print_app_report(r)

    # Print overall summary
    print("\n" + "=" * 70)
    print("  EVENTS WORKSPACE SUMMARY")
    print("=" * 70)
    print(f"\n  {'App Name':<20} {'Items':>7}  {'Last Activity':<22} {'Status'}")
    print(f"  {'-'*18:<20} {'-'*7:>7}  {'-'*20:<22} {'-'*12}")

    for r in results:
        status = classify_activity(r)
        status_label = {
            "active": "ACTIVE (< 30d)",
            "low-activity": "LOW (30-180d)",
            "dormant": "DORMANT (> 180d)",
            "empty": "EMPTY",
            "unknown": "UNKNOWN",
        }[status]
        last = r["last_activity"][:10] if r["last_activity"] else "N/A"
        print(f"  {r['name']:<20} {r['total_items']:>7}  {last:<22} {status_label}")

    total_items = sum(r["total_items"] for r in results)
    active_count = sum(1 for r in results if classify_activity(r) == "active")
    print(f"\n  Total items across all apps: {total_items}")
    print(f"  Active apps (last 30 days): {active_count}/{len(results)}")
    print()


if __name__ == "__main__":
    main()
