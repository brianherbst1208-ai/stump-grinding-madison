#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Madison Stump Grinding — static site generator.
Generates 17 pages + sitemap into folder-per-page clean-URL structure.
Run:  python3 build.py
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

SITE = {
    "name": "Madison Stump Grinding",
    "phone_display": "(608) 493-0540",
    "phone_tel": "+16084930540",
    "email": "brian@briansconsulting.com",
    "domain": "https://stumpgrindingmadison.com",
    "region": "WI",
    "hq_city": "Madison",
    "geo": {"lat": 43.0731, "lng": -89.4012},
}

# ------------------------------------------------------------------ icons
IC = {
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
    "clipboard": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/></svg>',
    "building": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18"/><path d="M5 21V7l7-4 7 4v14"/><path d="M9 9h.01M9 13h.01M9 17h.01M15 9h.01M15 13h.01M15 17h.01"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "stump": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20h16"/><path d="M7 20c0-3 1-5 5-5s5 2 5 5"/><ellipse cx="12" cy="15" rx="5" ry="2"/><path d="M12 15v-4M9.5 12.5 8 11M14.5 12.5 16 11"/></svg>',
    "roots": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v8"/><path d="M12 10c0 4-4 4-4 8M12 10c0 4 4 4 4 8M12 10v10"/><path d="M8 18v3M16 18v3M12 20v1"/></svg>',
    "alert": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><path d="M12 9v4M12 17h.01"/></svg>',
    "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 4 13c0-6 8-11 16-11 0 8-5 16-11 16z"/><path d="M4 20c3-3 6-5 9-6"/></svg>',
    "truck": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 17V6H3v11h1M14 17h-4M20 17h1v-5l-3-4h-4v9h1"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/></svg>',
    "map": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 6-9 12-9 12s-9-6-9-12a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
    "dollar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
}

# ------------------------------------------------------------------ nav / areas
SERVICES = [
    {"slug": "tree-stump-removal-grinding", "nav": "Tree Stump Removal & Grinding", "short": "Stump Removal & Grinding"},
    {"slug": "root-surface-grinding-land-clearing", "nav": "Root Surface Grinding & Land Clearing", "short": "Root Grinding & Land Clearing"},
    {"slug": "emergency-stump-debris-removal", "nav": "Emergency Stump & Debris Removal", "short": "Emergency Removal"},
]

CITY_ORDER = ["madison","sun-prairie","fitchburg","middleton","verona","waunakee",
              "stoughton","oregon","monona","deforest","mcfarland"]

def city_url(slug): return f"/stump-grinding-{slug}-wi/"
def svc_url(slug): return f"/{slug}/"

# ================================================================== components
def head(title, desc, canonical, schemas, hero_img=None, inline=False):
    css = '<link rel="stylesheet" href="/css/style.css">'
    fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">')
    if inline:
        with open(os.path.join(ROOT, "css", "style.css")) as f:
            css = "<style>\n" + f.read() + "\n</style>"
    schema_tags = "\n".join(
        '<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False) + '</script>'
        for s in schemas
    )
    favicon = ('<link rel="icon" href="data:image/svg+xml,'
               '%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E'
               '%3Crect width=%2732%27 height=%2732%27 rx=%277%27 fill=%27%231b4332%27/%3E'
               '%3Ctext x=%2716%27 y=%2722%27 font-size=%2718%27 text-anchor=%27middle%27 fill=%27%23ff922b%27 font-family=%27Arial%27 font-weight=%27bold%27%3ES%3C/text%3E%3C/svg%3E">')
    og_img = SITE["domain"] + "/og-image.jpg"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow">
<meta name="geo.region" content="US-WI">
<meta name="geo.placename" content="Madison, Wisconsin">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:site_name" content="{SITE['name']}">
<meta name="twitter:card" content="summary_large_image">
{favicon}
{fonts}
{css}
{schema_tags}
</head>
<body>"""

def callbar():
    return f"""
<div class="callbar">
  <div class="callbar__inner">
    <div class="callbar__msg">
      <span class="dot" aria-hidden="true"></span>
      <span class="callbar__msg-text">Serving Dane County &amp; Greater Madison &middot; Same-Day Response Available</span>
      <span class="callbar__msg-text-short">Same-Day Response Available</span>
    </div>
    <a class="callbar__phone" href="tel:{SITE['phone_tel']}">{IC['phone']} Call for a Free Quote: {SITE['phone_display']}</a>
  </div>
</div>"""

def header():
    svc_items = "".join(f'<a href="{svc_url(s["slug"])}">{s["nav"]}</a>' for s in SERVICES)
    area_items = "".join(f'<a href="{city_url(c["slug"])}">{c["name"]}</a>' for c in CITIES)
    return f"""
<header class="site-header">
  <nav class="nav" aria-label="Primary">
    <a class="brand" href="/" aria-label="{SITE['name']} home">
      <span class="brand__mark" aria-hidden="true">{IC['stump']}</span>
      <span class="brand__name">Madison Stump Grinding<span>Dane County, WI</span></span>
    </a>
    <button class="nav__toggle" aria-label="Toggle menu" aria-expanded="false" aria-controls="menu">&#9776;</button>
    <ul class="nav__links" id="menu">
      <li><a href="/">Home</a></li>
      <li class="has-drop"><a href="{svc_url(SERVICES[0]['slug'])}">Services</a>
        <div class="drop">{svc_items}</div></li>
      <li class="has-drop"><a href="{city_url('madison')}">Service Areas</a>
        <div class="drop drop--cols">{area_items}</div></li>
      <li><a href="/about/">About</a></li>
      <li><a href="/contact/">Contact</a></li>
      <li class="nav__cta"><a class="btn btn--primary" href="/contact/">Free Quote</a></li>
    </ul>
  </nav>
</header>"""

def lead_form(fid="lead", heading="Get Your Free On-Site Estimate", sub="No-obligation quote — most requests answered same day.", compact=False):
    svc_opts = "".join(f'<option value="{o}">{o}</option>' for o in [
        "Tree Stump Removal & Grinding","Root Surface Grinding","Land Clearing",
        "Emergency / Storm Debris Removal","Multiple Stumps","Commercial Project","Other / Not Sure"])
    return f"""
<form class="leadform" id="{fid}" action="#" method="post" enctype="multipart/form-data" data-lead data-demo="true" novalidate>
  <h3>{heading}</h3>
  <p class="leadform__sub">{sub}</p>
  <div class="field">
    <label for="{fid}-name">Full Name</label>
    <input id="{fid}-name" name="name" type="text" autocomplete="name" placeholder="Jane Doe" required>
    <span class="form-error">Please enter your name.</span>
  </div>
  <div class="field--row">
    <div class="field">
      <label for="{fid}-phone">Phone Number</label>
      <input id="{fid}-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="(608) 555-0123" required>
      <span class="form-error">Enter a valid phone number.</span>
    </div>
    <div class="field">
      <label for="{fid}-zip">Property Zip Code</label>
      <input id="{fid}-zip" name="zip" type="text" inputmode="numeric" pattern="[0-9]{{5}}" maxlength="5" placeholder="53703" required>
      <span class="form-error">Enter your 5-digit zip.</span>
    </div>
  </div>
  <div class="field">
    <label for="{fid}-service">Service Needed</label>
    <select id="{fid}-service" name="service" required>
      <option value="">Select a service…</option>
      {svc_opts}
    </select>
    <span class="form-error">Please choose a service.</span>
  </div>
  <div class="field">
    <label for="{fid}-msg">Tell Us About the Job</label>
    <textarea id="{fid}-msg" name="message" placeholder="How many stumps, approximate size, access notes…"></textarea>
  </div>
  <div class="field">
    <label for="{fid}-photo">Add a Photo (optional)</label>
    <div class="field-file"><input id="{fid}-photo" name="photo" type="file" accept="image/*"></div>
  </div>
  <input type="hidden" name="source_page" value="">
  <button class="btn btn--primary btn--block btn--lg" type="submit">Get My Free Quote →</button>
  <p class="form-note">Or call {SITE['phone_display']} — we answer 7 days a week.</p>
  <div class="form-success" role="status">✅ Thanks! Your request is in. We'll call you shortly to confirm your free on-site estimate.</div>
</form>"""

def trustbar():
    items = [
        ("shield","Fully Insured","Licensed &amp; covered"),
        ("clipboard","Free On-Site Estimates","No obligation"),
        ("building","Commercial &amp; Residential","Any property"),
        ("clock","Same-Day Response","7 days a week"),
    ]
    b = "".join(f"""
      <div class="badge"><span class="badge__ico">{IC[i]}</span>
      <span class="badge__txt"><strong>{t}</strong><span>{s}</span></span></div>""" for i,t,s in items)
    return f'<section class="trustbar" aria-label="Why homeowners trust us"><div class="trustbar__grid">{b}</div></section>'

def hero(loc_line, h1, lead_txt, checks=None, hero_img="/hero-home.jpg", fid="hero-lead", crumbs_html=""):
    style = f' style="--hero-img:url({hero_img})"' if hero_img else ""
    checks_html = ""
    if checks:
        checks_html = '<ul class="hero__checks">' + "".join(f"<li>{c}</li>" for c in checks) + "</ul>"
    return f"""
<section class="hero"{style}>
  <div class="hero__inner">
    <div class="hero__copy">
      {crumbs_html}
      <p class="hero__loc">{loc_line}</p>
      <h1>{h1}</h1>
      <p class="lead">{lead_txt}</p>
      {checks_html}
    </div>
    <div class="hero__form-wrap">
      {lead_form(fid=fid)}
    </div>
  </div>
</section>"""

def cta_band(h="Ready to Reclaim Your Yard?", p="Get a fast, free on-site estimate from Dane County's stump grinding specialists. No pressure, no hidden fees — just a clear price and a clean finish."):
    return f"""
