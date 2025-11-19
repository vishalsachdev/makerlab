# CSS & Styling Issues Fix Plan

## Overview
This document outlines CSS and styling issues found across the Illinois MakerLab website and provides a plan to fix them for consistency and better user experience.

---

## Issues Identified

### 1. **Messy HTML Structure & Legacy Squarespace Code**
**Affected Pages:**
- `resources.html` - Contains unformatted HTML with `sqs-html-content` divs
- `about-us.html` - Has `sqs-html-content` wrapper with inline styles
- `summer.html` - Messy HTML structure with unclosed divs
- `workshops.html` - Inline styles and messy formatting
- `contact.html` - Legacy Squarespace formatting
- `courses.html` - Unformatted content blocks
- `courses/making-things.html` - Legacy formatting
- `courses/digital-making.html` - Legacy formatting
- `online-summer-camps-2021.html` - Legacy formatting
- `volunteer.html` - Legacy formatting

**Issues:**
- `<div class="sqs-html-content">` wrappers with `data-sqsp-text-block-content` attributes
- Inline styles like `style="white-space:pre-wrap;"`
- Unclosed or improperly nested divs
- Missing semantic HTML structure
- Content not wrapped in proper sections

**Fix Strategy:**
- Remove `sqs-html-content` divs
- Remove inline styles and move to CSS classes
- Wrap content in semantic `<section>` tags with `service-section` class
- Add proper `<hr />` dividers between sections
- Clean up HTML structure

---

### 2. **Pricing Information Not in Tables**
**Affected Pages:**
- `workshops.html` - Pricing shown as plain text ($20 per workshop)
- `summer.html` - Camp pricing shown as plain text
- `pricingservices.html` - Private Tutoring pricing ($25) shown as plain text (could be table)

**Issues:**
- Pricing information displayed as plain paragraphs
- Inconsistent with `pricingservices.html` main tables
- Hard to scan and compare prices

**Fix Strategy:**
- Convert workshop pricing to table format
- Convert summer camp pricing to organized table/card format
- Consider converting Private Tutoring pricing to table format for consistency

---

### 3. **Image Styling Issues**
**Affected Pages:**
- `resources.html` - Images in gallery lack proper styling
- `gallery.html` - Images need consistent styling
- `summer.html` - Images need responsive styling
- `workshops.html` - Images need styling
- `online-ordering.html` - Fixed, but check for consistency

**Issues:**
- Images without `max-width: 100%` for responsiveness
- Missing `border-radius` for consistency
- No `alt` attributes on some images
- Images not properly contained in responsive containers

**Fix Strategy:**
- Add responsive image classes or inline styles
- Ensure all images have proper `alt` attributes
- Add consistent border-radius and spacing
- Use CSS classes for image styling instead of inline styles

---

### 4. **Missing Section Structure**
**Affected Pages:**
- `resources.html` - Content not in proper sections
- `about-us.html` - Single large content block
- `summer.html` - Camp listings not in structured sections
- `workshops.html` - Workshop listings not in structured sections
- `contact.html` - Form not in proper section

**Issues:**
- Content not wrapped in `<section class="service-section">`
- Missing `<hr />` dividers between major sections
- No clear visual hierarchy

**Fix Strategy:**
- Wrap all major content areas in `<section class="service-section">`
- Add `<hr />` dividers between sections
- Ensure consistent spacing and structure

---

### 5. **Inline Styles**
**Affected Pages:**
- Multiple pages have `style="white-space:pre-wrap;"` inline styles
- Some pages have inline styles for images
- `online-ordering.html` - Has inline styles (recently added, should be moved to CSS)

**Issues:**
- Inline styles make maintenance difficult
- Inconsistent styling
- Hard to update globally

**Fix Strategy:**
- Remove all inline styles
- Create CSS classes for common patterns
- Use utility classes where appropriate

---

### 6. **Missing Responsive Design Elements**
**Affected Pages:**
- `summer.html` - Camp cards not responsive
- `workshops.html` - Workshop cards not responsive
- `resources.html` - Image galleries need responsive grid

**Issues:**
- Content doesn't adapt well to mobile devices
- Grid layouts not using CSS Grid properly
- Cards not responsive

**Fix Strategy:**
- Implement responsive grid layouts using CSS Grid
- Add mobile-first media queries
- Ensure all cards and tables are responsive

---

### 7. **Inconsistent Button/Link Styling**
**Affected Pages:**
- `summer.html` - Links not styled as buttons
- `workshops.html` - Registration links not styled consistently
- `contact.html` - Form submission needs button styling

**Issues:**
- Some links styled as buttons, others not
- Inconsistent call-to-action styling
- Missing button classes

