# [Dope] Connect the site's schema.org markup into one small graph
**To:** any
**From:** Dope
**Repo:** makerlab
**File:** index.html, lab-hours.html, contact.html, summer.html, summer/*.html, courses/making-things.html, scripts/add_blog_schema.py, docs/development/commands.md
**Kind:** task
**Priority:** normal
**Requested by:** Vishal, 2026-11-13
**Authored and committed by:** [Dope]
**Needs Vishal:** yes

## What
Do the small version of Tony Seale's "Building Your Own Schema.org" idea. Do not build a custom vocabulary. Use standard schema.org terms and give each core thing one stable ID, so every page points at the same lab.

1. Give the lab one ID. In `index.html`, change the Organization block to `"@type": ["EducationalOrganization", "LocalBusiness"]` and add `"@id": "https://makerlab.illinois.edu/#org"`. Add `"@id": "https://makerlab.illinois.edu/#place"` to its location. Give the parent an ID and a sameAs link to the university's own site.

Example for `index.html`:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["EducationalOrganization", "LocalBusiness"],
      "@id": "https://makerlab.illinois.edu/#org",
      "name": "Illinois MakerLab",
      "url": "https://makerlab.illinois.edu/",
      "email": "uimakerlab@illinois.edu",
      "foundingDate": "2012",
      "location": { "@id": "https://makerlab.illinois.edu/#place" },
      "parentOrganization": {
        "@type": "CollegeOrUniversity",
        "@id": "https://illinois.edu/#org",
        "name": "University of Illinois Urbana-Champaign",
        "sameAs": "https://illinois.edu/"
      },
      "sameAs": ["https://www.instagram.com/uimakerlab/", "https://www.facebook.com/uimakerlab/"]
    },
    {
      "@type": "Place",
      "@id": "https://makerlab.illinois.edu/#place",
      "name": "Illinois MakerLab, Business Instructional Facility Room 3030",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "515 E Gregory Dr, Room 3030",
        "addressLocality": "Champaign",
        "addressRegion": "IL",
        "postalCode": "61820",
        "addressCountry": "US"
      },
      "geo": { "@type": "GeoCoordinates", "latitude": 40.0484, "longitude": -88.2424 }
    }
  ]
}
```

2. Point other pages at that ID. In `lab-hours.html` and `contact.html`, keep the hours and contact details but add `"@id": "https://makerlab.illinois.edu/#org"` to the LocalBusiness block. Remove the empty `"telephone": ""` on `lab-hours.html`. Use one address format everywhere.

3. Reuse the ID as organizer, provider and publisher. In `summer.html`, `courses/making-things.html`, and the BlogPosting template in `scripts/add_blog_schema.py`, replace each inline Organization copy with `{ "@id": "https://makerlab.illinois.edu/#org" }`. Replace inline camp locations with `{ "@id": "https://makerlab.illinois.edu/#place" }`.

4. Add one EducationEvent block to each camp page in `summer/`. Give each camp an ID such as `https://makerlab.illinois.edu/summer/minecraft-3d-printing.html#event`, and have `summer.html` link to those IDs instead of repeating the details. Generate these from `data/summer-camps-2026.json` in `scripts/sync_summer_data.py`, so the facts stay in one place. Use real session dates, not one June to July range. Leave out offers on past camps.

5. Add Open Graph and Twitter card tags (`og:title`, `og:description`, `og:url`, `og:image`, `twitter:card`) to the main pages. No page has them today, so shared links show no preview.

6. Check every changed page with the Schema Markup Validator (validator.schema.org) and Google's Rich Results Test. Run `python3 scripts/validate_agent_data.py` before pushing.

Do not add a custom `schema.makerlab...` vocabulary or a JSON-LD context file. Do not add Person markup for students, campers, parents, or guru staff beyond names already public on the page.

## Why
Vishal asked whether the site should act on Tony Seale's article. The article says each team should publish its data in a shared vocabulary, so nobody has to clean it up later. Its real target is internal data inside a large company, not SEO.

The site already ships a lot of schema.org JSON-LD. It has Organization, FAQPage, LocalBusiness, Service, EducationEvent, Course, BlogPosting and BreadcrumbList. These blocks are separate islands. Nothing uses `@id`, so search engines and AI agents see three or four different "Illinois MakerLab" entities with different addresses. Shared IDs turn the islands into one small graph. That is the useful part of the article, at a scale that fits a makerspace.

A custom ontology would add upkeep and no reader. Google and AI agents only understand schema.org terms. The lab has no internal data integration problem to solve.

## Notes
- Effort: about half a day for steps 1 to 3 and 5. Step 4 adds a few hours inside the sync script.
- Risk: the repo is public. Markup must never include camper, parent or registration data. Only use public catalog facts.
- Risk: the site deploys on push to main. Validate before merging.
- Past summer 2026 camps are marked `EventScheduled` with no offers. This is acceptable, but refresh them when 2027 camps are announced.
- `workshops.html` and `free-print-wednesday.html` could get Event markup later if they list dated sessions. I did not check their content.
- This is the first item in this repo's _agent-inbox/, created with Vishal's yes on 2026-11-13.
