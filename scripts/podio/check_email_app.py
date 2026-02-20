"""
Investigate the uimakerlab-emails app in Podio.

Discovers the app in the "lab-operations" workspace, inspects its fields,
lists recent items, and checks for hooks/flows.

Usage:
    python check_email_app.py

Podio API docs referenced:
    - Get space by org + URL label: GET /space/org/{org_id}/url/{url_label}
    - Get apps by space: GET /app/space/{space_id}/
    - Get app details: GET /app/{app_id}
    - Filter items: POST /item/app/{app_id}/filter/
    - Get hooks: GET /hook/app/{app_id}/
    - Get comments on item: GET /comment/item/{item_id}/
    - Add comment to item: POST /comment/item/{item_id}/
"""

import json
import sys
import time
from podio_client import get_client

# Known org ID from existing scripts
ORG_ID = 528575

# The workspace URL slug from the Podio URL:
# https://podio.com/illinois-makerlab/lab-operations/apps/uimakerlab-emails
SPACE_URL_LABEL = "lab-operations"

# We'll discover the app ID dynamically
EMAIL_APP_SLUG = "uimakerlab-emails"


def separator(title):
    """Print a section separator."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def find_lab_operations_space(client):
    """Find the lab-operations workspace by URL label."""
    separator("STEP 1: Find 'lab-operations' workspace")

    # Method 1: Try the direct URL-label lookup
    # GET /space/org/{org_id}/url/{url_label}
    try:
        space = client.get(f"/space/org/{ORG_ID}/url/{SPACE_URL_LABEL}")
        print(f"Found workspace via URL label lookup:")
        print(f"  Name: {space.get('name')}")
        print(f"  Space ID: {space.get('space_id')}")
        print(f"  URL: {space.get('url')}")
        print(f"  URL label: {space.get('url_label')}")
        return space
    except Exception as e:
        print(f"URL label lookup failed: {e}")
        print("Falling back to listing all workspaces...\n")

    # Method 2: List all workspaces and search by name/URL
    workspaces = client.get(f"/org/{ORG_ID}/space/")
    print(f"Found {len(workspaces)} workspaces in org {ORG_ID}:\n")

    target_space = None
    for ws in workspaces:
        name = ws.get("name", "Unnamed")
        sid = ws.get("space_id")
        url = ws.get("url", "")
        url_label = ws.get("url_label", "")
        marker = ""
        if "lab-operations" in url.lower() or "lab-operations" in url_label.lower():
            target_space = ws
            marker = "  <-- TARGET"
        print(f"  {name} (ID: {sid}) - {url_label}{marker}")

    if not target_space:
        # Also check by name
        for ws in workspaces:
            if "lab" in ws.get("name", "").lower() and "operation" in ws.get("name", "").lower():
                target_space = ws
                break

    if target_space:
        print(f"\nTarget workspace: {target_space.get('name')} (ID: {target_space.get('space_id')})")
    else:
        print("\nWARNING: Could not find 'lab-operations' workspace.")
        print("Listing all workspaces above for manual identification.")

    return target_space


def find_email_app(client, space_id):
    """Find the uimakerlab-emails app in the workspace."""
    separator("STEP 2: Find 'uimakerlab-emails' app")

    apps = client.get(f"/app/space/{space_id}/")
    print(f"Found {len(apps)} apps in workspace {space_id}:\n")

    email_app = None
    for app in apps:
        config = app.get("config", {})
        name = config.get("name", "Unnamed")
        app_id = app.get("app_id")
        url_label = app.get("url_label", "")
        marker = ""
        if EMAIL_APP_SLUG in url_label.lower() or "email" in name.lower():
            email_app = app
            marker = "  <-- TARGET"
        print(f"  {name} (ID: {app_id}, slug: {url_label}){marker}")

    if email_app:
        print(f"\nFound email app: {email_app.get('config', {}).get('name')} "
              f"(ID: {email_app.get('app_id')})")
    else:
        print(f"\nWARNING: Could not find app with slug '{EMAIL_APP_SLUG}'")
        print("Check the app names above for the correct one.")

    return email_app


def inspect_app_details(client, app_id):
    """Get full app details including all field definitions."""
    separator("STEP 3: App details and field structure")

    app = client.get(f"/app/{app_id}")

    config = app.get("config", {})
    print(f"App Name: {config.get('name')}")
    print(f"App ID: {app_id}")
    print(f"Item Name: {config.get('item_name', 'N/A')}")
    print(f"Description: {config.get('description', 'N/A')}")
    print(f"Default View: {config.get('default_view', 'N/A')}")
    print(f"Allow Comments: {config.get('allow_comments', 'N/A')}")
    print(f"Allow Attachments: {config.get('allow_attachments', 'N/A')}")

    # Mailbox info (important for email apps!)
    mailbox = app.get("mailbox", None)
    if mailbox:
        print(f"\nMailbox: {json.dumps(mailbox, indent=2)}")
    else:
        print(f"\nMailbox: None configured")

    # Integration info
    integration = app.get("integration", None)
    if integration:
        print(f"\nIntegration: {json.dumps(integration, indent=2)}")

    # Fields
    fields = app.get("fields", [])
    print(f"\n--- Fields ({len(fields)}) ---\n")

    for field in fields:
        fid = field.get("field_id")
        ext_id = field.get("external_id")
        ftype = field.get("type")
        fconfig = field.get("config", {})
        label = fconfig.get("label", ext_id)
        description = fconfig.get("description", "")
        required = fconfig.get("required", False)
        settings = fconfig.get("settings", {})

        print(f"  [{ftype}] {label}")
        print(f"    field_id: {fid}")
        print(f"    external_id: {ext_id}")
        print(f"    required: {required}")
        if description:
            print(f"    description: {description}")
        if settings:
            # Show category options, app references, etc.
            if ftype == "category":
                options = settings.get("options", [])
                if options:
                    opt_str = ", ".join(
                        f"{o.get('id')}={o.get('text', o.get('status', '?'))}"
                        for o in options[:10]
                    )
                    print(f"    options: [{opt_str}]")
            elif ftype == "app":
                ref_apps = settings.get("referenced_apps", [])
                if ref_apps:
                    for ra in ref_apps:
                        print(f"    references app: {ra.get('app_id')} ({ra.get('app', {}).get('name', '?')})")
            elif ftype == "contact":
                contact_type = settings.get("type", "")
                if contact_type:
                    print(f"    contact_type: {contact_type}")
            else:
                # Show first few settings keys
                keys = list(settings.keys())[:5]
                if keys:
                    print(f"    settings keys: {keys}")
        print()

    return app


def list_recent_items(client, app_id, limit=5):
    """List a few recent items to understand how the app is used."""
    separator(f"STEP 4: Recent items (last {limit})")

    result = client.post(f"/item/app/{app_id}/filter/", {
        "limit": limit,
        "offset": 0,
        "sort_by": "created_on",
        "sort_desc": True,
    })

    total = result.get("total", 0)
    items = result.get("items", [])
    print(f"Total items in app: {total}")
    print(f"Showing most recent {len(items)}:\n")

    for item in items:
        item_id = item.get("item_id")
        title = item.get("title", "Untitled")
        created = item.get("created_on", "Unknown")
        created_by = item.get("created_by", {}).get("name", "Unknown")

        print(f"  [{item_id}] {title}")
        print(f"    Created: {created} by {created_by}")

        # Show field values
        for field in item.get("fields", []):
            label = field.get("label", field.get("external_id", "?"))
            values = field.get("values", [])
            if values:
                val = values[0]
                if "value" in val:
                    v = val["value"]
                    if isinstance(v, dict):
                        v = v.get("text", v.get("name", v.get("title", str(v))))
                    # Truncate long values
                    v_str = str(v)
                    if len(v_str) > 120:
                        v_str = v_str[:120] + "..."
                    print(f"    {label}: {v_str}")
                elif "embed" in val:
                    print(f"    {label}: [embed: {val['embed'].get('original_url', 'attached')}]")
                elif "file" in val:
                    print(f"    {label}: [file: {val['file'].get('name', 'attached')}]")

        print()

    # Get comments on the first item to see email thread patterns
    if items:
        first_item_id = items[0]["item_id"]
        first_title = items[0].get("title", "Untitled")
        print(f"--- Comments on most recent item: [{first_item_id}] {first_title} ---\n")

        time.sleep(0.5)  # Rate limiting
        comments = client.get(f"/comment/item/{first_item_id}/")
        print(f"  Total comments: {len(comments)}\n")

        for i, comment in enumerate(comments[:5], 1):
            author = comment.get("created_by", {}).get("name", "Unknown")
            created = comment.get("created_on", "")
            value = comment.get("value", "")
            files = comment.get("files", [])

            # Truncate long comments
            if len(value) > 300:
                value = value[:300] + "... [truncated]"

            print(f"  Comment {i}: {author} ({created})")
            if files:
                print(f"    Attachments: {len(files)} files")
            print(f"    {value}")
            print()

        if len(comments) > 5:
            print(f"  ... and {len(comments) - 5} more comments")

    return items


def check_hooks(client, app_id):
    """Check for webhooks/flows configured on the app."""
    separator("STEP 5: Hooks and flows")

    try:
        hooks = client.get(f"/hook/app/{app_id}/")
        print(f"Found {len(hooks)} hooks on app {app_id}:\n")

        for hook in hooks:
            hook_id = hook.get("hook_id")
            status = hook.get("status")
            htype = hook.get("type")
            url = hook.get("url", "N/A")
            print(f"  Hook {hook_id}:")
            print(f"    Status: {status}")
            print(f"    Type/Event: {htype}")
            print(f"    URL: {url}")
            print()

        if not hooks:
            print("  No webhooks configured on this app.")
            print("  (Workflow Automation flows create hooks, but may also show here.)")

    except Exception as e:
        print(f"  Error fetching hooks: {e}")
        print("  (You may need admin access to view hooks.)")


def summarize_email_capabilities():
    """Print a summary of what we learned about Podio email capabilities."""
    separator("SUMMARY: Podio Email API Capabilities")

    print("""
