"""Builds Tracy Najjingo's portfolio site.

Outputs:
  dist/                     deployable multi-page static site (Netlify, Vercel, Cloudflare Pages, any host)
  preview/index.html        one-page preview with hash routes (uses preview/assets/) for sharing as a link

Edit the CONFIG and content below, then run:  python3 build.py
"""
import html, json, os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- CONFIG
EMAIL = "tracynajjimngo01@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/tracy-najjingo-1318a8418"
LINKEDIN_LABEL = "in/tracy-najjingo-1318a8418"
WHATSAPP = "971527675035"          # country code, no + or spaces. Empty hides the WhatsApp buttons.
WHATSAPP_LABEL = "+971 52 767 5035"
SITE_URL = "https://www.tracynajjingo.com"
OG_IMAGE = "https://pub-bb2e103a32db4e198524a2e9ed8f35b4.r2.dev/lovp_7cyf5cw4sa9c38wcyee6f8e6p1/40c820aac6ce23d3eb4375d8768a19d9_1794568563783.png"

# ---------------------------------------------------------------- BRANDS
# key -> (name, logo file or None, website or None, what I did)
BRANDS = {
    "crwd": ("CRWD Dubai", "crwd-dubai.svg", "https://crwdmarketing.com/ae", "Where I lead marketing today"),
    "tradershub": ("Traders Hub", "traders-hub.png", "https://www.tradershub.ae/", "Social media and content"),
    "tfg": ("Traders Financial Group", "traders-financial-group.png", "https://www.tfg-ae.com/", "Brand design and paid advertising"),
    "engage": ("Engage Clinic", "engage-clinic.png", "https://engageclinic.ae/", "Rebrand, brand design and social"),
    "ccea": ("CCEA", "ccea.png", "https://ccea.ae/", "Branding and design"),
    "fos": ("Factory of Sight", "factory-of-sight.png", "https://factoryofsight.com/", "Design"),
    "gamma": ("GAMMA USA", "gamma-usa.svg", "https://www.gammabeyond.com/en/", "Design"),
    "klowe": ("KLOWE", None, None, "Full rebrand and brand strategy"),
    "altara": ("Altara Group", None, None, "Strategy for five brands at once"),
    "altarasocial": ("Altara Social", "altara-social.png", "https://altarasocial.ae/", "Strategy and influencer plan"),
    "altaralaw": ("Altara Law", "altara-law.png", "https://altaralaw.com/", "Strategy and influencer plan"),
    "elite": ("Elite Supplements", "elite-supplements.svg", "https://elitesupps.ae/", "Strategy, influencer plan and brand"),
    "hrprime": ("Prime HR Advisory", "prime-hr.png", "https://primehradvisory.com/", "Strategy and influencer plan"),
    "amedanca": ("Amedanca Travels", "amedanca-travels.png", "https://amedanca.ae/", "Strategy and influencer plan"),
    "talentec": ("Talentec", "talentec.svg", "https://talentec.co/en", "Brand work, case study coming soon"),
    "shopify": ("Shopify stores", "shopify.png", "https://www.shopify.com/", "Beauty, fashion and fragrance stores"),
    "lamise": ("Lamise Beauty", "lamise-beauty.svg", "https://www.lamisebeauty.com/", "Online shop, Google search and campaigns"),
    "hme": ("Home Experts", "home-experts.png", "https://www.homeexperts.ae/", "Strategy, content and promotions"),
    "hazo": ("Hazo Branding", "hazo-branding.png", "https://hazobranding.com/", "Social content and the content calendar"),
    "emmaship": ("EMA Ship Management", "ema-ship.png", "https://emaship.com/", "Marketing at CRWD Dubai"),
    "dessecrew": ("DESE Crew Management", "dese-crew.png", "https://www.desecrew.com/en", "Marketing at CRWD Dubai"),
    "avalar": ("Avalar", "avalar.svg", "https://avalar.com/", "Marketing at CRWD Dubai"),
    "aureum": ("Aureum", "aureum.png", "https://aureum.ae/", "Marketing at CRWD Dubai"),
}

CRWD_ROLE = "Done at CRWD Dubai, where I lead marketing. I set the plan and the look, and lead the designers and editors who make it."

