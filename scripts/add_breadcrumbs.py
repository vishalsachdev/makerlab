#!/usr/bin/env python3
"""
Add BreadcrumbList JSON-LD Schema.org markup to all static pages.
Skips pages that already have JSON-LD and the homepage.
"""

import json
import re
from pathlib import Path

# Page metadata for breadcrumb display names
PAGE_NAMES = {
    'about-us': 'About Us',
    'birthday-parties': 'Birthday Parties',
    'contact': 'Contact',
    'courses': 'Courses',
    'faq': 'FAQ',
    'free-print-wednesday': 'Free Print Wednesday',
    'gallery': 'Gallery',
    'lab-hours': 'Lab Hours',
    'lab-staff': 'Lab Staff',
    'online-courses': 'Online Courses',
    'online-ordering': 'Online Ordering',
    'partners': 'Partners',
    'pricingservices': 'What We Offer',
    'private-events': 'Private Events',
    'resources': 'Resources',
    'summer': 'Summer Camps',
    'waiver-forms': 'Waiver Forms',
    'workshops': 'Workshops',
}

# Subdirectory page names
SUBDIR_PAGES = {
    'courses/making-things': ('Courses', 'Making Things'),
    'courses/digital-making': ('Courses', 'Digital Making'),
    'summer/minecraft-3d-printing': ('Summer Camps', 'Minecraft + 3D Printing'),
    'summer/adventures-in-3d-modeling-and-printing': ('Summer Camps', 'Adventures in 3D Modeling'),
    'summer/generative-ai-3d-printing': ('Summer Camps', 'Generative AI + 3D Printing'),
}


def get_title_from_html(content):
    """Extract page title from HTML."""
    match = re.search(r'<title>(.*?)\s*-\s*Illinois MakerLab</title>', content)
    if match:
        return match.group(1).strip()
    match = re.search(r'<h1>(.*?)</h1>', content, re.DOTALL)
    if match:
        return re.sub(r'<[^>]+>', '', match.group(1)).strip()
    return None


def create_breadcrumb_schema(crumbs):
    """Create BreadcrumbList JSON-LD from a list of (name, url) tuples."""
    items = []
    for i, (name, url) in enumerate(crumbs, 1):
        item = {
            "@type": "ListItem",
            "position": i,
            "name": name,
        }
        if url:
            item["item"] = url
        items.append(item)

    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


def add_breadcrumb_to_file(file_path, base_dir):
    """Add BreadcrumbList JSON-LD to a static page."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip homepage
    if file_path.name == 'index.html' and file_path.parent == base_dir:
        return False

    # Skip blog index (handled by add_blog_schema.py)
    rel_path = file_path.relative_to(base_dir)
    if str(rel_path).startswith('blog/'):
        return False

    # Check if already has BreadcrumbList schema
    if '"BreadcrumbList"' in content:
        return False

    slug = file_path.stem
    rel_str = str(rel_path).replace('.html', '')

    # Build breadcrumb trail
    crumbs = [("Home", "https://makerlab.illinois.edu/")]

    if rel_str in SUBDIR_PAGES:
        parent_name, page_name = SUBDIR_PAGES[rel_str]
        parent_slug = str(rel_path.parent)
        crumbs.append((parent_name, f"https://makerlab.illinois.edu/{parent_slug}.html"))
        crumbs.append((page_name, None))  # Current page has no URL
    else:
        display_name = PAGE_NAMES.get(slug)
        if not display_name:
            display_name = get_title_from_html(content)
        if not display_name:
            display_name = slug.replace('-', ' ').title()
        crumbs.append((display_name, None))

    schema = create_breadcrumb_schema(crumbs)
    schema_json = json.dumps(schema, indent=2, ensure_ascii=False)
    schema_tag = f'  <script type="application/ld+json">\n  {schema_json.replace(chr(10), chr(10) + "  ")}\n  </script>'

    # If file already has ld+json, append to existing @graph or add new script
    if 'application/ld+json' in content:
        # Check if it uses @graph already
        if '"@graph"' in content:
            # Add BreadcrumbList to existing @graph
            existing_match = re.search(
                r'(<script type="application/ld\+json">)\s*(\{.*?"@graph"\s*:\s*\[)(.*?)(\]\s*\})\s*(</script>)',
                content, re.DOTALL
            )
            if existing_match:
                breadcrumb_item = json.dumps({
                    "@type": "BreadcrumbList",
                    "itemListElement": schema["itemListElement"]
                }, indent=2, ensure_ascii=False)
                new_content = content[:existing_match.end(3)] + ',\n      ' + breadcrumb_item.replace('\n', '\n      ') + content[existing_match.start(4):]
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return True
        # Add as separate script tag
        new_content = content.replace('</head>', f'{schema_tag}\n</head>')
    else:
        new_content = content.replace('</head>', f'{schema_tag}\n</head>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True


def main():
    base_dir = Path('/Users/vishal/code/makerlab')

    # Find all static HTML files
    html_files = []
    for pattern in ['*.html', 'courses/*.html', 'summer/*.html']:
        html_files.extend(base_dir.glob(pattern))

    print(f'Found {len(html_files)} static HTML files')

    updated = 0
    skipped = 0

    for file_path in sorted(html_files):
        # Skip archive
        if 'archive' in str(file_path):
            continue

        if add_breadcrumb_to_file(file_path, base_dir):
            updated += 1
        else:
            skipped += 1

    print(f'\nUpdated: {updated}, Skipped: {skipped}')


if __name__ == '__main__':
    main()
