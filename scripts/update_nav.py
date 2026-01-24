#!/usr/bin/env python3
"""
Update navigation in all HTML files to use dropdown menus.
"""

import os
import re
from pathlib import Path

# Navigation templates
NAV_ROOT = '''        <nav class="main-nav">
          <ul>
            <li><a href="index.html">Home</a></li>
            <li class="nav-dropdown">
              <a href="about-us.html">About</a>
              <ul class="dropdown-menu">
                <li><a href="about-us.html">About Us</a></li>
                <li><a href="lab-staff.html">Lab Staff</a></li>
                <li><a href="partners.html">Partners</a></li>
                <li><a href="faq.html">FAQ</a></li>
              </ul>
            </li>
            <li class="nav-dropdown">
              <a href="pricingservices.html">What We Offer</a>
              <ul class="dropdown-menu">
                <li><a href="pricingservices.html">Services &amp; Pricing</a></li>
                <li><a href="summer.html">Summer Camps</a></li>
                <li><a href="birthday-parties.html">Birthday Parties</a></li>
                <li><a href="workshops.html">Workshops</a></li>
                <li><a href="courses.html">Courses</a></li>
                <li><a href="resources.html">Resources</a></li>
              </ul>
            </li>
            <li><a href="online-ordering.html">Order Online</a></li>
            <li><a href="blog/index.html">Blog</a></li>
            <li><a href="lab-hours.html">Lab Hours</a></li>
            <li><a href="contact.html">Contact</a></li>
          </ul>
        </nav>'''

NAV_SUBDIR = '''        <nav class="main-nav">
          <ul>
            <li><a href="../index.html">Home</a></li>
            <li class="nav-dropdown">
              <a href="../about-us.html">About</a>
              <ul class="dropdown-menu">
                <li><a href="../about-us.html">About Us</a></li>
                <li><a href="../lab-staff.html">Lab Staff</a></li>
                <li><a href="../partners.html">Partners</a></li>
                <li><a href="../faq.html">FAQ</a></li>
              </ul>
            </li>
            <li class="nav-dropdown">
              <a href="../pricingservices.html">What We Offer</a>
              <ul class="dropdown-menu">
                <li><a href="../pricingservices.html">Services &amp; Pricing</a></li>
                <li><a href="../summer.html">Summer Camps</a></li>
                <li><a href="../birthday-parties.html">Birthday Parties</a></li>
                <li><a href="../workshops.html">Workshops</a></li>
                <li><a href="../courses.html">Courses</a></li>
                <li><a href="../resources.html">Resources</a></li>
              </ul>
            </li>
            <li><a href="../online-ordering.html">Order Online</a></li>
            <li><a href="../blog/index.html">Blog</a></li>
            <li><a href="../lab-hours.html">Lab Hours</a></li>
            <li><a href="../contact.html">Contact</a></li>
          </ul>
        </nav>'''

NAV_ARCHIVE = '''        <nav class="main-nav">
          <ul>
            <li><a href="../../index.html">Home</a></li>
            <li class="nav-dropdown">
              <a href="../../about-us.html">About</a>
              <ul class="dropdown-menu">
                <li><a href="../../about-us.html">About Us</a></li>
                <li><a href="../../lab-staff.html">Lab Staff</a></li>
                <li><a href="../../partners.html">Partners</a></li>
                <li><a href="../../faq.html">FAQ</a></li>
              </ul>
            </li>
            <li class="nav-dropdown">
              <a href="../../pricingservices.html">What We Offer</a>
              <ul class="dropdown-menu">
                <li><a href="../../pricingservices.html">Services &amp; Pricing</a></li>
                <li><a href="../../summer.html">Summer Camps</a></li>
                <li><a href="../../birthday-parties.html">Birthday Parties</a></li>
                <li><a href="../../workshops.html">Workshops</a></li>
                <li><a href="../../courses.html">Courses</a></li>
                <li><a href="../../resources.html">Resources</a></li>
              </ul>
            </li>
            <li><a href="../../online-ordering.html">Order Online</a></li>
            <li><a href="../../blog/index.html">Blog</a></li>
            <li><a href="../../lab-hours.html">Lab Hours</a></li>
            <li><a href="../../contact.html">Contact</a></li>
          </ul>
        </nav>'''

def get_nav_for_path(file_path):
    """Return appropriate nav based on file path depth."""
    rel_path = str(file_path)
    if '/archive/pages/' in rel_path:
        return NAV_ARCHIVE
    elif '/blog/' in rel_path or '/courses/' in rel_path or '/summer/' in rel_path:
        return NAV_SUBDIR
    else:
        return NAV_ROOT

def update_nav_in_file(file_path):
    """Update navigation in a single HTML file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match existing nav
    nav_pattern = r'<nav class="main-nav">.*?</nav>'

    if not re.search(nav_pattern, content, re.DOTALL):
        print(f"  Skipped (no nav found): {file_path}")
        return False

    new_nav = get_nav_for_path(file_path)
    new_content = re.sub(nav_pattern, new_nav, content, flags=re.DOTALL)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Updated: {file_path}")
        return True
    else:
        print(f"  No changes: {file_path}")
        return False

def main():
    base_dir = Path('/Users/vishal/code/makerlab')

    # Find all HTML files
    html_files = []
    for pattern in ['*.html', 'blog/*.html', 'courses/*.html', 'summer/*.html', 'archive/pages/*.html']:
        html_files.extend(base_dir.glob(pattern))

    print(f"Found {len(html_files)} HTML files")

    updated_count = 0
    for file_path in sorted(html_files):
        if update_nav_in_file(file_path):
            updated_count += 1

    print(f"\nUpdated {updated_count} files")

if __name__ == '__main__':
    main()