# ---------------------------------------------------------------- PROJECTS
# shot=True uses assets/shots/<slug>-d.jpg and -m.jpg (screenshots of the live site).
# cats drive the filter on the Work page.
PROJECTS = [
    dict(slug="engage-clinic", brand="engage", shot="engage", context="CRWD Dubai", tint="oklch(0.93 0.035 300)",
         title="A therapy clinic, rebranded from the ground up.",
         summary="A full rebrand for a UAE early-intervention therapy clinic, from strategy and identity to the social campaigns that launched it.",
         tags=["Rebrand", "Brand design", "Social campaigns"], cats=["branding", "design", "social", "campaigns"],
         did=[("Brand plan", "Who the clinic speaks to, and what it stands for."),
              ("Rebrand & design", "A new look and a new voice, used everywhere the clinic shows up."),
              ("Launch campaign", "Social campaigns that introduced the new brand and brought in free-consultation bookings.")],
         role=CRWD_ROLE),
    dict(slug="traders-financial-group", brand="tfg", shot="tfg", context="CRWD Dubai", tint="oklch(0.27 0.03 20)",
         title="Wealth management that looks the part.",
         summary="Brand and design for a UAE wealth-management firm, and the paid campaigns that bring prospective clients in.",
         tags=["Brand design", "Campaign strategy", "Paid ads"], cats=["design", "strategy", "campaigns"],
         did=[("Brand & design", "A look built on trust: clear services, a clear story and one clear next step."),
              ("Campaign strategy", "Who to reach, where, and what to say."),
              ("Paid advertising", "Campaigns that put the firm in front of the right investors.")],
         role=CRWD_ROLE),
    dict(slug="ccea", brand="ccea", shot="ccea", context="CRWD Dubai", tint="oklch(0.94 0.03 230)",
         title="An identity and a store for a fashion label.",
         summary="Branding and design for a fashion label, carried through its collections and online store.",
         tags=["Branding", "Design"], cats=["branding", "design", "ecommerce"],
         did=[("Branding", "The label’s look, feel and voice."),
              ("Design", "How the collections, the brand story and the store look and read.")],
         role=CRWD_ROLE),
    dict(slug="lamise-beauty", brand="lamise", shot="lamise", context="Shopify stores · 2021–2023", tint="oklch(0.94 0.04 350)",
         title="K-beauty, found and sold online.",
         summary="I ran the online store for a UAE K-beauty retailer from start to finish, from getting it found on Google to the campaigns that got it sold.",
         tags=["Online shop", "Google search", "Campaigns"], cats=["ecommerce", "campaigns"],
         did=[("Running the shop", "Products, collections and offers, every day."),
              ("Google search", "Got shoppers in from Google without paying for every click."),
              ("Campaigns", "Campaigns that turned visits into orders.")],
         role="Part of my Shopify chapter, 2021 to 2023, when I ran beauty, fashion and fragrance stores from start to finish."),
    dict(slug="factory-of-sight", brand="fos", shot="fos", context="CRWD Dubai", tint="oklch(0.25 0.03 255)",
         title="An eyewear brand that sells on mood.",
         summary="Design for an eyewear brand, led by its campaign photos.",
         tags=["Design", "Campaign photos"], cats=["design", "campaigns", "ecommerce"],
         did=[("Design", "A dark, film-like look that lets the campaign photos sell.")],
         role=CRWD_ROLE),
    dict(slug="gamma-usa", brand="gamma", shot="gamma", context="CRWD Dubai", tint="oklch(0.92 0.03 250)",
         title="A clear story for an innovation consultancy.",
         summary="Brand and design for an innovation and strategy consultancy that works with SMEs.",
         tags=["Brand design", "Message"], cats=["design", "strategy"],
         did=[("Message", "A story built around the two problems its clients bring: how to innovate, and how to transform."),
              ("Design", "A clean, confident look to match.")],
         role=CRWD_ROLE),
    dict(slug="altara-group", brand="altara", shot=None, context="Altara Group · 2025", tint="oklch(0.93 0.025 70)",
         title="Five brands. One strategist.",
         summary="Law, travel, HR, wellness and social. Each got its own marketing plan and influencer plan, and I led the content team that made it happen.",
         tags=["Strategy", "Influencer plans", "Leading content"], cats=["strategy", "social"],
         did=[("A plan for every brand", "Each of the five brands got its own marketing plan."),
              ("Influencer plans", "A dedicated influencer plan for each brand."),
              ("Leading content", "I led the content team that made it happen.")],
         role="Five brands under one group, across law, travel, HR, wellness and social, each with its own audience.",
         sub=["altarasocial", "altaralaw", "elite", "hrprime", "amedanca"]),
    dict(slug="elite-supplements", brand="elite", shot="elite", context="Altara Group · 2025", tint="oklch(0.9 0.05 285)",
         title="A supplements brand with a plan behind it.",
         summary="A marketing plan, an influencer plan and brand work for a UAE sports-supplements shop.",
         tags=["Strategy", "Influencer plan", "Brand"], cats=["strategy", "branding", "social", "ecommerce"],
         did=[("Strategy", "Who the store is for and how it wins them."),
              ("Influencer plan", "Which creators to work with, and how."),
              ("Brand", "A consistent look and voice across the store and social.")],
         role="One of the five Altara Group brands I ran strategy for in 2025."),
    dict(slug="home-maintenance-experts", brand="hme", shot=None, context="2023–2025", tint="oklch(0.93 0.03 160)",
         title="From clicks to booked jobs.",
         summary="A Dubai home-services brand needed customers, not likes. I built the strategy, content and promotions that turned homeowners into bookings.",
         tags=["Strategy", "Content", "Promotions"], cats=["strategy", "campaigns", "social"],
         did=[("Strategy", "A digital marketing plan built around bookings."),
              ("Content", "Content made for homeowners ready to book."),
              ("Promotions", "Promotions that turned interest into booked jobs.")],
         role="Two and a half years as digital marketing lead for a Dubai home-services brand."),
    dict(slug="hazo-branding", brand="hazo", shot=None, context="Uganda · 2020", tint="oklch(0.25 0.01 20)",
         title="Where I learned what makes people stop scrolling.",
         summary="Social content and the content calendar for a branding house in Uganda. My first brand job, and where the question behind all my work started.",
         tags=["Social content", "Content calendar"], cats=["social"],
         did=[("Social content", "Posts, captions and visuals for the studio’s social accounts."),
              ("Content calendar", "Planning what goes out, when, and why.")],
         role="Why do some posts sell and others don’t? This is where I started asking."),
]
HOME_FEATURED = ["engage-clinic", "traders-financial-group", "ccea", "lamise-beauty", "factory-of-sight", "gamma-usa"]
HOME_STRATEGY = ["altara-group", "elite-supplements"]
MORE_BRANDS = ["emmaship", "dessecrew", "avalar", "aureum", "tradershub", "klowe", "talentec", "altarasocial", "altaralaw", "hrprime", "amedanca", "crwd"]
LOGO_WALL = ["engage", "tfg", "ccea", "lamise", "fos", "gamma", "emmaship", "dessecrew", "avalar", "aureum", "hrprime", "hme", "elite", "altarasocial", "altaralaw", "amedanca", "talentec", "crwd"]
FILTERS = [("all", "All work"), ("branding", "Branding"), ("design", "Design"), ("ecommerce", "Online shops"),
           ("social", "Social & content"), ("campaigns", "Campaigns"), ("strategy", "Strategy")]