<section class="section ctaband">
  <div class="container">
    <h2>{h}</h2>
    <p>{p}</p>
    <a class="btn btn--ghost-light btn--lg" href="/contact/">Request My Free Quote</a>
    <div><a class="ctaband__phone" href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a></div>
  </div>
</section>"""

def area_chips(exclude=None, heading="Proudly Serving Dane County Communities"):
    links = "".join(f'<li><a href="{city_url(c["slug"])}">{c["name"]}</a></li>'
                    for c in CITIES if c["slug"] != exclude)
    return f"""
<section class="section section--tight section--sand">
  <div class="container center">
    <p class="eyebrow">Local Coverage</p>
    <h2>{heading}</h2>
    <p class="lead">Fast, insured stump grinding across the Greater Madison area. Don't see your town? Give us a call — if you're in Dane County, we'll be there.</p>
    <ul class="chips">{links}</ul>
  </div>
</section>"""

def faq_block(faqs, heading="Frequently Asked Questions"):
    items = ""
    for q, a in faqs:
        items += f"""
    <div class="faq__item">
      <button class="faq__q" type="button">{q}</button>
      <div class="faq__a"><div class="faq__a-inner">{a}</div></div>
    </div>"""
    return f"""
<section class="section">
  <div class="container">
    <div class="center"><p class="eyebrow">Good to Know</p><h2>{heading}</h2></div>
    <div class="faq">{items}</div>
  </div>
</section>"""

def floatcall():
    return f'<a class="floatcall" href="tel:{SITE["phone_tel"]}">{IC["phone"]} Call Now</a>'

def footer():
    svc = "".join(f'<li><a href="{svc_url(s["slug"])}">{s["short"]}</a></li>' for s in SERVICES)
    half = (len(CITIES)+1)//2
    col_a = "".join(f'<li><a href="{city_url(c["slug"])}">{c["name"]}, WI</a></li>' for c in CITIES[:half])
    col_b = "".join(f'<li><a href="{city_url(c["slug"])}">{c["name"]}, WI</a></li>' for c in CITIES[half:])
    return f"""
<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div>
        <div class="brand">
          <span class="brand__mark" aria-hidden="true">{IC['stump']}</span>
          <span class="brand__name" style="color:#fff">Madison Stump Grinding<span>Dane County, WI</span></span>
        </div>
        <p class="footer__brandtext">Locally operated stump grinding and land clearing serving Madison and the surrounding Dane County communities. Fully insured. Free on-site estimates.</p>
        <ul class="footer__contact" style="list-style:none;padding:0;margin:14px 0 0">
          <li>{IC['phone']} <a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a></li>
          <li>{IC['mail']} <a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
          <li>{IC['clock']} <span>Mon–Sun, 7:00am – 7:00pm</span></li>
        </ul>
      </div>
      <div>
        <h4>Services</h4>
        <ul>{svc}<li><a href="/contact/">Free Estimate</a></li></ul>
      </div>
      <div>
        <h4>Service Areas</h4>
        <ul>{col_a}</ul>
      </div>
      <div>
        <h4>More Areas</h4>
        <ul>{col_b}</ul>
        <a class="btn btn--primary" href="/contact/" style="margin-top:10px">Get a Free Quote</a>
      </div>
    </div>
  </div>
  <div class="container">
    <div class="footer__bottom">
      <span>&copy; <span id="year">2026</span> {SITE['name']}. All rights reserved.</span>
      <span><a href="/about/">About</a> &middot; <a href="/contact/">Contact</a> &middot; <a href="/sitemap.xml">Sitemap</a></span>
    </div>
  </div>
  <p class="footer__disclaimer">Madison Stump Grinding is a local lead service. Phone number, business details, imagery, and testimonials shown are placeholders for demonstration and should be replaced with the operating provider's real information. Pricing figures are typical ballpark ranges only; every quote is confirmed with a free on-site estimate.</p>
</footer>"""

# ------------------------------------------------------------------ schema
def local_business_schema(page_url, name_suffix=None):
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": SITE["domain"] + "/#business",
        "name": SITE["name"],
        "image": SITE["domain"] + "/og-image.jpg",
        "url": page_url,
        "telephone": SITE["phone_tel"],
        "email": SITE["email"],
        "priceRange": "$$",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "123 Terrace Ave (placeholder)",
            "addressLocality": "Madison",
            "addressRegion": "WI",
            "postalCode": "53703",
            "addressCountry": "US"
        },
        "geo": {"@type": "GeoCoordinates", "latitude": SITE["geo"]["lat"], "longitude": SITE["geo"]["lng"]},
        "areaServed": [{"@type": "City", "name": f'{c["name"]}, WI'} for c in CITIES] +
                      [{"@type": "AdministrativeArea", "name": "Dane County, WI"}],
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
            "opens": "07:00", "closes": "19:00"
        }],
        "makesOffer": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["nav"]}} for s in SERVICES
        ],
    }

def breadcrumb_schema(trail):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": n, "item": SITE["domain"] + u}
            for i, (n, u) in enumerate(trail)
        ],
    }

def faq_schema(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}}
            for q, a in faqs
        ],
    }

# ================================================================== PAGE CONTENT
# ---- CITIES (bespoke copy) ----
CITIES = [
 {
  "slug":"madison","name":"Madison","zips":"53703, 53704, 53705, 53711, 53713, 53714, 53716, 53717, 53718, 53719",
  "hoods":["Near West Side","Tenney-Lapham","Marquette / Willy Street","Nakoma","Westmorland","Maple Bluff","Shorewood Hills","Schenk-Atwood","Vilas","Monroe Street"],
  "meta_title":"Stump Grinding Madison WI | Free On-Site Quotes",
  "meta_desc":"Fully insured stump grinding in Madison, WI. Clay-ready equipment, tight backyard access & same-day response. Call (608) 493-0540 for a free quote.",
  "lead":"From the isthmus to the far west side, we grind stumps clean, haul the mess, and leave your Madison yard ready to replant.",
  "body":"""
<p>Madison's tree canopy is one of the city's signatures — the burr oaks along the UW Arboretum, the elms shading Monroe Street, the towering silver maples over near-west-side bungalows. When one of those trees finally comes down, the stump left behind on a tight isthmus lot can be stubborn and unsightly. <strong>Madison Stump Grinding</strong> removes it cleanly, whether you're on a narrow terrace lot in Tenney-Lapham or a deep, mature parcel in Nakoma or Maple Bluff.</p>

<h2>Grinding Built for Madison Clay and Oak-Wilt Pressure</h2>
<p>Most Madison homes sit on heavy lake-plain clay left behind by glacial Lake Yahara, and that dense soil packs tight around old root systems. Our grinders are geared for it. Oak wilt also moves aggressively through Dane County's red oaks, and emerald ash borer has taken thousands of ash trees across the city — so we grind the resulting stumps well below grade and can haul the grindings offsite so nothing lingers to attract pests or fungus.</p>

<h2>How Much Does Stump Grinding Cost in Madison?</h2>
<p>Residential stump grinding in Madison is usually priced by the stump's diameter measured at ground level — typically <strong>$3 to $5 per inch</strong>, with a job minimum around $150. A single average stump often lands between $150 and $350, and we discount every additional stump ground on the same visit. Because access, root flare, and grindings haul-away all affect the number, we confirm every price with a free on-site estimate before we start.</p>

<h2>Compact Equipment for Tight Isthmus Lots</h2>
<p>Plenty of Madison backyards — especially in Marquette, Vilas, and the Wil-Mar district — are reachable only through a standard 36-inch gate. Our track-mounted grinders fit through those openings and roll across your lawn on rubber tracks that minimize turf damage. For larger commercial sites near the Beltline or campus, we bring higher-horsepower machines that clear big-diameter stumps and root systems quickly.</p>

<p>We serve every Madison neighborhood, from Shorewood Hills and Westmorland to Schenk-Atwood and the far east side near I-90. Ready for a clean, level yard again? Call {phone} or request your free quote today.</p>
""",
  "faqs":[
   ("How much does stump grinding cost in Madison?","Most single stumps in Madison run between $150 and $350, priced at roughly $3–$5 per inch of ground-level diameter with a job minimum near $150. Multiple stumps ground on the same visit are discounted. Every quote is confirmed with a free on-site estimate."),
   ("How deep do you grind the stump?","Our standard is 4–6 inches below grade, which is enough for sod, seed, or a new garden bed. If you plan to replant a tree in the same spot, we can grind 8–12 inches deeper on request."),
   ("Do you handle oak wilt and emerald ash borer stumps?","Yes. We grind diseased oak and ash stumps below grade and can haul the grindings offsite so infected material isn't left to spread. Oak wilt is active across Dane County, so timely removal matters."),
   ("Do you clean up the wood chips afterward?","We always rake the site back level. You can keep the nutrient-rich grindings as mulch, or we can haul them away and backfill with clean topsoil for a small additional charge."),
  ],
 },
 {
  "slug":"sun-prairie","name":"Sun Prairie","zips":"53590",
  "hoods":["Cannery Row","Smith's Crossing","Village Green","O'Keeffe area","Downtown / Cannery Square"],
  "meta_title":"Stump Grinding Sun Prairie WI | Fast Free Quotes",
  "meta_desc":"Insured stump grinding in Sun Prairie, WI. New-subdivision lot clearing, sod-safe equipment & same-day response. Call (608) 493-0540 for a free estimate.",
  "lead":"Sun Prairie is growing fast — and we help homeowners and builders clear the stumps and hedgerows left behind.",
  "body":"""
