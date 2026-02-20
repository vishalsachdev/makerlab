"""
Podio Organization Inventory
Lists all workspaces, apps, item counts, and last activity for org 528575.
"""

import time
from datetime import datetime, timezone
from podio_client import get_client

ORG_ID = 528575
SIX_MONTHS_AGO = datetime.now(timezone.utc).replace(microsecond=0) - __import__('datetime').timedelta(days=180)


def get_item_count_and_last_activity(client, app_id):
    """Get total item count and most recent item's created_on date."""
    try:
        result = client.post(f"/item/app/{app_id}/filter/", {
            "limit": 1,
            "sort_by": "created_on",
            "sort_desc": True,
        })
        total = result.get("total", 0)
        last_activity = None
        if result.get("items"):
            last_activity = result["items"][0].get("created_on")
        return total, last_activity
    except Exception as e:
        return None, None


def parse_date(date_str):
    """Parse Podio date string to datetime."""
    if not date_str:
        return None
    # Podio dates look like "2026-02-18 14:23:00"
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def is_dormant(total, last_activity_str):
    """Flag as dormant if 0 items or no activity in 6+ months."""
    if total is not None and total == 0:
        return True
    dt = parse_date(last_activity_str)
    if dt and dt < SIX_MONTHS_AGO:
        return True
    return False


def main():
    client = get_client()
    print(f"Authenticated. Inventorying org {ORG_ID}...\n")

    # Step 1: Get all workspaces
    print("Fetching workspaces...")
    spaces = client.get(f"/org/{ORG_ID}/space/")
    print(f"Found {len(spaces)} workspaces.\n")
    time.sleep(0.5)

    # Step 2: For each workspace, get apps and item counts
    workspace_data = []

    for space in spaces:
        space_id = space["space_id"]
        space_name = space["name"]
        print(f"--- Workspace: {space_name} (ID: {space_id}) ---")

        try:
            apps = client.get(f"/app/space/{space_id}/")
        except Exception as e:
            print(f"  ERROR fetching apps: {e}")
            workspace_data.append({
                "name": space_name,
                "space_id": space_id,
                "apps": [],
                "total_items": 0,
                "error": str(e),
            })
            time.sleep(0.5)
            continue

        time.sleep(0.5)

        app_list = []
        ws_total = 0

        for app in apps:
            app_id = app["app_id"]
            app_name = app.get("config", {}).get("name", app.get("name", "Unknown"))
            print(f"  Querying: {app_name} (app_id={app_id})...", end=" ", flush=True)

            total, last_activity = get_item_count_and_last_activity(client, app_id)
            time.sleep(0.5)

            dormant = is_dormant(total, last_activity)
            flag = " ** DORMANT **" if dormant else ""

            if total is not None:
                ws_total += total
                print(f"{total} items, last activity: {last_activity or 'N/A'}{flag}")
            else:
                print(f"ERROR fetching items{flag}")

            app_list.append({
                "app_id": app_id,
                "name": app_name,
                "total": total,
                "last_activity": last_activity,
                "dormant": dormant,
            })

        workspace_data.append({
            "name": space_name,
            "space_id": space_id,
            "apps": app_list,
            "total_items": ws_total,
        })
        print()

    # Sort workspaces by total items descending
    workspace_data.sort(key=lambda w: w["total_items"], reverse=True)

    # Print summary
    print("\n" + "=" * 80)
    print("PODIO ORGANIZATION INVENTORY — Illinois MakerLab (org 528575)")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Dormant = 0 items OR no new items in 6+ months (before {SIX_MONTHS_AGO.strftime('%Y-%m-%d')})")
    print("=" * 80)

    grand_total = 0
    total_apps = 0
    dormant_apps = 0

    for ws in workspace_data:
        ws_total = ws["total_items"]
        grand_total += ws_total
        n_apps = len(ws["apps"])
        total_apps += n_apps
        n_dormant = sum(1 for a in ws["apps"] if a["dormant"])
        dormant_apps += n_dormant

        dormant_note = f"  ({n_dormant} dormant)" if n_dormant else ""
        print(f"\n{'─' * 70}")
        print(f"WORKSPACE: {ws['name']}  (space_id={ws['space_id']})")
        print(f"  Total items: {ws_total:,} across {n_apps} apps{dormant_note}")

        if ws.get("error"):
            print(f"  ⚠ Error: {ws['error']}")
            continue

        if not ws["apps"]:
            print("  (no apps)")
            continue

        # Sort apps by total items descending
        sorted_apps = sorted(ws["apps"], key=lambda a: a["total"] or 0, reverse=True)
        for app in sorted_apps:
            flag = " [DORMANT]" if app["dormant"] else ""
            total_str = f"{app['total']:,}" if app["total"] is not None else "ERROR"
            last_str = app["last_activity"] or "N/A"
            print(f"    {app['name']:<40} app_id={app['app_id']:<12} items={total_str:<8} last={last_str}{flag}")

    print(f"\n{'=' * 80}")
    print(f"GRAND TOTAL: {grand_total:,} items across {total_apps} apps in {len(workspace_data)} workspaces")
    print(f"DORMANT APPS: {dormant_apps} of {total_apps}")
    print("=" * 80)


if __name__ == "__main__":
    main()