SERVICES = [
    ("Marketing strategy", "Big ideas with a business case behind every one."),
    ("Campaign launches", "Planned, launched and tracked, from the first post to the last sale."),
    ("Branding & design", "One voice, one look, everywhere your customer looks."),
    ("Social & influencer", "Campaigns people talk about, built on a real plan."),
    ("Getting found online", "Found on Google, named by AI, chosen by customers."),
    ("Creative lead", "I write the idea. Directors, editors and designers shoot it."),
]

CHAPTERS = [  # year, headline, where, what I did, brands shown
    ("2020", "Learned what makes people stop scrolling.", "Hazo Branding · Uganda",
     ["Social content", "The content calendar", "Posts, captions & visuals", "One big question: why do some posts sell?"], []),
    ("2021", "Learned what makes them buy.", "Shopify stores · 2021–2023",
     ["Worked on e-commerce brands", "Ran stores from start to finish", "Got them found on Google", "Campaigns that got them sold", "Beauty, fashion & fragrance"], ["lamise", "shopify"]),
    ("2023", "Sold digital products and ran the campaigns behind them.", "Digital products & campaigns · 2023–2025",
     ["Sold digital products", "Ran campaigns", "Turned attention into sales"], ["hme"], "Also: Home Experts, strategy, content and promotions"),
    ("2025", "Ran strategy for five brands at once.", "Altara Group",
     ["5 marketing plans", "5 influencer plans", "Led the content team", "Law, travel, HR, wellness & social"], ["altarasocial", "altaralaw", "elite", "hrprime", "amedanca"]),
    ("Now", "Leading the plan, the brand and the team.", "CRWD Dubai · Marketing Manager",
     ["Marketing strategy", "Campaign launches", "Rebrands & design", "Paid ads", "Social & content", "Leading the team"], ["engage", "tfg", "ccea", "fos", "gamma", "tradershub", "klowe", "emmaship", "dessecrew", "avalar", "aureum"]),
]

# ---------------------------------------------------------------- HELPERS
e = html.escape
ARROW = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ARROW_UP = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>'
BACK = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>'
MAIL = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>'
IN = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 10v7M7 7v.01M11 17v-4a2.5 2.5 0 0 1 5 0v4M11 10v7"/></svg>'
WA = '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1.3-4A8 8 0 1 1 8 18.7z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5l1-1.5-2-1-1 .8a4 4 0 0 1-2-2l.8-1-1-2z"/></svg>'
for _p in PROJECTS:
    for _cat in ("social", "campaigns"):
        if _cat not in _p["cats"]:
            _p["cats"].append(_cat)
P = {p["slug"]: p for p in PROJECTS}
# brands without a project page, shown under the Social & content filter
SOCIAL_BRANDS = ["emmaship", "dessecrew", "avalar", "aureum", "tradershub", "klowe", "altarasocial", "altaralaw", "hrprime", "amedanca", "talentec", "crwd"]


