#!/usr/bin/env python3
"""Fetch registration data from FormBuilder API and update session availability on the website.

Usage:
    python3 scripts/update_availability.py          # fetch + update
    python3 scripts/update_availability.py --dry-run # fetch + show counts, don't write files

Requires: Bearer token in FORMBUILDER_TOKEN env var or data/.env file.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "summer-camps-2026.json"
SNAPSHOT_PATH = ROOT / "data" / "registrations-snapshot.json"
AVAILABILITY_PATH = ROOT / "data" / "session-availability.json"

ENDPOINT_ID = "d182387d-ce09-4fbd-b114-b40f011cdd90"
API_URL = f"https://appserv7.admin.uillinois.edu/FormBuilderService/api/DataEndpoint/{ENDPOINT_ID}"

# Map API field names → camp IDs in summer-camps-2026.json
FIELD_TO_CAMP = {
    "Minecraft and 3D Printing": "minecraft",
    "Adventures in 3D Modeling": "adventures",
    "GenAI and 3d Printing": "genai",
    "Build Your Own Robot Arm": "robot-arm",
    "AI Robotics with Reachy Mini": "reachy",
}

# Map FormBuilder session codes → session index (chronological order)
CODE_TO_SESSION = {
    "minecraft": {
        "MINECRAFT_JUN1": 0, "MINECRAFT_JUN2": 1, "MINECRAFT_JUN3": 2,
        "MINECRAFT_JUL2": 3, "MINECRAFT_JUL3": 4, "MINECRAFT_JUL4": 5,
    },
    "adventures": {"ADV3D_JUN1": 0, "ADV3D_JUL1": 1},
    "genai": {"GENAI3D_JUN1": 0, "GENAI3D_JUL1": 1},
    "robot-arm": {"ROBOTARM_JUN1": 0, "ROBOTARM_JUN2": 1, "ROBOTARM_JUL1": 2},
    "reachy": {"AIROBOTICS_JUN1": 0, "AIROBOTICS_JUL1": 1, "AIROBOTICS_JUL2": 2},
}


def get_token() -> str:
    """Read token from env var or data/.env file."""
    token = os.environ.get("FORMBUILDER_TOKEN")
    if token:
        return token
    env_path = ROOT / "data" / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("FORMBUILDER_TOKEN="):
                return line.split("=", 1)[1].strip()
    raise RuntimeError("Set FORMBUILDER_TOKEN env var or add it to data/.env")


def fetch_registrations(token: str) -> list[dict]:
    """Fetch all registrations from FormBuilder API."""
    req = urllib.request.Request(API_URL, headers={
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    })
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def compute_availability(registrations: list[dict], camps: list[dict]) -> dict:
    """Compute per-session availability from registration data."""
    # Count registrations per session code
    camp_counts: dict[str, dict[str, int]] = {}
    for field, cid in FIELD_TO_CAMP.items():
        codes: dict[str, int] = {}
        for r in registrations:
            val = r.get(field, "").strip()
            if val:
                for code in val.split(", "):
                    codes[code] = codes.get(code, 0) + 1
        camp_counts[cid] = codes

    # Build availability per camp
    availability = {}
    for camp in camps:
        cid = camp["id"]
        max_c = camp["max_campers"]
        mapping = CODE_TO_SESSION.get(cid, {})
        counts = camp_counts.get(cid, {})
        avail = []
        for i in range(len(camp["sessions"])):
            code = next((c for c, idx in mapping.items() if idx == i), None)
            count = counts.get(code, 0) if code else 0
            remaining = max(0, max_c - count)
            avail.append({"count": count, "max": max_c, "remaining": remaining})
        availability[cid] = avail
    return availability


def waitlist_mailto(camp_name: str, session_summary: str) -> str:
    """Generate a mailto link for waitlist requests."""
    import urllib.parse
    subject = urllib.parse.quote(f"Waitlist Request: {camp_name} — {session_summary}")
    body = urllib.parse.quote(
        f"Hi,\n\nI would like to join the waitlist for:\n\n"
        f"Camp: {camp_name}\nSession: {session_summary}\n\n"
        f"Camper Name: \nParent/Guardian Name: \nEmail: \nPhone: \n\nThank you!"
    )
    return f'<a href="mailto:uimakerlab@illinois.edu?subject={subject}&body={body}" style="color: #0455A4; text-decoration: underline;">Join Waitlist</a>'


def badge_html(remaining: int, camp_name: str = "", session_summary: str = "") -> str:
    """Generate availability badge HTML."""
    if remaining <= 0:
        sold_out = '<span style="color: #d32f2f; font-weight: bold;">SOLD OUT</span>'
        if camp_name and session_summary:
            return f'{sold_out} · {waitlist_mailto(camp_name, session_summary)}'
        return sold_out
    elif remaining <= 2:
        return f'<span style="color: #e04e39; font-weight: bold;">{remaining} spot{"" if remaining == 1 else "s"} left</span>'
    else:
        return f"{remaining} spots left"


def update_summer_html(camps: list[dict], availability: dict) -> None:
    """Update session lines on summer.html with availability badges."""
    path = ROOT / "summer.html"
    content = path.read_text()

    for camp in camps:
        cid = camp["id"]
        avail = availability[cid]
        parts = camp["summary_sessions_line"].split(", ")

        # Build regex that matches the session line with or without existing badges
        # Each part like "Jun 1–5 (AM)" possibly followed by " — ..." (badge text or plain)
        old_pattern_parts = []
        for part in parts:
            escaped = re.escape(part)
            old_pattern_parts.append(escaped + r"(?:\s*—\s*(?:<span[^>]*>.*?</span>(?:\s*·\s*<a[^>]*>.*?</a>)?|\d+ spots? left))?")
        old_pattern = r"<br>".join(old_pattern_parts)

        # Build new line with badges for ALL sessions
        new_parts = []
        for i, part in enumerate(parts):
            new_parts.append(f'{part} — {badge_html(avail[i]["remaining"], camp["name"], part)}')
        new_line = "<br>".join(new_parts)

        content = re.sub(old_pattern, new_line, content, count=1)

    path.write_text(content)


def update_detail_pages(camps: list[dict], availability: dict) -> None:
    """Update session tables on detail pages with availability column."""
    for camp in camps:
        cid = camp["id"]
        path = ROOT / camp["detail_file"]
        content = path.read_text()
        avail = availability[cid]

        # Ensure Availability header exists
        if "Availability</th>" not in content:
            content = content.replace(
                '<th style="padding: 0.5rem; text-align: left;">Time</th>\n                </tr>',
                '<th style="padding: 0.5rem; text-align: left;">Time</th>\n                  <th style="padding: 0.5rem; text-align: left;">Availability</th>\n                </tr>',
            )

        # Update or add availability cell for each session row
        for i, session in enumerate(camp["sessions"]):
            remaining = avail[i]["remaining"]
            session_summary = f'{session["dates"]} ({session["time"]})'
            badge = badge_html(remaining, camp["name"], session_summary)
            date_str = re.escape(session["dates"])
            time_str = re.escape(session["time"])

            # Match the full row: date cell + time cell, optionally existing availability cell, then </tr>
            pattern = (
                rf"({date_str}</td><td[^>]*>{time_str}</td>)"
                rf"(?:<td[^>]*>.*?</td>)?"
                rf"(</tr>)"
            )
            replacement = rf'\1<td style="padding: 0.5rem;">{badge}</td>\2'
            content = re.sub(pattern, replacement, content, count=1)

        path.write_text(content)


def print_report(camps: list[dict], availability: dict, registrations: list[dict]) -> None:
    """Print availability report to stdout."""
    total_cap = 0
    total_filled = 0

    print(f"Registrations fetched: {len(registrations)}")
    print()

    for camp in camps:
        cid = camp["id"]
        avail = availability[cid]
        print(f"{camp['name']} (max {camp['max_campers']}/session)")
        for i, session in enumerate(camp["sessions"]):
            a = avail[i]
            total_cap += a["max"]
            total_filled += a["count"]
            remaining = a["remaining"]
            if remaining <= 0:
                status = "SOLD OUT"
            elif remaining <= 2:
                status = f"{remaining} spot{'s' if remaining != 1 else ''} left"
            else:
                status = f"{remaining} spots left"
            print(f"  {session['dates']} ({session['time']}): {a['count']}/{a['max']} — {status}")
        print()

    print(f"Total: {total_filled}/{total_cap} filled, {total_cap - total_filled} spots remaining")


def main() -> None:
    parser = argparse.ArgumentParser(description="Update camp session availability")
    parser.add_argument("--dry-run", action="store_true", help="Show counts without updating files")
    args = parser.parse_args()

    camps_data = json.loads(DATA_PATH.read_text())
    camps = camps_data["camps"]

    token = get_token()
    registrations = fetch_registrations(token)

    # Save snapshot
    SNAPSHOT_PATH.write_text(json.dumps(registrations, indent=2) + "\n")

    availability = compute_availability(registrations, camps)

    # Save availability
    AVAILABILITY_PATH.write_text(json.dumps(availability, indent=2) + "\n")

    print_report(camps, availability, registrations)

    if args.dry_run:
        print("\n(dry run — no files updated)")
        return

    update_summer_html(camps, availability)
    update_detail_pages(camps, availability)
    print("\nWebsite updated.")


if __name__ == "__main__":
    main()
