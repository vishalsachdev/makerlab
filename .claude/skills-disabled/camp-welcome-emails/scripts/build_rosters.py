#!/usr/bin/env python3
"""Build per-session parent-email rosters for camps starting a target Monday.

Usage:
    python3 build_rosters.py                      # target = next Monday (>= 4 days out)
    python3 build_rosters.py --monday 2026-07-06  # explicit target Monday

Reads (all under the makerlab repo root, resolved automatically):
    data/registrations-snapshot.json   live registrations (run scripts/update_availability.py first!)
    data/summer-camps-2026.json        camp/session config (source of truth for dates)
    data/registrations-*.csv           dated roster CSV for cross-assertion (if it covers the week)
    data/*ReportDump*.csv              newest FormBuilder report dump, for parent emails
    data/cancellations.csv             fallback emails + defense-in-depth cancellation check

Writes:
    data/parent-emails/<slug>-rosters.json   (gitignored; NEVER write PII outside data/)

SAFETY: session codes are mapped to sessions ONLY via CODE_TO_SESSION imported from
scripts/update_availability.py. FormBuilder codes are NOT chronological (e.g. for
"reachy", AIROBOTICS_JUL1 = Jul 27-31 and AIROBOTICS_JUL2 = Jul 6-10). Never infer
a session from the code text. This script exists because doing so once sent welcome
emails to the wrong week's roster (2026-07-05 incident).
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import sys
import unicodedata
from datetime import date, timedelta
from pathlib import Path


def find_repo_root() -> Path:
    """Walk upward from this file until we find the makerlab repo root."""
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "data" / "summer-camps-2026.json").exists():
            return parent
    raise RuntimeError("Could not locate makerlab repo root (data/summer-camps-2026.json)")


ROOT = find_repo_root()

# Import the AUTHORITATIVE code->session mapping. update_availability.py is
# import-safe (constants + functions only; main() is __main__-guarded), so this
# cannot drift the way a copied dict would.
sys.path.insert(0, str(ROOT / "scripts"))
import update_availability as ua  # noqa: E402

FIELD_TO_CAMP = ua.FIELD_TO_CAMP
CODE_TO_SESSION = ua.CODE_TO_SESSION

MONTH_ABBR = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
              7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}


def norm(s: str) -> str:
    """Normalize a name/label for comparison: unicode, whitespace, case."""
    s = unicodedata.normalize("NFKC", s or "")
    return " ".join(s.split()).casefold()


def norm_dash(s: str) -> str:
    """Normalize en-dash vs hyphen so 'Jul 6-10' == 'Jul 6–10'."""
    return (s or "").replace("–", "-").replace("—", "-")


def next_monday(today: date) -> tuple[date, list[str]]:
    """Next Monday >= 4 days out (skill normally runs Wednesdays -> 5 days)."""
    warnings = []
    days_ahead = (7 - today.weekday()) % 7  # Monday = 0
    if days_ahead == 0:
        days_ahead = 7
    candidate = today + timedelta(days=days_ahead)
    if (candidate - today).days < 4:
        warnings.append(
            f"SKIPPING the imminent Monday {candidate.isoformat()} (only "
            f"{(candidate - today).days} days out; the >=4-day rule assumes its welcome "
            f"emails already went out last Wednesday). Use --monday {candidate.isoformat()} "
            f"to target it anyway."
        )
        candidate += timedelta(days=7)
    lead = (candidate - today).days
    if lead != 5:
        warnings.append(
            f"Lead time is {lead} days (normal Wednesday run = 5). "
            f"Adjust the 'next week'/'on Monday' wording in the drafts if needed."
        )
    return candidate, warnings


def week_bits(monday: date) -> tuple[str, str]:
    """Return (dates_label, slug) for a Mon-Fri camp week, e.g. ('Jul 6–10', 'jul-6-10')."""
    friday = monday + timedelta(days=4)
    if monday.month == friday.month:
        label = f"{MONTH_ABBR[monday.month]} {monday.day}–{friday.day}"
        slug = f"{MONTH_ABBR[monday.month].lower()}-{monday.day}-{friday.day}"
    else:  # no cross-month weeks in 2026, but don't silently mismatch
        label = f"{MONTH_ABBR[monday.month]} {monday.day}–{MONTH_ABBR[friday.month]} {friday.day}"
        slug = (f"{MONTH_ABBR[monday.month].lower()}-{monday.day}-"
                f"{MONTH_ABBR[friday.month].lower()}-{friday.day}")
    return label, slug


def find_target_sessions(camps: list[dict], dates_label: str) -> list[dict]:
    """All (camp, session index, code) whose dates string equals the target week."""
    out = []
    for camp in camps:
        cid = camp["id"]
        code_map = CODE_TO_SESSION.get(cid, {})
        idx_to_code = {idx: code for code, idx in code_map.items()}
        for i, sess in enumerate(camp["sessions"]):
            if norm_dash(sess["dates"]) == norm_dash(dates_label):
                code = idx_to_code.get(i)
                if code is None:
                    sys.exit(f"FATAL: no FormBuilder code for {cid} session index {i} "
                             f"({sess['dates']}) in CODE_TO_SESSION — fix scripts/update_availability.py")
                period = "AM" if sess["time"].startswith("9:") else "PM"
                out.append({
                    "camp_id": cid,
                    "camp_name": camp["name"],
                    "field": next(f for f, c in FIELD_TO_CAMP.items() if c == cid),
                    "session_index": i,
                    "code": code,
                    "dates": sess["dates"],
                    "time": sess["time"],
                    "period": period,
                })
    return out


def build_rosters(snapshot: list[dict], sessions: list[dict]) -> None:
    """Attach roster lists (camper, parent, form_response_id) to each session dict."""
    for s in sessions:
        roster = []
        for r in snapshot:
            val = (r.get(s["field"]) or "").strip()
            if not val:
                continue
            codes = [c.strip() for c in val.split(",")]
            if s["code"] in codes:
                roster.append({
                    "camper": f'{r.get("Camper First Name", "").strip()} {r.get("Camper Last Name", "").strip()}'.strip(),
                    "parent": f'{r.get("Parent First Name", "").strip()} {r.get("Parent Last Name", "").strip()}'.strip(),
                    "form_response_id": r.get("FormResponseId"),
                })
        s["roster"] = sorted(roster, key=lambda x: norm(x["camper"]))


def cross_assert_csv(sessions: list[dict], dates_label: str) -> list[str]:
    """Assert API rosters == dated registrations CSV rosters. Hard-fail on mismatch."""
    warnings = []
    csv_paths = [p for p in glob.glob(str(ROOT / "data" / "registrations-*.csv"))
                 if "snapshot" not in p]
    rows = []
    for p in csv_paths:
        try:
            with open(p, newline="", encoding="utf-8-sig") as f:
                rdr = csv.DictReader(f)
                if rdr.fieldnames and {"camp", "session", "camper"} <= set(rdr.fieldnames):
                    rows.extend(list(rdr))
        except Exception:
            continue

    week_prefix = norm_dash(dates_label)
    week_rows = [r for r in rows if norm_dash(r.get("session", "")).startswith(week_prefix)]
    if not week_rows:
        warnings.append(
            f"NO cross-check CSV covers the week '{dates_label}' — roster built from the "
            f"FormBuilder API snapshot ONLY. Strongly consider exporting/updating a dated "
            f"registrations CSV (data/registrations-<month>-2026.csv) and re-running."
        )
        return warnings

    mismatches = []
    for s in sessions:
        expected_session = norm_dash(f'{s["dates"]} ({s["time"]})')
        csv_campers = {norm(r["camper"]) for r in week_rows
                       if norm(r.get("camp", "")) == norm(s["camp_name"])
                       and norm_dash(r.get("session", "")) == expected_session}
        api_campers = {norm(x["camper"]) for x in s["roster"]}
        if csv_campers != api_campers:
            only_api = sorted(api_campers - csv_campers)
            only_csv = sorted(csv_campers - api_campers)
            mismatches.append(
                f'  {s["camp_name"]} {s["dates"]} ({s["time"]}) [{s["code"]}]:\n'
                f"    in API snapshot but NOT in CSV: {only_api or '—'}\n"
                f"    in CSV but NOT in API snapshot: {only_csv or '—'}"
            )
    if mismatches:
        print("\n" + "=" * 70)
        print("HARD FAIL: roster mismatch between FormBuilder API snapshot and the")
        print("dated registrations CSV. Do NOT send emails until this is resolved")
        print("(late registration, cancellation, or a stale CSV — verify in FormBuilder).")
        print("=" * 70)
        print("\n".join(mismatches))
        sys.exit(1)
    print(f"Cross-check OK: API snapshot matches dated CSV for all "
          f"{len(sessions)} session(s) of {dates_label}.")
    return warnings


def detect_all_day(sessions: list[dict]) -> set[str]:
    """Campers appearing in both an AM and a PM session this week (normalized names)."""
    am = {norm(x["camper"]) for s in sessions if s["period"] == "AM" for x in s["roster"]}
    pm = {norm(x["camper"]) for s in sessions if s["period"] == "PM" for x in s["roster"]}
    return am & pm


def load_email_index() -> dict[str, list[str]]:
    """parent normalized name -> emails, from newest ReportDump CSV + cancellations.csv."""
    index: dict[str, list[str]] = {}

    dumps = sorted(glob.glob(str(ROOT / "data" / "*ReportDump*.csv")),
                   key=lambda p: Path(p).stat().st_mtime)
    if dumps:
        newest = dumps[-1]
        print(f"Parent emails from: {Path(newest).name}")
        with open(newest, newline="", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                name = norm(f'{r.get("first_name", "")} {r.get("last_name", "")}')
                if not name:
                    continue
                emails = index.setdefault(name, [])
                for col in ("email", "email2"):
                    e = (r.get(col) or "").strip()
                    if e and e.lower() not in [x.lower() for x in emails]:
                        emails.append(e)
    else:
        print("WARNING: no *ReportDump*.csv found in data/ — emails from cancellations.csv only.")

    canc = ROOT / "data" / "cancellations.csv"
    if canc.exists():
        with open(canc, newline="", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                name = norm(r.get("parent_name", ""))
                e = (r.get("parent_email") or "").strip()
                if name and e:
                    emails = index.setdefault(name, [])
                    if e.lower() not in [x.lower() for x in emails]:
                        emails.append(e)
    return index


def check_cancellations(sessions: list[dict], dates_label: str) -> list[str]:
    """Defense in depth: warn if a rostered camper/response appears fully cancelled."""
    warnings = []
    canc = ROOT / "data" / "cancellations.csv"
    if not canc.exists():
        return ["data/cancellations.csv not found — skipped cancellation cross-check."]
    with open(canc, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    week = norm_dash(dates_label).casefold()
    for s in sessions:
        for x in s["roster"]:
            for r in rows:
                same_camper = norm(r.get("camper_name", "")) == norm(x["camper"])
                same_ref = (r.get("reference") or "").strip() and \
                    (r.get("reference") or "").strip() == (x["form_response_id"] or "")
                sess_txt = norm_dash(r.get("session", "")).casefold()
                camp_txt = norm(r.get("camp", ""))
                hits_week = week.split("–")[0] in sess_txt or week in sess_txt
                if (same_camper or same_ref) and hits_week and camp_txt and camp_txt in norm(s["camp_name"]):
                    warnings.append(
                        f'CANCELLATION-LOG HIT: rostered camper "{x["camper"]}" '
                        f'({s["camp_name"]} {s["dates"]}) appears in data/cancellations.csv '
                        f'(row: {r.get("date")}, status: {r.get("refund_status", "")[:80]}). '
                        f"The data endpoint should already exclude cancelled responses — "
                        f"verify in FormBuilder before emailing (may be a partial cancel or a re-registration)."
                    )
    return warnings


def main() -> None:
    ap = argparse.ArgumentParser(description="Build camp welcome-email rosters for a target Monday")
    ap.add_argument("--monday", help="Target Monday, YYYY-MM-DD (default: next Monday >= 4 days out)")
    args = ap.parse_args()

    warnings: list[str] = []
    if args.monday:
        target = date.fromisoformat(args.monday)
        if target.weekday() != 0:
            sys.exit(f"FATAL: {target.isoformat()} is not a Monday.")
    else:
        target, w = next_monday(date.today())
        warnings += w

    dates_label, slug = week_bits(target)
    print(f"Target week: {dates_label} (Monday {target.isoformat()})\n")

    snapshot_path = ROOT / "data" / "registrations-snapshot.json"
    if not snapshot_path.exists():
        sys.exit("FATAL: data/registrations-snapshot.json missing — run "
                 "`python3 scripts/update_availability.py` first.")
    import datetime as _dt
    age_h = (_dt.datetime.now().timestamp() - snapshot_path.stat().st_mtime) / 3600
    if age_h > 24:
        warnings.append(f"registrations-snapshot.json is {age_h:.0f}h old — re-run "
                        f"`python3 scripts/update_availability.py` for fresh data.")

    snapshot = json.loads(snapshot_path.read_text())
    camps = json.loads((ROOT / "data" / "summer-camps-2026.json").read_text())["camps"]

    sessions = find_target_sessions(camps, dates_label)
    if not sessions:
        sys.exit(f"No camp sessions start on {dates_label}. Nothing to do.")

    build_rosters(snapshot, sessions)
    warnings += cross_assert_csv(sessions, dates_label)
    warnings += check_cancellations(sessions, dates_label)

    all_day = detect_all_day(sessions)
    email_index = load_email_index()

    missing_emails: list[dict] = []

    def family_groups(roster: list[dict], exclude_all_day: bool) -> list[dict]:
        fams: dict[str, dict] = {}
        for x in roster:
            is_ad = norm(x["camper"]) in all_day
            if exclude_all_day and is_ad:
                continue
            f = fams.setdefault(norm(x["parent"]), {
                "parent": x["parent"],
                "emails": email_index.get(norm(x["parent"]), []),
                "campers": [],
            })
            if x["camper"] not in f["campers"]:
                f["campers"].append(x["camper"])
        return sorted(fams.values(), key=lambda f: norm(f["parent"]))

    out_sessions = []
    for s in sessions:
        fams = family_groups(s["roster"], exclude_all_day=True)
        for f in fams:
            if not f["emails"]:
                missing_emails.append({"parent": f["parent"], "campers": f["campers"],
                                       "session": f'{s["camp_name"]} {s["dates"]} ({s["time"]})'})
        out_sessions.append({
            "camp_id": s["camp_id"], "camp_name": s["camp_name"], "code": s["code"],
            "dates": s["dates"], "time": s["time"], "period": s["period"],
            "roster": s["roster"],
            "draft_file": f"data/parent-emails/{slug}-{s['camp_id']}.md",
            "families": fams,
        })

    # Combined all-day group (one email per family, only if any all-day campers)
    all_day_roster = [x for s in sessions for x in s["roster"] if norm(x["camper"]) in all_day]
    seen = set()
    ad_unique = [x for x in all_day_roster
                 if not (norm(x["camper"]) in seen or seen.add(norm(x["camper"])))]
    ad_families = family_groups(ad_unique, exclude_all_day=False)
    for f in ad_families:
        if not f["emails"]:
            missing_emails.append({"parent": f["parent"], "campers": f["campers"],
                                   "session": f"ALL-DAY {dates_label}"})

    result = {
        "target_monday": target.isoformat(),
        "week": dates_label,
        "slug": slug,
        "sessions": out_sessions,
        "all_day": {
            "draft_file": f"data/parent-emails/{slug}-combined-allday.md",
            "campers": sorted(x["camper"] for x in ad_unique),
            "families": ad_families,
        },
        "missing_emails": missing_emails,
    }

    out_dir = ROOT / "data" / "parent-emails"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"{slug}-rosters.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")

    # ---- Human-readable summary ----
    print()
    for s in out_sessions:
        print(f'{s["camp_name"]} — {s["dates"]} ({s["time"]}) [{s["code"]}]: '
              f'{len(s["roster"])} camper(s)')
        for x in s["roster"]:
            tag = "  [ALL-DAY → combined email]" if norm(x["camper"]) in all_day else ""
            print(f'  {x["camper"]} — parent {x["parent"]}{tag}')
        print(f'  → email group ({len(s["families"])} families, all-day excluded):')
        for f in s["families"]:
            print(f'    {f["parent"]} <{"; ".join(f["emails"]) or "NO EMAIL"}> ({", ".join(f["campers"])})')
        print()
    if ad_families:
        print(f"ALL-DAY combined email ({len(ad_families)} families):")
        for f in ad_families:
            print(f'  {f["parent"]} <{"; ".join(f["emails"]) or "NO EMAIL"}> ({", ".join(f["campers"])})')
        print()
    else:
        print("No all-day campers this week — no combined email needed.\n")

    if missing_emails:
        print("!" * 70)
        print("MISSING EMAIL — these families have NO address on file (likely registered")
        print("after the last ReportDump export). Pull their email from FormBuilder admin")
        print("or the uimakerlab OWA mailbox before sending:")
        for m in missing_emails:
            print(f'  {m["parent"]} ({", ".join(m["campers"])}) — {m["session"]}')
        print("!" * 70)
        print()

    for w in warnings:
        print(f"WARNING: {w}")
    print(f"\nWrote {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