class Ctx:
    def __init__(self, mode):
        self.mode = mode  # "dist" or "preview"

    def href(self, route):
        if self.mode == "dist":
            return "/" + route if route else "/"
        return "#" + (route.replace("/", "-") if route else "home")

    def asset(self, name):
        return ("/assets/" if self.mode == "dist" else "assets/") + name


def initials(name):
    words = [w for w in name.replace("&", "").split() if w[0].isalpha()]
    if len(words) == 1:
        return words[0][:2].upper()
    return (words[0][0] + words[1][0]).upper()


def is_dark(tint):
    return float(tint.split("(")[1].split()[0]) < 0.5


def mark(c, key, size=""):
    name, logo, _, _ = BRANDS[key]
    if logo:
        return f'<span class="mark{size}"><img src="{c.asset(logo)}" alt=""></span>'
    return f'<span class="mark{size} mono" aria-hidden="true">{e(initials(name))}</span>'


def brand_tile(c, key, show_desc=False):
    name, _, site, desc = BRANDS[key]
    inner = mark(c, key) + f'<span class="bt-text"><span class="bt-name">{e(name)}</span>' + \
        (f'<span class="bt-desc">{e(desc)}</span>' if show_desc else "") + "</span>"
    if site:
        return f'<a class="btile" href="{site}" target="_blank" rel="noopener">{inner}<span class="sr">(opens in a new tab)</span></a>'
    return f'<div class="btile">{inner}</div>'


def browser(c, shot, alt, eager=False):
    load = "" if eager else ' loading="lazy"'
    return (f'<div class="browser"><div class="browser-bar" aria-hidden="true"><i></i><i></i><i></i></div>'
            f'<img src="{c.asset("shots/" + shot + "-d.jpg")}" alt="{e(alt)}" width="1280" height="800"{load}></div>')


def phone(c, shot, alt, eager=False):
    load = "" if eager else ' loading="lazy"'
    return f'<div class="phone"><img src="{c.asset("shots/" + shot + "-m.jpg")}" alt="{e(alt)}" width="600" height="1299"{load}></div>'


def cover(c, p, big=False, eager=False):
    name = BRANDS[p["brand"]][0]
    dark = " on-dark" if is_dark(p["tint"]) else ""
    if p["shot"]:
        inner = browser(c, p["shot"], f"{name} website on desktop", eager) + phone(c, p["shot"], f"{name} website on mobile", eager)
        return f'<div class="cover cover-shot{" big" if big else ""}{dark}" style="--tint:{p["tint"]}">{inner}</div>'
    subs = p.get("sub")
    if subs:
        inner = '<div class="cover-marks">' + "".join(mark(c, k, " lg") for k in subs) + "</div>"
    else:
        inner = mark(c, p["brand"], " xl")
    return f'<div class="cover cover-brand{" big" if big else ""}{dark}" style="--tint:{p["tint"]}">{inner}<span class="cover-name">{e(name)}</span></div>'


def chips(tags):
    return '<ul class="chips">' + "".join(f"<li>{e(t)}</li>" for t in tags) + "</ul>"


def pcard(c, slug, size=""):
    p = P[slug]
    name = BRANDS[p["brand"]][0]
    return (f'<a class="pcard{size}" href="{c.href("work/" + slug)}" data-cats="{" ".join(p["cats"])}">{cover(c, p)}'
            f'<div class="pcard-meta"><p class="pcard-client"><span>{e(name)}</span><span class="muted">{e(p["context"])}</span></p>'
            f'<h3 class="pcard-title">{e(p["title"])}</h3>{chips(p["tags"])}</div></a>')


def bcard(c, key):
    name, _, site, desc = BRANDS[key]
    cov = f'<div class="cover cover-brand" style="--tint:oklch(0.93 0.02 235)">{mark(c, key, " xl")}<span class="cover-name">{e(name)}</span></div>'
    meta = (f'<div class="pcard-meta"><p class="pcard-client"><span>{e(name)}</span></p>'
            f'<h3 class="pcard-title">{e(desc)}</h3>{chips(["Social & content", "Campaigns"])}</div>')
    attrs = f'class="pcard bcard" data-cats="social campaigns" data-only="social campaigns" hidden'
    if site:
        return f'<a {attrs} href="{site}" target="_blank" rel="noopener">{cov}{meta}</a>'
    return f'<div {attrs}>{cov}{meta}</div>'


def section(inner, cls=""):
    return f'<section class="sec {cls}"><div class="wrap">{inner}</div></section>'


def eyebrow(t):
    return f'<p class="eyebrow">{e(t)}</p>'


def head(eb, title, more_href=None, more_label=None, c=None):
    link = f'<a class="tlink" href="{more_href}">{more_label} {ARROW}</a>' if more_href else ""
    return f'<div class="sec-head"><div>{eyebrow(eb)}<h2 class="display-2">{title}</h2></div>{link}</div>'


