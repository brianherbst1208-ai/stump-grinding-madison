# Madison Stump Grinding — Rank-and-Rent Local SEO Website

A complete, deployable multi-page static website targeting stump grinding customers
across Dane County / Greater Madison, Wisconsin. Built as a **rank-and-rent** lead-gen
site: rank it, then rent it to a local operator (or run it as your own).

**17 pages** · clean folder-per-page URLs · LocalBusiness + FAQ + Breadcrumb schema ·
sticky call bar · above-the-fold lead form on every page · trust badges · FAQ accordions.

---

## 1. File structure & URLs

Each page is an `index.html` inside its own folder, so any static host serves it at a
clean, trailing-slash URL — exactly what the SEO plan calls for.

```
/                                         index.html                (Homepage)
/tree-stump-removal-grinding/             ...service page
/root-surface-grinding-land-clearing/     ...service page
/emergency-stump-debris-removal/          ...service page
/stump-grinding-madison-wi/               ...city landing page
/stump-grinding-sun-prairie-wi/           ...city landing page
/stump-grinding-fitchburg-wi/             ...(+ Middleton, Verona, Waunakee,
/stump-grinding-...-wi/                       Stoughton, Oregon, Monona,
                                              DeForest, McFarland)
/about/                                    About Us
/contact/                                  Contact / Free Estimate
/css/style.css      /js/main.js      /images/*.jpg
/sitemap.xml        /robots.txt
```

## 2. How to deploy

> **Hosting on GitHub Pages at stumpgrindingmadison.com?** See **`DEPLOY-GITHUB.md`** for the exact Pages + DNS steps. The `CNAME` and `.nojekyll` files are already included.


The site is 100% static — no build step or server required.

- **Netlify (easiest):** drag the whole `madison-stump-grinding` folder onto
  https://app.netlify.com/drop . Clean URLs work automatically.
- **Vercel:** `vercel deploy` from this folder, or import via the dashboard.
- **Cloudflare Pages / GitHub Pages:** point the project at this folder.
- **Traditional cPanel / any web host:** upload the folder contents to `public_html/`.
  The folder-per-page structure gives you the clean URLs with no `.htaccess` rules needed.

After deploying, point your domain at the host and you're live.

## 3. ⚠️ Placeholders to replace before going live

Everything below is demo data. Search-and-replace across the project (or edit
`build.py` and re-run — see §5).

| Placeholder | Current value | Replace with |
|---|---|---|
| **Phone** | `(608) 555-0147` (display) / `+16085550147` (`tel:`) | Your real tracking number, both formats |
| **Business name** | `Madison Stump Grinding` | Operator's business name (optional) |
| **Email** | `quotes@stumpgrindingmadison.com` (placeholder) | Real inbox |
| **Domain** | `https://stumpgrindingmadison.com` (already configured) | Only change if your domain changes |
| **Street address** | `123 Terrace Ave (placeholder)` in JSON-LD | Real address, or remove for a pure service-area business |
| **Images** | AI-generated stock in `/images/` | Real job photos (keep the same filenames to avoid editing HTML) |
| **Testimonials** | 3 sample quotes on the homepage | Real, permissioned customer reviews (or remove) |
| **Stats** | `15+ years`, `5,000+ stumps` on homepage | Accurate figures |
| **Pricing** | `$3–$5 / inch`, `$150` minimum ranges | Confirm they match the operator's real pricing |

> The footer carries a short disclaimer noting the details are placeholders. Remove it once
> you've swapped in real information.

## 4. Wiring the lead-capture form (currently demo mode)

Every form has `action="#"` and `data-demo="true"`, so on submit `js/main.js` validates the
fields and shows a success message **without sending anything**. To capture real leads:

**Option A — Formspree (works on any host, supports the photo upload):**
1. Create a form at https://formspree.io and copy your endpoint (e.g. `https://formspree.io/f/abc123`).
2. In each page, set the form's `action` to that endpoint and remove `data-demo="true"`.
3. The form already uses `method="post"` and `enctype="multipart/form-data"`, so the
   **Name, Phone, Service Needed, Property Zip, Message, and Photo** fields all submit as-is.
   (File uploads require a paid Formspree plan.)

**Option B — Netlify Forms (if hosting on Netlify):**
Add `netlify` and `name="quote"` attributes to each `<form>`, remove `data-demo`, and
Netlify captures submissions automatically (file uploads supported).

Tip: fastest path is to edit the `lead_form()` function in `build.py` once, then re-run the
build so all 17 pages update together.

## 5. Editing content & regenerating

All copy, meta tags, FAQs, and schema live in **`build.py`** (single source of truth).

```bash
python3 build.py     # regenerates all 17 pages + sitemap.xml + robots.txt
```

- City copy: the `CITIES` list. Each entry has `meta_title`, `meta_desc`, `lead`, `body`,
  and `faqs`. Every city page is 300–600 words of unique, locally tailored copy.
- Service copy: the `SERVICE_PAGES` dict.
- Global styling: `css/style.css`. Interactions (mobile nav, accordion, form): `js/main.js`.

## 6. SEO checklist after launch

- [ ] Replace all placeholders (§3) and wire the form (§4).
- [ ] Submit `sitemap.xml` in **Google Search Console** and **Bing Webmaster Tools**.
- [ ] Create/claim a **Google Business Profile** with matching NAP (name, address, phone).
- [ ] Confirm NAP is identical everywhere (site, GBP, citations) — consistency drives local rank.
- [ ] Validate structured data at https://search.google.com/test/rich-results
      (LocalBusiness on every page; FAQ + Breadcrumb on city/service pages).
- [ ] Add Google Analytics / a call-tracking number if desired.

## 7. What's included per page

- **On-page SEO:** unique `<title>` (<60 chars) + meta description (<155 chars), canonical,
  Open Graph/Twitter tags, semantic H1/H2/H3, geo meta.
- **Schema (JSON-LD):** `LocalBusiness` with an `areaServed` array of all 11 communities on
  every page; `BreadcrumbList` on interior pages; `FAQPage` on city & service pages; `Service`
  schema on service pages.
- **Conversion:** sticky top call bar, above-the-fold lead form, four trust badges
  (Fully Insured · Free On-Site Estimates · Commercial & Residential · Same-Day Response),
  FAQ accordions, CTA bands, and a floating mobile "Call Now" button.
- **Accessible & responsive:** keyboard-friendly accordion, mobile nav, reduced-motion support.

---

*Generated as a demonstration rank-and-rent build. Replace demo data with the operating
provider's real information before advertising or accepting live leads.*