<p>Few Dane County towns have grown like Sun Prairie. New subdivisions keep rising on what were farm fields a decade ago, and with that growth comes a steady mix of leftover fence-line trees, cleared hedgerows, and aging silver maples in established neighborhoods near Cannery Square. <strong>Madison Stump Grinding</strong> keeps Sun Prairie yards clean and buildable, from Smith's Crossing to the streets around Angell Park.</p>

<h2>Clearing Stumps on Sun Prairie's Newer Lots</h2>
<p>A lot of local grinding jobs sit on former agricultural ground — glacial till and clay loam that can hide wide, shallow root systems along old field edges. When a builder or homeowner needs a lot finished for landscaping, we grind those stumps low and clear the root flare so new sod and irrigation can go in without a hump or hollow left behind.</p>

<h2>How Much Does Stump Grinding Cost in Sun Prairie?</h2>
<p>Expect the same fair, diameter-based pricing we use across Dane County: roughly <strong>$3 to $5 per inch</strong> measured at ground level, with a minimum of about $150 and a discount on every extra stump. Builders clearing several lots or a full hedgerow get volume pricing. We give you a firm number after a quick, free on-site look.</p>

<h2>Protecting New Sod, Sprinklers, and Hardscape</h2>
<p>Newer Sun Prairie homes often have fresh sod and in-ground irrigation, so careful work matters. We locate heads and lines before we grind, use track machines that spread their weight across your lawn, and rake the area smooth when we finish. The result is a level, plantable spot — not a torn-up yard.</p>

<p>Whether it's a single backyard stump near Sheehan Park or a builder's punch list of lots, call {phone} or request your free Sun Prairie quote online.</p>
""",
  "faqs":[
   ("How much does stump grinding cost in Sun Prairie?","Single stumps typically run $150–$350, based on about $3–$5 per inch of diameter with a $150 minimum. Builders or homeowners clearing multiple stumps or a hedgerow receive volume pricing confirmed during a free on-site estimate."),
   ("How deep do you grind the stump?","We grind 4–6 inches below grade as standard so you can lay sod or seed right away, and deeper if you're replanting or installing hardscape over the spot."),
   ("Can you clear stumps on a new-construction lot?","Absolutely. We regularly finish builder lots and cleared hedgerows in Sun Prairie's newer subdivisions, grinding low enough for grading, sod, and irrigation."),
   ("Will grinding damage my new sprinkler system?","We ask you to mark heads and lines, or we help locate them, and we work around them carefully. Our track grinders spread weight to protect fresh sod."),
  ],
 },
 {
  "slug":"fitchburg","name":"Fitchburg","zips":"53711, 53713, 53719, 53575",
  "hoods":["Jamestown","Belmar","Swan Creek","Nine Springs","Seminole Forest","Fitchburg Center"],
  "meta_title":"Stump Grinding Fitchburg WI | Free On-Site Quote",
  "meta_desc":"Insured stump grinding in Fitchburg, WI. Wet-clay ready gear near Nine Springs, residential & commercial, same-day response. Call (608) 493-0540.",
  "lead":"From Jamestown backyards to commercial sites off Seminole Highway, we grind Fitchburg's stumps down and out.",
  "body":"""
<p>Fitchburg blends established neighborhoods, newer subdivisions, and working commercial corridors — and each brings its own kind of stump. Around Jamestown and Swan Creek you'll find mature yard trees; near the Nine Springs E-Way and the wetlands south of the Beltline, the ground stays wet and the clay runs deep. <strong>Madison Stump Grinding</strong> handles all of it across Fitchburg.</p>

<h2>Grinding in Fitchburg's Wet Clay</h2>
<p>Much of Fitchburg sits on low, moisture-holding clay, especially near Nine Springs and the marshy margins toward Lake Waubesa. Saturated ground can bog down light equipment, so we bring track-mounted grinders that stay stable on soft soil and grind cleanly without churning your lawn into ruts. That matters when you want the spot plantable, not a mud pit.</p>

<h2>How Much Does Stump Grinding Cost in Fitchburg?</h2>
<p>Our Fitchburg pricing follows the same transparent formula: about <strong>$3 to $5 per inch</strong> of stump diameter, a job minimum near $150, and a discount for each additional stump. Larger commercial removals off Fitchrona Road or Seminole Highway are quoted per site. You'll always get the number before we begin — free, on site, no pressure.</p>

<h2>Residential and Commercial — One Local Crew</h2>
<p>We're equally at home in a Belmar backyard and on a Fitchburg Center commercial lot. For homeowners we focus on tidy, low grinding and a raked-level finish; for property managers and builders we clear stumps and surface roots on schedule so paving, landscaping, or resale can move forward without delay.</p>

<p>Need a stump gone in Fitchburg? Call {phone} or send us a photo through the quick quote form for a fast estimate.</p>
""",
  "faqs":[
   ("How much does stump grinding cost in Fitchburg?","Most residential stumps run $150–$350, based on roughly $3–$5 per inch with a $150 minimum. Commercial sites are quoted per project. Every price is set with a free on-site estimate."),
   ("Can you grind stumps in wet or low-lying yards?","Yes. Fitchburg's clay and the wet ground near Nine Springs are no problem for our track-mounted grinders, which stay stable on soft soil and avoid tearing up the lawn."),
   ("How deep do you grind?","Standard depth is 4–6 inches below grade for sod or seed; we go deeper for replanting or where hardscape will sit over the old stump."),
   ("Do you do commercial stump and root grinding?","We do. We handle Fitchburg Center properties, retail lots, and builder sites, clearing stumps and surface roots on a schedule that fits your project."),
  ],
 },
 {
  "slug":"middleton","name":"Middleton","zips":"53562",
  "hoods":["Middleton Hills","Bishops Bay","Tiedeman's Pond","Pheasant Branch","Downtown Middleton"],
  "meta_title":"Stump Grinding Middleton WI | Free Estimates",
  "meta_desc":"Fully insured stump grinding in Middleton, WI, the Good Neighbor City. Mature-tree lots, lawn-safe equipment, same-day quotes. Call (608) 493-0540.",
  "lead":"In the Good Neighbor City, we treat your lawn like our own — clean grinding, careful cleanup, fair prices.",
  "body":"""
<p>Middleton earned its "Good Neighbor City" nickname, and its tree-lined streets show it. Established neighborhoods near Pheasant Branch Conservancy and along the drumlin ridges toward Bishops Bay are full of mature oaks, ashes, and silver maples — beautiful, until one has to come down and leaves a wide stump behind. <strong>Madison Stump Grinding</strong> removes those stumps neatly and respects the polished yards Middleton is known for.</p>

<h2>Big Trees, Established Lawns</h2>
<p>Middleton's older lots often feature large-diameter stumps with sprawling root flares, sometimes close to patios, walks, or garden beds. We grind the whole stump plus the surface roots that heave sidewalks and mower decks, working carefully around hardscape near homes in Middleton Hills and the streets off University Avenue.</p>

<h2>How Much Does Stump Grinding Cost in Middleton?</h2>
<p>Pricing is straightforward: roughly <strong>$3 to $5 per inch</strong> of ground-level diameter, a minimum around $150, and a discount on each added stump. Bigger legacy trees cost more simply because there's more wood to grind. We'll walk the yard with you and give a firm, free quote before any work starts.</p>

<h2>A Clean, Lawn-Safe Finish</h2>
<p>Because Middleton homeowners take pride in their landscaping, we use rubber-tracked machines that limit turf marks, lay down protection over sensitive paths when needed, and rake the site level when we're done. You can reseed, sod, or plant the same week.</p>

<p>We also coordinate easily with the tree services and landscapers many Middleton homeowners already use. After a takedown near Pheasant Branch or in the neighborhoods off University Avenue, we arrive to grind the stump and surface roots so the finished project looks seamless — no torn-up lawn, no lingering hump. One call, and the last reminder of that old tree is gone for good.</p>

<p>From Tiedeman's Pond to Bishops Bay, call {phone} or request your free Middleton estimate and get your yard back.</p>
""",
  "faqs":[
   ("How much does stump grinding cost in Middleton?","Single stumps generally run $150–$350 at about $3–$5 per inch, with a $150 minimum and discounts for additional stumps. Large legacy trees cost more; we confirm with a free on-site quote."),
   ("Can you grind large stumps near patios and sidewalks?","Yes. Many Middleton lots have big stumps close to hardscape. We grind the stump and the surface roots that lift walks, working carefully to protect nearby patios and beds."),
   ("How deep do you grind the stump?","Typically 4–6 inches below grade for lawn restoration, or deeper on request if you're replanting or building over the area."),
   ("Will your equipment tear up my lawn?","We use rubber-tracked grinders that spread weight to minimize turf damage, add ground protection where needed, and rake the site level before we leave."),
  ],
 },
 {
  "slug":"verona","name":"Verona","zips":"53593",
  "hoods":["Scenic Ridge","Cathedral Point","Sugar Creek","Hometown Junction","Badger Prairie area"],
  "meta_title":"Stump Grinding Verona WI | Free Quotes, Insured",
  "meta_desc":"Insured stump grinding in Verona, WI, Hometown of Epic. Rolling-terrain & acreage clearing, same-day response. Call (608) 493-0540 for a free quote.",
  "lead":"On Verona's rolling Driftless-edge lots and larger acreages, we grind stumps and clear ground with the right-sized machine.",
  "body":"""
<p>Verona sits on the eastern edge of Wisconsin's Driftless Area, where the land starts to roll and the soil turns rockier than the flat clay of the Madison basin. As the "Hometown of Epic" has grown, so have its subdivisions near Scenic Ridge and its larger rural lots out toward Badger Prairie and the Ice Age Trail. <strong>Madison Stump Grinding</strong> serves all of it, from a single backyard stump to acreage clearing.</p>

