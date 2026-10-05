#!/usr/bin/env python3
"""
Builds the Google Ads landing pages from one template.

Usage (from the repo root):
    python3 lp-src/build_landing_pages.py                 # Conservative, all pages
    python3 lp-src/build_landing_pages.py standard        # Standard version
    python3 lp-src/build_landing_pages.py conservative piles

Output: piles.html, fistula.html, varicose-veins.html in the repo root.
Vercel serves them at /piles, /fistula and /varicose-veins.
The copy is the copy in the approval document. Change it here, then rebuild.
"""
import sys
import html
import urllib.parse
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent

PHONE_DISPLAY = "+91 81052 32787"
PHONE_TEL = "+918105232787"
WA_NUMBER = "918105232787"
CLINIC = "Dr. Kishan's Surgical Care"
DOCTOR = "Dr. Kishan Rao"
SPECIALTY = "General, Laparoscopic & LASER Surgeon"

MAPS = "https://www.google.com/maps/search/?api=1&query="
LOCATIONS = [
    {
        "name": CLINIC,
        "where": "Inside Bhat's Nursing Home, Mannagudda, Mangalore",
        "short": "Mangalore",
        "day": "Monday to Friday",
        "time": "10 am to 1 pm and 3 pm to 6 pm",
        "map": MAPS + urllib.parse.quote("Bhat's Nursing Home, Mannagudda, Mangaluru, Karnataka"),
    },
    {
        "name": "Adarsha Hospital",
        "where": "Puttur",
        "short": "Puttur",
        "day": "Saturday",
        "time": "9 am to 11 am",
        "map": MAPS + urllib.parse.quote("APMC Road, Bolwar, Puttur, Karnataka 574201"),
    },
    {
        "name": "Namma Arogyadhama",
        "where": "Ayyanakatte",
        "short": "Ayyanakatte",
        "day": "Sunday",
        "time": "9 am to 5 pm",
        "map": MAPS + urllib.parse.quote("Ayyanakatte, near Bellare, Sullia Taluk, Karnataka"),
    },
]

COMMON_FAQS = [
    ("How do I book an appointment?",
     f"Call {PHONE_DISPLAY} or send a WhatsApp message. We will confirm your day, time and location."),
    ("What should I bring?",
     "Any earlier reports, scans and prescriptions, along with a list of the medicines you take."),
    ("Is LASER treatment right for everyone?",
     "No. Suitability depends on your examination and, where needed, tests. You will be told plainly whether LASER or another approach fits your case."),
    ("What will it cost?",
     "Cost depends on your condition, the treatment advised and the hospital. After your assessment you will be guided on what to expect before you decide anything."),
]

STEPS = [
    ("A careful examination",
     "You are heard first, then examined with respect for your privacy. If needed, tests are advised to rule out other causes."),
    ("A clear explanation",
     "You are told what the problem is, what your options are and what each one involves, in plain language."),
    ("A plan that fits you",
     "Simple measures and medicines where they are enough. A procedure or surgery only when it is genuinely needed, with follow-up afterwards."),
]

DISCLAIMER = ("The information on this page is for general education and appointment guidance only. "
              "It is not a substitute for personal medical advice, diagnosis or treatment. "
              "Always consult a qualified clinician for individual care decisions. "
              "Surgical suitability and outcomes vary by patient.")

