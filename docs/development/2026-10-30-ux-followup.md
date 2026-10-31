# MakerLab UX recommendations: follow-up review

Review against merged PR #39 and the director's October 30 equipment update.

Confirmed fleet includes Bambu Lab P1 with AMS 2 combo, Bambu Lab H2D Combo,
and Elegoo Neptune Max. No resin printers. Bambu Studio is used for Bambu Lab
printers. Prices do not change. Exact P1 variant and Neptune generation/build
limits are not inferred; staff confirm fit and preparation for each job.

| Earlier recommendation | Status and next action |
| --- | --- |
| Homepage actions and large banners | PR #39 adds early quote/visit actions, smaller homepage and task banners, and compact mobile cards. No additional redesign proposed. |
| Duplicate hours cards | PR #39 keeps the seasonal hours notice and changes the other card to a quote action. |
| Long ordering instructions | PR #39 adds an early form anchor and collapses preparation details. This follow-up replaces the outdated Cura/nozzle workflow with Bambu Studio guidance. |
| Desktop/mobile dropdowns | PR #39 covers taps, hover, keyboard, Escape, outside dismissal, hidden focus targets and focus across breakpoints. Existing regressions remain in place. |
| Mobile type and pricing-table scrolling | PR #39 keeps body text at 16px and wraps pricing tables. Physical-device and text-zoom checks remain outstanding. |
| Equipment accuracy | This follow-up updates About, resources, services/schema, FAQ/schema, quote/order guidance and agent metadata; removes current SLA/resin availability and legacy dimensions. Historical Ultimaker photos/partnerships are labeled as earlier support. |
| Pricing correctness | PR #39 fixes one $4 fee per order, matches all six published rates, and applies the $10 campus-account minimum. This follow-up changes no prices or calculation logic. |
| One source for pricing | Still recommended: one configuration for calculator rates, visible tables, fee/minimum copy and agent responses. Current browser tests catch table/calculator drift, but values are still duplicated. |
| Estimator inputs | Coordinates are currently assumed to be millimeters; this follow-up makes that assumption visible. Unit selection, robust geometry checks, file/triangle limits and consistent quantity bounds remain follow-up work. Printer-specific capacity warnings require confirmed model variants/configurations. |
| Estimator calibration | Compare representative models with Bambu Studio results using actual lab printer/filament profiles. Calibration needs model files plus sliced material weights (including supports/purge where relevant). Changing the slicer name does not establish better estimator accuracy. |
| Quote-to-order handoff | PR #39 explains reattachment and adds direct form links. Preserving file/options, multiple different models in one order, and an integrated order form remain a larger integration. Do not imply file transfer is implemented. |
| Payment policy | Exactly-$20 deposit handling and Podio's Check/Free choices remain unresolved. They need a policy decision and authorized external-form edits; published fees are unchanged. |
| Visiting and closures | PR #39 brings location/directions forward. A reliable today/open indicator needs a maintained schedule with explicit holiday/exception dates and America/Chicago timezone handling; do not derive it from weekly hours alone. |
| Contact | PR #39 adds a direct email address and standalone form fallback. A response-time promise needs an operational commitment before publication. |
| Featured projects | PR #39 labels older homepage stories as featured projects. New current work requires approved project evidence/photos, not invented content. |
| Camps | PR #39 archives 2026 details and preserves the established 2027 email-interest path. A native interest form still needs a destination and operating workflow. |
| Mobile and form acceptance | Chromium tests cover 320–1366px reflow and touch navigation at 360/390/430px. Physical iPhone Safari/Android, screen readers, 200% text zoom and actual Podio file/date/validation interactions remain unverified. |

## Suggested sequence

1. Merge the equipment/slicer consistency update after review.
2. Centralize pricing and validate estimator input units, quantities and geometry.
3. Calibrate estimates against real Bambu Studio jobs; confirm exact printer
   configurations before adding build-envelope validation.
4. Integrate quote/order handoff and resolve the outstanding payment policies.
5. Complete physical-device and external-form acceptance testing.

Do not recalibrate the weight approximation, change pricing, add resin support,
or publish precise printer limits based only on a brand/model-family name.