<h2>Grinding on Rolling, Rocky Ground</h2>
<p>Verona's terrain can put stumps on slopes and in rockier soil, which is hard on undersized equipment. We match the machine to the job — nimble track grinders for sloped backyards, higher-horsepower units for big stumps and stony ground — so the stump comes out fully instead of being skimmed off the top.</p>

<h2>How Much Does Stump Grinding Cost in Verona?</h2>
<p>Standard Dane County pricing applies: about <strong>$3 to $5 per inch</strong> of diameter, a minimum near $150, and per-stump discounts. Rural properties clearing multiple stumps, windbreaks, or brush get a per-project quote. Every estimate is free and given on site so there are no surprises.</p>

<h2>From Backyards to Acreage Clearing</h2>
<p>Plenty of Verona homeowners have room to spread out, and that often means more than one stump. We handle fence-line trees, old orchard stumps, and lot clearing for new builds along with everyday backyard removals — grinding low and hauling debris so the ground is ready for pasture, lawn, or construction.</p>

<p>As Epic's workforce has fueled Verona's growth, we've become a familiar sight in its newer neighborhoods — grinding builder-left stumps, clearing the occasional boulder-bound root system, and prepping yards for landscaping. Whether you commute to the campus or work the ridge land outside town, you get the same fair price and the same clean finish.</p>

<p>Serving Verona and the surrounding countryside — call {phone} or request your free quote today.</p>
""",
  "faqs":[
   ("How much does stump grinding cost in Verona?","Single stumps typically run $150–$350 at roughly $3–$5 per inch with a $150 minimum. Acreage clearing and multiple stumps are quoted per project during a free on-site estimate."),
   ("Can you grind stumps on a slope or rocky ground?","Yes. Verona's rolling, rockier terrain is why we size the machine to the job — track grinders for slopes and heavy-duty units for big or stony stumps."),
   ("Do you clear larger rural properties and windbreaks?","We do. We handle fence lines, old orchards, and lot clearing on Verona-area acreage, grinding low and hauling the debris."),
   ("How deep do you grind the stump?","Usually 4–6 inches below grade for lawn or pasture, and deeper where you plan to replant or build."),
  ],
 },
 {
  "slug":"waunakee","name":"Waunakee","zips":"53597",
  "hoods":["Village Center","Ripp Park area","Kilkenny Farms","Westbridge","Six Mile Creek"],
  "meta_title":"Stump Grinding Waunakee WI | Free On-Site Quote",
  "meta_desc":"Insured stump grinding in Waunakee, WI. Farmland-to-subdivision clearing, wetland-edge care, same-day response. Call (608) 493-0540 for a free quote.",
  "lead":"There's only one Waunakee in the world — and one local crew that grinds its stumps clean and hauls the mess.",
  "body":"""
<p>Waunakee likes to say it's the "only Waunakee in the world," and its steady growth north of Lake Mendota has turned a lot of former cropland into new neighborhoods around Kilkenny Farms and Westbridge. That transition leaves behind fence-line trees and hedgerow stumps, while older streets near the Village Center have their own mature shade trees. <strong>Madison Stump Grinding</strong> handles both.</p>

<h2>From Farm Fields to Finished Yards</h2>
<p>The rich prairie loam over clay that made Waunakee good farmland also grows big, deep-rooted trees along old field edges. When those come out for a new subdivision or a bigger backyard, we grind the stumps low and clear the surface roots so graders, sod, and landscaping can follow without a bump left in the lawn.</p>

<h2>How Much Does Stump Grinding Cost in Waunakee?</h2>
<p>Waunakee jobs follow our standard rate: roughly <strong>$3 to $5 per inch</strong> of stump diameter, a minimum around $150, and a discount for every extra stump on the same visit. Hedgerow and multi-stump clearing is quoted per project. We confirm the price with a free on-site estimate before we start.</p>

<h2>Careful Work Near Wetlands and Creeks</h2>
<p>Parts of Waunakee sit close to Six Mile Creek and low wetland margins where the ground stays soft. Our track-mounted grinders keep their footing on that softer soil and grind cleanly without rutting the yard — so even a low-lying lot ends up level and plantable.</p>

<p>Waunakee's tight-knit, small-town feel is a big part of why we enjoy working here, and we treat every yard like a neighbor's. From a single stump behind a Village Center home to a builder's row of lots on the edge of town, we show up when we say we will, quote honestly, and leave the ground clean and level.</p>

<p>Whether you're near Ripp Park or out toward the creek, call {phone} or request your free Waunakee quote online.</p>
""",
  "faqs":[
   ("How much does stump grinding cost in Waunakee?","Most single stumps run $150–$350 at about $3–$5 per inch with a $150 minimum. Hedgerow and multi-stump clearing is quoted per project during a free on-site estimate."),
   ("Can you clear hedgerows and old fence-line trees?","Yes. As Waunakee's former farmland becomes new neighborhoods, we regularly grind hedgerow and fence-line stumps low enough for grading and sod."),
   ("How deep do you grind the stump?","Standard is 4–6 inches below grade for lawn; we grind deeper for replanting or where hardscape will go over the spot."),
   ("Can you work on soft ground near Six Mile Creek?","We can. Our track grinders stay stable on the soft, low soil near creeks and wetlands and grind without rutting the yard."),
  ],
 },
 {
  "slug":"stoughton","name":"Stoughton","zips":"53589",
  "hoods":["Historic Downtown","Mandt Park","Kettle Park","Riverside","Nordic Ridge"],
  "meta_title":"Stump Grinding Stoughton WI | Free Estimates",
  "meta_desc":"Insured stump grinding in Stoughton, WI. Legacy riverfront trees, tight older-lot access, same-day response. Call (608) 493-0540 for a free quote.",
  "lead":"Along the Yahara in historic Stoughton, we remove the big legacy stumps other crews won't touch.",
  "body":"""
<p>Stoughton wears its history proudly — Norwegian heritage, the Syttende Mai festival, and a walkable downtown of restored tobacco warehouses along the Yahara River. Those older, established lots also hold some of Dane County's largest legacy trees, and when a century-old maple or oak finally comes down, the stump can be enormous. <strong>Madison Stump Grinding</strong> has the equipment to finish the job.</p>

<h2>Big Legacy Stumps Along the Yahara</h2>
<p>Riverside neighborhoods near Mandt Park and the historic district are full of mature trees on rich, silty river-bottom soil. Their stumps are often wide and deeply rooted. We bring high-horsepower grinders that chew through big-diameter hardwood stumps and the sprawling surface roots that come with them — no half-measures.</p>

<h2>How Much Does Stump Grinding Cost in Stoughton?</h2>
<p>Pricing stays simple and honest: about <strong>$3 to $5 per inch</strong> of diameter, a minimum near $150, and a discount for additional stumps. Very large legacy stumps run higher because of their sheer size, but you'll know the exact figure from a free on-site estimate before any grinding begins.</p>

<h2>Tight Access on Older Lots</h2>
<p>Stoughton's historic lots weren't built for modern equipment — narrow drives, close-set homes, and gated backyards are common. Our compact track grinders fit through standard gates and maneuver in tight side yards, so we can reach stumps other crews say they can't, without damaging fences or gardens.</p>

<p>We're proud to help keep Stoughton's historic streetscape looking its best. When a beloved old tree finally has to come down, grinding the stump cleanly lets a replacement take its place and preserves the leafy character that makes the neighborhoods near the river and downtown so distinctive. Ask us about grinding deep enough to replant right where the old tree stood.</p>

<p>From the historic district to Kettle Park, call {phone} or request your free Stoughton quote today.</p>
""",
  "faqs":[
   ("How much does stump grinding cost in Stoughton?","Single stumps typically run $150–$350 at roughly $3–$5 per inch with a $150 minimum. Very large legacy stumps cost more; every price is confirmed with a free on-site estimate."),
   ("Can you grind very large, old stumps?","Yes. Stoughton's historic lots have some of the county's biggest legacy stumps, and we bring high-horsepower grinders built to handle wide hardwood stumps and heavy surface roots."),
   ("Can you reach a backyard stump on a tight older lot?","Usually, yes. Our compact track grinders fit through standard 36-inch gates and maneuver in narrow side yards common in Stoughton's older neighborhoods."),
   ("How deep do you grind the stump?","We grind 4–6 inches below grade as standard, and deeper when you plan to replant or build over the spot."),
  ],
 },
 {
  "slug":"oregon","name":"Oregon","zips":"53575",
  "hoods":["Rome Corners","Jaycee Park area","Alpine Meadows","Downtown Oregon","Bergamont"],
  "meta_title":"Stump Grinding Oregon WI | Free On-Site Quotes",
  "meta_desc":"Insured stump grinding in Oregon, WI. Windbreak & fence-line clearing, village and rural service, same-day response. Call (608) 493-0540.",
  "lead":"In the Village of Oregon and the farmland around it, we grind stumps and clear windbreaks fast.",
  "body":"""
<p>The Village of Oregon has the feel of a small town with room to breathe, ringed by working farmland in southern Dane County. That mix means we see everything here — tidy backyard stumps in Bergamont and Alpine Meadows, plus old windbreaks and fence-line trees on rural parcels near Rome Corners. <strong>Madison Stump Grinding</strong> covers the whole area.</p>

<h2>Windbreak and Fence-Line Clearing</h2>
<p>Oregon's agricultural edges are lined with the remains of old windbreaks and property-line trees, and clearing them is one of our most common local jobs. We grind those stumps low and process the surface roots so the ground can go back to lawn, crop, or new construction without a row of humps left behind.</p>

<h2>How Much Does Stump Grinding Cost in Oregon?</h2>
<p>Our pricing is the same fair, diameter-based rate we use across Dane County: about <strong>$3 to $5 per inch</strong>, a minimum near $150, and a discount on each added stump. Multi-stump windbreak and lot clearing is quoted per project. You get a firm number from a free on-site visit — never a guess over the phone.</p>

