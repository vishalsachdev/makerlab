# Illinois MakerLab Website

Webmaster guide for [makerlab.illinois.edu](https://makerlab.illinois.edu)

## Quick Start

```bash
# Run locally
python3 -m http.server 8000
# Visit http://localhost:8000
```

## Making Changes

### Edit a Page
1. Find the HTML file (e.g., `about-us.html`, `lab-hours.html`)
2. Edit content directly in the HTML
3. Commit and push - site auto-deploys

### Update Navigation
Navigation uses dropdowns. To change site-wide:
1. Edit templates in `scripts/update_nav.py`
2. Run `python3 scripts/update_nav.py`
3. Commit all changed files

### Add a New Page
1. Copy an existing page as template
2. Update content, title, meta description
3. Run `python3 scripts/add_toolkit.py` to ensure brand toolkit is included
4. Add to navigation if needed (see above)

### Blog Posts
- Posts are in `blog/` as individual HTML files
- Use existing post as template
- Monthly blog generation from Podio: see `scripts/podio/README.md`

### Summer Camps
- Main page: `summer.html` (pricing, dates)
- Individual camps: `summer/*.html`
- Update annually before registration opens

## Key Files

| File | Purpose |
|------|---------|
| `css/style.css` | All site styles |
| `js/main.js` | Mobile menu, blog search, breadcrumbs |
| `CLAUDE.md` | AI assistant instructions (for Claude Code) |
| `WEBMASTER-TODO.md` | Known issues and tasks |

## Deployment

Automatic via GitHub Actions on push to `main`. No build step needed.

- **Live**: https://makerlab.illinois.edu
- **Backup**: https://vishalsachdev.github.io/makerlab/

## File Structure

```
makerlab/
├── *.html           # Main pages (32 active)
├── blog/            # Blog posts (291)
├── courses/         # Course pages
├── summer/          # Summer camp pages
├── css/style.css    # Stylesheet
├── js/main.js       # JavaScript
├── images/          # All images
├── api/             # JSON APIs for LLM agents
├── scripts/         # Utility scripts
│   ├── podio/       # Blog generation from Podio
│   └── update_nav.py
└── archive/         # Old/archived content
```

## AI Agent Support

The site is optimized for AI agents (ChatGPT, Claude, Perplexity, etc.):

| Endpoint | Purpose |
|----------|---------|
| `/llms.txt` | Plain text summary for AI agents |
| `/agent-guide.json` | Detailed agent usage instructions |
| `/api/site-info.json` | Contact, hours, services |
| `/api/pages.json` | Page index with descriptions |
| `/api/blog/posts.json` | Searchable blog index |

All LLM crawlers are explicitly allowed in `robots.txt`.

## Branding

Illinois colors (in CSS variables):
- Orange: `#FF5F05`
- Blue: `#13294B`

Brand toolkit loaded from CDN - do not remove from `<head>`.

## Contact

Questions? Email uimakerlab@illinois.edu

---

*For detailed technical docs, see `CLAUDE.md`*
