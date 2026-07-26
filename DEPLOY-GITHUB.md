# Deploying to GitHub Pages — stumpgrindingmadison.com

This repo is ready to serve as a static site on **GitHub Pages** at your custom domain
**stumpgrindingmadison.com**. The `CNAME` and `.nojekyll` files are already included, and
all canonical tags, the sitemap, Open Graph tags, and schema already point at
`https://stumpgrindingmadison.com`.

Two steps below happen in the GitHub UI and your DNS registrar — they can't be done through
the API, so they're yours to click.

---

## Step 1 — Turn on GitHub Pages

1. Go to the repo: **github.com/brianherbst1208-ai/stump-grinding-madison**
2. **Settings → Pages**
3. Under **Build and deployment → Source**, choose **Deploy from a branch**
4. Set **Branch** to `main` and folder to **/ (root)**, then **Save**

GitHub will build the site. Within a minute or two it will be live at the temporary URL:
`https://brianherbst1208-ai.github.io/stump-grinding-madison/`

## Step 2 — Confirm the custom domain + HTTPS

1. Still in **Settings → Pages**, the **Custom domain** field should already show
   `stumpgrindingmadison.com` (read from the `CNAME` file). If not, type it and **Save**.
2. Add the DNS records in Step 3 so GitHub can verify the domain.
3. Once the DNS check passes, tick **Enforce HTTPS** (GitHub issues a free TLS certificate —
   this can take a few minutes to an hour after DNS resolves).

## Step 3 — Point your domain's DNS at GitHub

At your domain registrar (wherever `stumpgrindingmadison.com` is managed), add these records.

**Apex domain (`stumpgrindingmadison.com`) — four A records:**

| Type | Name / Host | Value |
|------|-------------|-------|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |

**(Optional but recommended) IPv6 — four AAAA records:**

| Type | Name / Host | Value |
|------|-------------|-------|
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |

**`www` subdomain — one CNAME (so www.stumpgrindingmadison.com also works):**

| Type | Name / Host | Value |
|------|-------------|-------|
| CNAME | `www` | `brianherbst1208-ai.github.io.` |

> DNS changes can take anywhere from a few minutes to 24–48 hours to propagate. You can check
> progress with `dig stumpgrindingmadison.com +short` — it should return the four GitHub IPs.

---

## After it's live

- Visit **https://stumpgrindingmadison.com** and click through the pages.
- Validate structured data: https://search.google.com/test/rich-results
- Submit **https://stumpgrindingmadison.com/sitemap.xml** in Google Search Console.
- Still placeholders to replace before advertising (see `README.md §3`): the **phone number
  (608) 555-0147**, the **lead-form backend** (currently demo mode — wire to Formspree/Netlify),
  and the **testimonials / stats / imagery**.

## Updating the site later

Edit content in `build.py` (single source of truth), run `python3 build.py`, and commit the
changed files. GitHub Pages redeploys automatically on every push to `main`.
