# CLAUDE.md - AI Assistant Guide for Illinois MakerLab Website

This document provides comprehensive guidance for AI assistants working with the Illinois MakerLab website codebase.

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Technology Stack](#technology-stack)
- [Key Files and Their Purpose](#key-files-and-their-purpose)
- [Development Workflow](#development-workflow)
- [Content Generation Process](#content-generation-process)
- [Coding Conventions](#coding-conventions)
- [Deployment](#deployment)
- [Testing and Quality Assurance](#testing-and-quality-assurance)
- [Git Workflow](#git-workflow)
- [Important Guidelines for AI Assistants](#important-guidelines-for-ai-assistants)

---

## Project Overview

**Project Name:** Illinois MakerLab Website
**Type:** Static website
**Live URL:** https://vishalsachdev.github.io/makerlab/
**Purpose:** Replica of the Illinois MakerLab website showcasing the world's first business school 3D printing lab at UIUC

### Key Features
- 45+ complete pages covering all aspects of the MakerLab
- 291 blog posts from 2012-2025
- Responsive design with mobile-first approach
- Illinois branding (Orange: #FF5F05, Blue: #13294B)
- GitHub Pages deployment with automated CI/CD

### About Illinois MakerLab
- **Mission:** Learn. Make. Share.
- **Location:** Business Instructional Facility, Room 3030, UIUC
- **Focus:** 3D printing, digital making, courses, summer camps, and community engagement
- **Director:** Dr. Vishal Sachdev
- **Executive Director:** Dr. Aric Rindfleisch

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
├── *.html                       # 45+ root-level page files
├── content_data.json            # Structured content data (1MB+)
├── Squarespace-Wordpress-Export-11-18-2025.xml  # Original content export
├── parse_export.py              # XML to JSON converter
├── extract_content.py           # Content extraction script
├── archive/
│   └── generate_site.py         # Archived - one-time migration tool (no longer used)
├── README.md                    # User-facing documentation
├── docs/                         # Documentation directory
│   ├── README.md                # Documentation index
│   ├── CLAUDE.md                # This file - AI assistant guide
│   ├── deployment/              # Deployment guides
│   │   ├── DEPLOYMENT.md        # Deployment instructions
│   │   └── GITHUB_PAGES_SETUP.md # GitHub Pages setup guide
│   ├── integration/             # Integration guides
│   │   ├── BRAND_TOOLKIT_INTEGRATION.md
│   │   └── INSTAGRAM_API_SETUP.md
│   └── development/             # Development plans
│       └── CSS_FIXES_PLAN.md
└── CLAUDE.md                    # This file - AI assistant guide
```

### Important Directories

- **`blog/`**: Contains 291+ generated blog post HTML files
- **`courses/`**: Course-specific content pages
- **`summer/`**: Summer camp information pages
- **`css/`**: Single stylesheet with CSS Grid, Flexbox, and CSS variables
- **`js/`**: Single JavaScript file with vanilla JS (no dependencies)
- **Root**: 45+ main website pages (about, contact, services, etc.)

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

#### `parse_export.py`
**Purpose:** Parse WordPress/Squarespace XML export and convert to JSON
**Input:** `Squarespace-Wordpress-Export-11-18-2025.xml`
**Output:** `content_data.json`
**Functionality:**
- Extracts site metadata (title, description)
- Parses pages and blog posts
- Categorizes content by URL structure
- Sorts posts by date (newest first)

#### `extract_content.py`
**Purpose:** Extract and process content from JSON
**Note:** Appears to be a legacy/helper script

#### `generate_site.py` (ARCHIVED)
**Status:** Archived to `archive/` directory - no longer used for day-to-day operations
**Original Purpose:** Generate complete static website from JSON data
**Note:** This was a one-time migration tool. All content is now edited directly in HTML files.
**Key Functions (for reference):**
- `create_html_template()`: Creates full page HTML with nav and footer
- `clean_content()`: Sanitizes and prepares content HTML
- `slugify()`: Creates URL-friendly slugs
- `create_page_filename()`: Converts links to proper file paths
**Output:** All HTML files (pages, blog index, blog posts)

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

**When to regenerate:** Only if the XML export is updated or content needs modification

```bash
# Step 1: Parse XML to JSON (if XML is updated)
python3 parse_export.py
# Output: content_data.json

# Step 2: Generate all HTML files
python3 generate_site.py
# Output: All HTML files (45 pages + 291 blog posts)
```

**Important:** Generated HTML files are committed to the repository for static hosting. The Python scripts are build tools, not runtime dependencies.

### Making Changes

#### Content Changes
1. **Minor text edits**: Edit HTML files directly
2. **Major content changes**: Update `content_data.json` and regenerate
3. **New pages**: Add to `content_data.json` or create HTML manually

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
parse_export.py
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

**Current approach:** Images hosted on Squarespace CDN
**URLs:** `https://images.squarespace-cdn.com/...`
**Production consideration:** Download and host locally for reliability

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

1. **Don't break existing functionality**: Test thoroughly
2. **Don't introduce dependencies**: No npm packages, frameworks, etc.
3. **Don't modify branding**: Illinois colors are fixed
4. **Don't remove accessibility features**: ARIA labels, alt text, etc.
5. **Don't change URL structure**: Would break existing links
6. **Don't commit secrets**: API keys, credentials, etc.
7. **Don't ignore mobile**: Always test responsive design
8. **Don't skip testing**: Even for "small" changes
9. **Don't modify Python scripts**: Unless regenerating content
10. **Don't push directly to main**: Use feature branches

### Common Tasks

#### Adding a New Page

```bash
# Creating a new page (manual approach - recommended)
1. Create HTML file: new-page.html
2. Use existing page as template (copy structure from similar page)
3. Update navigation in all pages manually (or use find/replace)
4. Test locally
5. Commit and push

# Note: generate_site.py is archived and no longer used
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
# For minor text changes:
1. Edit HTML file directly
2. Test locally
3. Commit and push

# For major content updates:
1. Edit HTML files directly
2. Test locally
3. Commit all changed files
4. Push

# Note: generate_site.py is archived - all edits are done directly in HTML
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
- Verify CDN URLs are correct
- Check network tab in dev tools
- Consider hosting images locally
- Verify image URLs in content

#### Issue: GitHub Pages not deploying
- Check Actions tab for errors
- Verify workflow permissions
- Ensure branch is correct
- Check Pages settings enabled

### Performance Considerations

- **Images**: Currently using CDN, consider local hosting for production
- **CSS**: Single file, could minify for production
- **JS**: Single file, could minify for production
- **HTML**: Generated files, already optimized
- **Caching**: GitHub Pages handles this automatically

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
# Parse XML to JSON (one-time migration - already done)
python3 parse_export.py

# Generate all HTML files (archived - no longer used)
# python3 archive/generate_site.py  # Only for emergency restoration

# Start local server
python3 -m http.server 8000
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

---

## Additional Resources

- [README.md](../README.md) - User-facing documentation
- [docs/deployment/DEPLOYMENT.md](deployment/DEPLOYMENT.md) - Detailed deployment instructions
- [docs/deployment/GITHUB_PAGES_SETUP.md](deployment/GITHUB_PAGES_SETUP.md) - GitHub Pages configuration
- [docs/README.md](README.md) - Documentation index
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [MDN Web Docs](https://developer.mozilla.org/) - HTML/CSS/JS reference
- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/) - Accessibility standards

---

**Last Updated:** 2025-11-18
**Maintained By:** AI Assistants working with vishalsachdev/makerlab repository
**Questions?** Refer to README.md or contact the repository maintainers
