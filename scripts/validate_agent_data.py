#!/usr/bin/env python3
"""Validate AI agent files (llms.txt, site-info.json, agent-guide.json) against actual site content.

Run after updating pages, blog posts, or summer camps to catch stale data.

Usage:
    python3 scripts/validate_agent_data.py
"""

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUMMER_DATA = ROOT / "data" / "summer-camps-2026.json"
ERRORS = []
WARNINGS = []


def error(msg):
    ERRORS.append(msg)
    print(f"  ✗ {msg}")


def warn(msg):
    WARNINGS.append(msg)
    print(f"  ⚠ {msg}")


def ok(msg):
    print(f"  ✓ {msg}")


def count_blog_posts():
    blog_dir = ROOT / "blog"
    posts = [f for f in blog_dir.glob("*.html") if f.name != "index.html"]
    return len(posts)


def count_active_pages():
    """Count root-level HTML pages (excluding archive, blog, etc.)"""
    pages = [f for f in ROOT.glob("*.html")]
    return len(pages)


def count_sitemap_urls():
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        return 0
    content = sitemap.read_text()
    return content.count("<url>")


def count_summer_camps():
    """Count EducationEvent entries in summer.html schema"""
    summer = ROOT / "summer.html"
    if not summer.exists():
        return 0
    content = summer.read_text()
    return content.count('"EducationEvent"')


def load_summer_data():
    if not SUMMER_DATA.exists():
        warn("Canonical summer data file not found: data/summer-camps-2026.json")
        return None
    return json.loads(SUMMER_DATA.read_text())


def get_camp_names():
    """Extract camp names from summer.html schema (EducationEvent names only)"""
    summer = ROOT / "summer.html"
    if not summer.exists():
        return []
    content = summer.read_text()
    # Find JSON-LD script blocks and parse EducationEvent names
    names = []
    for m in re.finditer(r'"@type"\s*:\s*"EducationEvent"[^}]*?"name"\s*:\s*"([^"]+)"', content, re.DOTALL):
        names.append(m.group(1))
    return names


def check_file_contains(filepath, expected, label):
    """Check that a file contains an expected string."""
    content = filepath.read_text()
    if expected in content:
        ok(f"{label}")
    else:
        error(f"{label} — expected '{expected}' in {filepath.name}")


def validate_blog_count():
    print("\n📝 Blog post count:")
    actual = count_blog_posts()

    # Check llms.txt
    llms = (ROOT / "llms.txt").read_text()
    match = re.search(r'(\d+)\s*(?:\+\s*)?posts', llms)
    if match:
        llms_count = int(match.group(1))
        if llms_count == actual:
            ok(f"llms.txt: {llms_count} posts")
        else:
            error(f"llms.txt says {llms_count} posts, actual is {actual}")
    else:
        warn("llms.txt: couldn't find post count")

    # Check site-info.json
    site_info = json.loads((ROOT / "api" / "site-info.json").read_text())
    si_count = site_info.get("statistics", {}).get("totalBlogPosts", 0)
    if si_count == actual:
        ok(f"site-info.json: {si_count} posts")
    else:
        error(f"site-info.json says {si_count} posts, actual is {actual}")

    # Check agent-guide.json
    agent = json.loads((ROOT / "agent-guide.json").read_text())
    ag_count = agent.get("content_structure", {}).get("overview", {}).get("totalBlogPosts", 0)
    if ag_count == actual:
        ok(f"agent-guide.json: {ag_count} posts")
    else:
        error(f"agent-guide.json says {ag_count} posts, actual is {actual}")


