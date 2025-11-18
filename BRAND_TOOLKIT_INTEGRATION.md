# Illinois Campus Brand Toolkit Integration

**Phase 1: Setup & Resource Integration** ✅ COMPLETE

## Overview

This document tracks the integration of the official University of Illinois Campus Brand Toolkit into the MakerLab website.

## Phase 1: Completed Tasks

### 1. Toolkit CDN Resources Added

Successfully integrated toolkit resources into **all 337 HTML files**:

- **CSS**: `//cdn.toolkit.illinois.edu/3/toolkit.css`
  - Added before custom `/css/style.css` to allow custom overrides
  - Provides base typography, colors, and component styles

- **JavaScript**: `//cdn.toolkit.illinois.edu/3/toolkit.js` (type="module")
  - Added before custom `/js/main.js`
  - Enables interactive toolkit components

### 2. Implementation Method

Created Python script (`add_toolkit.py`) to automate integration:
- Scans all HTML files recursively
- Inserts toolkit CSS before first `<link>` tag
- Inserts toolkit JS before first `<script>` tag
- Skips files already containing toolkit resources

**Result**: All 337 files updated successfully with zero errors.

### 3. Brand Standards Analysis

#### Colors ✅ Already Compliant

Current MakerLab colors match official Illinois brand guidelines:

| Color Name | Hex Code | Current Variable | Status |
|------------|----------|------------------|---------|
| Illini Orange | #FF5F05 | `--illinois-orange` | ✅ Match |
| Illini Blue | #13294B | `--illinois-blue` | ✅ Match |
| Cloud | #E8E9EA | `--illinois-cloud` | ✅ Match |

**Additional Official Colors Available**:
- Altgeld Orange: #C84113 (accessible alternative)
- Storm Gray: #707372 (neutral option)
- Supporting colors for icons/charts: Industrial, Arches, Patina, Berry, Harvest, Prairie, Earth

#### Typography ⚠️ Needs Update

**Official Illinois Fonts**:
- **Montserrat**: Display font for headlines and subheadings
- **Source Sans Pro**: Primary font for body text, captions, and most content
- **Georgia**: For large blocks of copy and subheadings
- **Open Sans Condensed**: Narrow option (use sparingly)

**Current MakerLab Fonts**:
- Helvetica Neue, Arial, sans-serif

**Action Required**: Phase 2 will update font stack to match toolkit standards.

### 4. Available Toolkit Components

#### Layout & Structure
- Page, Columns, Grid, Spacer
- Hero, Page Title
- Header, Header Menu, Footer

#### Content Display
- Content (standard styles)
- Content variations: Introduction, Lede, Inset
- Card, Carousel
- Quote, Statistic
- Award List, Profile, Profile Card, Profile List

#### Navigation
- Breadcrumbs
- Section Nav (auto & manual)
- Pagination, Back to Top
- Tabs, Accordion

#### Interactive Elements
- Modal, Tooltip
- Call to Action
- Icon Panel

#### Media
- Video, Video Short
- Icon

#### Styling Utilities
- Global Button Styles
- Global Image Cover
- Global Screen Reader (accessibility)

### 5. Integration Testing Required

Before Phase 2, we should verify:
1. ✅ Toolkit CSS loads without conflicts
2. ✅ Toolkit JS loads and executes properly
3. ⏳ No visual regressions on key pages
4. ⏳ Mobile responsiveness maintained
5. ⏳ Custom styles still work as expected

## Next Steps: Phase 2 Planning

### Recommended Component Migrations

**High Priority**:
1. **Typography**: Update to Montserrat/Source Sans Pro
2. **Buttons**: Migrate to toolkit button styles
3. **Header**: Evaluate toolkit header vs custom header
4. **Footer**: Consider toolkit footer integration

**Medium Priority**:
5. **Cards**: Update card grid to use toolkit card component
6. **Navigation**: Enhance with toolkit nav patterns
7. **Accessibility**: Add skip-to-content link
8. **GDPR**: Implement cookie banner

**Low Priority**:
9. **Hero Section**: Evaluate toolkit hero vs custom gradient
10. **Forms**: Update contact/order forms with toolkit styles

### Design Decisions Needed

1. **Header Component**:
   - Option A: Full toolkit header (campus-wide consistency)
   - Option B: Custom header with toolkit styling (maintain branding)
   - Option C: Hybrid approach (toolkit base + MakerLab customization)

2. **Footer Component**:
   - Similar options as header
   - Must preserve contact info and social links

3. **Version Strategy**:
   - Currently using: Major version 3 (auto-updates to 3.x)
   - Consider: Pin to specific minor/patch version for stability?

## Resources

- **Toolkit Documentation**: https://builder3.toolkit.illinois.edu/
- **Component Builder**: https://builder3.toolkit.illinois.edu/
- **Brand Guidelines**: https://brand.illinois.edu/
- **Color Standards**: https://brand.illinois.edu/visual-identity/color/
- **Typography Standards**: https://marketing.illinois.edu/visual-identity/typography

## Files Modified

- All 337 HTML files (toolkit resources added)
- `add_toolkit.py` (integration script - can be removed after Phase 1)

## Version Information

- Toolkit Version: 3.x (latest)
- Integration Date: 2025-11-18
- Updated By: Claude Code