**Fix Strategy:**
- Use consistent button classes (`.btn`, `.btn-primary`)
- Style all call-to-action links consistently
- Ensure buttons are accessible

---

### 8. **Content Formatting Issues**
**Affected Pages:**
- `resources.html` - Lists not properly formatted
- `about-us.html` - Paragraphs need better spacing
- `summer.html` - Camp descriptions need better formatting
- `workshops.html` - Workshop descriptions need formatting

**Issues:**
- Text blocks not properly formatted
- Missing line-height and spacing
- Hard to read long paragraphs

**Fix Strategy:**
- Add proper typography classes
- Improve line-height and spacing
- Break up long paragraphs
- Use lists where appropriate

---

## Priority Fix Order

### Phase 1: High Priority (Core Pages)
1. **resources.html** - Major content page, needs structure
2. **about-us.html** - Important page, needs cleanup
3. **summer.html** - Pricing and structure issues
4. **workshops.html** - Pricing and structure issues

### Phase 2: Medium Priority (Supporting Pages)
5. **contact.html** - Form and content structure
6. **courses.html** - Content formatting
7. **courses/making-things.html** - Legacy formatting
8. **courses/digital-making.html** - Legacy formatting

### Phase 3: Lower Priority (Less Visited Pages)
9. **online-summer-camps-2021.html** - Legacy formatting
10. **volunteer.html** - Legacy formatting
11. **gallery.html** - Image styling

---

## CSS Classes to Create/Use

### New CSS Classes Needed:
```css
/* Content formatting */
.content-section {
  margin-bottom: var(--spacing-xl);
}

.content-section h2 {
  color: var(--illinois-blue);
  margin-bottom: var(--spacing-md);
  font-size: 2rem;
}

.content-section h3 {
  color: var(--illinois-blue);
  margin-bottom: var(--spacing-sm);
  font-size: 1.5rem;
}

/* Responsive images */
.responsive-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin-bottom: var(--spacing-md);
}

/* Workshop/Camp cards */
.camp-card,
.workshop-card {
  background-color: var(--white);
  border-radius: 8px;
  padding: var(--spacing-md);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: var(--spacing-lg);
}

.camp-card img,
.workshop-card img {
  width: 100%;
  height: auto;
  border-radius: 4px;
  margin-bottom: var(--spacing-sm);
}

/* Pricing cards */
.pricing-card {
  background-color: var(--white);
  border-radius: 8px;
  padding: var(--spacing-md);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.pricing-card-price {
  font-size: 2rem;
  font-weight: 700;
  color: var(--illinois-orange);
  margin: var(--spacing-sm) 0;
}

/* Clean content wrapper */
.clean-content {
  line-height: 1.8;
}

.clean-content p {
  margin-bottom: var(--spacing-md);
}

.clean-content ul,
.clean-content ol {
  margin: var(--spacing-md) 0;
  padding-left: var(--spacing-lg);
}

.clean-content li {
  margin-bottom: var(--spacing-sm);
  line-height: 1.8;
}
```

---

## Implementation Steps

### For Each Page:

1. **Remove Legacy Code**
   - Remove `<div class="sqs-html-content">` wrappers
   - Remove `data-sqsp-text-block-content` attributes
   - Remove inline `style="white-space:pre-wrap;"` attributes

2. **Structure Content**
   - Wrap major sections in `<section class="service-section">`
   - Add `<h2>` headings for each section
   - Add `<hr />` dividers between sections

3. **Format Content**
   - Apply `.clean-content` class to content areas
   - Convert plain text pricing to tables where appropriate
   - Format lists properly

4. **Style Images**
   - Add responsive image styling
   - Ensure all images have `alt` attributes
   - Use consistent image containers

5. **Add Responsive Elements**
   - Implement responsive grids for cards
   - Ensure tables are responsive
   - Test on mobile devices

6. **Consistent Buttons/Links**
   - Style call-to-action links as buttons
   - Use consistent button classes
   - Ensure accessibility

---

## Testing Checklist

After fixes, test each page for:
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Consistent styling with other pages
- [ ] Proper HTML structure (validate)
- [ ] Images load and are responsive
- [ ] Tables display correctly
- [ ] Links and buttons work
- [ ] Content is readable and well-formatted
- [ ] No inline styles remain
- [ ] No legacy Squarespace code remains

---

## Estimated Time

- **Phase 1:** 4-6 hours (4 pages)
- **Phase 2:** 3-4 hours (4 pages)
- **Phase 3:** 2-3 hours (3 pages)
- **Total:** 9-13 hours

---

## Notes

- Keep existing functionality intact
- Maintain Illinois branding colors
- Ensure accessibility standards
- Test on multiple browsers
- Mobile-first approach

