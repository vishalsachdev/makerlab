# MakerLab Website - Webmaster TODO

**Generated:** January 20, 2026
**Site:** makerlab.illinois.edu

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
