# MakerLab mobile UX implementation plan

Authorized by the October 30 UX review and the instruction to proceed and open a PR.
Use the existing static HTML/CSS/JS stack, in an isolated clone on a feature branch.

- [x] Add browser regressions for desktop/touch/keyboard dropdown state, focus,
  outside dismissal, breakpoint changes, and narrow-screen primary journeys.
- [x] Unify dropdown state in `js/main.js`; keep existing relative links and
  no-JavaScript destinations. Hide collapsed menus from focus and accessibility.
- [x] Compact the homepage and mobile action cards; retain the current Fall hours
  notice, add hero quote/visit actions, and label older projects accurately.
- [x] Put order actions up front, collapse detailed preparation instructions,
  expose standalone form fallbacks, clarify quote handoff limitations, and bring
  visiting/contact information forward. Preserve published pricing and policies.
- [x] Keep body text at 16px on phones and make pricing tables fit narrow screens.
- [x] Test Chromium at 360/390/430px plus desktop, nested pages, and navigation
  without JavaScript. Run the existing Python tests and agent-data validator.
- [x] Review the final diff, document external-form/policy limitations, push the
  feature branch, and prepare the PR. Do not merge or deploy.

Review focus: touch hover versus taps; hidden submenu tab stops; Escape with the
pointer still over a trigger; focus after closing or resizing; 320px and 200%
zoom reflow; external forms unavailable. Do not claim physical-device testing.

Deferred: changing external Podio payment choices or the exactly-$20 rule requires
an approved policy; binary file transfer into Podio requires an integration.
No new interest-form service is introduced; keep the established 2027 email path.

## Added pricing correction and website cross-check

The instructor clarified that the $4 base charge applies once per order.
The calculator now adds it after multiplying material costs by copy count.
Published walk-in/online rates are unchanged: students 10¢/12¢, faculty/staff/
alumni/departments 25¢/30¢, other users 35¢/42¢. The online rates already include
the 20% staff-managed surcharge. A campus-account choice applies the published
faculty/staff rate and $10 minimum, including students paying by CFOAPAL.
The standard-PLA estimate explicitly excludes specialty/dual-color surcharges,
shipping and design work. Those fees are not silently included in the total.

The automated pricing check reads the pricing-page table, checks its six rates,
then exercises the actual OBJ upload and quote UI at both 20% and 100% infill,
1/2/10/99 copies, and all user/order types. A pre-fix two-copy estimate showed
$8.07 where the once-per-order calculation is $4.07.