def validate_summer_camps():
    print("\n🏕️  Summer camps:")
    actual_count = count_summer_camps()
    camp_names = get_camp_names()

    if actual_count == 0:
        warn("No EducationEvent schema found in summer.html")
        return

    ok(f"summer.html has {actual_count} camps in schema")

    # Check llms.txt mentions camp count
    llms = (ROOT / "llms.txt").read_text()
    if str(actual_count) in llms and "camp" in llms.lower():
        ok(f"llms.txt references {actual_count} camps")
    else:
        error(f"llms.txt doesn't mention {actual_count} camps")

    # Check site-info.json summer camps description
    # Use core keywords from camp names (strip "Camp", normalize spacing)
    def camp_keywords(name):
        """Extract distinguishing keywords from a camp name."""
        name = name.lower().replace(" camp", "").strip()
        # Return key distinguishing words
        if "minecraft" in name:
            return "minecraft"
        if "modeling" in name:
            return "modeling"
        if "generative" in name or "genai" in name:
            return "generative ai"
        if "robot arm" in name:
            return "robot arm"
        if "reachy" in name:
            return "reachy"
        return name

    site_info = json.loads((ROOT / "api" / "site-info.json").read_text())
    for svc in site_info.get("primaryServices", []):
        if "camp" in svc.get("name", "").lower():
            desc = svc.get("description", "").lower()
            missing = []
            for name in camp_names:
                kw = camp_keywords(name)
                if kw not in desc:
                    missing.append(name)
            if not missing:
                ok("site-info.json lists all camp names")
            else:
                error(f"site-info.json missing camps: {', '.join(missing)}")
            break
    else:
        error("site-info.json has no Summer Camps service entry")


def validate_summer_schedule_conflicts(data):
    print("\n⏱️  Summer schedule conflicts:")
    by_slot = {}
    for camp in data.get("camps", []):
        for session in camp.get("sessions", []):
            key = (session["dates"], session["time"])
            by_slot.setdefault(key, []).append(camp["name"])
    conflicts = {k: v for k, v in by_slot.items() if len(v) > 1}
    if conflicts:
        for (dates, time), camps in sorted(conflicts.items()):
            error(f"Time conflict {dates} | {time}: {', '.join(camps)}")
    else:
        ok("No same date/time conflicts across camps in canonical data")


def validate_summer_page_consistency(data):
    print("\n📄 Summer page consistency:")
    registration_url = data.get("registration_url", "")
    robot_cap = data.get("robot_max_capacity")

    # Main summer page robot capacity guideline
    summer_main = (ROOT / "summer.html").read_text()
    expected_robot_line = f"robot camps (Robot Arm and Reachy Mini) are limited to {robot_cap}."
    if expected_robot_line in summer_main:
        ok("summer.html robot capacity guideline matches canonical data")
    else:
        error("summer.html robot capacity guideline is out of sync")

    # Detail pages
    for camp in data.get("camps", []):
        detail_path = ROOT / camp["detail_file"]
        if not detail_path.exists():
            error(f"Missing detail page: {camp['detail_file']}")
            continue
        content = detail_path.read_text()

        if f"<p><strong>Ages:</strong> {camp['age_detail']}</p>" in content:
            ok(f"{detail_path.name}: ages match")
        else:
            error(f"{detail_path.name}: ages do not match canonical data")

        if f"<p><strong>Max campers:</strong> {camp['max_campers']} per session" in content:
            ok(f"{detail_path.name}: max campers match")
        else:
            error(f"{detail_path.name}: max campers do not match canonical data")

        if registration_url in content:
            ok(f"{detail_path.name}: registration URL matches")
        else:
            error(f"{detail_path.name}: registration URL missing or stale")

        table_match = re.search(
            r"<h3>Summer 2026 Dates</h3>\s*<table[^>]*>\s*<thead>.*?</thead>\s*<tbody>\s*(.*?)\s*</tbody>",
            content,
            re.DOTALL,
        )
        if not table_match:
            error(f"{detail_path.name}: missing Summer 2026 dates table")
            continue
        tbody = table_match.group(1)
        row_count = len(re.findall(r"<tr><td", tbody))
        expected_count = len(camp["sessions"])
        if row_count == expected_count:
            ok(f"{detail_path.name}: session row count matches ({expected_count})")
        else:
            error(f"{detail_path.name}: session row count {row_count}, expected {expected_count}")

        for idx, session in enumerate(camp["sessions"], start=1):
            row_pattern = re.compile(
                rf"<tr><td[^>]*>{idx}</td><td[^>]*>{re.escape(session['dates'])}</td><td[^>]*>{re.escape(session['time'])}</td></tr>"
            )
            if row_pattern.search(tbody):
                ok(f"{detail_path.name}: session {idx} matches ({session['dates']} | {session['time']})")
            else:
                error(f"{detail_path.name}: session {idx} mismatch for {session['dates']} | {session['time']}")


