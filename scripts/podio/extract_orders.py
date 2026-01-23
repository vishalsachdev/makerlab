"""
Extract Podio Orders with full details for analysis.
"""

import json
from podio_client import get_client

ORDERS_APP_ID = 6976602


def get_order_details(client, item_id):
    """Get full order details including comments and files."""
    item = client.get_item(item_id)
    comments = client.get(f"/comment/item/{item_id}/")

    # Extract field values and file links
    fields_dict = {}
    files = []

    for field in item.get("fields", []):
        label = field.get("label", field.get("external_id", "unknown"))
        values = field.get("values", [])
        if values:
            val = values[0]
            if "value" in val:
                v = val["value"]
                if isinstance(v, dict):
                    v = v.get("text", v.get("name", str(v)))
                fields_dict[label] = v
            elif "file" in val:
                f = val["file"]
                files.append({
                    "name": f.get("name"),
                    "link": f.get("link"),
                    "mimetype": f.get("mimetype")
                })

    # Extract comments and embedded files
    comment_list = []
    for comment in comments:
        text = comment.get("value", "")
        if text and not text.startswith("GlobiMail Activated"):
            author = comment.get("created_by", {}).get("name", "Unknown")
            date = comment.get("created_on", "")

            # Check for embedded files in comment
            for f in comment.get("files", []):
                files.append({
                    "name": f.get("name"),
                    "link": f.get("link"),
                    "mimetype": f.get("mimetype"),
                    "from_comment": True
                })

            comment_list.append({
                "author": author,
                "date": date,
                "text": text[:1000]  # Limit length
            })

    return {
        "item_id": item_id,
        "title": item.get("title", "Untitled"),
        "created": item.get("created_on", ""),
        "fields": fields_dict,
        "comments": comment_list[:20],  # Limit to 20 comments
        "files": files,
        "link": f"https://podio.com/illinois-makerlabpodiocom/daily-activities/apps/orders/items/{item_id}"
    }


def main():
    print("Connecting to Podio...")
    podio = get_client()

    print("Fetching orders...")
    result = podio.get_items(ORDERS_APP_ID, limit=50)
    items = result.get("items", [])

    print(f"Found {len(items)} orders. Fetching details...\n")

    orders = []
    for item in items:
        item_id = item["item_id"]
        title = item.get("title", item_id)
        print(f"  {title}...")

        try:
            order = get_order_details(podio, item_id)
            orders.append(order)
        except Exception as e:
            print(f"    Error: {e}")

    # Save to file
    output = {
        "total": len(orders),
        "orders": orders
    }

    with open("orders_extract.json", "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\nExtracted {len(orders)} orders to orders_extract.json")

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    for order in orders:
        files_count = len(order.get("files", []))
        comments_count = len(order.get("comments", []))
        print(f"\n{order['title']}")
        print(f"  Created: {order['created'][:10] if order['created'] else 'Unknown'}")
        print(f"  Files: {files_count}, Comments: {comments_count}")
        if order['fields'].get('Client'):
            print(f"  Client: {order['fields']['Client']}")
        if order['fields'].get('Status'):
            print(f"  Status: {order['fields']['Status']}")


if __name__ == "__main__":
    main()
