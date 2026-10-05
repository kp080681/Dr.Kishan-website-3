#!/usr/bin/env python3
"""
Builds the Google Ads landing pages from one template.

Design rule: the page has one job, a tap on Call or WhatsApp.
Everything above the fold is the keyword, one human line and two buttons.
Explanations live in collapsed questions, so they stay on the page for
Google and for patients who want depth, but nobody is forced to read them.

Usage (from the repo root):
    python3 lp-src/build_landing_pages.py                 # Conservative, all pages
    python3 lp-src/build_landing_pages.py standard        # Standard version
    python3 lp-src/build_landing_pages.py conservative piles

Output: piles.html, fistula.html, varicose-veins.html in the repo root.
Vercel serves them at /piles, /fistula and /varicose-veins.
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

# Shared answers, used on every page
QA_LASER = ("Is LASER treatment right for everyone?",
            "No. Suitability depends on your examination and, where needed, tests. You will be told plainly whether LASER or another approach fits your case.")
QA_COST = ("What will it cost?",
           "Cost depends on your condition, the treatment advised and the hospital. After your assessment you will be guided on what to expect before you decide anything.")
QA_BOOK = ("How do I book, and what should I bring?",
           f"Call {PHONE_DISPLAY} or send a WhatsApp message, and we will confirm your day, time and location. Bring any earlier reports, scans and prescriptions, and a list of the medicines you take.")

STEPS = [
    ("Careful examination", "Heard first, examined with respect for your privacy."),
    ("Clear explanation", "Your options, in plain language."),
    ("A plan that fits you", "Surgery only when it is genuinely needed."),
]

DISCLAIMER = ("The information on this page is for general education and appointment guidance only. "
              "It is not a substitute for personal medical advice, diagnosis or treatment. "
              "Always consult a qualified clinician for individual care decisions. "
              "Surgical suitability and outcomes vary by patient.")

# ---------------------------------------------------------------- copy
PAGES = {
    "piles": {
        "file": "piles.html",
        "title": f"Piles Treatment in Mangalore | LASER Options | {CLINIC}",
        "meta": "Piles treatment in Mangalore, including LASER options. A careful examination, a clear plan, and surgery only when it is truly needed. Call or WhatsApp to book.",
        "eyebrow": "Piles treatment in Mangalore",
        "h1": "Piles, handled with discretion and care.",
        "lead1": "Common, personal, and nothing to be embarrassed about.",
        "lead2": "A careful examination, a clear plan, and surgery only when truly needed.",
        "lead2_standard": f"Meet {DOCTOR} for a careful examination, a clear plan, and surgery only when truly needed.",
        "micro_laser": "LASER treatment options for suitable cases",
        "wa": "Hello, I would like to book a consultation for piles.",
        "familiar": [
            "Bleeding during bowel movements",
            "Itching or discomfort around the anus",
            "A swelling or lump near the anus",
            "Tissue that comes out during a bowel movement",
        ],
        "note": "Not every case of bleeding is piles. Only a proper examination can tell you what is really going on.",
        "laser": "LASER-based treatment is one of the options offered for suitable cases, and you will be told honestly whether it is right for you.",
        "qa": [
            ("What are piles?",
             "Piles are swollen blood vessels around the anus or lower rectum. They are common, and can range from mild irritation to bleeding, swelling or prolapse."),
            ("What can contribute to piles?",
             "Constipation, straining, sitting for long periods on the toilet, a low-fibre diet, pregnancy, obesity and repeated pressure during bowel movements can all contribute."),
            ("What are the treatment options?",
             "Early piles are often managed with fibre, fluids, stool-softening measures and medicines. When symptoms persist, prolapse is significant or bleeding keeps returning, a procedure or surgery may be considered."),
            ("Do I need surgery for piles?",
             "Not always. Many people are first advised simple measures and medicines. Surgery is recommended only when it is genuinely indicated, and you will be told why."),
            QA_LASER, QA_COST, QA_BOOK,
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
body{font-family:'Inter',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;color:var(--ink);background:var(--ivory-50);line-height:1.55;font-size:17px;-webkit-font-smoothing:antialiased;padding-bottom:86px}
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
.ctas{display:grid;gap:12px}

/* header */
.top{background:var(--ivory-50);border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:64px;padding-top:9px;padding-bottom:9px}
.brand{display:flex;align-items:center;gap:11px;text-decoration:none;min-width:0}
.brand img{width:42px;height:44px;flex:none;display:block}
.brand b{display:block;font:650 17px/1.15 'Inter Tight',system-ui,sans-serif;color:var(--navy-950)}
.brand span{display:block;font-size:12.5px;color:var(--brass-600);margin-top:3px;line-height:1.3}
.top .btn{display:none;min-height:46px;padding:0 18px;font-size:15.5px}
.top .btn svg{width:18px;height:18px}

/* hero */
.hero{background:linear-gradient(180deg,var(--ivory-50) 0%,var(--ivory-100) 100%);padding:26px 0 34px}
.hero-grid{display:grid;gap:24px}
.eyebrow{display:flex;align-items:center;gap:10px;margin-bottom:12px;font-size:14.5px;font-weight:600;color:var(--brass-600);letter-spacing:.01em}
.eyebrow::before{content:"";width:28px;height:1.5px;background:var(--brass-500);flex:none}
.hero h1{font-size:clamp(34px,9vw,58px);letter-spacing:-.02em;line-height:1.08}
.lead{margin-top:14px;font-size:clamp(18px,2.4vw,20px);color:#27342f;max-width:32em}
.lead b{display:block;color:var(--navy-950);font-weight:600;margin-bottom:4px}
.hero .ctas{margin-top:22px}
.micro{margin-top:16px;display:grid;gap:7px;font-size:14.5px;color:var(--navy-800);font-weight:500}
.micro span{display:flex;align-items:center;gap:8px}
.micro svg{width:18px;height:18px;color:var(--brass-600);flex:none}
.card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:22px 20px}
.sched{display:none}
.sched h2{font-size:20px}
.sched ul{margin-top:12px}
.sched li{padding:13px 0;border-top:1px solid var(--line);display:grid;gap:2px}
.sched li:first-child{border-top:0;padding-top:4px}
.sched strong{font-weight:650;color:var(--navy-950)}
.sched span{font-size:15.5px;color:#3a4742}
.sched p{margin-top:8px;font-size:14.5px;color:#4a5651}

/* sections */
.sec{padding:36px 0}
.sec.alt{background:var(--paper)}
.sec h2{font-size:clamp(25px,4.8vw,34px)}
.tick-list{display:grid;gap:8px;margin-top:18px}
.tick-list li{display:flex;gap:12px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:10px;padding:12px 14px;font-weight:500;font-size:16.5px}
.tick-list svg{width:22px;height:22px;flex:none;color:var(--brass-600)}
.note{margin-top:18px;border-left:3px solid var(--brass-500);padding:3px 0 3px 14px;font-size:17.5px;color:var(--navy-900);max-width:38em}
.sec .ctas{margin-top:22px}
.steps{margin-top:18px;background:#fff;border:1px solid var(--line);border-radius:12px;display:grid}
.step{display:flex;gap:14px;align-items:flex-start;padding:16px 18px;border-top:1px solid var(--line)}
.step:first-child{border-top:0}
.step .n{flex:none;width:34px;height:34px;border-radius:50%;border:1.5px solid var(--brass-500);color:var(--brass-600);font:650 17px/31px 'Inter Tight',sans-serif;text-align:center}
.step h3{font-size:18px}
.step p{margin-top:2px;font-size:16px;color:#34413c}
.strip{margin-top:14px;background:#FBF6E6;border:1px solid var(--brass-500);border-left-width:4px;border-radius:10px;padding:16px 18px;font-size:16.5px}
.strip b{color:var(--navy-950);font-weight:650}
.meet{margin-top:14px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:18px 20px}
.meet h3{font-size:19px}
.meet .cred{margin-top:4px;color:var(--brass-600);font-weight:600;font-size:15.5px}
.meet p{margin-top:8px;font-size:16.5px}
.where{margin-top:18px;background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden}
.row{padding:15px 18px;border-top:1px solid var(--line);display:grid;gap:8px}
.row:first-child{border-top:0}
.row b{font:650 17.5px/1.25 'Inter Tight',sans-serif;color:var(--navy-950)}
.row .sub{color:var(--brass-600);font-size:14.5px;font-weight:500;margin-top:2px}
.meta{display:flex;flex-wrap:wrap;align-items:center;gap:6px 16px;font-size:15.5px;color:#34413c}
.meta strong{color:var(--navy-950);font-weight:600}
.meta a{display:inline-flex;align-items:center;gap:6px;color:var(--navy-950);font-weight:600;font-size:15px;text-decoration:none;border-bottom:1.5px solid var(--brass-500);padding-bottom:1px}
.meta a svg{width:17px;height:17px;color:var(--brass-600)}
.fine{margin-top:12px;font-size:14.5px;color:#4a5651}
.qa{margin-top:14px}
details{border-bottom:1px solid var(--line)}
summary{list-style:none;cursor:pointer;padding:16px 38px 16px 0;font:600 17px/1.35 'Inter',sans-serif;color:var(--navy-950);position:relative}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";position:absolute;right:4px;top:50%;transform:translateY(-50%);font:400 27px/1 'Inter',sans-serif;color:var(--brass-600)}
details[open] summary::after{content:"\2212"}
details p{padding:0 8px 18px 0;font-size:16.5px;color:#30403a;max-width:46em}
.band{background:var(--ivory-100);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:34px 0;text-align:center}
.band h2{font-size:clamp(25px,4.6vw,32px)}
.band p{margin:8px auto 0;max-width:30em;font-size:17.5px;color:#2f3c37}
.band .ctas{max-width:460px;margin:20px auto 0}

/* footer */
.foot{padding:26px 0 22px;font-size:13.5px;color:#4a5651}
.foot p{max-width:56em}
.foot .row2{margin-top:12px;display:flex;flex-wrap:wrap;gap:6px 18px}
.foot a{color:var(--navy-950);text-underline-offset:3px}

/* sticky bar, phones only */
.sticky{position:fixed;left:0;right:0;bottom:0;z-index:50;display:flex;gap:10px;padding:10px 12px calc(10px + env(safe-area-inset-bottom));background:rgba(238,231,214,.97);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);border-top:1px solid rgba(11,46,41,.16)}
.sticky .btn{flex:1;min-height:52px;padding:0 10px;font-size:16.5px}
.js .sticky{transform:translateY(110%);transition:transform .25s ease}
.js .sticky.on{transform:none}

@media(min-width:520px){
  .ctas{grid-template-columns:auto auto;justify-content:start}
  .band .ctas{grid-template-columns:1fr 1fr}
}
@media(min-width:700px){
  .top .btn{display:inline-flex}
  .tick-list{grid-template-columns:1fr 1fr}
  .steps{grid-template-columns:repeat(3,1fr)}
  .step{border-top:0;border-left:1px solid var(--line)}
  .step:first-child{border-left:0}
  .row{grid-template-columns:1.4fr 1.6fr;align-items:center;gap:6px 24px}
  .meta{justify-content:space-between}
}
@media(min-width:900px){
  body{font-size:18px;padding-bottom:0}
  .sticky{display:none}
  .top{position:sticky;top:0;z-index:40}
  .top .wrap{min-height:74px}
  .hero{padding:52px 0 60px}
  .hero-grid{grid-template-columns:1.22fr .78fr;align-items:center;gap:56px}
  .sched{display:block}
  .m-sched{display:none!important}
  .sec{padding:54px 0}
  .qa-cols{display:grid;grid-template-columns:1fr 1fr;gap:0 56px}
}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.btn,.js .sticky{transition:none}}
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
<script>
(function () {
  var bar = document.querySelector('.sticky'), cta = document.querySelector('.hero .ctas');
  if (!bar || !cta || !('IntersectionObserver' in window)) return;
  document.documentElement.classList.add('js');
  new IntersectionObserver(function (entries) {
    var en = entries[0];
    bar.classList.toggle('on', !en.isIntersecting && en.boundingClientRect.top < 0);
  }, { threshold: 0 }).observe(cta);
})();
</script>
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


def cta_pair(p, loc):
    return f'<div class="ctas">{call_btn(loc, True)}{wa_btn(loc, p["wa"])}</div>'


def header(version):
    if version == "standard":
        name, sub = DOCTOR, SPECIALTY
    else:
        name, sub = CLINIC, "Mangalore, Puttur and Sullia"
    return f"""<header class="top">
  <div class="wrap">
    <a class="brand" href="/" aria-label="{e(name)}">
      <img src="/images/brand/logo-lp.png" alt="" width="42" height="44">
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
    lead2 = p["lead2_standard"] if version == "standard" else p["lead2"]
    return f"""<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">{e(p["eyebrow"])}</p>
      <h1>{e(p["h1"])}</h1>
      <p class="lead"><b>{e(p["lead1"])}</b>{e(lead2)}</p>
      {cta_pair(p, "hero")}
      <p class="micro">
        <span>{ICON_CHECK}Private, respectful consultations by appointment</span>
        <span>{ICON_CHECK}{e(p["micro_laser"])}</span>
        <span class="m-sched">{ICON_PIN}Mon to Fri Mangalore, Sat Puttur, Sun Ayyanakatte</span>
      </p>
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
    <p class="note">{e(p["note"])}</p>
    {cta_pair(p, "mid")}
  </div>
</section>"""