<h2>Village Lots and Rural Acreage Alike</h2>
<p>Whether it's a single stump behind a home near Jaycee Park or a dozen along a rural fence line, we bring the right machine. Compact track grinders handle village backyards without tearing up the lawn, while larger units make quick work of big rural stumps and stony ground.</p>

<p>Growing families keep choosing Oregon for its schools and small-town feel, and many inherit older yards with a stump or two the previous owner never dealt with. We're glad to knock those out — often several at once for a whole-yard reset — and leave the ground ready for a play set, a garden, or a fresh stretch of lawn.</p>

<p>Serving Oregon and the surrounding township — call {phone} or request your free quote online.</p>
""",
  "faqs":[
   ("How much does stump grinding cost in Oregon?","Single stumps generally run $150–$350 at about $3–$5 per inch with a $150 minimum. Windbreak and multi-stump clearing is quoted per project during a free on-site estimate."),
   ("Do you clear old windbreaks and fence-line trees?","Yes — it's one of our most common jobs around Oregon. We grind the stumps low and process surface roots so the ground returns to lawn, crop, or building site."),
   ("How deep do you grind the stump?","Standard depth is 4–6 inches below grade for lawn; we go deeper for replanting or construction."),
   ("Do you serve rural properties outside the village?","We do. We cover the Village of Oregon and the surrounding township, sizing our equipment to both village backyards and rural acreage."),
  ],
 },
 {
  "slug":"monona","name":"Monona","zips":"53716",
  "hoods":["Frost Woods","Winnequah","San Damiano area","Ahuska Park","Maywood"],
  "meta_title":"Stump Grinding Monona WI | Free Estimates, Insured",
  "meta_desc":"Insured stump grinding in Monona, WI. Lakefront lots, tight-access yards, hardscape-safe grinding, same-day response. Call (608) 493-0540.",
  "lead":"On Monona's compact lakefront lots, careful access and a clean finish are everything — and that's our specialty.",
  "body":"""
<p>Tucked against the east shore of Lake Monona and nearly surrounded by Madison, the city of Monona is a community of mature, established lots — Frost Woods, Winnequah, and the leafy streets near Ahuska Park. Big lakeshore oaks, ashes, and maples shade compact yards here, and when one comes down, the stump often sits in a tight space near a home, fence, or patio. <strong>Madison Stump Grinding</strong> is built for exactly that.</p>

<h2>Tight-Access, Hardscape-Safe Grinding</h2>
<p>Monona's smaller lots leave little room to work, with stumps frequently close to driveways, seawalls, and garden beds. Our compact track grinders slip through standard gates and maneuver in narrow side yards, and we take care to protect nearby hardscape and shoreline plantings while we grind the stump and its surface roots.</p>

<h2>How Much Does Stump Grinding Cost in Monona?</h2>
<p>You'll get the same transparent rate we offer countywide: roughly <strong>$3 to $5 per inch</strong> of stump diameter, a minimum around $150, and a discount for each extra stump. Because access and cleanup vary on lakefront lots, we always confirm the price with a free on-site estimate first.</p>

<h2>Lakeshore Trees, Handled with Care</h2>
<p>Ash loss from emerald ash borer has hit Monona's canopy hard, leaving many stumps behind. We grind them below grade and can haul the grindings so nothing is left to attract pests near the water. Then we rake the spot level so it blends right back into your yard.</p>

<p>Because Monona lots sit close together, we're mindful of neighbors too — quick, contained work, nothing left on the property line, and a clean sweep before we go. Whether it's a single ash stump beside the driveway or several along a shared fence, we keep the job tidy and the timeline short so the whole block stays happy.</p>

<p>From Winnequah to the Bridges golf area, call {phone} or request your free Monona quote today.</p>
""",
  "faqs":[
   ("How much does stump grinding cost in Monona?","Single stumps typically run $150–$350 at about $3–$5 per inch with a $150 minimum. Lakefront access and cleanup can affect the total, so we confirm with a free on-site estimate."),
   ("Can you reach a stump on a tight lakefront lot?","Yes. Monona's compact lots are our specialty — our track grinders fit through standard gates and work carefully around driveways, seawalls, and beds."),
   ("Do you handle emerald ash borer stumps?","We do. EAB has taken many of Monona's ash trees, and we grind those stumps below grade and can haul the grindings away from the shoreline."),
   ("How deep do you grind the stump?","Standard is 4–6 inches below grade for lawn restoration, and deeper if you plan to replant or install hardscape."),
  ],
 },
 {
  "slug":"deforest","name":"DeForest","zips":"53532",
  "hoods":["Windsor","Yahara area","Conservancy Place","Fireman's Park area","Prairie View"],
  "meta_title":"Stump Grinding DeForest WI | Free On-Site Quote",
  "meta_desc":"Insured stump grinding in DeForest, WI. New-build lot clearing, hedgerow removal, same-day response. Call (608) 493-0540 for a free estimate.",
  "lead":"Home of the Norski and growing fast — we clear DeForest's new-build stumps and old hedgerows alike.",
  "body":"""
<p>Just north of Madison where I-39, 90, and 94 split, DeForest and neighboring Windsor have become one of Dane County's fastest-growing corners. New subdivisions keep replacing farm fields, and that steady build-out leaves behind fence-line trees, hedgerow stumps, and the occasional big old yard tree near Fireman's Park. <strong>Madison Stump Grinding</strong> keeps up with the growth.</p>

<h2>Clearing New-Construction Lots</h2>
<p>A lot of DeForest grinding happens on lots being readied for landscaping. On former cropland with clay-loam soil, old trees leave wide, shallow roots that get in the way of grading and sod. We grind the stumps low and clear the root flare so builders and homeowners can finish the yard clean.</p>

<h2>How Much Does Stump Grinding Cost in DeForest?</h2>
<p>DeForest pricing matches the rest of Dane County: about <strong>$3 to $5 per inch</strong> of diameter, a minimum near $150, and a discount for each additional stump. Builders clearing multiple lots or a hedgerow get volume pricing. Every job starts with a free, no-pressure on-site estimate.</p>

<h2>Fast Turnaround for a Fast-Growing Town</h2>
<p>With so much building activity, schedules matter. We respond quickly — often the same day for estimates — and grind on a timeline that keeps your project moving, whether that's a single backyard stump or a punch list of lots along the Yahara.</p>

<p>Timing matters in a town building this fast. Spring and fall are our busiest DeForest seasons, as homeowners prep yards for fresh sod or clear a lot before the ground freezes — but grinding works year-round here, and we can often take a stump out between snows in winter. If you're closing on a new home or finishing a build near the Yahara, book early so the site is clear and level when your grader or landscaper arrives.</p>

<p>Serving DeForest and Windsor — call {phone} or request your free quote online.</p>
""",
  "faqs":[
   ("How much does stump grinding cost in DeForest?","Single stumps usually run $150–$350 at roughly $3–$5 per inch with a $150 minimum. Builders clearing multiple lots or hedgerows receive volume pricing confirmed on site."),
   ("Can you clear stumps on a new-construction lot?","Yes. We regularly finish DeForest and Windsor builder lots, grinding stumps low so grading, sod, and landscaping can follow."),
   ("How deep do you grind the stump?","We grind 4–6 inches below grade as standard for lawn, and deeper for replanting or where hardscape will sit over the spot."),
   ("How soon can you come out?","We usually provide same-day estimates and schedule grinding quickly — important in a fast-building area like DeForest."),
  ],
 },
 {
  "slug":"mcfarland","name":"McFarland","zips":"53558",
  "hoods":["Lake Waubesa shore","Babcock Park area","Larson Beach","Indian Mound","Woods Edge"],
  "meta_title":"Stump Grinding McFarland WI | Free Estimates",
  "meta_desc":"Insured stump grinding in McFarland, WI, on Lake Waubesa. Wet-soil ready gear, small-lot access, same-day response. Call (608) 493-0540.",
  "lead":"On the shore of Lake Waubesa, we grind McFarland's stumps clean without turning your yard to mud.",
  "body":"""
<p>McFarland sits on the south shore of Lake Waubesa, part of the Yahara chain of lakes, and its character is pure lakeside village — Babcock County Park, Larson Beach, and streets of mature shoreline trees. That waterfront setting also means wet ground and compact lots, a combination that calls for the right equipment. <strong>Madison Stump Grinding</strong> brings it.</p>

<h2>Grinding on McFarland's Wet Lakeside Soil</h2>
<p>Close to Lake Waubesa the water table runs high and the clay stays damp, which bogs down undersized machines. Our track-mounted grinders spread their weight and keep working on soft, low ground, grinding the stump fully without leaving deep ruts across your lawn or near the shoreline.</p>

<h2>How Much Does Stump Grinding Cost in McFarland?</h2>
<p>You'll get our standard countywide rate: roughly <strong>$3 to $5 per inch</strong> of stump diameter, a minimum around $150, and a discount on each additional stump. Tight lakefront access and haul-away can affect the total, so we confirm everything with a free on-site estimate before starting.</p>

<h2>Small-Lot Maneuvering, Clean Results</h2>
<p>Many McFarland homes have compact yards with limited access between the house and the water. Our equipment fits through standard gates and works in tight quarters, and we protect nearby beds, seawalls, and paths. When we finish, the spot is raked level and ready to reseed.</p>

<p>Living on the Yahara chain comes with mature, water-loving trees — willows, silver maples, and cottonwoods — that leave broad, wet stumps behind. Those species re-sprout aggressively when they're only cut, which is exactly why grinding well below grade matters here. We take the stump down far enough to stop the regrowth, then rake the spot so your lakeside lawn or garden bed picks right back up toward the water's edge.</p>

