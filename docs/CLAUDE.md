# CLAUDE.md - AI Assistant Guide for Illinois MakerLab Website

This document provides comprehensive guidance for AI assistants working with the Illinois MakerLab website codebase.

## Table of Contents

- [Project Overview](#project-overview)
- [Recent Changes (November 2025)](#recent-changes-november-2025)
- [Repository Structure](#repository-structure)
- [Technology Stack](#technology-stack)
- [Key Files and Their Purpose](#key-files-and-their-purpose)
- [Development Workflow](#development-workflow)
- [Content Generation Process](#content-generation-process)
- [Coding Conventions](#coding-conventions)
- [Deployment](#deployment)
- [Testing and Quality Assurance](#testing-and-quality-assurance)
- [Git Workflow](#git-workflow)
- [Archive Directory](#archive-directory)
- [Illinois Campus Brand Toolkit Integration](#illinois-campus-brand-toolkit-integration)
- [Important Guidelines for AI Assistants](#important-guidelines-for-ai-assistants)

---

## Project Overview

**Project Name:** Illinois MakerLab Website
**Type:** Static website
**Live URL:** https://vishalsachdev.github.io/makerlab/
**Purpose:** Replica of the Illinois MakerLab website showcasing the world's first business school 3D printing lab at UIUC

### Key Features
- 330+ total HTML pages (22 main pages + 291 blog posts + archived pages)
- 291 blog posts from 2012-2025
- Responsive design with mobile-first approach
- Illinois branding (Orange: #FF5F05, Blue: #13294B) with Campus Brand Toolkit integration
- Local image hosting (migrated from Squarespace CDN)
- Organized scripts and archived legacy files
- GitHub Pages deployment with automated CI/CD

### About Illinois MakerLab
- **Mission:** Learn. Make. Share.
- **Location:** Business Instructional Facility, Room 3030, UIUC
- **Focus:** 3D printing, digital making, courses, summer camps, and community engagement
- **Director:** Dr. Vishal Sachdev
- **Executive Director:** Dr. Aric Rindfleisch

---

## Recent Changes (November 2025)

This section highlights significant organizational and infrastructure changes made to the repository in November 2025.

### Repository Reorganization

1. **Scripts Directory Created** (`scripts/`)
   - All Python utility scripts moved to centralized location
   - Added comprehensive `scripts/README.md` documentation
   - Better organization for maintenance tools

2. **Archive Directory Created** (`archive/`)
   - Archived unused/unlinked HTML pages (13 pages) to `archive/pages/`
   - Moved `generate_site.py` to archive (no longer used)
   - Moved Squarespace export XML to archive
   - Added archive documentation

3. **Documentation Consolidated** (`docs/`)
   - All documentation in centralized `docs/` directory
   - Organized into subdirectories: deployment, integration, development
   - Comprehensive guides for all aspects of the project

### Image Migration Completed ✅

- **737+ images** migrated from Squarespace CDN to local hosting
- Images organized in `images/` directory by category (blog, events, general, staff, summer)
- All HTML files updated to use local image paths
- Benefits: Improved reliability, version control, offline development support

### Brand Toolkit Integration ✅

- Illinois Campus Brand Toolkit integrated into all HTML files
- Toolkit CSS and JS loaded from Illinois CDN
- `scripts/add_toolkit.py` for maintaining integration
- Phase 1 complete; Phase 2 planned for typography updates

### Key Stats (Current)

- **330+ total HTML files** (22 main pages + 291 blog posts + archived pages)
- **737+ local images** (migrated from CDN)
- **6 utility scripts** in `scripts/` directory
- **13 archived pages** in `archive/pages/`
- **Comprehensive documentation** in `docs/` directory

### What Changed in Workflows

**Before (Pre-November 2025):**
- Images hosted on Squarespace CDN (external dependency)
- Scripts scattered in root directory
- `generate_site.py` used for content generation
- No Brand Toolkit integration

**After (November 2025):**
- All images hosted locally in organized `images/` directory
- Scripts organized in `scripts/` directory with documentation
- Direct HTML editing (generate_site.py archived)
- Brand Toolkit integrated on all pages
- Archive directory for historical files

---

## Repository Structure

```
makerlab/
├── .github/
│   └── workflows/
│       └── static.yml           # GitHub Actions deployment workflow
├── .gitignore                   # Git ignore patterns
├── .nojekyll                    # Prevents Jekyll processing
├── blog/                        # 291 blog post HTML files
│   ├── index.html              # Blog listing page
│   └── [post-slug].html        # Individual blog posts
├── courses/                     # Course-specific pages
│   ├── digital-making.html
│   └── making-things.html
├── summer/                      # Summer camp pages
├── css/
│   └── style.css               # Main stylesheet (~600+ lines)
├── js/
│   └── main.js                 # Main JavaScript (~127 lines)
├── images/                      # Local image hosting (migrated from Squarespace CDN)
│   ├── blog/                   # Blog post images (737+ images)
│   ├── events/                 # Event and workshop images
│   ├── general/                # General site images
│   ├── staff/                  # Staff photos
│   └── summer/                 # Summer camp images
├── *.html                       # 22 root-level page files (active pages)
├── content_data.json            # Structured content data (1MB+)
├── download_log.txt             # Image download log from migration
├── scripts/                     # Utility scripts (organized Nov 2025)
│   ├── README.md               # Scripts documentation
│   ├── add_toolkit.py          # Add Brand Toolkit to HTML files
│   ├── download_squarespace_images.py  # Download images from Squarespace CDN
│   ├── fix_remaining_cdn_images.py    # Fix remaining CDN URLs
│   ├── parse_export.py         # XML to JSON converter
│   └── replace_squarespace_images.py  # Replace CDN URLs with local paths
├── archive/                     # Archived files (Nov 2025)
│   ├── README.md               # Archive documentation
│   ├── MIGRATION_SUMMARY.md    # Image migration summary
│   ├── Squarespace-Wordpress-Export-11-18-2025.xml  # Original content export
│   ├── generate_site.py        # Archived - one-time migration tool (no longer used)
│   ├── pages/                  # Archived HTML pages (13 pages)
│   │   ├── README.md
│   │   └── [archived pages]
│   └── scripts/                # Legacy migration scripts
├── README.md                    # User-facing documentation
└── docs/                        # Documentation directory
    ├── README.md                # Documentation index
    ├── CLAUDE.md                # This file - AI assistant guide
    ├── deployment/              # Deployment guides
    │   ├── DEPLOYMENT.md        # Deployment instructions
    │   └── GITHUB_PAGES_SETUP.md # GitHub Pages setup guide
    ├── integration/             # Integration guides
    │   ├── BRAND_TOOLKIT_INTEGRATION.md
    │   └── INSTAGRAM_API_SETUP.md
    └── development/             # Development plans
        └── CSS_FIXES_PLAN.md
```

### Important Directories

- **`blog/`**: Contains 291+ blog post HTML files
- **`courses/`**: Course-specific content pages
- **`summer/`**: Summer camp information pages
- **`css/`**: Single stylesheet with CSS Grid, Flexbox, and CSS variables
- **`js/`**: Single JavaScript file with vanilla JS (no dependencies)
- **`images/`**: Local image hosting (migrated from Squarespace CDN in Nov 2025)
  - `blog/` - 737+ blog post images
  - `events/`, `general/`, `staff/`, `summer/` - Categorized images
- **`scripts/`**: Utility scripts for site maintenance (organized Nov 2025)
  - Image migration tools
  - Content parsing scripts
  - Brand Toolkit integration
- **`archive/`**: Archived files (created Nov 2025)
  - `pages/` - 13 archived HTML pages (unused/unlinked)
  - Original Squarespace export XML
  - Legacy migration scripts
  - `generate_site.py` (no longer used)
- **`docs/`**: Comprehensive documentation
  - Deployment guides
  - Integration guides (Brand Toolkit, Instagram API)
  - Development plans
- **Root**: 22 active main website pages (about, contact, services, etc.)

---

## Technology Stack

### Frontend
- **HTML5**: Semantic markup, accessibility-focused
- **CSS3**: Modern CSS with Grid, Flexbox, CSS variables
- **JavaScript**: Vanilla JS (ES6+), no frameworks or libraries
- **Design**: Mobile-first responsive design

### Backend/Build
- **Python 3**: Content generation and processing
- **JSON**: Structured data storage
- **XML**: Original content from Squarespace export

### Deployment
- **GitHub Pages**: Hosting platform
- **GitHub Actions**: CI/CD automation
- **Static HTML**: No server-side processing required

### Browser Support
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

---

## Key Files and Their Purpose

### Python Scripts

**Location:** `scripts/` directory (organized November 2025)
**Documentation:** See `scripts/README.md` for detailed usage

#### Image Management Scripts

##### `scripts/download_squarespace_images.py`
**Purpose:** Download images from Squarespace CDN to local hosting
**Status:** Migration completed in Nov 2025
**Features:**
- Scans HTML files for Squarespace CDN URLs
- Downloads images to categorized folders (`images/blog/`, `images/events/`, etc.)
- Skips existing files, handles duplicates
- Logs all downloads to `download_log.txt`

##### `scripts/replace_squarespace_images.py`
**Purpose:** Replace Squarespace CDN URLs with local GitHub paths
**Status:** Migration completed in Nov 2025
**Features:**
- Maps local images by filename
- Updates HTML files with local paths
- Handles URL-encoded filenames

##### `scripts/fix_remaining_cdn_images.py`
**Purpose:** Fix edge cases in image URLs (special characters, Chinese characters)
**Status:** Migration completed in Nov 2025

#### Content Processing Scripts

##### `scripts/parse_export.py`
**Purpose:** Parse WordPress/Squarespace XML export and convert to JSON
**Input:** `archive/Squarespace-Wordpress-Export-11-18-2025.xml`
**Output:** `content_data.json`
**Status:** One-time migration, completed
**Functionality:**
- Extracts site metadata (title, description)
- Parses pages and blog posts
- Categorizes content by URL structure
- Sorts posts by date (newest first)

#### Integration Scripts

##### `scripts/add_toolkit.py`
**Purpose:** Add Illinois Campus Brand Toolkit to all HTML files
**Status:** Active maintenance script
**Usage:** Run after adding/regenerating HTML files
**Features:**
- Inserts toolkit CSS and JS into all HTML files
- Skips files already containing toolkit resources
- Ensures consistent branding across site

#### Archived Scripts

##### `archive/generate_site.py` (NO LONGER USED)
**Status:** Archived - one-time migration tool
**Original Purpose:** Generate complete static website from JSON data
**Note:** All content is now edited directly in HTML files. This script is preserved for reference only.
**Key Functions (for reference):**
- `create_html_template()`: Creates full page HTML with nav and footer
- `clean_content()`: Sanitizes and prepares content HTML
- `slugify()`: Creates URL-friendly slugs
- `create_page_filename()`: Converts links to proper file paths

### HTML Files

#### Navigation Structure
All pages use consistent navigation:
- Home → `/index.html`
- About → `/about-us.html`
- What We Offer → `/pricingservices.html`
- Courses → `/courses.html`
- Summer → `/summer.html`
- Blog → `/blog/index.html`
- Resources → `/resources.html`
- Contact → `/contact.html`

#### Key Pages
- **`index.html`**: Homepage with hero section, feature cards, latest news
- **`about-us.html`**: Information about the MakerLab
- **`pricingservices.html`**: Services and pricing information
- **`courses.html`**: Course offerings overview
- **`blog/index.html`**: Blog listing with all 291 posts
- **`contact.html`**: Contact information and form

#### URL Pattern
**Note:** URLs use `/makerlab/` prefix for GitHub Pages subdirectory hosting:
- Local/dev: `/css/style.css`
- Production: `/makerlab/css/style.css`

### CSS (`css/style.css`)

#### CSS Variables (Illinois Branding)
```css
--illinois-orange: #FF5F05;
--illinois-blue: #13294B;
--illinois-cloud: #E8E9EA;
--text-dark: #333333;
--text-light: #666666;
--max-width: 1200px;
--spacing-xs: 0.5rem;
--spacing-sm: 1rem;
--spacing-md: 2rem;
--spacing-lg: 3rem;
--spacing-xl: 4rem;
```

#### Key CSS Classes
- `.container`: Max-width wrapper (1200px)
- `.section`: Vertical spacing for content sections
- `.feature-card`: Homepage feature cards
- `.card-grid`: Grid layout for cards
- `.blog-post`: Blog post styling
- `.hero`: Homepage hero section
- `.site-header`: Sticky header
- `.main-nav`: Primary navigation
- `.mobile-menu-toggle`: Mobile hamburger menu

### JavaScript (`js/main.js`)

#### Key Features
1. **Mobile Menu**: Toggle functionality for hamburger menu
2. **Active Navigation**: Highlights current page in nav
3. **Smooth Scrolling**: For anchor links
4. **Gallery Lightbox**: Opens images in new window
5. **Form Validation**: Basic required field validation
6. **External Links**: Auto-adds target="_blank"
7. **Utility Functions**: `formatDate()`, `slugify()`

#### Event Listeners
- DOMContentLoaded for initialization
- Mobile menu toggle clicks
- Form submission validation
- Smooth scroll for anchor links
- Gallery image clicks

---

## Development Workflow

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/vishalsachdev/makerlab.git
cd makerlab

# View the site locally
python3 -m http.server 8000
# Visit http://localhost:8000
```

### Content Regeneration Workflow

**Current Status:** Content regeneration scripts are ARCHIVED (November 2025)
**Reason:** Site migration is complete. All content is now maintained directly in HTML files.

**Historical Process (no longer used):**
```bash
# Step 1: Parse XML to JSON (one-time migration, completed)
python3 scripts/parse_export.py
# Output: content_data.json

# Step 2: Generate all HTML files (one-time migration, completed)
python3 archive/generate_site.py  # ARCHIVED - DO NOT USE
# Output: All HTML files (pages + blog posts)
```

**Current Workflow:**
All content changes are now made by editing HTML files directly. The migration scripts are preserved in the `archive/` directory for historical reference only.

**Important Notes:**
- `generate_site.py` is in `archive/` and should NOT be used
- All HTML files are committed to the repository for static hosting
- Edit HTML files directly for content updates
- Use `scripts/add_toolkit.py` when adding new HTML files to ensure Brand Toolkit integration

### Making Changes

#### Content Changes
1. **Text edits**: Edit HTML files directly (all sizes of changes)
2. **New pages**: Create HTML manually using existing page as template
3. **After adding pages**: Run `python3 scripts/add_toolkit.py` to add Brand Toolkit resources
4. **Images**: Place in appropriate `images/` subdirectory and use local paths

#### Style Changes
1. Edit `css/style.css`
2. Use CSS variables for colors and spacing
3. Test responsive breakpoints (mobile, tablet, desktop)
4. Maintain Illinois branding guidelines

#### Functionality Changes
1. Edit `js/main.js`
2. Keep vanilla JavaScript (no dependencies)
3. Ensure cross-browser compatibility
4. Test mobile interactions

### Testing Locally

```bash
# Python server (recommended)
python3 -m http.server 8000

# Alternative: Node.js
npx http-server

# Alternative: PHP
php -S localhost:8000
```

**Test checklist:**
- [ ] Homepage loads correctly
- [ ] Navigation works on all pages
- [ ] Mobile menu toggles properly
- [ ] Blog index and posts are accessible
- [ ] CSS loads (check dev console)
- [ ] JavaScript works (check dev console)
- [ ] Images load from CDN
- [ ] Links are not broken
- [ ] Responsive design works (mobile, tablet, desktop)

---

## Content Generation Process

### Overview
The site uses a static site generation approach where Python scripts convert XML content into structured JSON, then generate complete HTML files.

### Data Flow

```
Squarespace XML Export
    ↓
scripts/parse_export.py
    ↓
content_data.json (structured)
    ↓
generate_site.py
    ↓
HTML Files (pages + blog)
```

### Content Data Structure

```json
{
  "site": {
    "title": "Illinois MakerLab",
    "description": "Learn. Make. Share.",
    "link": "https://makerlab.illinois.edu"
  },
  "pages": [
    {
      "title": "Page Title",
      "link": "/page-url",
      "slug": "page-url",
      "content": "<html content>",
      "pubDate": "date",
      "author": "author"
    }
  ],
  "posts": [
    {
      "title": "Post Title",
      "link": "/blog/post-slug",
      "slug": "post-slug",
      "content": "<html content>",
      "pubDate": "date",
      "author": "author"
    }
  ]
}
```

### HTML Template Structure

All pages follow this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Meta tags, title, CSS -->
</head>
<body>
  <header class="site-header">
    <!-- Logo, navigation, mobile menu -->
  </header>

  <main>
    <!-- Page-specific content -->
  </main>

  <footer class="site-footer">
    <!-- Footer sections, links, copyright -->
  </footer>

  <script src="/js/main.js"></script>
</body>
</html>
```

### Image Handling

**Current Status:** ✅ All images migrated to local hosting (November 2025)
**Location:** `images/` directory with organized subdirectories
**Migration:** Completed using scripts in `scripts/` directory
**Structure:**
- `images/blog/` - 737+ blog post images
- `images/events/` - Event and workshop images
- `images/general/` - General site images
- `images/staff/` - Staff photos
- `images/summer/` - Summer camp images

**Image Paths:**
- Root pages: `/images/category/filename.jpg`
- Blog posts: `../images/blog/filename.jpg`
- All pages use GitHub Pages subdirectory prefix: `/makerlab/images/...` in production

**Benefits:**
- Improved reliability (no external CDN dependency)
- Faster loading (GitHub CDN)
- Version control for all assets
- Offline development support

---

## Coding Conventions

### HTML Conventions

1. **Semantic HTML5**: Use proper tags (`<article>`, `<section>`, `<nav>`, `<header>`, `<footer>`)
2. **Accessibility**: Include ARIA labels, alt text, proper heading hierarchy
3. **Indentation**: 2 spaces
4. **Quotes**: Double quotes for attributes
5. **Class naming**: BEM-inspired (e.g., `blog-post`, `blog-post-title`, `blog-post-meta`)

### CSS Conventions

1. **CSS Variables**: Use for colors, spacing, breakpoints
2. **Mobile-first**: Write base styles for mobile, add media queries for larger screens
3. **Class naming**: Descriptive, hyphen-separated (e.g., `feature-card-content`)
4. **Organization**:
   - Variables → Reset → Typography → Layout → Components → Utilities
5. **Specificity**: Keep low, avoid IDs for styling
6. **Comments**: Section headers with `/* ========== Section Name ========== */`

### JavaScript Conventions

1. **ES6+**: Use modern JavaScript features
2. **Vanilla JS**: No frameworks or libraries
3. **Event delegation**: Where appropriate
4. **Comments**: Function-level documentation
5. **Naming**: camelCase for variables/functions
6. **Error handling**: Defensive programming with null checks

### Python Conventions

1. **PEP 8**: Follow Python style guide
2. **Type hints**: Not currently used, but acceptable to add
3. **Documentation**: Function docstrings
4. **Error handling**: Try-except for file operations

### File Naming

- **HTML**: kebab-case (e.g., `about-us.html`, `lab-hours.html`)
- **CSS/JS**: kebab-case (e.g., `style.css`, `main.js`)
- **Python**: snake_case (e.g., `generate_site.py`)
- **Blog posts**: slug format (e.g., `post-title-here.html`)

---

## Deployment

### GitHub Pages Configuration

**Repository:** vishalsachdev/makerlab
**Branch:** main (or feature branches for development)
**Deployment method:** GitHub Actions
**URL pattern:** `https://vishalsachdev.github.io/makerlab/`

### GitHub Actions Workflow

**File:** `.github/workflows/static.yml`

**Trigger:**
- Push to main branch
- Manual workflow dispatch

**Process:**
1. Checkout repository
2. Setup GitHub Pages
3. Upload artifact (entire repository)
4. Deploy to GitHub Pages

**Permissions:**
- `contents: read`
- `pages: write`
- `id-token: write`

### Deployment Process

```bash
# 1. Make changes locally
git add .
git commit -m "Description of changes"

# 2. Push to GitHub
git push origin branch-name

# 3. GitHub Actions automatically deploys (if on main branch)
# Monitor at: https://github.com/vishalsachdev/makerlab/actions

# 4. Site updates at: https://vishalsachdev.github.io/makerlab/
```

### Deployment Verification

After deployment, verify:
- [ ] Site loads at production URL
- [ ] All pages accessible
- [ ] CSS and JS load correctly
- [ ] Images load from CDN
- [ ] Navigation works
- [ ] Mobile responsive
- [ ] No console errors

### Custom Domain (Future)

To use `makerlab.illinois.edu`:
1. Add `CNAME` file with domain
2. Configure DNS (CNAME to vishalsachdev.github.io)
3. Update GitHub Pages settings
4. Enable HTTPS

---

## Testing and Quality Assurance

### Manual Testing Checklist

#### Functionality
- [ ] Homepage hero section displays
- [ ] Navigation menu works on all pages
- [ ] Mobile menu toggles correctly
- [ ] All internal links work
- [ ] Blog index lists all posts
- [ ] Individual blog posts load
- [ ] Course pages accessible
- [ ] Contact page displays
- [ ] Footer links work

#### Design/Responsiveness
- [ ] Mobile (320px-767px): Menu collapses, cards stack
- [ ] Tablet (768px-1023px): Layout adjusts properly
- [ ] Desktop (1024px+): Full layout displays
- [ ] Typography scales appropriately
- [ ] Images responsive (max-width: 100%)
- [ ] Touch targets adequate (mobile)

#### Performance
- [ ] Pages load quickly (<2s)
- [ ] Images optimized (or using CDN)
- [ ] CSS minified (for production)
- [ ] JS minified (for production)
- [ ] No console errors
- [ ] No broken links (404s)

#### Accessibility
- [ ] Heading hierarchy proper (h1→h2→h3)
- [ ] Alt text on images
- [ ] ARIA labels on interactive elements
- [ ] Keyboard navigation works
- [ ] Color contrast meets WCAG AA
- [ ] Focus indicators visible

### Browser Testing

Test in:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Chrome Mobile (Android)
- Safari Mobile (iOS)

### Validation Tools

```bash
# HTML validation
# Visit: https://validator.w3.org/
# Upload or paste HTML

# CSS validation
# Visit: https://jigsaw.w3.org/css-validator/
# Upload or paste CSS

# Accessibility check
# Visit: https://wave.webaim.org/
# Enter production URL
```

---

## Git Workflow

### Branch Strategy

**Main branch:** `main` (production)
**Feature branches:** `claude/feature-name-sessionid` (Claude AI development)
**Convention:** `claude/` prefix for AI assistant branches

### Branch Workflow

```bash
# Create feature branch
git checkout -b claude/feature-name-sessionid

# Make changes and commit
git add .
git commit -m "Descriptive commit message"

# Push to remote
git push -u origin claude/feature-name-sessionid

# Create pull request via GitHub UI
# After review and approval, merge to main
```

### Commit Message Guidelines

**Format:**
```
<type>: <subject>

<optional body>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: CSS/design changes
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat: Add new summer camp registration page

fix: Correct mobile menu toggle on iOS Safari

style: Update hero section spacing and colors

docs: Update README with deployment instructions
```

### Pull Request Process

1. **Create PR** with descriptive title
2. **Description** should include:
   - Summary of changes
   - Test plan
   - Screenshots (if design changes)
3. **Review checklist**:
   - Code follows conventions
   - No console errors
   - Responsive design tested
   - Accessibility maintained
4. **Merge** after approval
5. **Verify** deployment to production

### Git Best Practices

- Commit frequently with clear messages
- Don't commit generated files (unless required for static hosting)
- Keep commits focused and atomic
- Pull before pushing to avoid conflicts
- Use `.gitignore` for temporary files
- Never commit secrets or credentials

---

## Archive Directory

**Location:** `archive/`
**Purpose:** Preserve historical files no longer used in active development
**Created:** November 2025 during repository reorganization

### Contents

#### `archive/generate_site.py`
- **Status:** ARCHIVED - DO NOT USE
- **Original Purpose:** One-time static site generation from JSON
- **Why Archived:** Site migration complete; all content now edited directly in HTML
- **Use Case:** Historical reference only; emergency restoration if needed

#### `archive/Squarespace-Wordpress-Export-11-18-2025.xml`
- **Purpose:** Original Squarespace/WordPress export file
- **Size:** ~1.8MB
- **Use Case:** Source of truth for original content; reference for restoration

#### `archive/pages/` (13 archived HTML pages)
- **Contents:** Unused/unlinked HTML pages
- **Examples:** 3d-printing-conference.html, certificate.html, give.html, etc.
- **Reason:** Pages not linked from main navigation or other pages
- **Documentation:** See `archive/pages/README.md`

#### `archive/scripts/`
- **Contents:** Legacy migration scripts
- **Status:** Preserved for historical reference

#### `archive/MIGRATION_SUMMARY.md`
- **Purpose:** Summary of image migration process (Nov 2025)
- **Contents:** Details of Squarespace CDN → local hosting migration

### Important Notes

⚠️ **DO NOT:**
- Run `archive/generate_site.py` - it will overwrite current HTML files
- Delete archive files - they're preserved for historical reference
- Move files out of archive without understanding implications

✅ **DO:**
- Reference archived files for understanding historical decisions
- Consult `archive/pages/README.md` to understand why pages were archived
- Keep archive directory for potential future restoration needs

---

## Illinois Campus Brand Toolkit Integration

**Status:** ✅ Phase 1 Complete (November 2025)
**Documentation:** See `docs/integration/BRAND_TOOLKIT_INTEGRATION.md`

### Overview

All HTML files now integrate the official University of Illinois Campus Brand Toolkit to ensure campus-wide visual consistency and accessibility standards.

### Implementation

**Toolkit Resources Added:**
- **CSS:** `//cdn.toolkit.illinois.edu/3/toolkit.css` (loaded before custom styles)
- **JavaScript:** `//cdn.toolkit.illinois.edu/3/toolkit.js` (type="module")

**Integration Script:**
- `scripts/add_toolkit.py` - Automatically adds toolkit resources to all HTML files
- Skips files that already have toolkit integration
- Should be run whenever new HTML files are added

### Brand Compliance

✅ **Colors:** Already compliant
- Illinois Orange: #FF5F05 (`--illinois-orange`)
- Illinois Blue: #13294B (`--illinois-blue`)
- Cloud: #E8E9EA (`--illinois-cloud`)

⚠️ **Typography:** Planned for Phase 2
- Will update to Montserrat (headlines) and Source Sans Pro (body)
- Current: Helvetica Neue, Arial, sans-serif

### Available Components

The toolkit provides ready-to-use components:
- Layout: Page, Columns, Grid, Hero, Header, Footer
- Content: Cards, Quote, Statistic, Profile
- Navigation: Breadcrumbs, Section Nav, Pagination, Tabs, Accordion
- Interactive: Modal, Tooltip, Call to Action
- Media: Video embeds, Icons
- Utilities: Buttons, Image Cover, Screen Reader helpers

### Usage Guidelines

**When adding new HTML pages:**
1. Create page using existing template
2. Run `python3 scripts/add_toolkit.py` to add toolkit resources
3. Test that toolkit CSS/JS load without conflicts

**When updating styles:**
- Custom styles in `css/style.css` override toolkit defaults
- Use Illinois color variables for consistency
- Maintain mobile-first responsive approach

**Resources:**
- Toolkit builder: https://builder3.toolkit.illinois.edu/
- Brand guidelines: https://brand.illinois.edu/
- Typography guide: https://marketing.illinois.edu/visual-identity/typography

---

## Important Guidelines for AI Assistants

### What You Should Do

1. **Read existing code first**: Always examine current implementation before making changes
2. **Maintain consistency**: Follow established patterns and conventions
3. **Test locally**: Verify changes work before committing
4. **Preserve branding**: Keep Illinois colors and design system
5. **Document changes**: Update relevant documentation
6. **Use semantic HTML**: Maintain accessibility standards
7. **Keep it simple**: Vanilla JS, no unnecessary dependencies
8. **Mobile-first**: Always consider responsive design
9. **Ask for clarification**: When requirements are unclear
10. **Commit frequently**: With clear, descriptive messages

### What You Should NOT Do

1. **Don't run archived scripts**: NEVER run `archive/generate_site.py` - it will overwrite HTML files
2. **Don't break existing functionality**: Test thoroughly
3. **Don't introduce dependencies**: No npm packages, frameworks, etc.
4. **Don't modify branding**: Illinois colors are fixed; maintain Brand Toolkit integration
5. **Don't remove accessibility features**: ARIA labels, alt text, etc.
6. **Don't change URL structure**: Would break existing links
7. **Don't commit secrets**: API keys, credentials, etc.
8. **Don't ignore mobile**: Always test responsive design
9. **Don't skip testing**: Even for "small" changes
10. **Don't push directly to main**: Use feature branches
11. **Don't delete archived files**: They're preserved for historical reference
12. **Don't skip Brand Toolkit**: Run `scripts/add_toolkit.py` after adding new HTML pages

### Common Tasks

#### Adding a New Page

```bash
# Creating a new page (current recommended approach)
1. Copy an existing page as template
   cp about-us.html new-page.html

2. Edit content in new-page.html
   - Update title, meta tags
   - Replace content in <main> section
   - Keep header and footer structure

3. Add Brand Toolkit integration
   python3 scripts/add_toolkit.py
   # Ensures toolkit CSS/JS are included

4. Update navigation (if needed)
   - Add link to new page in header navigation
   - Update navigation in all pages (use find/replace or edit manually)

5. Test locally
   python3 -m http.server 8000
   # Visit http://localhost:8000/new-page.html

6. Commit and push
   git add new-page.html
   git commit -m "Add new page: [description]"
   git push -u origin branch-name

# IMPORTANT: Do NOT use archive/generate_site.py
```

#### Updating Styles

```bash
1. Edit css/style.css
2. Use CSS variables for colors/spacing
3. Test responsive breakpoints
4. Check browser compatibility
5. Commit and push
```

#### Fixing a Bug

```bash
1. Reproduce the bug locally
2. Identify root cause
3. Fix with minimal changes
4. Test thoroughly (all browsers/devices)
5. Commit with descriptive message
6. Push and create PR
```

#### Updating Content

```bash
# All content updates (minor and major):
1. Edit HTML file directly
2. Test locally (python3 -m http.server 8000)
3. Commit and push

# Adding new pages:
1. Create new HTML file using existing page as template
2. Add navigation links to other pages if needed
3. Run: python3 scripts/add_toolkit.py  # Ensures Brand Toolkit integration
4. Test locally
5. Commit and push

# Adding new images:
1. Place image in appropriate images/ subdirectory
2. Reference with local path in HTML
3. Test locally
4. Commit and push

# IMPORTANT: generate_site.py is archived - all edits are done directly in HTML
```

### Troubleshooting Guide

#### Issue: CSS not loading
- Check file path (absolute vs relative)
- Verify `/makerlab/` prefix for production
- Check browser console for 404 errors
- Clear browser cache

#### Issue: Navigation broken
- Verify all HTML files exist
- Check link paths (case-sensitive)
- Ensure consistent URL structure
- Test on production URL

#### Issue: Mobile menu not working
- Check `main.js` loaded
- Verify event listeners attached
- Test on actual mobile device
- Check console for JS errors

#### Issue: Images not displaying
- Verify image files exist in `images/` directory
- Check image path is correct (relative vs absolute)
- For blog posts, ensure path starts with `../images/`
- For root pages, ensure path is `/makerlab/images/` (production) or `/images/` (local)
- Check browser console for 404 errors
- Verify file extension matches (case-sensitive)

#### Issue: GitHub Pages not deploying
- Check Actions tab for errors
- Verify workflow permissions
- Ensure branch is correct
- Check Pages settings enabled

### Performance Considerations

- **Images**: ✅ Hosted locally in `images/` directory (migrated Nov 2025)
  - 737+ blog images organized by category
  - Served via GitHub Pages CDN
  - All images version controlled
- **CSS**: Single file, could minify for production
- **JS**: Single file, could minify for production
- **HTML**: Static files, already optimized
- **Caching**: GitHub Pages handles this automatically
- **Brand Toolkit**: Loaded from Illinois CDN (//cdn.toolkit.illinois.edu/3/)

### Security Considerations

- **No backend**: Static site, minimal security concerns
- **No user input**: Forms currently use external services
- **HTTPS**: Provided by GitHub Pages
- **Content Security**: All content from trusted source (Illinois MakerLab)
- **Dependencies**: None, reduces attack surface

### Accessibility Priorities

1. **Semantic HTML**: Always use proper tags
2. **Keyboard navigation**: Ensure all interactive elements accessible
3. **Screen readers**: Test with NVDA/JAWS/VoiceOver
4. **Color contrast**: Maintain WCAG AA minimum (4.5:1)
5. **Alt text**: Descriptive text for all images
6. **ARIA labels**: On buttons, navigation, landmarks
7. **Focus indicators**: Visible keyboard focus
8. **Heading hierarchy**: Logical document outline

---

## Quick Reference

### File Locations
- **Main CSS**: `css/style.css`
- **Main JS**: `js/main.js`
- **Homepage**: `index.html`
- **Blog index**: `blog/index.html`
- **Content data**: `content_data.json`
- **Deployment**: `.github/workflows/static.yml`

### Important URLs
- **Production**: https://vishalsachdev.github.io/makerlab/
- **GitHub Repo**: https://github.com/vishalsachdev/makerlab
- **Original Site**: https://makerlab.illinois.edu/

### Key Contacts
- **Director**: Dr. Vishal Sachdev
- **Email**: uimakerlab@illinois.edu
- **Location**: BIF Room 3030, UIUC

### Color Palette
- **Illinois Orange**: #FF5F05 (primary action color)
- **Illinois Blue**: #13294B (headings, nav)
- **Text Dark**: #333333 (body text)
- **Text Light**: #666666 (secondary text)
- **Background**: #FFFFFF (main)
- **Alt Background**: #F5F5F5 (sections)

### CSS Classes
- `.container` - Max-width wrapper
- `.section` - Vertical spacing
- `.hero` - Hero section
- `.feature-card` - Homepage cards
- `.card-grid` - Card layout
- `.blog-post` - Blog post styling
- `.btn` - Button styles
- `.btn-primary` - Orange button
- `.btn-secondary` - Blue button

### Python Commands
```bash
# Add Brand Toolkit to new/regenerated HTML files (active script)
python3 scripts/add_toolkit.py

# Start local development server
python3 -m http.server 8000

# Image migration scripts (migration completed Nov 2025, preserved for reference)
python3 scripts/download_squarespace_images.py  # Download images from CDN
python3 scripts/replace_squarespace_images.py   # Replace CDN URLs with local
python3 scripts/fix_remaining_cdn_images.py     # Fix edge cases

# Content migration scripts (one-time use, completed, preserved for reference)
python3 scripts/parse_export.py                 # Parse XML to JSON
# python3 archive/generate_site.py  # ARCHIVED - DO NOT USE
```

### Git Commands
```bash
# Create feature branch
git checkout -b claude/feature-name-sessionid

# Commit changes
git add .
git commit -m "Description"

# Push with retry on network errors
git push -u origin branch-name
```

---

## Version History

**Version 1.0** (2025-11-18)
- Initial CLAUDE.md creation
- Comprehensive documentation for AI assistants
- Based on repository state as of November 18, 2025

**Version 1.1** (2025-11-19)
- Updated repository structure (scripts reorganization, archive directory)
- Documented image migration completion (Squarespace CDN → local hosting)
- Updated file counts and locations
- Added Brand Toolkit integration status
- Enhanced archive directory documentation
- Updated workflow processes for current state

---

## Additional Resources

- [README.md](../README.md) - User-facing documentation
- [docs/deployment/DEPLOYMENT.md](deployment/DEPLOYMENT.md) - Detailed deployment instructions
- [docs/deployment/GITHUB_PAGES_SETUP.md](deployment/GITHUB_PAGES_SETUP.md) - GitHub Pages configuration
- [docs/integration/BRAND_TOOLKIT_INTEGRATION.md](integration/BRAND_TOOLKIT_INTEGRATION.md) - Brand Toolkit integration guide
- [docs/README.md](README.md) - Documentation index
- [scripts/README.md](../scripts/README.md) - Scripts documentation
- [archive/README.md](../archive/README.md) - Archive directory documentation
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [MDN Web Docs](https://developer.mozilla.org/) - HTML/CSS/JS reference
- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/) - Accessibility standards

---

**Last Updated:** 2025-11-19
**Maintained By:** AI Assistants working with vishalsachdev/makerlab repository
**Questions?** Refer to README.md or contact the repository maintainers
