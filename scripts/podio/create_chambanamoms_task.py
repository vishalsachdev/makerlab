"""
Create Podio task for ChambanaMoms media asset creation.
Assigned to Arundhati Raj, due Wed Feb 18.

Run this when the rate limit resets (~1 hour after last API call):
    python create_chambanamoms_task.py
"""

from podio_client import get_client
import requests

client = get_client()

task_data = {
    "text": (
        "ChambanaMoms Gold Package — Create media assets for summer camp promotion.\n\n"
        "See the repo folder: images/campaigns/chambanamoms-2026/ for all details.\n\n"
        "Tasks:\n"
        "1. Photograph SO-ARM100 robot arm and Reachy Mini Lite (clean product shots)\n"
        "2. Gather existing camp photos from images/summer/ folder\n"
        "3. Create 2 social media graphics in Canva (specs in image-briefs.txt)\n"
        "4. Select best action photo for Facebook album and round-up thumbnail\n"
        "5. Export MakerLab logo as PNG (transparent) and PDF (vector)\n"
        "6. Email all materials to mindy@chambanamoms.com\n\n"
        "All text copy (captions, listing, blurbs) is already written in the .txt files.\n"
        "README.md has the full guide with timeline and specs."
    ),
    "due_date": "2026-02-18",
    "responsible": 77030675,  # Arundhati Raj
    "description": (
        "Create and submit media assets for ChambanaMoms.com Gold sponsorship "
        "package ($550). Need social media graphics, robot product photos, and "
        "a Facebook album photo. Text deliverables are done. Full briefs in repo "
        "at images/campaigns/chambanamoms-2026/"
    ),
}

response = requests.post(
    "https://api.podio.com/task/",
    headers={"Authorization": f"OAuth2 {client.access_token}"},
    json=task_data,
)

if response.status_code in (200, 201):
    result = response.json()
    print(f"Task created successfully!")
    print(f"  Task ID: {result.get('task_id')}")
    print(f"  Assigned to: {result.get('responsible', {}).get('name')}")
    print(f"  Due: {result.get('due_date')}")
    print(f"  Link: {result.get('link')}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