<p>From the Waubesa shore to Woods Edge, call {phone} or request your free McFarland quote today.</p>
""",
  "faqs":[
   ("How much does stump grinding cost in McFarland?","Single stumps typically run $150–$350 at about $3–$5 per inch with a $150 minimum. Lakefront access and haul-away can affect the price, which we confirm with a free on-site estimate."),
   ("Can you grind stumps on wet ground near Lake Waubesa?","Yes. The high water table and damp clay near the lake are why we use track-mounted grinders that stay stable on soft soil without rutting the yard."),
   ("Can you reach a stump on a small lakeside lot?","Usually, yes. Our compact grinders fit through standard gates and work in the tight space between house and shoreline, protecting beds and seawalls."),
   ("How deep do you grind the stump?","Standard is 4–6 inches below grade for lawn, and deeper on request for replanting or hardscape."),
  ],
 },
]

# ---- SERVICES (bespoke copy) ----
SERVICE_PAGES = {
 "tree-stump-removal-grinding": {
   "name":"Tree Stump Removal & Grinding","icon":"stump","hero_img":"/service-stump.jpg",
   "meta_title":"Tree Stump Removal & Grinding | Madison, WI",
   "meta_desc":"Professional tree stump removal & grinding across Dane County, WI. Below-grade grinding, full cleanup, fully insured. Free quotes — call (608) 493-0540.",
   "lead":"The core of what we do: fast, complete stump grinding that gets the eyesore out and your yard back — below grade, cleaned up, and ready to plant.",
   "body":"""
<p>A ground-out stump is more than a cosmetic fix. Left in place, stumps sprout suckers, attract carpenter ants and termites, host fungus, wreck mower blades, and take up space you'd rather use. <strong>Madison Stump Grinding</strong> removes that headache the efficient way — mechanical grinding that turns the stump and its roots into usable mulch, without the huge hole and expense of full excavation.</p>

<h2>What's Included in Every Grinding Job</h2>
<ul class="ticklist">
  <li>Grinding the stump 4–6 inches below grade (deeper on request for replanting)</li>
  <li>Grinding exposed surface roots that lift lawns, walks, and driveways</li>
  <li>Raking the site level and backfilling the void with the grindings</li>
  <li>Optional haul-away of chips and clean topsoil backfill</li>
  <li>Full cleanup so the area is ready for sod, seed, or a new bed</li>
</ul>

<h2>How Much Does Stump Grinding Cost?</h2>
<p>Most jobs are priced by the stump's diameter measured at ground level — typically <strong>$3 to $5 per inch</strong>, with a job minimum around $150. A single average stump usually runs $150–$350, and each additional stump on the same visit is discounted. Root grinding, difficult access, and haul-away can affect the total, so we confirm a firm price with a free on-site estimate.</p>

<h2>How Deep Do You Grind?</h2>
<p>Our standard depth is 4–6 inches below the soil line, which is plenty for laying sod, seeding grass, or planting a garden bed. If you intend to replant a tree in the same location, we grind 8–12 inches deeper to clear the root plate. Just tell us your plans and we'll set the depth accordingly.</p>

<h2>Right-Sized Equipment, Property-Safe</h2>
<p>From compact track grinders that fit through a 36-inch gate to high-horsepower machines for large-diameter stumps, we bring the tool that fits your access and your stump. Rubber tracks spread weight to protect turf, and we lay down protection over sensitive paths when needed.</p>
""",
   "faqs":[
    ("How much does stump grinding cost?","Most single stumps run $150–$350, based on about $3–$5 per inch of ground-level diameter with a $150 minimum. Additional stumps are discounted. Every price is confirmed with a free on-site estimate."),
    ("How deep do you grind the stump?","Standard depth is 4–6 inches below grade — enough for sod, seed, or a garden bed. For replanting a tree in the same spot, we grind 8–12 inches deeper."),
    ("Is stump grinding better than full removal?","For most yards, yes. Grinding is faster, cheaper, and far less disruptive than excavating the entire root ball, and it leaves usable mulch instead of a large hole."),
    ("What do you do with the wood chips?","You can keep them as free mulch, or we'll haul them away and backfill with clean topsoil for a small additional charge. Either way, we rake the site level."),
   ],
 },
 "root-surface-grinding-land-clearing": {
   "name":"Root Surface Grinding & Land Clearing","icon":"roots","hero_img":"/service-roots.jpg",
   "meta_title":"Root Grinding & Land Clearing | Dane County WI",
   "meta_desc":"Surface root grinding & land clearing across Greater Madison, WI. Clear lots, hedgerows & invasive roots. Fully insured. Free quotes — call (608) 493-0540.",
   "lead":"Beyond single stumps: we grind heaving surface roots and clear overgrown lots, hedgerows, and fence lines so your ground is usable again.",
   "body":"""
<p>Sometimes the problem isn't one stump — it's a web of surface roots buckling your lawn, or an overgrown lot line you need cleared before you can build, farm, or landscape. <strong>Madison Stump Grinding</strong> handles both, combining root grinding with practical small-scale land clearing across Dane County.</p>

<h2>Surface Root Grinding</h2>
<p>Mature trees push roots to the surface, where they crack sidewalks, lift driveways, scalp under the mower, and trip up foot traffic. We grind those exposed roots down below grade so you can restore a smooth, safe lawn — without harming a healthy tree you want to keep, when the roots are ground carefully and selectively.</p>

<h2>Lot, Hedgerow & Fence-Line Clearing</h2>
<p>Across the Greater Madison area — from Verona acreage to former farm fields in Waunakee, Oregon, and DeForest — we clear the stumps and roots left after brush and small-tree removal. That includes old windbreaks, overgrown fence lines, and lots being readied for construction or grading.</p>
<ul class="ticklist">
  <li>Grinding multiple stumps and hedgerow remnants low for grading</li>
  <li>Removing surface roots that block sod, paving, or planting</li>
  <li>Clearing old windbreaks and fence-line trees on rural parcels</li>
  <li>Prepping lots so builders and landscapers can move in clean</li>
</ul>

<h2>How Is Land Clearing Priced?</h2>
<p>Single root-grinding jobs follow our standard <strong>$3–$5 per inch</strong> stump rate with a $150 minimum. Larger clearing projects are quoted per site based on the number and size of stumps, access, and haul-away needs. We'll walk the property with you and give a clear, free written estimate before any work begins.</p>

<h2>The Right Machine for Bigger Ground</h2>
<p>Land clearing calls for muscle. We bring higher-horsepower grinders for big stumps and stony or rooty ground, plus track machines that stay stable on soft or uneven soil, so even a rough parcel ends up graded, level, and ready for its next use.</p>
""",
   "faqs":[
    ("Can you grind surface roots without killing my tree?","In many cases, yes. Selective, careful grinding of exposed surface roots can smooth your lawn while preserving a healthy tree. We'll assess the tree first and advise honestly if grinding would risk its health."),
    ("How much does land clearing cost?","Single root-grinding jobs follow our $3–$5 per inch rate with a $150 minimum. Larger lot, hedgerow, and windbreak clearing is quoted per site after a free on-site walk-through."),
    ("Do you clear lots for new construction?","Yes. We grind stumps and surface roots low and clear hedgerow remnants so builders and landscapers can grade, pave, sod, or plant without obstruction."),
    ("Do you haul away the debris?","We can. Grindings can stay on site as mulch or be hauled away with clean backfill added, depending on your preference and the project scope."),
   ],
 },
 "emergency-stump-debris-removal": {
   "name":"Emergency Stump & Debris Removal","icon":"alert","hero_img":"/service-emergency.jpg",
   "meta_title":"Emergency Stump & Debris Removal | Madison WI",
   "meta_desc":"Same-day emergency stump & storm-debris removal in Dane County, WI. Fast, insured cleanup after storms. Call (608) 493-0540 for rapid response.",
   "lead":"When a storm drops a tree or you need a stump gone now, we respond fast — often same day — to clear the debris and grind what's left.",
   "body":"""
<p>Wisconsin storms don't wait for a convenient time. High winds off the lakes, heavy wet snow, and summer downbursts regularly bring trees down across Dane County — leaving hazards, blocked drives, and torn-out stumps behind. <strong>Madison Stump Grinding</strong> offers fast, insured emergency response to clear the mess and finish the job.</p>

<h2>Same-Day Response When It Matters</h2>
<p>We answer the phone seven days a week and prioritize urgent calls — a stump blocking access, a hazard near a home, or a real-estate closing on a deadline. In most of the Greater Madison area we can be on site the same day to assess and, in many cases, grind and clear on the spot.</p>

<h2>Storm Debris Cleanup &amp; Stump Grinding</h2>
<ul class="ticklist">
  <li>Grinding storm-snapped and uprooted stumps below grade</li>
  <li>Clearing and hauling branches, trunk sections, and debris</li>
  <li>Filling and leveling torn-out root craters left by fallen trees</li>
  <li>Coordinating with your tree service after a felling or takedown</li>
</ul>
<p>If a tree service has already dropped the tree, we're the crew that makes the stump and the ground-level mess disappear so your property looks whole again.</p>

<h2>What Does Emergency Removal Cost?</h2>
<p>Stump grinding still follows our fair <strong>$3–$5 per inch</strong> rate with a $150 minimum; debris hauling and craters are quoted based on volume and access. We give you a clear price up front, even on urgent jobs — no one wants a surprise bill on a bad day. Fully insured, so your property is protected throughout.</p>

