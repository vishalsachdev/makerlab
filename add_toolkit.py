#!/usr/bin/env python3
"""
Add Illinois Campus Brand Toolkit CDN resources to every HTML file in the project.
"""

from pathlib import Path
import re

# Toolkit CDN resources
TOOLKIT_CSS = '  <link rel="stylesheet" href="//cdn.toolkit.illinois.edu/3/toolkit.css">\n'
TOOLKIT_JS = '  <script src="//cdn.toolkit.illinois.edu/3/toolkit.js" type="module"></script>\n'


def update_html_file(file_path: Path) -> bool:
    """Insert the toolkit CSS and JS into the specified HTML file if missing."""
    content = file_path.read_text(encoding="utf-8")

    if "cdn.toolkit.illinois.edu" in content:
        print(f"Skipping {file_path} (already contains toolkit resources)")
        return False

    if "<link rel=\"stylesheet\"" in content:
        # Insert toolkit CSS before the first stylesheet link so custom styles can override
        content = re.sub(
            r"(\s*)(<link rel=\"stylesheet\")",
            r"\1" + TOOLKIT_CSS + r"\2",
            content,
            count=1,
        )
    elif "</head>" in content:
        content = content.replace("</head>", TOOLKIT_CSS + "</head>")
    else:
        print(f"Warning: {file_path} missing <head>; skipping CSS insert")

    if "<script src=" in content:
        # Insert toolkit JS before the first external script tag
        content = re.sub(
            r"(\s*)(<script src=)",
            r"\1" + TOOLKIT_JS + r"\2",
            content,
            count=1,
        )
    elif "</body>" in content:
        content = content.replace("</body>", TOOLKIT_JS + "</body>")
    else:
        print(f"Warning: {file_path} missing </body>; skipping JS insert")

    file_path.write_text(content, encoding="utf-8")
    print(f"Updated {file_path}")
    return True


def main():
    base_dir = Path(__file__).parent
    html_files = sorted(base_dir.glob("**/*.html"))
    print(f"Scanning {len(html_files)} HTML files")

    updated = 0
    for html_file in html_files:
        if update_html_file(html_file):
            updated += 1

    print(f"\nSuccessfully updated {updated} files")
    print(f"Skipped {len(html_files) - updated} files")


if __name__ == "__main__":
    main()