Podio provides several mechanisms for email integration:

1. APP MAILBOX (Built-in)
   - Each app can have a unique email address (e.g., appname+token@podio.com)
   - Emails sent TO this address create new items or add comments
   - Check the 'mailbox' field in app details above

2. GLOBIMAIL (Third-party integration)
   - Adds "GlobiMail Activated" comment to items with a compose link
   - Emails sent VIA GlobiMail appear as comments on items
   - Incoming emails matched to items also become comments
   - Already active on the Orders app (we filter these in extract_orders.py)

3. COMMENTS API (for triggering email flows)
   - POST /comment/item/{item_id}/ — add comment to an item
   - Body: {"value": "text", "file_ids": [...], "embed_url": "..."}
   - If GlobiMail or Workflow Automation is configured, adding a comment
     can trigger an email send

4. WORKFLOW AUTOMATION (GlobiFlow)
   - Can trigger on: item.create, item.update, comment.create
   - Actions available: "Send Email", "Create Comment", custom webhooks
   - "Send Email" action can use GlobiMail to send from your email
   - Replies can trigger flows back (Email Reply trigger)

5. HOOKS/WEBHOOKS API
   - GET /hook/app/{app_id}/ — list hooks on an app
   - POST /hook/app/{app_id}/ — create a webhook
   - Supported events: item.create, item.update, comment.create, etc.

