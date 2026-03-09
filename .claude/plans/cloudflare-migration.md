# Cloudflare Migration Plan — makerlab

## Current State
- **Type**: Static HTML (32 pages, 301 blog posts, search, 3D quote calculator)
- **Hosted on**: GitHub Pages via `static.yml` workflow with Python validation
- **Custom domain**: `makerlab.illinois.edu`
- **Beacon**: Missing
- **Entry point**: `index.html` (plus many sub-pages)

## Step 1: Add Cloudflare Web Analytics Beacon

**IMPORTANT**: This is a large multi-page site. The beacon needs to be added to ALL HTML pages, not just `index.html`.

Options:
1. **Script approach**: Write a script to inject the beacon into all `*.html` files before `</body>`
2. **Manual**: Add to layout/template if one exists, otherwise script is necessary

Beacon snippet:
```html
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "f6e8d77284b0466eb2ca753f03d64ec0"}'></script>
```

Check if `makerlab.illinois.edu` needs its own Cloudflare Web Analytics token (different hostname than `vishalsachdev.github.io`). If so, create a new site token at dash.cloudflare.com > Web Analytics.

## Step 2: Create Cloudflare Pages Project
1. Cloudflare Dashboard > Pages > Create a project
2. Connect GitHub repo: `vishalsachdev/makerlab`
3. Build settings:
   - **Framework preset**: None
   - **Build command**: `python scripts/validate_agent_data.py` (preserves existing validation)
   - **Build output directory**: `/`
4. Deploy

## Step 3: Configure Custom Domain
1. Pages project > Custom domains > Add `makerlab.illinois.edu`
2. **DNS caveat**: `makerlab.illinois.edu` is likely managed by UIUC IT, not your Cloudflare account
   - You'll need to coordinate with UIUC IT to update the DNS record to point to `<project>.pages.dev`
   - Alternative: Keep it on GitHub Pages if DNS change is blocked, and just add the beacon
3. If DNS is under your control, add CNAME `makerlab` → `<project>.pages.dev`

## Step 4: Verify Deployment
- Check all 32 pages render correctly
- Test blog search functionality
- Test 3D quote calculator
- Verify API JSON files (`api/site-info.json`, `api/pages.json`, `api/blog/posts.json`)

## Step 5: Decommission GitHub Pages
1. Remove `.github/workflows/static.yml`
2. Disable GitHub Pages in repo Settings > Pages
3. Commit and push

## Notes
- **Largest site in the fleet** — thorough testing required
- Custom domain `makerlab.illinois.edu` may be managed by UIUC IT — confirm DNS control before proceeding
- If DNS is not under your control, the fallback is: add beacon + keep on GitHub Pages
- The validation script may need adjustment for Cloudflare Pages build environment (Python availability)