def visit(p, version):
    cards = "".join(
        f'<div class="step"><div class="n">{i}</div><div><h3>{e(t)}</h3><p>{e(d)}</p></div></div>'
        for i, (t, d) in enumerate(STEPS, 1)
    )
    meet = ""
    if version == "standard":
        meet = f"""<div class="meet">
      <h3>{e(DOCTOR)}</h3>
      <div class="cred">{e(SPECIALTY)}. MBBS (BMC), MS (Gold Medalist), FMAS, DMAS</div>
      <p>{e(DOCTOR)} explains every option clearly and recommends surgery only when it is genuinely indicated.</p>
    </div>"""
    return f"""<section class="sec">
  <div class="wrap">
    <h2>What happens at your visit</h2>
    <div class="steps">{cards}</div>
    <div class="strip"><b>LASER options.</b> {e(p["laser"])}</div>
    {meet}
  </div>
</section>"""


def where():
    rows = "".join(
        f"""<div class="row">
      <div><b>{e(l["name"])}</b><div class="sub">{e(l["where"])}</div></div>
      <div class="meta"><span><strong>{e(l["day"])}</strong>, {e(l["time"])}</span><a href="{e(l["map"])}" target="_blank" rel="noopener">{ICON_PIN}<span>Directions</span></a></div>
    </div>"""
        for l in LOCATIONS
    )
    return f"""<section class="sec alt">
  <div class="wrap">
    <h2>Where and when</h2>
    <div class="where">{rows}</div>
    <p class="fine">Consultations are by appointment. Timings can change, so please call or WhatsApp to confirm before you visit.</p>
  </div>
</section>"""


