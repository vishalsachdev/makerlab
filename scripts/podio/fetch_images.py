"""
Fetch images from Podio orders for blog posts.
"""

import os
import json
import requests
from pathlib import Path
from podio_client import get_client

ORDERS_APP_ID = 6976602
IMAGE_DIR = str(Path(__file__).parent.parent.parent / "images" / "blog")

# Orders to fetch images for
BLOG_ORDERS = [
    3211041335,  # mitras_cyberrunner_part_2
    3186648431,  # mitras_cyberrunner_part_1
    3178374184,  # Jen_Melba_eye_tracker_sensor
    3198060359,  # emmamd2_ece445_enclosure
    3186537150,  # amishp2_daft_punk_helmet
    3191193662,  # spnair2_Landscape Tile Prototype
    3189833239,  # md45_Water_Pump
    3173959369,  # Pelmore_msba_keychain
    3176908193,  # bcknghm_headlight mount
    3192620031,  # Unlocked 2 tetrahedra
]


def get_files_for_order(client, item_id):
    """Get all files attached to an order."""
    item = client.get_item(item_id)
    files = []

    # Files from fields
    for field in item.get("fields", []):
        for val in field.get("values", []):
            if "file" in val:
                f = val["file"]
                files.append({
                    "file_id": f.get("file_id"),
                    "name": f.get("name"),
                    "link": f.get("link"),
                    "mimetype": f.get("mimetype"),
                    "size": f.get("size"),
                })

    # Files from comments
    comments = client.get(f"/comment/item/{item_id}/")
    for comment in comments:
        for f in comment.get("files", []):
            files.append({
                "file_id": f.get("file_id"),
                "name": f.get("name"),
                "link": f.get("link"),
                "mimetype": f.get("mimetype"),
                "size": f.get("size"),
                "from_comment": True,
            })

    return item, files


def download_file(client, file_info, order_title, output_dir):
    """Download a file from Podio."""
    file_id = file_info.get("file_id")
    name = file_info.get("name", f"file_{file_id}")
    mimetype = file_info.get("mimetype", "")

    # Only download images
    if not mimetype.startswith("image/"):
        return None

    # Create safe filename
    safe_title = "".join(c if c.isalnum() or c in "-_" else "_" for c in order_title)
    ext = name.split(".")[-1] if "." in name else "jpg"
    filename = f"{safe_title}_{file_id}.{ext}"
    filepath = os.path.join(output_dir, filename)

    if os.path.exists(filepath):
        print(f"    Already exists: {filename}")
        return filename

    # Download via Podio API
    try:
        url = f"https://api.podio.com/file/{file_id}/raw"
        headers = {"Authorization": f"OAuth2 {client.access_token}"}
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"    Downloaded: {filename}")
        return filename
    except Exception as e:
        print(f"    Error downloading {name}: {e}")
        return None


def main():
    print("Connecting to Podio...")
    client = get_client()

    os.makedirs(IMAGE_DIR, exist_ok=True)

    results = {}

    for item_id in BLOG_ORDERS:
        print(f"\nFetching order {item_id}...")
        try:
            item, files = get_files_for_order(client, item_id)
            title = item.get("title", str(item_id))
            print(f"  Title: {title}")
            print(f"  Found {len(files)} files")

            # Filter to images only
            images = [f for f in files if f.get("mimetype", "").startswith("image/")]
            print(f"  Images: {len(images)}")

            downloaded = []
            for f in images[:10]:  # Limit to 10 images per order
                filename = download_file(client, f, title, IMAGE_DIR)
                if filename:
                    downloaded.append(filename)

            results[item_id] = {
                "title": title,
                "created": item.get("created_on", ""),
                "total_files": len(files),
                "images_found": len(images),
                "downloaded": downloaded,
            }

        except Exception as e:
            print(f"  Error: {e}")
            results[item_id] = {"error": str(e)}

    # Save results
    with open("blog_images.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*60}")
    print("SUMMARY")
    print("="*60)
    for item_id, info in results.items():
        if "error" in info:
            print(f"\n{item_id}: ERROR - {info['error']}")
        else:
            print(f"\n{info['title']}")
            print(f"  Images found: {info['images_found']}, Downloaded: {len(info['downloaded'])}")
            for img in info['downloaded']:
                print(f"    - {img}")


if __name__ == "__main__":
    main()
