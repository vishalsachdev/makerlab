# MakerLab Website - Webmaster TODO

**Generated:** January 20, 2026
**Site:** makerlab.illinois.edu

---

## Already Fixed

- [x] **Missing `</script>` tag in index.html** - Fixed broken HTML that could break page rendering
- [x] **Lab hours updated** - Changed to Spring 2026 hours: Weekdays 2-7pm starting January 26

---

## High Priority

### 1. Google Analytics Not Configured
**File:** `index.html` (lines 10-16)
**Issue:** Analytics ID is placeholder text `GA_MEASUREMENT_ID`
**Action:** Replace with actual Google Analytics ID or remove the tracking code entirely

```html
<!-- Current (broken) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
```

### 2. Sitemap Contains 19 Missing Pages (404 errors)
**File:** `sitemap.xml`
**Issue:** These pages are listed in sitemap but don't exist, causing SEO issues and broken crawls

**Missing pages to remove from sitemap.xml:**
- `2098.html`
- `3d-printing-conference.html`
- `5437.html`
- `6268.html`
- `certificate.html`
- `gallery-1.html`
- `give.html`
- `hackillinois.html`
- `home-five.html`
- `internship-database.html`
- `makerlab-wrapped.html`
- `makerlab-x-makers-for-covid.html`
- `mijireh-secure-checkout.html`
- `online-ordering-1.html`
- `past-gurus.html`
- `practicum.html`
- `scholarships.html`
- `summer-2020-response.html`
- `summer-jobs.html`

**Action:** Either create these pages OR remove them from `sitemap.xml`

**Note:** Some of these pages exist in `archive/pages/` - decide if they should be restored or left archived.

---

## Medium Priority

### 3. External Image References (Squarespace CDN)
**Issue:** Some blog posts still reference images from Squarespace CDN
**Example URLs:** `http://static1.squarespace.com/static/59ebf554edaed825d0d8e200/...`
**Risk:** Images may break if Squarespace changes CDN policies
**Action:** Download images locally and update references, or verify they still work

### 4. Update Base URL for Custom Domain
**Files:** `sitemap.xml`, `index.html` (JSON-LD), `api/*.json`
**Issue:** URLs currently point to `vishalsachdev.github.io/makerlab/`
**Action:** Once DNS is active, update to `makerlab.illinois.edu`

---

## Low Priority / Nice to Have

### 5. Footer Copyright Year
**Files:** All HTML files
**Issue:** Footer shows `2025` - consider updating to `2026` or making it dynamic

### 6. Blog Post Dates
**Issue:** Some blog posts have dates that don't match their content
**Action:** Audit blog posts for date accuracy

---

## DNS Setup (Pending IT)

Provide IT services:
| Field | Value |
|-------|-------|
| Record Type | CNAME |
| Host | `makerlab` |
| Target | `vishalsachdev.github.io` |

After DNS propagates:
1. GitHub will show green checkmark for DNS
2. Enable "Enforce HTTPS" in GitHub Pages settings
3. Update all internal URLs to use `https://makerlab.illinois.edu`

---

## Site Structure Reference

```
makerlab/
├── index.html          # Homepage
├── 45+ page files      # Main content pages
├── blog/               # 291 blog posts
├── courses/            # Course pages
├── summer/             # Summer camp pages
├── api/                # JSON APIs for LLM agents
├── css/style.css       # Main stylesheet
├── js/main.js          # Main JavaScript
├── images/             # All images
├── sitemap.xml         # Sitemap (needs cleanup)
└── robots.txt          # Bot instructions
```

---

## Contact

Questions? Reach out to Vishal Sachdev or check the repository at:
https://github.com/vishalsachdev/makerlab