def questions(p):
    def block(items):
        return "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in items)
    qa = p["qa"]
    half = (len(qa) + 1) // 2
    return f"""<section class="sec">
  <div class="wrap">
    <h2>Questions you may have</h2>
    <div class="qa qa-cols">
      <div>{block(qa[:half])}</div>
      <div>{block(qa[half:])}</div>
    </div>
  </div>
</section>"""


def closing(p):
    return f"""<section class="band">
  <div class="wrap">
    <h2>Take the first step today</h2>
    <p>One call or one WhatsApp message is all it takes.</p>
    {cta_pair(p, "close")}
  </div>
</section>"""


def footer():
    return f"""<footer class="foot">
  <div class="wrap">
    <p>{e(DISCLAIMER)}</p>
    <div class="row2"><span>&copy; {e(CLINIC)}</span><a href="/">Main website</a></div>
  </div>
</footer>"""


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
        visit(p, version),
        where(),
        questions(p),
        closing(p),
        footer(),
        sticky(p),
    ])
    out = BASE.substitute(title=e(p["title"]), meta=e(p["meta"]), css=CSS, body=body)
    (ROOT / p["file"]).write_text(out, encoding="utf-8")
    print("built", p["file"], f"({version}, {len(out)//1024} KB)")


if __name__ == "__main__":
    args = list(sys.argv[1:])
    version = "conservative"
    if args and args[0] in ("conservative", "standard"):
        version = args.pop(0)
    keys = args or list(PAGES)
    for k in keys:
        build(k, version)