<h2>Insured, Local, and Ready</h2>
<p>Emergency work is no place for an uninsured operator. We carry liability coverage, work safely around structures and utilities, and know the Dane County communities we serve — so help is genuinely local and genuinely fast.</p>
""",
   "faqs":[
    ("How fast can you respond to an emergency?","We answer calls seven days a week and prioritize urgent jobs. In most of the Greater Madison area we can be on site the same day to assess and often grind and clear immediately."),
    ("Do you remove storm debris as well as the stump?","Yes. We grind storm-snapped and uprooted stumps below grade, clear and haul branches and trunk sections, and fill the crater left by a fallen tree."),
    ("What does emergency stump removal cost?","Grinding follows our standard $3–$5 per inch rate with a $150 minimum; debris hauling is quoted by volume and access. You'll get a clear price up front, even on urgent calls."),
    ("Are you insured for emergency tree and stump work?","Yes. We carry liability coverage and work carefully around homes and utilities, so your property is protected throughout the job."),
   ],
 },
}

# add name lookups
for c in CITIES:
    c["name_full"] = f'{c["name"]}, WI'
SVC_BY_SLUG = SERVICE_PAGES

# ================================================================== assembly
def write(path_parts, html_str):
    d = os.path.join(ROOT, *path_parts)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    with open(d, "w", encoding="utf-8") as f:
        f.write(html_str)

def page_shell(inner, title, desc, canonical, schemas, hero_img=None, inline=False):
    return (head(title, desc, canonical, schemas, hero_img, inline)
            + callbar() + header() + inner + footer() + floatcall()
            + ('\n<script src="/js/main.js"></script>' if not inline
               else "\n<script>\n" + open(os.path.join(ROOT,"js","main.js")).read() + "\n</script>")
            + "\n</body>\n</html>")

def crumbs(trail):
    parts = []
    for i,(n,u) in enumerate(trail):
        if i < len(trail)-1:
            parts.append(f'<a href="{u}">{n}</a>')
        else:
            parts.append(f'<span>{n}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + " / ".join(parts) + "</nav>"

# ---------- CITY PAGES ----------
def build_city(c, inline=False):
    url = SITE["domain"] + city_url(c["slug"])
    trail = [("Home","/"),("Service Areas", city_url("madison")),(f'{c["name"]}, WI', city_url(c["slug"]))]
    schemas = [local_business_schema(url), breadcrumb_schema(trail), faq_schema(c["faqs"])]
    body = c["body"].replace("{phone}", f'<a href="tel:{SITE["phone_tel"]}">{SITE["phone_display"]}</a>')
    hoods = ", ".join(c["hoods"])
    inner = (
        hero(
            loc_line=f'Stump Grinding &middot; {c["name"]}, Wisconsin',
            h1=f'Stump Grinding in {c["name"]}, WI',
            lead_txt=c["lead"],
            hero_img="/hero-home.jpg",
            fid=f'lead-{c["slug"]}',
            crumbs_html=crumbs(trail),
        )
        + trustbar()
        + f"""
<section class="section">
  <div class="container">
    <article class="prose">
      {body}
      <h3>Neighborhoods &amp; Areas We Serve in {c['name']}</h3>
      <p>We grind stumps throughout {c['name']} and the surrounding area, including {hoods} — and every zip code in between ({c['zips']}).</p>
    </article>
  </div>
</section>"""
        + faq_block(c["faqs"], heading=f'Stump Grinding FAQs — {c["name"]}, WI')
        + area_chips(exclude=c["slug"])
        + cta_band(h=f'Get Your Free {c["name"]} Stump Grinding Quote',
                   p=f'Fast, fully insured stump grinding for {c["name"]} homeowners and businesses. Same-day estimates available — call now or request a quote online.')
    )
    return page_shell(inner, c["meta_title"], c["meta_desc"], url, schemas,
                      hero_img="/hero-home.jpg", inline=inline)

# ---------- SERVICE PAGES ----------
def build_service(slug, inline=False):
    s = SERVICE_PAGES[slug]
    url = SITE["domain"] + svc_url(slug)
    trail = [("Home","/"),("Services", svc_url(slug)),(s["name"], svc_url(slug))]
    schemas = [local_business_schema(url), breadcrumb_schema(trail),
               {"@context":"https://schema.org","@type":"Service","name":s["name"],
                "provider":{"@id":SITE["domain"]+"/#business"},
                "areaServed":[{"@type":"City","name":f'{c["name"]}, WI'} for c in CITIES],
                "description": s["meta_desc"]},
               faq_schema(s["faqs"])]
    body = s["body"].replace("{phone}", f'<a href="tel:{SITE["phone_tel"]}">{SITE["phone_display"]}</a>')
    other = "".join(f'<li><a href="{svc_url(k)}">{v["name"]}</a></li>'
                    for k,v in SERVICE_PAGES.items() if k != slug)
    inner = (
        hero(
            loc_line="Dane County &amp; Greater Madison, WI",
            h1=s["name"],
            lead_txt=s["lead"],
            hero_img=s["hero_img"],
            fid=f'lead-{slug}',
            crumbs_html=crumbs(trail),
        )
        + trustbar()
        + f"""
<section class="section">
  <div class="container">
    <article class="prose">
      {body}
      <h3>Related Services</h3>
      <ul>{other}</ul>
    </article>
  </div>
</section>"""
        + faq_block(s["faqs"])
        + area_chips()
        + cta_band()
    )
    return page_shell(inner, s["meta_title"], s["meta_desc"], url, schemas,
                      hero_img=s["hero_img"], inline=inline)

# ---------- HOMEPAGE ----------
def build_home(inline=False):
    url = SITE["domain"] + "/"
    home_faqs = [
      ("How much does stump grinding cost in the Madison area?","Most single stumps run $150–$350, priced at about $3–$5 per inch of ground-level diameter with a $150 minimum. Additional stumps on the same visit are discounted, and every quote is confirmed with a free on-site estimate."),
      ("How deep do you grind stumps?","Standard depth is 4–6 inches below grade — enough for sod, seed, or a garden bed. If you're replanting a tree in the same spot, we grind 8–12 inches deeper."),
      ("Are you insured?","Yes, we're fully insured for stump grinding and land-clearing work, so your property is protected on every job."),
      ("Do you offer same-day service?","We offer same-day estimates across most of the Greater Madison area and same-day grinding when our schedule allows — especially for emergencies and storm cleanup."),
      ("Do you clean up afterward?","Always. We rake the site level and either leave the grindings as mulch or haul them away with clean topsoil backfill for a small additional charge."),
    ]
    schemas = [local_business_schema(url),
               {"@context":"https://schema.org","@type":"WebSite","name":SITE["name"],"url":SITE["domain"]},
               faq_schema(home_faqs)]
    services_cards = "".join(f"""
      <div class="card">
        <span class="card__ico">{IC[s['icon']]}</span>
        <h3>{s['name']}</h3>
        <p>{s['lead']}</p>
        <a class="card__link" href="{svc_url(slug)}">Learn more</a>
      </div>""" for slug,s in [(k, SERVICE_PAGES[k]) for k in [x['slug'] for x in SERVICES]])

    inner = (
        hero(
            loc_line="Dane County &amp; Greater Madison, Wisconsin",
            h1="Stump Grinding &amp; Land Clearing, Done Right",
            lead_txt="Fully insured, locally operated, and fast. We grind stumps below grade, clear the debris, and leave your yard level and ready to plant — from Madison to every corner of Dane County.",
            checks=["Free on-site estimates","Same-day response available","Backyard-gate access machines","Full cleanup &amp; haul-away"],
            hero_img="/hero-home.jpg",
            fid="lead-home",
        )
        + trustbar()
        + f"""
<section class="section">
  <div class="container">
    <div class="center"><p class="eyebrow">What We Do</p><h2>Stump &amp; Land Services for Every Property</h2>
    <p class="lead">Residential and commercial. One local crew, the right equipment, and a clean finish every time.</p></div>
    <div class="grid grid--3" style="margin-top:36px">{services_cards}</div>
  </div>
</section>

<section class="section section--sand">
  <div class="container split">
    <div>
      <p class="eyebrow">Why Homeowners Choose Us</p>
      <h2>Local Know-How, Property-Safe Results</h2>
      <p class="lead">Dane County's clay soils, tight isthmus lots, oak wilt, and emerald ash borer are all part of our daily work. We bring the right machine and the local experience to match.</p>
      <ul class="ticklist">
        <li><strong>Insured &amp; professional</strong> — your property is protected on every job.</li>
        <li><strong>Compact to heavy-duty equipment</strong> — from 36-inch-gate backyards to commercial lots.</li>
        <li><strong>Below-grade grinding</strong> — 4–6 inches deep as standard, deeper for replanting.</li>
        <li><strong>Real cleanup</strong> — raked level, grindings as mulch or hauled away.</li>
      </ul>
      <a class="btn btn--green btn--lg" href="/contact/">Get a Free Estimate</a>
    </div>
    <div><img src="/service-stump.jpg" alt="Stump grinder removing a tree stump in a Dane County backyard" loading="lazy"></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="center"><p class="eyebrow">Simple Process</p><h2>From Quote to Clean Yard in Four Steps</h2></div>
    <div class="steps" style="margin-top:44px">
      <div class="step"><h4>Request a Quote</h4><p>Call or fill out the form with your zip and a photo. We respond fast — often the same day.</p></div>
      <div class="step"><h4>Free On-Site Estimate</h4><p>We measure the stump, check access, and give you a firm, no-pressure price in writing.</p></div>
      <div class="step"><h4>We Grind It Out</h4><p>The right machine arrives, grinds below grade, and processes the surface roots.</p></div>
      <div class="step"><h4>Clean &amp; Level Finish</h4><p>We rake the site smooth and leave mulch or haul it away — ready to sod or plant.</p></div>
    </div>
  </div>
</section>