KEY INSIGHT: To send emails via Podio API, you would typically:
  a) Create an item in an email-focused app (if it has GlobiMail/flow)
  b) Add a comment to an item (if comment.create triggers an email flow)
  c) Use the app mailbox address as the reply-to in external emails
  d) Use Workflow Automation's "Send Email" action (GUI-only, not API)

NEXT STEPS:
  - Run this script to discover the email app's structure
  - Look for GlobiMail integration on the email app
  - Check if Workflow Automation flows exist (hooks will show them)
  - Test creating an item or comment to see if it triggers email
""")


def main():
    print("Podio Email App Investigation")
    print("Authenticating...")

    client = get_client()
    print("Authenticated successfully!")

    # Step 1: Find the workspace
    space = find_lab_operations_space(client)
    if not space:
        print("\nERROR: Could not find lab-operations workspace. Exiting.")
        sys.exit(1)

    space_id = space.get("space_id")
    time.sleep(0.5)  # Rate limiting

    # Step 2: Find the email app
    email_app = find_email_app(client, space_id)
    if not email_app:
        print("\nERROR: Could not find email app. Check the app list above.")
        sys.exit(1)

    app_id = email_app.get("app_id")
    time.sleep(0.5)

    # Step 3: Get full app details (fields, config, mailbox)
    app_details = inspect_app_details(client, app_id)
    time.sleep(0.5)

    # Step 4: List recent items
    items = list_recent_items(client, app_id, limit=5)
    time.sleep(0.5)

    # Step 5: Check hooks/flows
    check_hooks(client, app_id)

    # Summary
    summarize_email_capabilities()

    # Save raw app details to JSON for reference
    output_file = "email_app_details.json"
    with open(output_file, "w") as f:
        json.dump(app_details, f, indent=2, default=str)
    print(f"Raw app details saved to {output_file}")


if __name__ == "__main__":
    main()
