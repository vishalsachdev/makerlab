"""
Audit the UIMakerLab Emails app (ID: 12703942) in Podio.
Produces a summary of total items, date range, activity buckets,
field structure, and status distribution.
"""

import time
from datetime import datetime, timedelta
from collections import Counter
from podio_client import get_client

APP_ID = 12703942


def main():
    client = get_client()
    print("Authenticated successfully.\n")

    # ── 1. Total item count ──────────────────────────────────────────
    print("Fetching total item count...")
    result = client.post(f"/item/app/{APP_ID}/filter/", {"limit": 1})
    total = result["total"]
    print(f"  Total items: {total}\n")
    time.sleep(0.5)

    # ── 2. 5 most recent items ───────────────────────────────────────
    print("Fetching 5 most recent items...")
    newest = client.post(f"/item/app/{APP_ID}/filter/", {
        "limit": 5,
        "sort_by": "created_on",
        "sort_desc": True,
    })
    print("  Most recent items:")
    for item in newest["items"]:
        print(f"    - Item {item['item_id']}: created {item['created_on']}  title: {item.get('title', 'N/A')}")
    newest_date = newest["items"][0]["created_on"] if newest["items"] else "N/A"
    time.sleep(0.5)

    # ── 3. 5 oldest items ────────────────────────────────────────────
    print("\nFetching 5 oldest items...")
    oldest = client.post(f"/item/app/{APP_ID}/filter/", {
        "limit": 5,
        "sort_by": "created_on",
        "sort_desc": False,
    })
    print("  Oldest items:")
    for item in oldest["items"]:
        print(f"    - Item {item['item_id']}: created {item['created_on']}  title: {item.get('title', 'N/A')}")
    oldest_date = oldest["items"][0]["created_on"] if oldest["items"] else "N/A"
    time.sleep(0.5)

    # ── 4. Count items by time buckets ───────────────────────────────
    now = datetime.utcnow()
    cutoff_30 = now - timedelta(days=30)
    cutoff_90 = now - timedelta(days=90)
    cutoff_365 = now - timedelta(days=365)

    count_30 = 0
    count_90 = 0
    count_365 = 0

    print("\nCounting items by date buckets (paginating recent items)...")
    offset = 0
    batch_size = 100
    done = False

    while not done:
        batch = client.post(f"/item/app/{APP_ID}/filter/", {
            "limit": batch_size,
            "offset": offset,
            "sort_by": "created_on",
            "sort_desc": True,
        })
        items = batch["items"]
        if not items:
            break

        for item in items:
            # Parse created_on — format: "2024-01-15 14:30:00"
            created_str = item["created_on"]
            try:
                created = datetime.strptime(created_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                # Some Podio dates include timezone info
                created = datetime.fromisoformat(created_str.replace("Z", "+00:00")).replace(tzinfo=None)

            if created >= cutoff_30:
                count_30 += 1
            if created >= cutoff_90:
                count_90 += 1
            if created >= cutoff_365:
                count_365 += 1
            else:
                # Past the 365-day boundary; no need to continue
                done = True
                break

        offset += batch_size
        if offset >= total:
            break
        print(f"  ... processed {min(offset, total)} / {total} items")
        time.sleep(0.5)

    print(f"  Items in last 30 days:  {count_30}")
    print(f"  Items in last 90 days:  {count_90}")
    print(f"  Items in last 12 months: {count_365}")

    # Average items per month
    if oldest_date != "N/A":
        try:
            first = datetime.strptime(oldest_date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            first = datetime.fromisoformat(oldest_date.replace("Z", "+00:00")).replace(tzinfo=None)
        months = max(1, (now - first).days / 30.44)
        avg_per_month = total / months
        print(f"  Average items/month:    {avg_per_month:.1f}")
    time.sleep(0.5)

    # ── 5. App details / field structure ─────────────────────────────
    print("\nFetching app details...")
    app = client.get(f"/app/{APP_ID}")
    app_name = app.get("config", {}).get("name", "Unknown")
    print(f"  App name: {app_name}")
    print(f"  App ID:   {APP_ID}")

    fields = app.get("fields", [])
    print(f"\n  Fields ({len(fields)}):")
    print(f"  {'Field Name':<35} {'External ID':<30} {'Type':<15}")
    print(f"  {'-'*35} {'-'*30} {'-'*15}")

    category_field_ids = []
    for field in fields:
        fname = field.get("config", {}).get("label", field.get("label", "?"))
        ftype = field.get("type", "?")
        ext_id = field.get("external_id", "?")
        print(f"  {fname:<35} {ext_id:<30} {ftype:<15}")
        if ftype == "category":
            category_field_ids.append((field["field_id"], fname, field))

    time.sleep(0.5)

    # ── 6. Category / status field distributions ─────────────────────
    if category_field_ids:
        print(f"\n  Category field distributions:")
        for field_id, fname, field_def in category_field_ids:
            # Show the possible options from field config
            options = field_def.get("config", {}).get("settings", {}).get("options", [])
            option_map = {opt["id"]: opt.get("text", str(opt["id"])) for opt in options}
            print(f"\n  --- {fname} (field_id={field_id}) ---")
            if options:
                print(f"  Defined options: {', '.join(option_map.values())}")

            # Count distribution by filtering
            dist = Counter()
            offset2 = 0
            while True:
                batch2 = client.post(f"/item/app/{APP_ID}/filter/", {
                    "limit": 100,
                    "offset": offset2,
                    "sort_by": "created_on",
                    "sort_desc": True,
                })
                items2 = batch2["items"]
                if not items2:
                    break
                for item in items2:
                    found = False
                    for f in item.get("fields", []):
                        if f.get("field_id") == field_id:
                            for val in f.get("values", []):
                                v = val.get("value", {})
                                if isinstance(v, dict):
                                    dist[v.get("text", str(v.get("id", "?")))] += 1
                                else:
                                    dist[str(v)] += 1
                            found = True
                            break
                    if not found:
                        dist["(empty)"] += 1
                offset2 += 100
                if offset2 >= total:
                    break
                time.sleep(0.5)

            print(f"  Distribution (total {sum(dist.values())}):")
            for val, cnt in dist.most_common():
                pct = cnt / max(1, sum(dist.values())) * 100
                print(f"    {val:<30} {cnt:>6}  ({pct:5.1f}%)")
    else:
        print("\n  No category fields found — skipping status distribution.")

    # ── Summary ──────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("AUDIT SUMMARY: UIMakerLab Emails App")
    print("=" * 60)
    print(f"  App Name:           {app_name}")
    print(f"  App ID:             {APP_ID}")
    print(f"  Total Items:        {total}")
    print(f"  Date Range:         {oldest_date} → {newest_date}")
    print(f"  Last 30 days:       {count_30}")
    print(f"  Last 90 days:       {count_90}")
    print(f"  Last 12 months:     {count_365}")
    if oldest_date != "N/A":
        print(f"  Avg items/month:    {avg_per_month:.1f}")
    print(f"  Number of fields:   {len(fields)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
