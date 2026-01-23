"""
Inspect a specific order in detail.
"""

from podio_client import get_client
import json
import sys

ORDERS_APP_ID = 6976602


def inspect_order(client, item_id):
    """Get full details of an order including all comments."""
    print(f"Fetching order {item_id}...\n")

    # Get the item
    item = client.get_item(item_id)

    print(f"Title: {item.get('title', 'Untitled')}")
    print(f"Created: {item.get('created_on', 'Unknown')}")
    print(f"Link: {item.get('link', '')}")

    # Print all fields
    print("\n--- FIELDS ---")
    for field in item.get("fields", []):
        external_id = field.get("external_id", "unknown")
        label = field.get("label", external_id)
        values = field.get("values", [])

        if values:
            val = values[0]
            if "value" in val:
                v = val["value"]
                if isinstance(v, dict):
                    v = v.get("text", v.get("name", str(v)))
                print(f"  {label}: {v}")
            elif "embed" in val:
                print(f"  {label}: [File: {val['embed'].get('original_url', 'attached')}]")
            elif "file" in val:
                print(f"  {label}: [File: {val['file'].get('name', 'attached')}]")

    # Get comments
    print("\n--- COMMENTS/EMAILS ---")
    comments = client.get(f"/comment/item/{item_id}/")

    for i, comment in enumerate(comments, 1):
        created = comment.get("created_on", "")
        created_by = comment.get("created_by", {}).get("name", "Unknown")
        value = comment.get("value", "")

        # Skip GlobiMail activation messages
        if value.startswith("GlobiMail Activated"):
            continue

        print(f"\n[{i}] {created_by} - {created}")
        print("-" * 40)

        # Clean up and show the comment
        # Trim very long comments
        if len(value) > 2000:
            print(value[:2000] + "\n... [truncated]")
        else:
            print(value)

    return item, comments


def main():
    if len(sys.argv) < 2:
        print("Usage: python inspect_order.py <item_id>")
        print("\nExamples from recent scan:")
        print("  python inspect_order.py 3178374184  # eye_tracker_sensor")
        print("  python inspect_order.py 3159959623  # Keychain_Phone_Holder")
        print("  python inspect_order.py 3133696461  # Illini Dice")
        print("  python inspect_order.py 3211041335  # cyberrunner")
        return

    item_id = sys.argv[1]
    client = get_client()
    inspect_order(client, item_id)


if __name__ == "__main__":
    main()