# ---------------------------------------------------------------- copy
PAGES = {
    "piles": {
        "file": "piles.html",
        "label": "piles",
        "title": f"Piles Treatment in Mangalore | LASER Options | {CLINIC}",
        "meta": "Piles treatment in Mangalore, including LASER options. A careful examination, a clear plan, and surgery only when it is truly needed. Call or WhatsApp to book.",
        "h1": "Piles Treatment in Mangalore, Including LASER Options",
        "sub": f"Piles are common, and you do not have to suffer in silence. Visit {CLINIC} for a careful examination and a clear plan, with surgery only when it is truly needed.",
        "sub_standard": f"Piles are common, and you do not have to suffer in silence. Meet {DOCTOR} for a careful examination and a clear plan, with surgery only when it is truly needed.",
        "wa": "Hello, I would like to book a consultation for piles.",
        "familiar": [
            "Bleeding during bowel movements",
            "Itching or discomfort around the anus",
            "A swelling or lump near the anus",
            "Tissue that comes out during a bowel movement",
        ],
        "familiar_note": "Not every case of bleeding is piles. Only a proper examination can tell you what is really going on.",
        "understand_title": "Understanding piles",
        "understand": [
            ("What it is", "Piles are swollen blood vessels around the anus or lower rectum. They are common, and can range from mild irritation to bleeding, swelling or prolapse."),
            ("What can contribute", "Constipation, straining, sitting for long periods on the toilet, a low-fibre diet, pregnancy, obesity and repeated pressure during bowel movements can all contribute."),
        ],
        "options_title": "Treatment options for piles",
        "options": [
            ("To begin with", "Early piles are often managed with fibre, fluids, stool-softening measures and medicines."),
            ("If symptoms continue", "When symptoms persist, prolapse is significant or bleeding keeps returning, a procedure or surgery may be considered."),
            ("LASER options", "LASER-based treatment is one of the options offered for suitable cases, and you will be told honestly whether it is right for you."),
        ],
        "faq_title": "Questions about piles",
        "faqs": [
            ("Do I need surgery for piles?",
             "Not always. Many people are first advised simple measures and medicines. Surgery is recommended only when it is genuinely indicated, and you will be told why."),
            ("Is bleeding always a sign of piles?",
             "No. Bleeding can have other causes, which is why an examination matters. Depending on your age and symptoms, tests may be advised to rule out other causes."),
            ("How are piles diagnosed?",
             "Through a careful history and a local examination. In some cases, further tests such as proctoscopy, sigmoidoscopy or colonoscopy may be advised."),
        ],
    },
}

# ---------------------------------------------------------------- icons
ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1L6.6 10.8z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>'
ICON_WA = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 3.2a8.8 8.8 0 0 0-7.5 13.4L3.2 20.8l4.3-1.2A8.8 8.8 0 1 0 12 3.2Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M9 8.6c.2-.4.5-.4.8-.4.2 0 .4.2.5.4l.6 1.3c.1.2 0 .4-.1.6l-.5.6c.7 1.3 1.6 2.1 2.9 2.8l.6-.6c.2-.2.4-.2.6-.1l1.3.6c.2.1.4.3.4.5 0 .5-.4 1.2-1.1 1.4-.7.2-2.1.1-3.9-1.2-1.8-1.3-2.9-3-3.1-4.1-.1-.6.1-1.3.5-1.8Z" fill="currentColor"/></svg>'
ICON_CHECK = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.6"/><path d="M7.6 12.3l3 3 5.8-6.2" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_PIN = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 21s7-6.2 7-11.2A7 7 0 0 0 5 9.8C5 14.8 12 21 12 21Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><circle cx="12" cy="9.8" r="2.4" stroke="currentColor" stroke-width="1.7"/></svg>'

