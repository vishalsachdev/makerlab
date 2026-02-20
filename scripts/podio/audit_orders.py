"""
Audit the Podio Orders app (ID: 6976602).
Produces a summary of total items, date range, activity levels, and field structure.
"""

import time
from datetime import datetime, timedelta
from podio_client import get_client

APP_ID = 6976602


def main():
    client = get_client()
    print("Authenticated successfully.\n")

    # 1. Total item count
    print("Fetching total item count...")
    result = client.post(f"/item/app/{APP_ID}/filter/", {"limit": 1})
    total = result["total"]
    print(f"  Total items: {total}")
    time.sleep(0.5)

    # 2. 5 most recent items
    print("\nFetching 5 most recent items...")
    recent = client.post(f"/item/app/{APP_ID}/filter/", {
        "limit": 5,
        "offset": 0,
        "sort_by": "created_on",
        "sort_desc": True,
    })
    print("  Most recent items:")
    for item in recent["items"]:
        created = item.get("created_on", "unknown")
        title = item.get("title", "(no title)")
        print(f"    - {title}  |  created: {created}  |  item_id: {item['item_id']}")
    time.sleep(0.5)

    # 3. 5 oldest items
    print("\nFetching 5 oldest items...")
    oldest = client.post(f"/item/app/{APP_ID}/filter/", {
        "limit": 5,
        "offset": 0,
        "sort_by": "created_on",
        "sort_desc": False,
    })
    print("  Oldest items:")
    for item in oldest["items"]:
        created = item.get("created_on", "unknown")
        title = item.get("title", "(no title)")
        print(f"    - {title}  |  created: {created}  |  item_id: {item['item_id']}")
    time.sleep(0.5)

    # 4. Count items in last 30 days, 90 days, 12 months
    # Paginate through recent items (sorted newest-first) until we pass the 12-month mark
    now = datetime.utcnow()
    cutoff_30 = now - timedelta(days=30)
    cutoff_90 = now - timedelta(days=90)
    cutoff_365 = now - timedelta(days=365)

    count_30 = 0
    count_90 = 0
    count_365 = 0
    done = False
    offset = 0
    batch_size = 100

    print("\nCounting items by recency (paginating newest-first)...")
    while not done:
        batch = client.post(f"/item/app/{APP_ID}/filter/", {
            "limit": batch_size,
            "offset": offset,
            "sort_by": "created_on",
            "sort_desc": True,
        })
        items = batch.get("items", [])
        if not items:
            break

        for item in items:
            created_str = item.get("created_on", "")
            if not created_str:
                continue
            # Podio format: "2026-02-19 14:30:00"
            try:
                created_dt = datetime.strptime(created_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue

            if created_dt >= cutoff_30:
                count_30 += 1
            if created_dt >= cutoff_90:
                count_90 += 1
            if created_dt >= cutoff_365:
                count_365 += 1
            else:
                # Past the 12-month window; since sorted desc, we can stop
                done = True
                break

        offset += batch_size
        if offset >= total:
            break
        print(f"  ...processed {min(offset, total)} / {total} items")
        time.sleep(0.5)

    print(f"\n  Items in last 30 days:  {count_30}")
    print(f"  Items in last 90 days:  {count_90}")
    print(f"  Items in last 12 months: {count_365}")

    # Calculate date range and average items/month
    oldest_date_str = oldest["items"][0].get("created_on", "") if oldest["items"] else ""
    newest_date_str = recent["items"][0].get("created_on", "") if recent["items"] else ""

    if oldest_date_str and newest_date_str:
        oldest_dt = datetime.strptime(oldest_date_str, "%Y-%m-%d %H:%M:%S")
        newest_dt = datetime.strptime(newest_date_str, "%Y-%m-%d %H:%M:%S")
        months_active = max(1, (newest_dt.year - oldest_dt.year) * 12 + (newest_dt.month - oldest_dt.month))
        avg_per_month = total / months_active
    else:
        oldest_dt = newest_dt = None
        months_active = 0
        avg_per_month = 0

    # 5. App field structure
    print("\nFetching app field structure...")
    time.sleep(0.5)
    app_info = client.get(f"/app/{APP_ID}")
    fields = app_info.get("fields", [])

    # ========== SUMMARY ==========
    print("\n" + "=" * 60)
    print("  PODIO ORDERS APP AUDIT SUMMARY")
    print("=" * 60)
    print(f"\n  Total items:          {total}")
    if oldest_dt and newest_dt:
        print(f"  Date range:           {oldest_dt.strftime('%Y-%m-%d')} to {newest_dt.strftime('%Y-%m-%d')}")
        print(f"  Months active:        {months_active}")
        print(f"  Avg items/month:      {avg_per_month:.1f}")
    print(f"\n  Items last 30 days:   {count_30}")
    print(f"  Items last 90 days:   {count_90}")
    print(f"  Items last 12 months: {count_365}")

    print(f"\n  Fields ({len(fields)}):")
    print(f"  {'Field Name':<40} {'Type':<20} {'External ID'}")
    print(f"  {'-'*40} {'-'*20} {'-'*30}")
    for f in fields:
        config = f.get("config", {})
        label = config.get("label", f.get("label", "(no label)"))
        ftype = f.get("type", "unknown")
        ext_id = f.get("external_id", "")
        print(f"  {label:<40} {ftype:<20} {ext_id}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