<section class="section section--green">
  <div class="container">
    <div class="stats">
      <div><div class="stat__num">15+</div><div class="stat__lbl">Years of local experience</div></div>
      <div><div class="stat__num">5,000+</div><div class="stat__lbl">Stumps ground out</div></div>
      <div><div class="stat__num">11</div><div class="stat__lbl">Dane County communities</div></div>
      <div><div class="stat__num">Same-Day</div><div class="stat__lbl">Response available</div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="center"><p class="eyebrow">What Neighbors Say</p><h2>Trusted Across the Greater Madison Area</h2></div>
    <div class="grid grid--3" style="margin-top:36px">
      <div class="quote"><div class="quote__stars">★★★★★</div><p>"Ground out three huge maple stumps in our Monona backyard in one afternoon and left it perfectly level. Fair price and great cleanup."</p><p class="quote__who">Sarah K.<span>Monona, WI</span></p></div>
      <div class="quote"><div class="quote__stars">★★★★★</div><p>"Fast, insured, and professional. They fit the grinder through our narrow gate on the isthmus without a scratch on the fence."</p><p class="quote__who">Dave R.<span>Madison, WI</span></p></div>
      <div class="quote"><div class="quote__stars">★★★★★</div><p>"Cleared a whole fence line of old stumps on our Verona property. Showed up on time and quoted exactly what they charged."</p><p class="quote__who">The Hansons<span>Verona, WI</span></p></div>
    </div>
  </div>
</section>"""
        + area_chips()
        + faq_block(home_faqs)
        + cta_band()
    )
    return page_shell(inner, "Stump Grinding Madison WI | Dane County | Free Quotes",
                      "Fully insured stump grinding & land clearing across Madison & Dane County, WI. Below-grade grinding, full cleanup, same-day response. Call (608) 493-0540.",
                      url, schemas, hero_img="/hero-home.jpg", inline=inline)

# ---------- ABOUT ----------
def build_about(inline=False):
    url = SITE["domain"] + "/about/"
    trail = [("Home","/"),("About","/about/")]
    schemas = [local_business_schema(url), breadcrumb_schema(trail)]
    inner = (
        hero(
            loc_line="About Madison Stump Grinding",
            h1="Your Local Dane County Stump Grinding Team",
            lead_txt="Locally operated, fully insured, and genuinely fast. We started with one grinder and a simple promise: clear pricing, clean work, and respect for your property.",
            hero_img="/about-team.jpg",
            fid="lead-about",
            crumbs_html=crumbs(trail),
        )
        + trustbar()
        + f"""
<section class="section">
  <div class="container split">
    <div>
      <p class="eyebrow">Our Story</p>
      <h2>Built on Clean Work and Straight Talk</h2>
      <p>Madison Stump Grinding was founded to do one thing exceptionally well: get stumps out of the ground and leave yards better than we found them. Over years of working across Dane County's clay soils, tight isthmus lots, and rolling Verona acreage, we've learned that homeowners want three things — a fair, upfront price, careful work around their property, and a genuine cleanup at the end.</p>
      <p>That's the whole business. We're not a national franchise or a call center. We're a local crew that knows the difference between a Monona lakefront lot and a DeForest new-build, and we bring the right machine for each.</p>
      <a class="btn btn--green btn--lg" href="/contact/">Request a Free Estimate</a>
    </div>
    <div><img src="/about-team.jpg" alt="Local stump grinding crew with equipment in Dane County, Wisconsin" loading="lazy"></div>
  </div>
</section>

<section class="section section--sand">
  <div class="container">
    <div class="center"><p class="eyebrow">What We Stand For</p><h2>Values That Show Up in the Work</h2></div>
    <div class="grid grid--4" style="margin-top:36px">
      <div class="card"><span class="card__ico">{IC['shield']}</span><h3>Fully Insured</h3><p>Liability coverage on every job, so your property and your peace of mind are protected.</p></div>
      <div class="card"><span class="card__ico">{IC['dollar']}</span><h3>Honest Pricing</h3><p>Clear, diameter-based quotes given on site and in writing — no surprises, no upsells.</p></div>
      <div class="card"><span class="card__ico">{IC['leaf']}</span><h3>Property-Safe</h3><p>Track machines, gate-width access, and careful work around lawns, beds, and hardscape.</p></div>
      <div class="card"><span class="card__ico">{IC['clock']}</span><h3>Responsive</h3><p>We answer seven days a week and offer same-day estimates and emergency response.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split">
    <div><img src="/service-roots.jpg" alt="Land clearing and root grinding on a Dane County property" loading="lazy"></div>
    <div>
      <p class="eyebrow">Why Local Matters</p>
      <h2>We Know Dane County Ground</h2>
      <p>Oak wilt in the red oaks. Emerald ash borer thinning the canopy from Madison to Monona. Heavy lake-plain clay that packs around old roots, and the softer, wetter soil near Nine Springs and Lake Waubesa. These aren't textbook facts to us — they're the conditions we work in every week.</p>
      <p>That local knowledge means faster estimates, the right equipment on the first trip, and advice you can trust about depth, replanting, and cleanup for your specific property.</p>
    </div>
  </div>
</section>"""
        + area_chips()
        + cta_band()
    )
    return page_shell(inner, "About Us | Madison Stump Grinding, Dane County WI",
                      "Locally operated, fully insured stump grinding for Madison & Dane County, WI. Honest pricing, property-safe work, fast response. Call (608) 493-0540.",
                      url, schemas, hero_img="/about-team.jpg", inline=inline)

# ---------- CONTACT ----------
def build_contact(inline=False):
    url = SITE["domain"] + "/contact/"
    trail = [("Home","/"),("Contact","/contact/")]
    schemas = [local_business_schema(url), breadcrumb_schema(trail)]
    contact_faqs = [
      ("How do I get a free estimate?","Call (608) 493-0540 or fill out the quote form with your name, phone, property zip, and a photo if you have one. We respond fast — usually the same day — and schedule a free on-site estimate."),
      ("What areas do you serve?","We serve Madison and the surrounding Dane County communities, including Sun Prairie, Fitchburg, Middleton, Verona, Waunakee, Stoughton, Oregon, Monona, DeForest, and McFarland."),
      ("What are your hours?","We're reachable seven days a week, 7:00am to 7:00pm, with emergency response available for storm damage and urgent hazards."),
    ]
    schemas.append(faq_schema(contact_faqs))
    inner = (
        f"""
<section class="pagehero" style="--hero-img:url(/hero-home.jpg)">
  <div class="pagehero__inner">
    {crumbs(trail)}
    <p class="hero__loc">Free Estimates &middot; Dane County, WI</p>
    <h1>Contact Us for a Free Stump Grinding Quote</h1>
    <p class="lead">Tell us about your stump or clearing job and we'll get you a fast, no-obligation price. Call {SITE['phone_display']} or use the form below — we answer seven days a week.</p>
  </div>
</section>
{trustbar()}
<section class="section">
  <div class="container withform">
    <div>
      <p class="eyebrow">Get In Touch</p>
      <h2>Request Your Free On-Site Estimate</h2>
      <p class="lead">The fastest way to a clean yard. Share a few details and, if you can, a photo of the stump — it helps us quote accurately before we arrive.</p>
      <div class="grid grid--2" style="margin-top:24px">
        <div class="card"><span class="card__ico">{IC['phone']}</span><h3>Call or Text</h3><p><a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a><br>Seven days a week</p></div>
        <div class="card"><span class="card__ico">{IC['mail']}</span><h3>Email</h3><p><a href="mailto:{SITE['email']}">{SITE['email']}</a><br>We reply quickly</p></div>
        <div class="card"><span class="card__ico">{IC['clock']}</span><h3>Hours</h3><p>Mon–Sun<br>7:00am – 7:00pm</p></div>
        <div class="card"><span class="card__ico">{IC['map']}</span><h3>Service Area</h3><p>Madison &amp;<br>all of Dane County</p></div>
      </div>
    </div>
    <aside class="withform__aside">
      {lead_form(fid="contact-lead", heading="Free Quote Request", sub="Most requests answered the same day.")}
    </aside>
  </div>
</section>"""
        + faq_block(contact_faqs)
        + area_chips()
        + cta_band()
    )
    return page_shell(inner, "Contact | Free Stump Grinding Quote | Madison WI",
                      "Contact Madison Stump Grinding for a free, same-day estimate in Dane County, WI. Call (608) 493-0540 or request a quote online. Residential & commercial.",
                      url, schemas, hero_img="/hero-home.jpg", inline=inline)

# ================================================================== sitemap
def build_sitemap():
    urls = ["/","/about/","/contact/"] + [svc_url(s["slug"]) for s in SERVICES] + [city_url(c["slug"]) for c in CITIES]
    items = "".join(f"  <url><loc>{SITE['domain']}{u}</loc><changefreq>monthly</changefreq><priority>{'1.0' if u=='/' else '0.8'}</priority></url>\n" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}</urlset>\n'

def build_robots():
    return f"User-agent: *\nAllow: /\n\nSitemap: {SITE['domain']}/sitemap.xml\n"

# ================================================================== main
def main():
    # deploy versions (external css/js)
    write(["index.html"], build_home())
    write(["about","index.html"], build_about())
    write(["contact","index.html"], build_contact())
    for slug in SERVICE_PAGES:
        write([slug,"index.html"], build_service(slug))
    for c in CITIES:
        write([f'stump-grinding-{c["slug"]}-wi',"index.html"], build_city(c))
    write(["sitemap.xml"], build_sitemap())
    write(["robots.txt"], build_robots())
    # GitHub Pages support files
    write(["CNAME"], "stumpgrindingmadison.com\n")
    write([".nojekyll"], "")
    print("Built 17 pages + sitemap.xml + robots.txt + CNAME + .nojekyll")

if __name__ == "__main__":
    main()