CSS = r"""
:root{--navy-950:#0B2E29;--navy-900:#123B34;--navy-800:#1A4740;--ivory-50:#EEE7D6;--ivory-100:#E6DCC3;--paper:#F6F1E4;--brass-500:#B08A3E;--brass-600:#8F6F2E;--ink:#182420;--ivory-text:#F3EEDD;--line:rgba(20,33,31,.12)}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{font-family:'Inter',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;color:var(--ink);background:var(--ivory-50);line-height:1.6;font-size:17px;-webkit-font-smoothing:antialiased;padding-bottom:86px}
h1,h2,h3{font-family:'Inter Tight','Inter',system-ui,sans-serif;font-weight:650;color:var(--navy-950);letter-spacing:-.012em;line-height:1.15}
ul{list-style:none}
.wrap{max-width:1060px;margin:0 auto;padding:0 20px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:54px;padding:0 24px;border-radius:6px;font:600 17px/1 'Inter',system-ui,sans-serif;text-decoration:none;border:1.5px solid var(--navy-950);cursor:pointer;transition:transform .12s ease,background .15s ease;white-space:nowrap}
.btn:active{transform:scale(.98)}
.btn svg{width:21px;height:21px;flex:none}
.btn-primary{background:var(--navy-950);color:var(--ivory-text)}
.btn-primary:hover{background:var(--navy-800)}
.btn-ghost{background:transparent;color:var(--navy-950)}
.btn-ghost:hover{background:rgba(11,46,41,.07)}

/* header */
.top{background:var(--ivory-50);border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:70px;padding-top:10px;padding-bottom:10px}
.brand{display:flex;align-items:center;gap:11px;text-decoration:none;min-width:0}
.brand img{width:44px;height:46px;flex:none;display:block}
.brand b{display:block;font:650 17px/1.15 'Inter Tight',system-ui,sans-serif;color:var(--navy-950)}
.brand span{display:block;font-size:12.5px;color:var(--brass-600);margin-top:3px;line-height:1.3}
.top .btn{display:none;min-height:46px;padding:0 18px;font-size:15.5px}
.top .btn svg{width:18px;height:18px}

/* hero */
.hero{background:linear-gradient(180deg,var(--ivory-50) 0%,var(--ivory-100) 100%);padding:34px 0 42px}
.hero-grid{display:grid;gap:28px}
.hero h1{font-size:clamp(31px,7.6vw,50px);letter-spacing:-.018em}
.lead{margin-top:16px;font-size:clamp(17.5px,2.4vw,20px);color:#27342f;max-width:34em}
.ctas{display:grid;gap:12px;margin-top:26px}
.chips{display:flex;flex-wrap:wrap;gap:10px 22px;margin-top:24px;font-size:15px;color:var(--navy-800);font-weight:500}
.chips li{display:flex;align-items:center;gap:8px}
.chips svg{width:19px;height:19px;color:var(--brass-600);flex:none}
.card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:22px 20px}
.sched h2{font-size:20px}
.sched ul{margin-top:12px}
.sched li{padding:13px 0;border-top:1px solid var(--line);display:grid;gap:2px}
.sched li:first-child{border-top:0;padding-top:4px}
.sched strong{font-weight:650;color:var(--navy-950)}
.sched span{font-size:15.5px;color:#3a4742}
.sched p{margin-top:8px;font-size:14.5px;color:#4a5651}

/* sections */
.sec{padding:50px 0}
.sec.alt{background:var(--paper)}
.sec h2{font-size:clamp(26px,4.8vw,36px)}
.prose p{margin-top:14px;max-width:44em;font-size:18px}
.center{text-align:center}
.center p{margin-left:auto;margin-right:auto}
.center .meet{margin-left:auto;margin-right:auto}
.two,.three{display:grid;gap:14px;margin-top:24px}
.tcard,.opt{background:#fff;border:1px solid var(--line);border-radius:12px;padding:24px 22px}
.tcard h3,.opt h3{font-size:19px;color:var(--brass-600)}
.tcard p,.opt p{margin-top:10px;font-size:17.5px;color:#27342f}
.opt.laser{background:#FBF6E6;border-color:var(--brass-500);border-top:3px solid var(--brass-500)}
.opt.laser h3{color:var(--navy-950)}
.tick-list{display:grid;gap:12px;margin-top:24px}
.tick-list li{display:flex;gap:13px;align-items:flex-start;background:#fff;border:1px solid var(--line);border-radius:10px;padding:15px 16px;font-weight:500}
.tick-list svg{width:23px;height:23px;flex:none;color:var(--brass-600);margin-top:1px}
.note{margin-top:24px;border-left:3px solid var(--brass-500);padding:4px 0 4px 16px;font-size:18.5px;color:var(--navy-900);max-width:40em}
.steps{display:grid;gap:14px;margin-top:26px}
.step{background:#fff;border:1px solid var(--line);border-radius:12px;padding:22px 20px}
.step .n{font:650 36px/1 'Inter Tight',sans-serif;color:var(--brass-500)}
.step h3{font-size:20px;margin-top:10px}
.step p{margin-top:8px;font-size:16.5px;color:#34413c}
.band{background:var(--ivory-100);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:38px 0;text-align:center}
.band h2{font-size:clamp(24px,4.4vw,32px)}
.band p{margin:10px auto 0;max-width:34em;font-size:18px;color:#2f3c37}
.band .ctas{max-width:460px;margin:22px auto 0}
.locs{display:grid;gap:14px;margin-top:26px}
.loc{background:#fff;border:1px solid var(--line);border-radius:12px;padding:22px 20px;display:flex;flex-direction:column;gap:4px}
.loc h3{font-size:19px}
.loc .where{color:var(--brass-600);font-size:15px;font-weight:500}
.loc .when{margin-top:10px;font-weight:600;color:var(--navy-950)}
.loc .time{color:#3a4742;font-size:16px}
.loc a{margin-top:14px;display:inline-flex;align-items:center;gap:7px;color:var(--navy-950);font-weight:600;font-size:15.5px;text-decoration:none;border-bottom:1.5px solid var(--brass-500);align-self:flex-start;padding-bottom:2px}
.loc a svg{width:18px;height:18px;color:var(--brass-600)}
.fine{margin-top:18px;font-size:15px;color:#4a5651}
.faq-group{margin-top:26px}
.faq-group h3{font-size:20px;margin-bottom:6px}
details{border-bottom:1px solid var(--line)}
summary{list-style:none;cursor:pointer;padding:18px 40px 18px 0;font:600 17.5px/1.35 'Inter',sans-serif;color:var(--navy-950);position:relative}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";position:absolute;right:4px;top:50%;transform:translateY(-50%);font:400 28px/1 'Inter',sans-serif;color:var(--brass-600)}
details[open] summary::after{content:"\2212"}
details p{padding:0 8px 20px 0;font-size:17px;color:#30403a;max-width:46em}
.meet{margin-top:18px;max-width:46em}
.meet .cred{margin-top:8px;color:var(--brass-600);font-weight:600}

/* footer */
.foot{padding:34px 0 28px;font-size:14px;color:#4a5651}
.foot p{max-width:56em}
.foot .row{margin-top:14px;display:flex;flex-wrap:wrap;gap:6px 18px}
.foot a{color:var(--navy-950);text-underline-offset:3px}

/* sticky bar, phones only */
.sticky{position:fixed;left:0;right:0;bottom:0;z-index:50;display:flex;gap:10px;padding:10px 12px calc(10px + env(safe-area-inset-bottom));background:rgba(238,231,214,.97);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);border-top:1px solid rgba(11,46,41,.16)}
.sticky .btn{flex:1;min-height:52px;padding:0 10px;font-size:16.5px}

@media(min-width:520px){
  .ctas{grid-template-columns:auto auto;justify-content:start}
  .band .ctas{grid-template-columns:1fr 1fr}
}
@media(min-width:700px){
  .top .btn{display:inline-flex}
  .two{grid-template-columns:1fr 1fr}
  .tick-list{grid-template-columns:1fr 1fr}
  .steps{grid-template-columns:repeat(3,1fr)}
  .locs{grid-template-columns:repeat(3,1fr)}
}
@media(min-width:900px){
  body{font-size:18px;padding-bottom:0}
  .sticky{display:none}
  .top{position:sticky;top:0;z-index:40}
  .top .wrap{min-height:76px}
  .hero{padding:58px 0 66px}
  .hero-grid{grid-template-columns:1.22fr .78fr;align-items:center;gap:56px}
  .sec{padding:68px 0}
  .three{grid-template-columns:repeat(3,1fr)}
  .faq-cols{display:grid;grid-template-columns:1fr 1fr;gap:0 56px}
}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.btn{transition:none}}
"""

