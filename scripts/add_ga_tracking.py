#!/usr/bin/env python3
"""
Add Google Analytics (gtag.js) tracking to all active HTML pages.
Skips archive/ pages and files that already have the GA snippet.

GA Property: G-R2GVFSKNPE
"""

from pathlib import Path

GA_ID = 'G-R2GVFSKNPE'

GA_SNIPPET = f'''  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA_ID}');
  </script>'''


def add_ga_to_file(file_path):
    """Add GA snippet before </head> if not already present."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if GA_ID in content:
        return False

    if '</head>' not in content:
        return False

    content = content.replace('</head>', GA_SNIPPET + '\n</head>', 1)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def main():
    base_dir = Path('/Users/vishal/code/makerlab')

    # Active pages only — skip archive/
    html_files = []
    for pattern in ['*.html', 'blog/*.html', 'courses/*.html', 'summer/*.html']:
        html_files.extend(base_dir.glob(pattern))

    print(f'Found {len(html_files)} active HTML files')

    updated = 0
    skipped = 0

    for file_path in sorted(html_files):
        rel = file_path.relative_to(base_dir)
        if add_ga_to_file(file_path):
            print(f'  + {rel}')
            updated += 1
        else:
            skipped += 1

    print(f'\nUpdated: {updated}, Already had GA: {skipped}')


if __name__ == '__main__':
    main()
