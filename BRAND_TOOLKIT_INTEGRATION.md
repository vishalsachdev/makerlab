# Illinois Campus Brand Toolkit Integration

**Phase 1: Setup & Resource Integration** ✅ COMPLETE

## Overview

This document tracks the integration of the official University of Illinois Campus Brand Toolkit into the MakerLab static site.

## Phase 1: Completed Tasks

### 1. Toolkit CDN Resources Added

Successfully integrated toolkit resources into **all HTML files**:

- **CSS**: `//cdn.toolkit.illinois.edu/3/toolkit.css`
  - Loaded before the project stylesheet so MakerLab overrides remain effective
  - Delivers baseline typography, palette, and utility styles
- **JavaScript**: `//cdn.toolkit.illinois.edu/3/toolkit.js` (type="module")
  - Loaded before the custom `/js/main.js`
  - Ensures toolkit components can initialize before MakerLab scripts run

### 2. Automation Script

`add_toolkit.py`:
- Recursively walks every `.html` file in the repository
- Inserts the toolkit CSS right before the first `<link rel="stylesheet">`
- Inserts the toolkit JS right before the first `<script src=...>`
- Skips files that already already link to `cdn.toolkit.illinois.edu`

### 3. Brand Standards Analysis

#### Colors ✅ Already Compliant

| Color Name     | Hex Code  | Project Variable        | Status |
|----------------|-----------|-------------------------|--------|
| Illini Orange  | `#FF5F05` | `--illinois-orange`     | ✅ Match |
| Illini Blue    | `#13294B` | `--illinois-blue`       | ✅ Match |
| Cloud          | `#E8E9EA` | `--illinois-cloud`      | ✅ Match |

Additional official colors are available for future components (Altgeld Orange, Storm Gray, Industrial, etc.).

#### Typography ⚠️ Needs Update

Official brand fonts:
- **Montserrat** for headlines/subheads
- **Source Sans Pro** for body copy, captions, and labels
- **Georgia**, **Open Sans Condensed** for select use cases

Current stack: `Helvetica Neue, Arial, sans-serif`

**Action**: Phase 2 will replace the font stack to align with the brand fonts.

### 4. Toolkit Components

Toolkit provides ready-to-apply layouts, cards, navigation, media, and utility components:

- Layout & Structure: Page, Columns, Grid, Hero, Header, Footer
- Content Display: Content variants (Introduction, Lede, Inset), Cards, Quote, Statistic, Profile
- Navigation: Breadcrumbs, Section Nav, Pagination, Tabs, Accordion
- Interactive: Modal, Tooltip, Call to Action, Icon Panel
- Media: Video embeds, Icon
- Utilities: Global Button, Image Cover, Screen Reader helpers

### 5. Integration Testing Checklist

Before Phase 2:

1. ✅ Toolkit CSS loads without CSS conflicts
2. ✅ Toolkit JS executes without console errors
3. ⏳ Key pages look unchanged (hero, feature cards, blog listing)
4. ⏳ Custom responsive layout still works on phones/tablets
5. ⏳ MakerLab scripts (`/js/main.js`) still behave the same

### Next Steps: Phase 2 Planning

**High priority**
1. Update typography to Montserrat/Source Sans Pro
2. Adopt toolkit button styles
3. Evaluate header and footer components (toolkit vs. custom)
4. Improve accessibility (skip-to-content, keyboard focus, contrast)

**Mid priority**
5. Rebuild card grids with toolkit card components
6. Enhance navigation with toolkit Tabs/Section Nav
7. Add GDPR/compliance banner component (optional)
8. Modernize forms with toolkit styling helpers

**Low priority**
9. Hero and hero gradient: consider toolkit hero component
10. Consider toolkit media components for video embeds

### Design Decisions Needed

1. Header / Footer approach: full toolkit, custom, or hybrid?
2. Version pinning: toolkit uses `3.x` CDN; consider locking to a patch for stability

## Resources

- **Toolkit builder & docs**: https://builder3.toolkit.illinois.edu/
- **Illinois brand guidelines**: https://brand.illinois.edu/
- **Colors**: https://brand.illinois.edu/visual-identity/color/
- **Typography**: https://marketing.illinois.edu/visual-identity/typography

## Files Updated

- All HTML files now load the toolkit resources
- `README.md` documents the integration
- `add_toolkit.py` makes the integration repeatable

## Versioning

- Toolkit Version: 3.x (updated automatically)
- Integration date: 2025-11-18
- Updated by: Claude Code contribution
