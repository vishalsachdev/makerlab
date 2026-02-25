#!/usr/bin/env python3
"""Sync duplicated summer-camp facts from canonical JSON into site files.

Usage:
    python3 scripts/sync_summer_data.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "summer-camps-2026.json"


def load_data() -> dict:
    return json.loads(DATA_PATH.read_text())


def replace_regex(content: str, pattern: str, repl: str, flags: int = 0, count: int = 0) -> str:
    updated, n = re.subn(pattern, repl, content, flags=flags, count=count)
    if n == 0:
        raise ValueError(f"Pattern not found: {pattern}")
    return updated


def sessions_label(n: int) -> str:
    return "session" if n == 1 else "sessions"


def ensure_no_time_conflicts(data: dict) -> None:
    by_slot: dict[tuple[str, str], list[str]] = {}
    for camp in data["camps"]:
        for s in camp["sessions"]:
            key = (s["dates"], s["time"])
            by_slot.setdefault(key, []).append(camp["name"])
    conflicts = {k: v for k, v in by_slot.items() if len(v) > 1}
    if conflicts:
        lines = ["Found schedule conflicts in canonical summer data:"]
        for (dates, time), camps in sorted(conflicts.items()):
            lines.append(f"- {dates} | {time}: {', '.join(camps)}")
        raise ValueError("\n".join(lines))


def sync_summer_main(data: dict) -> None:
    path = ROOT / "summer.html"
    content = path.read_text()

    pricing = data["pricing"]
    content = replace_regex(
        content,
        r"<p style=\"font-size: 1\.2rem; margin: 0;\"><strong>Early Bird: \$\d+</strong> \(register by [^)]+\)</p>",
        f"<p style=\"font-size: 1.2rem; margin: 0;\"><strong>Early Bird: ${pricing['early_bird_price']}</strong> (register by {pricing['early_bird_deadline_main']})</p>",
        count=1,
    )
    content = replace_regex(
        content,
        r"<p style=\"font-size: 1\.2rem; margin: 0\.5rem 0 0 0;\"><strong>Regular: \$\d+</strong></p>",
        f"<p style=\"font-size: 1.2rem; margin: 0.5rem 0 0 0;\"><strong>Regular: ${pricing['regular_price']}</strong></p>",
        count=1,
    )
    content = replace_regex(
        content,
        r"robot camps \(Robot Arm and Reachy Mini\) are limited to \d+\.",
        f"robot camps (Robot Arm and Reachy Mini) are limited to {data['robot_max_capacity']}.",
        count=1,
    )

    for camp in data["camps"]:
        href = re.escape(camp["card_href"])
        block_pattern = (
            rf"(<h3><a href=\"{href}\">.*?</a></h3>\s*"
            rf"<p>.*?</p>\s*"
            rf"<p><strong>Ages:</strong> )[^<]+"
            rf"(&nbsp;\|&nbsp; <strong>Max:</strong> )\d+( campers</p>\s*"
            rf"<p style=\"font-size: 0\.9rem; color: #555;\"><strong>)\d+ (?:session|sessions):</strong> [^<]+(</p>)"
        )
        repl = (
            rf"\g<1>{camp['age_summary']} \g<2>{camp['max_campers']}\g<3>"
            rf"{len(camp['sessions'])} {sessions_label(len(camp['sessions']))}:</strong> {camp['summary_sessions_line']}\4"
        )
        content = replace_regex(content, block_pattern, repl, flags=re.S, count=1)

    path.write_text(content)


def render_sessions_rows(sessions: list[dict]) -> str:
    rows = []
    for idx, session in enumerate(sessions, start=1):
        border = ' style="padding: 0.5rem; border-bottom: 1px solid #ddd;"' if idx < len(sessions) else ' style="padding: 0.5rem;"'
        rows.append(f'<tr><td{border}>{idx}</td><td{border}>{session["dates"]}</td><td{border}>{session["time"]}</td></tr>')
    return "\n                ".join(rows)


def sync_detail_pages(data: dict) -> None:
    pricing = data["pricing"]
    for camp in data["camps"]:
        path = ROOT / camp["detail_file"]
        content = path.read_text()

        content = replace_regex(
            content,
            r"<p><strong>Ages:</strong> .*?</p>",
            f"<p><strong>Ages:</strong> {camp['age_detail']}</p>",
            count=1,
        )
        content = replace_regex(
            content,
            r"<p><strong>Max campers:</strong> .*?</p>",
            f"<p><strong>Max campers:</strong> {camp['max_campers']} per session</p>" if camp["id"] in {"minecraft", "adventures", "genai"} else f"<p><strong>Max campers:</strong> {camp['max_campers']} per session (small group, maximum hands-on time)</p>",
            count=1,
        )
        content = replace_regex(
            content,
            r"<p><strong>Price:</strong> \$\d+ \(\$\d+ early bird by [^)]+\)</p>",
            f"<p><strong>Price:</strong> ${pricing['regular_price']} (${pricing['early_bird_price']} early bird by {pricing['early_bird_deadline_detail']})</p>",
            count=1,
        )

        tbody_pattern = (
            r"(<h3>Summer 2026 Dates</h3>\s*<table style=\"width: 100%; border-collapse: collapse; margin-top: 0\.5rem;\">\s*"
            r"<thead>.*?</thead>\s*<tbody>)(.*?)(</tbody>)"
        )
        content = replace_regex(
            content,
            tbody_pattern,
            rf"\g<1>\n                {render_sessions_rows(camp['sessions'])}\n              \3",
            flags=re.S,
            count=1,
        )

        content = re.sub(
            r"https://appserv7\.admin\.uillinois\.edu/FormBuilderSurvey/Survey/gies_college_of_business/illinois_makerlab/summer_\d{4}/",
            data["registration_url"],
            content,
        )

        path.write_text(content)

    forms_path = ROOT / "summer" / "camp-forms.html"
    forms_content = forms_path.read_text()
    forms_content = re.sub(
        r"https://appserv7\.admin\.uillinois\.edu/FormBuilderSurvey/Survey/gies_college_of_business/illinois_makerlab/summer_\d{4}/",
        data["registration_url"],
        forms_content,
    )
    forms_path.write_text(forms_content)


def camps_sentence(data: dict, plus_and: bool = True) -> str:
    names = [c["name"] for c in data["camps"]]
    if plus_and:
        body = ", ".join(names[:-1]) + f", and {names[-1]}"
    else:
        body = ", ".join(names)
    return body


def sync_faq(data: dict) -> None:
    path = ROOT / "faq.html"
    content = path.read_text()
    names = camps_sentence(data)
    robot_cap = data["robot_max_capacity"]
    faq_json_text = (
        f"Yes! We offer five week-long summer camps for youth ages 10+, including {names}. "
        f"Robot camps are limited to {robot_cap} campers per session. "
        "Visit makerlab.illinois.edu/summer.html for details."
    )
    faq_html_text = (
        f"Yes! We offer five week-long <a href=\"summer.html\">summer camps</a> for youth ages 10+, including {names}. "
        f"Robot camps are limited to {robot_cap} campers per session, and Reachy Mini includes a Jul 6-10 afternoon session."
    )

    content = replace_regex(
        content,
        r"(\"name\": \"Do you offer summer camps\?\",[\s\S]*?\"text\": \").*?(\")",
        rf"\g<1>{faq_json_text}\2",
        count=1,
    )
    content = replace_regex(
        content,
        r"(<h2>Q: Do you offer summer camps\?</h2>\s*<p>A: ).*?(</p>)",
        rf"\g<1>{faq_html_text}\2",
        flags=re.S,
        count=1,
    )
    path.write_text(content)


def sync_api_and_llms(data: dict) -> None:
    names_no_and = camps_sentence(data, plus_and=False)
    names_with_and = camps_sentence(data, plus_and=True)
    robot_cap = data["robot_max_capacity"]
    reachy_note = "Reachy Mini includes a Jul 6-10 afternoon session."
    pricing = data["pricing"]

    site_info_path = ROOT / "api" / "site-info.json"
    site_info = json.loads(site_info_path.read_text())
    for svc in site_info["primaryServices"]:
        if svc.get("name") == "Summer Camps":
            svc["description"] = (
                f"Five week-long camps for ages 10+: {names_no_and}. "
                f"Robot camps are limited to {robot_cap} campers per session. "
                f"{reachy_note} ${pricing['regular_price']}/week (${pricing['early_bird_price']} early bird)."
            )
    for qa in site_info["commonQuestions"]:
        if qa.get("question") == "Do you offer summer camps?":
            qa["answer"] = (
                f"Yes! Five week-long camps for ages 10+: {names_with_and}. "
                f"Robot camps are limited to {robot_cap} campers per session, and Reachy Mini includes a Jul 6-10 afternoon session. "
                f"${pricing['regular_price']}/week (${pricing['early_bird_price']} early bird). See summer.html for schedule and registration."
            )
    site_info_path.write_text(json.dumps(site_info, indent=2) + "\n")

    pages_path = ROOT / "api" / "pages.json"
    pages = json.loads(pages_path.read_text())
    for page in pages["pages"]:
        if page.get("slug") == "summer":
            page["description"] = (
                f"Week-long summer camps for youth ages 10+. Five camps: {names_with_and}. "
                f"Robot camps are limited to {robot_cap} campers per session."
            )
    pages_path.write_text(json.dumps(pages, indent=2) + "\n")

    llms_path = ROOT / "llms.txt"
    llms = llms_path.read_text()
    llms = replace_regex(
        llms,
        r"2\. Summer Camps - .*",
        (
            f"2. Summer Camps - Five week-long camps for youth ages 10+ "
            f"({names_no_and}). Robot camps are limited to {robot_cap} campers per session, "
            "and Reachy Mini includes a Jul 6-10 afternoon session."
        ),
        count=1,
    )
    llms = replace_regex(
        llms,
        r"A: Yes! Five week-long camps for ages 10\+.*",
        (
            f"A: Yes! Five week-long camps for ages 10+ including {names_no_and.replace(', AI Robotics with Reachy Mini', ', and AI Robotics with Reachy Mini')}. "
            f"Robot camps are limited to {robot_cap} campers per session, and Reachy Mini includes a Jul 6-10 afternoon session. "
            f"${pricing['regular_price']}/week (${pricing['early_bird_price']} early bird). See /summer.html"
        ),
        count=1,
    )
    llms_path.write_text(llms)


def main() -> None:
    data = load_data()
    ensure_no_time_conflicts(data)
    sync_summer_main(data)
    sync_detail_pages(data)
    sync_faq(data)
    sync_api_and_llms(data)
    print("Summer data synced from canonical JSON.")


if __name__ == "__main__":
    main()