def cta(c):
    return section(f'''<div class="cta">{eyebrow("Let’s talk")}
<h2 class="display-2">Got a brand with big plans?</h2>
<a class="btn" href="{c.href("contact")}">Start a conversation {ARROW_UP}</a></div>''', "sec-cta")


def services():
    return '<div class="services">' + "".join(
        f'<div class="svc"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in SERVICES) + "</div>"


def logo_wall(c):
    return '<ul class="logowall">' + "".join(
        f'<li title="{e(BRANDS[k][0])}"><img src="{c.asset(BRANDS[k][1])}" alt="{e(BRANDS[k][0])}"></li>' for k in LOGO_WALL) + "</ul>"


def portrait_x(c, cls=""):
    return (f'<figure class="px {cls}"><div class="px-arch" aria-hidden="true"><span class="px-orb"></span></div>'
            f'<img class="px-img" src="{c.asset("tracy-cutout.webp")}" alt="Portrait of Tracy Najjingo" width="712" height="823">'
            f'<span class="px-tag px-tag-a" aria-hidden="true"><i></i>Brand &amp; marketing</span>'
            f'<span class="px-tag px-tag-b" aria-hidden="true"><i></i>Dubai · since 2020</span></figure>')


CHAPTER_LINKS = {"Now": ["crwd"], "2025": ["altarasocial"], "2021": ["shopify"], "2020": ["hazo"]}


def chapter_links(year):
    keys = [k for k in CHAPTER_LINKS.get(year, []) if BRANDS[k][2]]
    if not keys:
        return ""
    return '<p class="jx-links">' + "".join(
        f'<a href="{BRANDS[k][2]}" target="_blank" rel="noopener">Visit {e("Shopify" if k == "shopify" else BRANDS[k][0])} {ARROW_UP}</a>' for k in keys) + "</p>"


def journey(c, uid):
    CH = list(reversed(CHAPTERS))  # newest first: Now, then back in time
    reel = "".join(f'<span>{e(y)}</span>' for y, *_ in CH)
    tabs = "".join(f'<button type="button" role="tab" class="jx-tab" id="{uid}-tab-{i}" aria-controls="{uid}-panel-{i}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}" data-sub="{e(ch[2].split(" · ")[0])}">{e(y)}</button>' for i, (y, *_), ch in ((i, ch, ch) for i, ch in enumerate(CH)))
    panels = ""
    for i, (y, line, where, did, brands, *rest) in enumerate(CH):
        cards = "".join(f'<li style="--i:{k}">{e(d)}</li>' for k, d in enumerate(did))
        note = f'<span class="jx-note">{e(rest[0])}</span>' if rest else ""
        logos = ('<div class="jx-brands">' + "".join(mark(c, b, " sm") for b in brands) + note + "</div>") if brands else ""
        panels += (f'<div class="jx-panel" role="tabpanel" id="{uid}-panel-{i}" aria-labelledby="{uid}-tab-{i}"{"" if i == 0 else " hidden"}>'
                   f'<p class="jx-where">{e(where)}</p><h3 class="jx-line">{e(line)}</h3>{chapter_links(y)}'
                   f'<p class="eyebrow jx-did-label">What I did</p><ul class="jx-cards">{cards}</ul>{logos}</div>')
    return f'''<div class="jx" data-journey>
<div class="jx-stage">
  <div class="jx-glow" aria-hidden="true"><i></i><i></i><i></i></div>
  <div class="jx-orb">
    <svg class="jx-ring" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="48" pathLength="100"/></svg>
    <div class="jx-year" aria-hidden="true"><div class="jx-reel">{reel}</div></div>
    <span class="jx-sub" aria-hidden="true">{e(CH[0][2].split(" · ")[0])}</span>
  </div>
</div>
<div class="jx-tabs" role="tablist" aria-label="Years">{tabs}<button type="button" class="jx-play" aria-label="Pause the timeline" data-playing="true"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path class="i-pause" d="M9 6v12M15 6v12"/><path class="i-play" d="M8 5l11 7-11 7z"/></svg></button></div>
<div class="jx-panels">{panels}</div>
</div>'''


# ---------------------------------------------------------------- PAGES
PROCESS = [
    ("Listen", "I start with the customer: who buys, why, and what stops them."),
    ("Plan", "I set the marketing plan: who to talk to, where, what to spend and what success looks like."),
    ("Brand & design", "I shape how the brand looks and sounds, and lead the designers who make it."),
    ("Launch", "I launch the campaign: posts, influencers, ads and the dates they go live."),
    ("Improve", "I watch what sells, drop what doesn’t and spend more on what works."),
]


def process():
    return '<ol class="process">' + "".join(
        f'<li><span class="pr-n">0{i}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(PROCESS, 1)) + "</ol>"


def page_home(c):
    hero = f'''<section class="hero"><div class="wrap hero-grid">
<div class="hero-copy">{eyebrow("Brand & marketing strategist · Dubai")}
<h1 class="display-1 hero-name notranslate">Tracy Najjingo</h1>
<div class="actions"><a class="btn" href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">{WA} WhatsApp me</a><a class="btn btn-ghost" href="mailto:{EMAIL}">{MAIL} Email me</a><a class="tlink" href="#journey">My journey {ARROW}</a></div></div>
{portrait_x(c, "px-hero")}
</div></section>'''
    story = section(head("My journey", "Six years, one question.", c.href("about"), "Read my story") + journey(c, "jx-home"), "sec-journey")
    story = story.replace('<section class="sec sec-journey">', '<section class="sec sec-journey" id="journey">', 1)
    how = section(head("How I work", "Plan first. Then launch.") + process(), "sec-process")
    strategy = section(head("Strategy & campaigns", "Strategies I’ve set. Campaigns I’ve launched.") +
                       '<div class="pgrid">' + "".join(pcard(c, s) for s in HOME_STRATEGY) + "</div>")
    featured = section(head("Selected work", "Brands I’ve shaped.", c.href("work"), "All projects") +
                       '<div class="pgrid">' + "".join(pcard(c, s) for s in HOME_FEATURED) + "</div>", "sec-work")
    logos = section(f'<div class="logos-head">{eyebrow("Trusted by")}<p class="muted">23 brands and counting, across the UAE and Uganda.</p></div>' + logo_wall(c), "sec-tight")
    return hero + story + how + strategy + featured + logos + cta(c)


def page_work(c):
    filt = '<div class="filters" role="group" aria-label="Filter projects">' + "".join(
        f'<button type="button" class="chip-btn" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{e(t)}</button>' for k, t in FILTERS) + "</div>"
    grid = '<div class="pgrid" id="project-grid">' + "".join(pcard(c, p["slug"]) for p in PROJECTS) + "".join(bcard(c, k) for k in SOCIAL_BRANDS) + "</div>"
    top = section(eyebrow("Work") + '<h1 class="display-1">Brands I’ve <em>moved.</em></h1>' +
                  '<p class="lede">Marketing strategy, brand design and campaign launches for brands across the UAE and Uganda. Pick a discipline or browse everything.</p>' + filt + grid, "sec-first")
    prog = section(f'<div class="soon">{eyebrow("In progress")}<h2 class="display-3">A hotel guests can’t wait to check into.</h2><p class="lede-sm">I’m shaping the strategy and the creative vision behind a new hotel brand. More soon.</p></div>', "sec-tight")
    more = section(head("More brands", "Also worked with.") + '<div class="blist">' + "".join(brand_tile(c, k, True) for k in MORE_BRANDS) + "</div>")
    return top + prog + more + cta(c)


def page_about(c):
    hero = section(
                   f'<div class="about-grid">{portrait_x(c, "px-about")}<div class="about-copy story"><h1 class="story-title">My journey</h1><p class="lede story-lead">I started as a social media manager in Uganda. I had a phone full of drafts, a content calendar and a lot of curiosity. Every post taught me something about people: what makes them stop, what makes them care and what makes them come back.</p><p class="story-p">Then I stepped into e-commerce. I ran online stores for beauty, fashion and perfume brands, from product pages to getting found on Google to the first sale of the day. That was where I learned that a beautiful brand still needs a reason to click “buy.”</p><p class="story-p">From stores I moved into campaigns. In Dubai I helped a home-services business turn attention into real customers and booked jobs. Then I took on five brands at once, across law, travel, HR, wellness and social, each with its own audience and its own voice.</p><p class="story-p">Today I set the strategy and lead the team. As Marketing Manager at <a class="story-link" href="https://crwdmarketing.com/ae" target="_blank" rel="noopener">CRWD Dubai</a>, I guide marketing teams and campaigns for brands across the UAE. I set the vision, and directors, editors and designers bring it to life. AI now works alongside us, helping brands get found faster, create more and grow with the right tools.</p><p class="story-p">I’m proud of every brand that trusted me along the way. Each one taught me something, and each one is part of this story.</p><a class="tlink" href="{c.href("work")}">See the work {ARROW}</a></div></div>', "sec-first sec-about-hero")
    story = section(head("Year by year", "Six years, one question.") + journey(c, "jx-about"), "sec-journey")
    how = section(head("How I work", "Plan first. Then launch.") + process()) + section(head("What I do", "I build the plan. My team builds the magic.") + services())
    return hero + story + how + cta(c)


def contact_buttons(c):
    b = []
    if WHATSAPP:
        b.append(f'<a class="cbtn dark" href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener"><span class="cbtn-ic">{WA}</span>WhatsApp {WHATSAPP_LABEL} {ARROW_UP}</a>')
    b.append(f'<a class="cbtn {"light" if WHATSAPP else "dark"}" href="mailto:{EMAIL}"><span class="cbtn-ic">{MAIL}</span>{EMAIL} {ARROW_UP}</a>')
    b.append(f'<a class="cbtn light" href="{LINKEDIN}" target="_blank" rel="noopener"><span class="cbtn-ic">{IN}</span>{LINKEDIN_LABEL} {ARROW_UP}</a>')
    return '<div class="cbtns">' + "".join(b) + "</div>"


def page_contact(c):
    form = f'''<form class="cform" id="contact-form" novalidate>
<h2 class="form-title">Or send a message</h2>
<div class="frow"><label for="cf-name">Name</label><input id="cf-name" name="name" autocomplete="name" required></div>
<div class="frow"><label for="cf-email">Email</label><input id="cf-email" name="email" type="email" autocomplete="email" required></div>
<div class="frow"><label for="cf-company">Company <span class="opt">(optional)</span></label><input id="cf-company" name="company" autocomplete="organization"></div>
<div class="frow"><label for="cf-message">What are you working on?</label><textarea id="cf-message" name="message" rows="5" required></textarea></div>
<button class="btn" type="submit">Send message {ARROW_UP}</button>
<p class="form-status" id="cf-status" role="status" aria-live="polite"></p>
</form>'''
    return section(eyebrow("Contact") + '<h1 class="display-1">Got a brand with big plans? <em>Let’s talk.</em></h1>' +
                   f'<div class="contact-grid"><div><p class="lede">Based in Dubai, UAE. Working with brands across the UAE and beyond. I reply within one working day.</p>{contact_buttons(c)}</div>{form}</div>', "sec-first")


def page_project(c, i):
    p = PROJECTS[i]
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    name, _, site, _ = BRANDS[p["brand"]]
    visit = f'<a class="btn" href="{site}" target="_blank" rel="noopener">Visit the live site {ARROW_UP}</a>' if site and p["shot"] else ""
    top = section(f'''<a class="tlink back" href="{c.href("work")}">{BACK} All work</a>
<div class="case-brand top">{mark(c, p["brand"], " sm")}<span>{e(name)}</span><span class="dot">{e(p["context"])}</span></div>
<h1 class="display-1">{e(p["title"])}</h1>
<div class="proj-intro"><p class="lede">{e(p["summary"])}</p><div class="proj-side">{chips(p["tags"])}{visit}</div></div>''', "sec-first sec-proj")
    hero = f'<section class="proj-hero"><div class="wrap">{cover(c, p, big=True, eager=True)}</div></section>'
    did = section(eyebrow("What I did") + '<ol class="did">' + "".join(
        f'<li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in p["did"]) + "</ol>")
    role_inner = f'<div class="role">{eyebrow("My role" if p["shot"] else "The context")}<p class="brief">{e(p["role"])}</p></div>'
    if p["shot"]:
        role = section(f'<div class="role-grid">{role_inner}{phone(c, p["shot"], f"{name} on mobile")}</div>')
    else:
        role = section(role_inner)
    out = top + hero + did + role
    if p.get("sub"):
        out += section(eyebrow("The five brands") + '<div class="blist">' + "".join(brand_tile(c, k, True) for k in p["sub"]) + "</div>")
    out += section(f'''<a class="next" href="{c.href("work/" + nxt["slug"])}"><span class="next-copy"><span class="eyebrow">Next project</span>
<span class="next-name">{e(BRANDS[nxt["brand"]][0])}</span><span class="display-3">{e(nxt["title"])}</span><span class="tlink">View project {ARROW}</span></span>{cover(c, nxt)}</a>''')
    return out + cta(c)


PAGES = [
    ("", "Tracy Najjingo · Brand & Marketing Strategist, Dubai",
     "Tracy Najjingo, brand and marketing strategist in Dubai. Marketing strategy, brand design and campaign launches for brands including Engage Clinic, Traders Financial Group, CCEA, Lamise Beauty and more.", page_home),
    ("work", "Work · Tracy Najjingo",
     "Marketing strategy, rebrands, brand design and campaign launches by Tracy Najjingo for brands across the UAE and Uganda.", page_work),
    ("about", "About Tracy Najjingo · From Uganda to Dubai",
     "From a branding studio in Uganda to leading marketing at CRWD Dubai: the story of brand and marketing strategist Tracy Najjingo.", page_about),
    ("contact", "Contact Tracy Najjingo · Brand & Marketing in Dubai",
     "Got a brand with big plans? Get in touch with Tracy Najjingo on WhatsApp, email or LinkedIn.", page_contact),
] + [("work/" + p["slug"], f'{BRANDS[p["brand"]][0]} · Tracy Najjingo', p["summary"], (lambda i: lambda c: page_project(c, i))(i))
     for i, p in enumerate(PROJECTS)]


LANGUAGES = [("en", "EN · English"), ("ar", "AR · العربية"), ("fr", "FR · Français"), ("ru", "RU · Русский"),
             ("zh-CN", "ZH · 中文"), ("hi", "HI · हिन्दी"), ("es", "ES · Español"), ("de", "DE · Deutsch"),
             ("it", "IT · Italiano"), ("pt", "PT · Português"), ("tr", "TR · Türkçe"), ("sw", "SW · Kiswahili"), ("lg", "LG · Luganda")]


def nav(c):
    links = "".join(f'<a href="{c.href(r)}" data-nav="{r}">{t}</a>' for r, t in [("work", "Work"), ("about", "About"), ("contact", "Contact")])
    opts = "".join(f'<option value="{code}">{label}</option>' for code, label in LANGUAGES)
    lang = (f'<label class="lang notranslate" title="Language"><span class="sr">Language</span>'
            f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>'
            f'<span class="lang-code" aria-hidden="true">EN</span><select id="lang-select" aria-label="Choose a language">{opts}</select></label>')
    return f'<header class="nav"><nav class="nav-pill" aria-label="Main"><a class="logo notranslate" href="{c.href("")}">Tracy Najjingo</a><div class="nav-links">{links}{lang}</div></nav></header><div id="google_translate_element" hidden></div>'


def footer(c):
    wa = f'<a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">WhatsApp</a>' if WHATSAPP else ""
    float_btn = (f'<a class="float-mail" href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">{WA}<span>WhatsApp me</span></a>' if WHATSAPP
                 else f'<a class="float-mail" href="mailto:{EMAIL}">{MAIL}<span>{EMAIL}</span></a>')
    return f'''<footer class="foot"><div class="wrap"><div class="foot-top"><div><p class="logo">Tracy Najjingo</p><p class="foot-sub">Brand &amp; marketing strategist · Dubai, UAE</p></div>
<div class="foot-links"><a href="{c.href("work")}">Work</a><a href="{c.href("about")}">About</a><a href="{c.href("contact")}">Contact</a><a href="mailto:{EMAIL}">{EMAIL}</a>{wa}<a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></div></div>
<p class="copy">© 2026 Tracy Najjingo. Website screenshots show live client sites.</p></div></footer>{float_btn}'''


FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@300;400;500;600&family=Inter:wght@400;500;600&display=swap">'


def build():
    css = open(os.path.join(ROOT, "src", "styles.css")).read()
    js = open(os.path.join(ROOT, "src", "site.js")).read().replace("__EMAIL__", EMAIL)

    # ---- dist (multi-page)
    dist = os.path.join(ROOT, "dist")
    shutil.rmtree(dist, ignore_errors=True)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(dist, "assets"))
    open(os.path.join(dist, "styles.css"), "w").write(css)
    open(os.path.join(dist, "site.js"), "w").write(js)
    c = Ctx("dist")
    person = {"@context": "https://schema.org", "@type": "Person", "name": "Tracy Najjingo", "jobTitle": "Brand & Marketing Strategist",
              "address": {"@type": "PostalAddress", "addressLocality": "Dubai", "addressCountry": "AE"}, "email": EMAIL, "sameAs": [LINKEDIN], "url": SITE_URL}
    for route, title, desc, fn in PAGES:
        url = SITE_URL + ("/" + route if route else "/")
        ld = f'<script type="application/ld+json">{json.dumps(person)}</script>' if route == "" else ""
        doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{OG_IMAGE}"><meta name="twitter:card" content="summary_large_image">
{FONTS}<link rel="stylesheet" href="/styles.css">{ld}</head>
<body data-route="{route}">{nav(c)}<main id="main">{fn(c)}</main>{footer(c)}<script src="/site.js"></script></body></html>'''
        d = os.path.join(dist, route)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(doc)
    home_html = open(os.path.join(dist, "index.html")).read()
    open(os.path.join(dist, "404.html"), "w").write(home_html)
    open(os.path.join(dist, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
        "".join(f"<url><loc>{SITE_URL}/{r}</loc></url>" for r, *_ in PAGES) + "</urlset>")
    open(os.path.join(dist, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")

    # ---- preview (one page, hash routes, assets alongside)
    prev_dir = os.path.join(ROOT, "preview")
    shutil.rmtree(prev_dir, ignore_errors=True)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(prev_dir, "assets"))
    c = Ctx("preview")
    views = "".join(f'<div class="view" data-view="{c.href(r)[1:]}" data-title="{e(t)}"{"" if r == "" else " hidden"}>{fn(c)}</div>' for r, t, _, fn in PAGES)
    prev = f'''<title>Tracy Najjingo Portfolio</title><meta name="claude:viewport-fit-sides" content="cover">
{FONTS}<style>{css}</style>{nav(c)}<main id="main">{views}</main>{footer(c)}<script>{js}</script>'''
    open(os.path.join(prev_dir, "index.html"), "w").write(prev)
    print("built", len(PAGES), "pages")


if __name__ == "__main__":
    build()
