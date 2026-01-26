# MakerLab Website - Webmaster TODO

**Updated:** January 25, 2026
**Site:** makerlab.illinois.edu

---

## Recently Completed (Jan 25, 2026)

### AI Agent Readiness
- [x] **Created llms.txt** - Plain text summary for AI agents at root
- [x] **Updated all URLs to custom domain** - agent-guide.json, site-info.json, robots.txt, sitemap.xml now use makerlab.illinois.edu
- [x] **Added meaningful descriptions to pages.json** - All 32 active pages now have unique, descriptive summaries
- [x] **Added FAQPage schema to faq.html** - Schema.org structured data for search engines and AI
- [x] **Expanded FAQ content** - Added 5 new common questions (ordering, summer camps, birthday parties, courses, contact)
- [x] **Updated robots.txt** - Added llms.txt to allowed paths for agents
- [x] **Updated agent-guide.json** - Added llms.txt endpoint documentation

### Content & Data Accuracy
- [x] **Fixed Digital Making course status** - Removed discontinued BADM 357 from active courses, updated to Making Things (BADM 331) only
- [x] **Cleaned up pages.json** - Separated active (32), archived (4), and legacy (8) pages
- [x] **Updated homepage structured data** - Fixed URL, corrected course info in JSON-LD
- [x] **Added main.js to index.html** - Was missing script include

### Code Quality
- [x] **Consolidated CSS duplication** - Merged 4 duplicate .reviews-grid definitions into single clean section (~120 lines removed)

---

## Already Fixed

- [x] **Missing `</script>` tag in index.html** - Fixed broken HTML that could break page rendering
- [x] **Lab hours updated** - Changed to Spring 2026 hours: Weekdays 2-7pm starting January 26
- [x] **Sitemap cleaned** - Removed 19 orphaned page entries (now 317 valid URLs)
- [x] **Custom domain verified** - makerlab.illinois.edu DNS verified with GitHub Pages
- [x] **Footer years updated** - Main site pages updated to 2026 (blog posts remain 2025 as historical)
- [x] **Squarespace CDN removed** - All external CDN dependencies removed; broken images noted as unavailable
- [x] **Newsletter page archived** - No longer sending newsletters; links removed

---

## High Priority

### 1. ~~Google Analytics Not Configured~~ FIXED
**Status:** Configured with `G-R2GVFSKNPE` on January 23, 2026

---

## Medium Priority

### 3. ~~External Image References (Squarespace CDN)~~ FIXED
**Status:** All Squarespace CDN references removed. Original images were unavailable (expired).

### 4. ~~Update Base URL for Custom Domain~~ DONE
**Status:** DNS verified and working.

---

## Low Priority / Nice to Have

### 5. Blog Post Dates
**Issue:** Some blog posts have dates that don't match their content
**Action:** Audit blog posts for date accuracy

---

## DNS Setup - COMPLETE

Custom domain `makerlab.illinois.edu` is verified and active.
- TXT record added for GitHub verification
- HTTPS enforced via GitHub Pages

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
├── sitemap.xml         # Sitemap (317 URLs)
└── robots.txt          # Bot instructions
```

---

## Contact

Questions? Reach out to Vishal Sachdev or check the repository at:
https://github.com/vishalsachdev/makerlab