BASE = Template("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title>
<meta name="description" content="${meta}">
<meta name="robots" content="noindex, follow">
<meta name="theme-color" content="#0B2E29">
<link rel="icon" type="image/png" sizes="32x32" href="/images/brand/favicon-32x32.png">
<link rel="apple-touch-icon" href="/images/brand/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Inter+Tight:wght@650&display=swap" rel="stylesheet">
<style>${css}</style>
</head>
<body>
${body}
<script src="/lp-track.js" defer></script>
</body>
</html>
""")


def e(text):
    return html.escape(text, quote=True)


def wa_url(text):
    return f"https://wa.me/{WA_NUMBER}?text=" + urllib.parse.quote(text)


def call_btn(loc, primary=True, label=None):
    cls = "btn btn-primary" if primary else "btn btn-ghost"
    text = label or f"Call {PHONE_DISPLAY}"
    return f'<a class="{cls}" href="tel:{PHONE_TEL}" data-conv="call" data-loc="{loc}">{ICON_PHONE}<span>{e(text)}</span></a>'


def wa_btn(loc, wa_text, primary=False, label="WhatsApp Us"):
    cls = "btn btn-primary" if primary else "btn btn-ghost"
    return f'<a class="{cls}" href="{e(wa_url(wa_text))}" target="_blank" rel="noopener" data-conv="whatsapp" data-loc="{loc}">{ICON_WA}<span>{e(label)}</span></a>'


def header(version):
    if version == "standard":
        name, sub = DOCTOR, SPECIALTY
    else:
        name, sub = CLINIC, "Mangalore, Puttur and Sullia"
    return f"""<header class="top">
  <div class="wrap">
    <a class="brand" href="/" aria-label="{e(name)}">
      <img src="/images/brand/logo-lp.png" alt="" width="44" height="46">
      <div><b>{e(name)}</b><span>{e(sub)}</span></div>
    </a>
    {call_btn("header", True, "Call Now")}
  </div>
</header>"""


def schedule_card():
    rows = "".join(
        f'<li><strong>{e(l["day"])}, {e(l["short"])}</strong><span>{e(l["time"])}</span></li>' for l in LOCATIONS
    )
    return f"""<aside class="card sched" aria-label="When you can visit">
  <h2>When you can visit</h2>
  <ul>{rows}</ul>
  <p>Consultations are by appointment. Please call or WhatsApp to confirm your slot.</p>
</aside>"""


def hero(p, version):
    sub = p["sub_standard"] if version == "standard" else p["sub"]
    chips = ["By appointment", "Mangalore, Puttur and Sullia", "Surgery only when truly needed"]
    chip_html = "".join(f"<li>{ICON_CHECK}<span>{e(c)}</span></li>" for c in chips)
    return f"""<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>{e(p["h1"])}</h1>
      <p class="lead">{e(sub)}</p>
      <div class="ctas">
        {call_btn("hero", True)}
        {wa_btn("hero", p["wa"])}
      </div>
      <ul class="chips">{chip_html}</ul>
    </div>
    {schedule_card()}
  </div>
</section>"""


def familiar(p):
    items = "".join(f"<li>{ICON_CHECK}<span>{e(x)}</span></li>" for x in p["familiar"])
    return f"""<section class="sec alt">
  <div class="wrap">
    <h2>Does this sound familiar?</h2>
    <ul class="tick-list">{items}</ul>
    <p class="note">{e(p["familiar_note"])}</p>
  </div>
</section>"""


def understand(p):
    cards = "".join(
        f'<div class="tcard"><h3>{e(lab)}</h3><p>{e(txt)}</p></div>' for lab, txt in p["understand"]
    )
    return f"""<section class="sec">
  <div class="wrap">
    <h2>{e(p["understand_title"])}</h2>
    <div class="two">{cards}</div>
  </div>
</section>"""


def steps():
    cards = "".join(
        f'<div class="step"><div class="n">{i}</div><h3>{e(t)}</h3><p>{e(d)}</p></div>'
        for i, (t, d) in enumerate(STEPS, 1)
    )
    return f"""<section class="sec alt">
  <div class="wrap">
    <h2>How your consultation works</h2>
    <div class="steps">{cards}</div>
  </div>
</section>"""


def options(p):
    cards = []
    for i, (lab, txt) in enumerate(p["options"]):
        cls = "opt laser" if i == len(p["options"]) - 1 else "opt"
        cards.append(f'<div class="{cls}"><h3>{e(lab)}</h3><p>{e(txt)}</p></div>')
    return f"""<section class="sec">
  <div class="wrap">
    <h2>{e(p["options_title"])}</h2>
    <div class="three">{"".join(cards)}</div>
  </div>
</section>"""


def band(p, loc, title, text):
    return f"""<section class="band">
  <div class="wrap">
    <h2>{e(title)}</h2>
    <p>{e(text)}</p>
    <div class="ctas">
      {call_btn(loc, True)}
      {wa_btn(loc, p["wa"])}
    </div>
  </div>
</section>"""


def about(version):
    if version == "standard":
        return f"""<section class="sec alt">
  <div class="wrap prose center">
    <h2>Meet your surgeon</h2>
    <div class="meet">
      <h3>{e(DOCTOR)}</h3>
      <p class="cred">{e(SPECIALTY)}<br>MBBS (BMC), MS (Gold Medalist), FMAS, DMAS</p>
      <p>{e(DOCTOR)} treats a wide range of general, laparoscopic and LASER surgical conditions in Mangalore. He explains every option clearly and recommends surgery only when it is genuinely indicated.</p>
    </div>
  </div>
</section>"""
    return f"""<section class="sec alt">
  <div class="wrap prose center">
    <h2>About the clinic</h2>
    <p>{e(CLINIC)} sees patients by appointment at three locations across Mangalore, Puttur and Sullia. Every visit begins with a careful assessment, and every recommendation comes with a clear explanation.</p>
  </div>
</section>"""


def locations():
    cards = "".join(
        f"""<div class="loc">
      <h3>{e(l["name"])}</h3>
      <div class="where">{e(l["where"])}</div>
      <div class="when">{e(l["day"])}</div>
      <div class="time">{e(l["time"])}</div>
      <a href="{e(l["map"])}" target="_blank" rel="noopener">{ICON_PIN}<span>Get Directions</span></a>
    </div>"""
        for l in LOCATIONS
    )
    return f"""<section class="sec">
  <div class="wrap">
    <h2>Where and when</h2>
    <div class="locs">{cards}</div>
    <p class="fine">Timings can change, so please call or WhatsApp to confirm before you visit.</p>
  </div>
</section>"""


def faq(p):
    def block(items):
        return "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in items)
    return f"""<section class="sec alt">
  <div class="wrap">
    <h2>Common questions</h2>
    <div class="faq-cols">
      <div class="faq-group"><h3>{e(p["faq_title"])}</h3>{block(p["faqs"])}</div>
      <div class="faq-group"><h3>Booking and visits</h3>{block(COMMON_FAQS)}</div>
    </div>
  </div>
</section>"""


def sticky(p):
    return f"""<div class="sticky">
  {call_btn("sticky", True, "Call Now")}
  {wa_btn("sticky", p["wa"], False, "WhatsApp")}
</div>"""


def build(key, version):
    p = PAGES[key]
    body = "\n".join([
        header(version),
        hero(p, version),
        familiar(p),
        understand(p),
        steps(),
        options(p),
        band(p, "mid", "Ready to talk?", "One call or one WhatsApp message is all it takes to book."),
        about(version),
        locations(),
        faq(p),
        band(p, "close", "Take the first step today",
             "One call or one WhatsApp message is all it takes. You will be examined carefully, your options explained clearly, and surgery advised only when it is truly needed."),
        f"""<footer class="foot">
  <div class="wrap">
    <p>{e(DISCLAIMER)}</p>
    <div class="row"><span>&copy; {e(CLINIC)}</span><a href="/">Main website</a></div>
  </div>
</footer>""",
        sticky(p),
    ])
    out = BASE.substitute(title=e(p["title"]), meta=e(p["meta"]), css=CSS, body=body)
    (ROOT / p["file"]).write_text(out, encoding="utf-8")
    print("built", p["file"], f"({version}, {len(out)//1024} KB)")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    version = "conservative"
    if args and args[0] in ("conservative", "standard"):
        version = args.pop(0)
    keys = args or list(PAGES)
    for k in keys:
        build(k, version)
