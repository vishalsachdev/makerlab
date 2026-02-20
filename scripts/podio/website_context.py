"""
Build website context for LLM email classification and reply drafting.
Loads key content from the MakerLab website into a single context string.
"""

import json
import os
import re

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")


def load_file(relative_path):
    """Load a file from the repo root."""
    path = os.path.join(REPO_ROOT, relative_path)
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""


def extract_summer_camp_details():
    """Extract key summer camp info from summer.html."""
    html = load_file("summer.html")
    if not html:
        return "Summer camp details not available."

    # Strip HTML tags for plain text
    text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    # Extract the main content area (between key markers)
    # Return a trimmed version with key details
    return text[:3000]


def get_website_context():
    """Build the full website context string for LLM consumption."""
    llms_txt = load_file("llms.txt")
    site_info = load_file("api/site-info.json")

    # Parse site-info for structured data
    try:
        info = json.loads(site_info)
        common_qa = "\n".join(
            f"Q: {q['question']}\nA: {q['answer']} (See: https://makerlab.illinois.edu{q['url']})"
            for q in info.get("commonQuestions", [])
        )
    except (json.JSONDecodeError, KeyError):
        common_qa = ""

    summer_details = extract_summer_camp_details()

    context = f"""=== ILLINOIS MAKERLAB WEBSITE CONTENT ===

{llms_txt}

=== SUMMER CAMPS 2026 (DETAILED) ===

Five camps, 8 weeks (Jun 1 - Jul 31, no camp week of Jun 29-Jul 3).
Schedule: 3 hrs/day, 5 days (9am-12pm or 1pm-4pm).
Pricing: $250/week, $225 early bird (through March 15, 2026).
Ages: 10-17 (varies by camp).

Registration: https://appserv7.admin.uillinois.edu/FormBuilderSurvey/Survey/gies_college_of_business/illinois_makerlab/summer_2026/
Summer camps page: https://makerlab.illinois.edu/summer.html

Camps:
1. Minecraft + 3D Printing (Ages 10+) - flagship, 8 sessions
2. Adventures in 3D Modeling (Ages 10-17) - Uses Fusion 360, 2 sessions
3. Generative AI + 3D Printing (Ages 12+) - 2 sessions
4. Build Your Own Robot Arm (Ages 12+) - NEW, SO-ARM100, max 5 campers, 2 sessions
5. AI Robotics with Reachy Mini (Ages 12+) - NEW, Reachy Mini Lite, max 5 campers, 2 sessions

Add-ons: Lunch supervision (12-1pm) $10/day, late pickup at 5pm $10/day.
Computers provided (MakerLab iMacs). Minecraft accounts provided for Minecraft camp.

Refund Policy: $20 non-refundable deposit. 21+ days before: full refund minus deposit.
20-8 days: half refund minus deposit. 7 days or less: no refund. Can switch sessions if seats available.

=== COMMON Q&A ===

{common_qa}

=== KEY URLS ===

Homepage: https://makerlab.illinois.edu
Summer Camps: https://makerlab.illinois.edu/summer.html
Registration: https://appserv7.admin.uillinois.edu/FormBuilderSurvey/Survey/gies_college_of_business/illinois_makerlab/summer_2026/
Services & Pricing: https://makerlab.illinois.edu/pricingservices.html
Lab Hours: https://makerlab.illinois.edu/lab-hours.html
Contact: https://makerlab.illinois.edu/contact.html
Online Ordering: https://makerlab.illinois.edu/online-ordering.html
Birthday Parties: https://makerlab.illinois.edu/birthday-parties.html
FAQ: https://makerlab.illinois.edu/faq.html
"""
    return context


if __name__ == "__main__":
    ctx = get_website_context()
    print(f"Context length: {len(ctx)} chars")
    print(ctx[:500] + "...")