def validate_sitemap():
    print("\n🗺️  Sitemap:")
    actual = count_sitemap_urls()
    if actual == 0:
        warn("sitemap.xml not found or empty")
        return

    agent = json.loads((ROOT / "agent-guide.json").read_text())
    for key, val in agent.get("api_endpoints", {}).items():
        if "sitemap" in key:
            desc = val.get("description", "")
            match = re.search(r'(\d+)', desc)
            if match:
                stated = int(match.group(1))
                if stated == actual:
                    ok(f"agent-guide.json sitemap count: {stated}")
                else:
                    error(f"agent-guide.json says {stated} URLs, sitemap has {actual}")
            break


def validate_json_parseable():
    print("\n🔧 JSON validity:")
    for name in ["api/site-info.json", "agent-guide.json", "api/pages.json", "api/blog/posts.json"]:
        filepath = ROOT / name
        if not filepath.exists():
            error(f"{name} not found")
            continue
        try:
            json.loads(filepath.read_text())
            ok(f"{name} is valid JSON")
        except json.JSONDecodeError as e:
            error(f"{name} has invalid JSON: {e}")


def validate_dates():
    print("\n📅 Last updated dates:")
    today = __import__("datetime").date.today().isoformat()

    for name, path_key in [
        ("site-info.json", "api/site-info.json"),
        ("agent-guide.json", "agent-guide.json"),
    ]:
        filepath = ROOT / path_key
        data = json.loads(filepath.read_text())
        updated = data.get("site", {}).get("lastUpdated", "unknown")
        # Warn if more than 60 days old
        if updated != "unknown":
            from datetime import date
            try:
                updated_date = date.fromisoformat(updated)
                days_old = (date.today() - updated_date).days
                if days_old > 60:
                    warn(f"{name} lastUpdated is {days_old} days old ({updated})")
                else:
                    ok(f"{name} lastUpdated: {updated} ({days_old} days ago)")
            except ValueError:
                warn(f"{name} lastUpdated format unclear: {updated}")

    # Check llms.txt
    llms = (ROOT / "llms.txt").read_text()
    match = re.search(r'Last Updated:\s*(\d{4}-\d{2}-\d{2})', llms)
    if match:
        from datetime import date
        updated_date = date.fromisoformat(match.group(1))
        days_old = (date.today() - updated_date).days
        if days_old > 60:
            warn(f"llms.txt lastUpdated is {days_old} days old ({match.group(1)})")
        else:
            ok(f"llms.txt lastUpdated: {match.group(1)} ({days_old} days ago)")


def main():
    print("=" * 50)
    print("MakerLab Agent Data Validator")
    print("=" * 50)

    validate_json_parseable()
    validate_blog_count()
    validate_summer_camps()
    summer_data = load_summer_data()
    if summer_data:
        validate_summer_schedule_conflicts(summer_data)
        validate_summer_page_consistency(summer_data)
    validate_sitemap()
    validate_dates()

    print("\n" + "=" * 50)
    if ERRORS:
        print(f"❌ {len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        print("\nFix these before pushing:")
        for e in ERRORS:
            print(f"  - {e}")
        sys.exit(1)
    elif WARNINGS:
        print(f"✅ No errors, {len(WARNINGS)} warning(s)")
        sys.exit(0)
    else:
        print("✅ All agent data is consistent!")
        sys.exit(0)


if __name__ == "__main__":
    main()
