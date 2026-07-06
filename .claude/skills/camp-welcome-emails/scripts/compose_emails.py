#!/usr/bin/env python3
"""Open Outlook compose windows for camp welcome emails (NEVER sends).

Usage:
    python3 compose_emails.py data/parent-emails/<slug>-rosters.json            # all emails
    python3 compose_emails.py <rosters.json> --only adventures                  # one camp id
    python3 compose_emails.py <rosters.json> --only allday                      # combined email
    python3 compose_emails.py <rosters.json> --dry-run                          # print, no Outlook

For each email group in the rosters JSON (built by build_rosters.py), this:
  1. reads the draft markdown at the group's `draft_file` (recipient header above
     the first `---` is stripped; body below it is the email),
  2. converts body md -> HTML with pandoc, wraps it in an Aptos 12pt div,
  3. opens a Microsoft Outlook compose window via AppleScript with
     To = "Illinois MakerLab" <uimakerlab@illinois.edu> and each family
     email as a BCC recipient.

It stops at the open compose window — the user reviews, switches the From
account to uimakerlab@illinois.edu (delegate access), and sends manually.
Requires: Outlook for Mac running, pandoc installed, macOS Automation permission.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TO_NAME = "Illinois MakerLab"
TO_ADDR = "uimakerlab@illinois.edu"


def find_repo_root() -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "data" / "summer-camps-2026.json").exists():
            return parent
    raise RuntimeError("Could not locate makerlab repo root")


ROOT = find_repo_root()


def parse_draft(path: Path) -> tuple[str, str]:
    """Return (subject, body_markdown). Header above first `---` holds Subject."""
    text = path.read_text()
    if "\n---\n" not in text:
        sys.exit(f"FATAL: {path} has no `---` separator between header and body.")
    header, body = text.split("\n---\n", 1)
    m = re.search(r"^\*\*Subject:\*\*\s*(.+)$", header, re.MULTILINE)
    if not m:
        sys.exit(f"FATAL: no '**Subject:** ...' line in the header of {path}.")
    return m.group(1).strip(), body.strip()


def md_to_html(md: str) -> str:
    res = subprocess.run(["pandoc", "-f", "markdown", "-t", "html"],
                         input=md, capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"pandoc failed: {res.stderr}")
    return ('<div style="font-family: Aptos, \'Segoe UI\', sans-serif; '
            f'font-size: 12pt;">{res.stdout}</div>')


def esc(s: str) -> str:
    """Escape a string for embedding in AppleScript double quotes."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def open_compose(subject: str, html: str, bcc: list[str]) -> None:
    bcc_lines = "\n".join(
        f'    make new bcc recipient at newMsg with properties '
        f'{{email address:{{address:"{esc(a)}"}}}}' for a in bcc
    )
    script = f'''
tell application "Microsoft Outlook"
    set newMsg to make new outgoing message with properties {{subject:"{esc(subject)}", content:"{esc(html)}"}}
    make new recipient at newMsg with properties {{email address:{{name:"{esc(TO_NAME)}", address:"{esc(TO_ADDR)}"}}}}
{bcc_lines}
    open newMsg
    activate
end tell
'''
    with tempfile.NamedTemporaryFile("w", suffix=".applescript", delete=False) as f:
        f.write(script)
        tmp = f.name
    res = subprocess.run(["osascript", tmp], capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"osascript failed: {res.stderr}\n(Is Outlook running? Automation permission granted?)")


def main() -> None:
    ap = argparse.ArgumentParser(description="Open Outlook compose windows for welcome emails")
    ap.add_argument("rosters", help="Path to <slug>-rosters.json from build_rosters.py")
    ap.add_argument("--only", help="camp_id (e.g. adventures) or 'allday' — compose just one email")
    ap.add_argument("--dry-run", action="store_true", help="Print recipients/subjects, no Outlook")
    args = ap.parse_args()

    data = json.loads(Path(args.rosters).read_text())

    groups = []  # (label, draft_file, families)
    for s in data["sessions"]:
        if args.only and args.only != s["camp_id"]:
            continue
        groups.append((f'{s["camp_name"]} {s["dates"]} ({s["period"]})',
                       s["draft_file"], s["families"]))
    ad = data.get("all_day", {})
    if ad.get("families") and (not args.only or args.only == "allday"):
        groups.append((f'ALL-DAY combined {data["week"]}', ad["draft_file"], ad["families"]))

    if not groups:
        sys.exit("No matching email groups.")

    blocked = False
    for label, draft_file, families in groups:
        bcc = [e for f in families for e in f["emails"]]
        missing = [f["parent"] for f in families if not f["emails"]]
        draft_path = ROOT / draft_file
        print(f"\n=== {label} ===")
        print(f"Draft: {draft_file}")
        print(f"BCC ({len(bcc)}): {', '.join(bcc) or '—'}")
        if missing:
            print(f"!! MISSING EMAIL for: {', '.join(missing)} — resolve before/right after sending "
                  f"(FormBuilder admin or uimakerlab OWA), then send them a separate copy.")
        if not families:
            print("No non-all-day families for this session — skipping.")
            continue
        if not draft_path.exists():
            print(f"!! Draft file missing: {draft_file} — write it first (see SKILL.md step 4).")
            blocked = True
            continue
        subject, body_md = parse_draft(draft_path)
        print(f"Subject: {subject}")
        if args.dry_run:
            continue
        if not bcc:
            print("No resolvable addresses at all — NOT opening a compose window.")
            continue
        open_compose(subject, md_to_html(body_md), bcc)
        print("Compose window opened. REMINDER: switch the From account to "
              "uimakerlab@illinois.edu before sending. This script never sends.")

    if blocked:
        sys.exit(1)


if __name__ == "__main__":
    main()
