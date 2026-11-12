"""Builds the 2Serious Exotic mockup pages from shared header/menu/footer.
Run: python3 _build.py  (writes *.html next to this file)"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
U = lambda pid, w=1600: f"https://images.unsplash.com/{pid}?w={w}&q=80"

PAGES = [  # file, menu label, menu sub
    ("index.html", "Home", ""),
    ("collection.html", "The Collection", "What we lease"),
    ("deals.html", "Deals", "Recently delivered"),
    ("leasing.html", "Leasing", "How it works & FAQ"),
    ("calculator.html", "Calculator", "Price a lease"),
    ("apply.html", "Get Approved", "Apply in minutes"),
]

ARROW = '<svg width="14" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M0 5h12M8 1l4 4-4 4" stroke="currentColor" stroke-width="1.3"/></svg>'

def head(title, desc):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,200..800&family=Inter:wght@300;400;500&display=swap">
<link rel="stylesheet" href="site.css">
</head>
<body>
"""

def chrome(current):
    links = "\n".join(
        f'      <a href="{f}"{" aria-current=\"page\"" if f == current else ""}>{label}{f"<small>{sub}</small>" if sub else ""}</a>'
        for f, label, sub in PAGES)
    return f"""<header id="hdr">
  <div class="row pad">
    <button class="menu" id="menu-open" aria-label="Open menu" aria-controls="overlay" aria-expanded="false"><i></i><span class="label">Menu</span></button>
    <a class="logo" href="index.html">2Serious<small>Exotic</small></a>
    <div class="right"><a class="tel" href="tel:+19545943642">954.594.3642</a><a href="apply.html">Get approved</a></div>
  </div>
</header>

<div class="overlay" id="overlay" aria-hidden="true">
  <div class="row pad">
    <button class="close" id="menu-close" aria-label="Close menu"><i></i><span class="label">Close</span></button>
    <a class="logo" href="index.html">2Serious<small>Exotic</small></a>
    <div class="right"><a href="apply.html">Get approved</a></div>
  </div>
  <nav class="pad" aria-label="Site">
{links}
  </nav>
  <div class="foot pad"><span class="label mute">Direct line · 954.594.3642</span><span class="label mute">Fort Lauderdale, Florida</span><a class="label" href="https://www.instagram.com/2seriousexoticdeals/">Instagram</a></div>
</div>
"""

FOOTER = """
<footer class="pad">
  <div class="fcols">
    <div style="display:grid;gap:18px;align-content:start"><span class="logo" style="align-items:flex-start">2Serious<small style="padding-left:0">Exotic</small></span><span class="mute" style="max-width:34ch">Exotic and luxury vehicle leasing. Fort Lauderdale, Florida.</span></div>
    <div><span class="label mute">Leasing</span><ul><li><a href="collection.html">The collection</a></li><li><a href="deals.html">Recent deals</a></li><li><a href="leasing.html">How leasing works</a></li><li><a href="calculator.html">Calculator</a></li></ul></div>
    <div><span class="label mute">Start</span><ul><li><a href="apply.html">Get approved</a></li><li><a href="tel:+19545943642">954.594.3642</a></li></ul></div>
    <div><span class="label mute">Follow</span><ul><li><a href="https://www.instagram.com/2seriousexoticdeals/">Instagram<br>@2seriousexoticdeals</a></li></ul></div>
  </div>
  <div class="legal"><p>© 2026 2Serious Exotic LLC. All rights reserved. All terms subject to credit approval and may change without notice at the discretion of 2Serious Exotic LLC. Example figures are illustrative unless marked as a client deal. Logos and names © their owners; 2Serious Exotic LLC has no affiliation with manufacturers.</p><a href="credits.html">Photo credits</a></div>
</footer>
<script src="site.js"></script>
</body>
</html>
"""

def page(fname, title, desc, body):
    html = head(title, desc) + chrome(fname) + "<main>\n" + body + "\n</main>\n" + FOOTER
    open(os.path.join(HERE, fname), "w").write(html)

def cta_band(img, alt, credit=""):
    cr = f'<span class="credit">{credit}</span>' if credit else ""
    return f"""<section class="enquire">
  <img src="{img}" alt="{alt}" loading="lazy">
  <div class="in pad">
    <span class="label">Private client desk</span>
    <h2 class="xl">Your next car<br><span class="thin">starts with a call</span></h2>
    <span class="tel">954.594.3642</span>
    <div class="row"><a class="cut" href="apply.html">Get approved today</a><a class="cut ghost" href="calculator.html">Price a lease</a></div>
  </div>{cr}
</section>"""

# ---------------------------------------------------------------- data
CREDITS = json.load(open(os.path.join(HERE, "img/credits.json")))
def cr(key):
    c = CREDITS[key]; return f"Photo: {c['author']} / {c['license']}"

DELIVERED = [  # img, alt, top line, model, status, credit key
    ("img/gallardo-spyder.jpg", "Yellow Lamborghini Gallardo Spyder", "2007", "Lamborghini<br>Gallardo Spyder", "Leased", "gallardo-spyder"),
    ("img/ferrari-roma.jpg", "Silver Ferrari Roma", "Ferrari", "Roma", "Leased", "ferrari-roma"),
    ("img/ferrari-488.jpg", "Red Ferrari 488 GTB", "2016", "Ferrari<br>488 GTB", "Approved", "ferrari-488"),
    ("img/gallardo-black.jpg", "Yellow Lamborghini Gallardo LP560-4", "Lamborghini", "Gallardo", "Delivered", "gallardo-black"),
    ("img/supra.jpg", "Blue Toyota Supra (A80)", "Toyota", "Supra<br>MK4", "Leased", "supra"),
    ("img/ram-trx.jpg", "Red RAM 1500 TRX", "RAM", "1500 TRX", "Leased", "ram-trx"),
]

def delivered_grid(n=6):
    items = "\n".join(f"""    <figure class="dcar"><div class="ph"><img src="{i}" alt="{a}" loading="lazy"></div><figcaption><div><span class="yr">{y}</span><b>{m}</b></div><span class="status">{s}</span></figcaption></figure>"""
                      for i, a, y, m, s, _ in DELIVERED[:n])
    return f'<div class="dgrid">\n{items}\n  </div>'

ARTURA_SHEET = """<div class="ledger">
    <div>
      <h3>The structure</h3>
      <dl>
        <div><dt>Sales price</dt><dd>$234,327.50</dd></div>
        <div><dt>Capitalized cost reduction</dt><dd>&minus;$54,527.13</dd></div>
        <div><dt>Total capitalized amount</dt><dd>$179,800.37</dd></div>
        <div><dt>Term</dt><dd>60 months</dd></div>
        <div><dt>Mileage allowance</dt><dd>3,500 / yr</dd></div>
        <div><dt>Balloon</dt><dd>$63,700.00</dd></div>
        <div><dt>Base monthly payment</dt><dd>$3,622.48</dd></div>
        <div><dt>FL sales &amp; use tax on payment</dt><dd>$271.69</dd></div>
        <div class="tot"><dt>Total monthly payment</dt><dd>$3,894.17</dd></div>
      </dl>
    </div>
    <div>
      <h3>Due at signing</h3>
      <dl>
        <div><dt>Capitalized cost reduction</dt><dd>$54,527.13</dd></div>
        <div><dt>First + pre-paid last month</dt><dd>$7,788.34</dd></div>
        <div><dt>Taxes, title, lien &amp; bank fees</dt><dd>$7,684.53</dd></div>
        <div class="tot"><dt>Total due at signing</dt><dd>$70,000.00</dd></div>
      </dl>
    </div>
    <p class="fine">Actual client deal, September 2026. Personal details removed. Lessee may pay off the lease, including the balloon, at any time.</p>
  </div>"""

# type, make, model, img, alt, term, miles, down, from
COLLECTION = [
    ("Supercar", "Lamborghini", "Huracán EVO", U("photo-1612825173281-9a193378527e", 1000), "Orange Lamborghini Huracán EVO", "36 mo", "5,000", "$45K", "$2,680"),
    ("Supercar", "Lamborghini", "Aventador S", U("photo-1571607388263-1044f9ea01dd", 1000), "Lamborghini Aventador S with doors raised", "36 mo", "5,000", "$80K", "$3,530"),
    ("Supercar", "Ferrari", "SF90 Stradale", U("photo-1632441730372-d8509de481d1", 1000), "Yellow Ferrari SF90 Stradale", "39 mo", "3,000", "$95K", "$4,810"),
    ("Supercar", "McLaren", "Artura Spider", "img/artura.jpg", "Orange McLaren Artura", "60 mo", "3,500", "$54.5K", "$3,894"),
    ("Supercar", "Ferrari", "488 GTB", "img/ferrari-488.jpg", "Red Ferrari 488 GTB", "48 mo", "3,500", "$40K", "$2,450"),
    ("Supercar", "McLaren", "720S", U("photo-1542362567-b07e54358753", 1000), "Silver McLaren 720S", "36 mo", "2,000", "$40K", "$3,390"),
    ("Hypercar", "Bugatti", "Chiron", "img/chiron.jpg", "Blue Bugatti Chiron", "60 mo", "2,000", "Bespoke", ""),
    ("Grand tourer", "Bentley", "Flying Spur", U("photo-1618418721668-0d1f72aa4bab", 1000), "Bentley Flying Spur at night", "48 mo", "7,500", "$50K", "$2,300"),
    ("Grand tourer", "Rolls-Royce", "Wraith", U("photo-1631295868223-63265b40d9e4", 1000), "Rolls-Royce Wraith under palm trees", "48 mo", "5,000", "$60K", "$3,500"),
    ("Grand tourer", "Ferrari", "Roma", "img/ferrari-roma.jpg", "Silver Ferrari Roma", "48 mo", "5,000", "$45K", "$2,750"),
    ("Grand tourer", "Mercedes-AMG", "GT", U("photo-1617814076367-b759c7d7e738", 1000), "Mercedes-AMG GT by a marina", "48 mo", "7,500", "$30K", "$1,690"),
    ("Supercar", "Porsche", "911 GT3 RS", U("photo-1580274455191-1c62238fa333", 1000), "Black Porsche 911 GT3 RS", "36 mo", "3,000", "$50K", "$3,150"),
    ("SUV & truck", "RAM", "1500 TRX", "img/ram-trx.jpg", "Red RAM 1500 TRX", "60 mo", "10,000", "$20K", "$1,390"),
    ("SUV & truck", "Land Rover", "Range Rover Sport", U("photo-1563720223185-11003d516935", 1000), "Black Range Rover Sport", "48 mo", "10,000", "$20K", "$1,450"),
    ("Modern classic", "Toyota", "Supra MK4", "img/supra.jpg", "Blue Toyota Supra A80", "48 mo", "5,000", "$25K", "$1,350"),
    ("Modern classic", "Lamborghini", "Gallardo Spyder", "img/gallardo-spyder.jpg", "Yellow Lamborghini Gallardo Spyder", "48 mo", "5,000", "$20K", "$1,290"),
    ("Modern classic", "Lamborghini", "Gallardo LP560-4", "img/gallardo-black.jpg", "Yellow Lamborghini Gallardo LP560-4", "48 mo", "5,000", "$25K", "$1,450"),
]

def vcard(c):
    t, mk, model, img, alt, term, miles, down, frm = c
    price = f'<span class="from">{frm}<small>/MO</small></span>' if frm else '<span class="from" style="font-size:18px;letter-spacing:.1em">ON REQUEST</span>'
    return f"""    <article class="vcard" data-type="{t}">
      <span class="type">{t}</span>
      <div class="ph"><img src="{img}" alt="{alt}" loading="lazy"></div>
      <div class="body">
        <div><span class="mk">{mk}</span><h3>{model}</h3></div>
        <dl><div><dt>Term</dt><dd>{term}</dd></div><div><dt>Miles/yr</dt><dd>{miles}</dd></div><div><dt>Down</dt><dd>{down}</dd></div></dl>
        <div class="ft">{price}<a class="arrowlink" href="apply.html" aria-label="Enquire about {mk} {model}">{ARROW}</a></div>
      </div>
    </article>"""

# ---------------------------------------------------------------- pages
def build_home():
    src = open(os.path.join(HERE, "..", "mockup-v3.html")).read()
    body = src.split("<main>", 1)[1].split("</main>", 1)[0]
    for i, (_, _, _, _, _, k) in enumerate(DELIVERED):
        pass
    swaps = {"deals/gallardo-spyder.jpg": "img/gallardo-spyder.jpg", "deals/ferrari-roma.jpg": "img/ferrari-roma.jpg",
             "deals/ferrari-488.jpg": "img/ferrari-488.jpg", "deals/gallardo-black.jpg": "img/gallardo-black.jpg",
             "deals/supra.jpg": "img/supra.jpg", "deals/ram-trx.jpg": "img/ram-trx.jpg",
             'alt="Grey 2007 Lamborghini Gallardo Spyder"': 'alt="Yellow Lamborghini Gallardo Spyder"',
             'alt="Yellow Ferrari Roma, front view"': 'alt="Silver Ferrari Roma"',
             'alt="Black Lamborghini Gallardo from behind"': 'alt="Yellow Lamborghini Gallardo LP560-4"',
             'alt="Black widebody Toyota Supra"': 'alt="Blue Toyota Supra A80"',
             'alt="Custom black RAM TRX with light bar"': 'alt="Red RAM 1500 TRX"',
             "<b>Supra<br>Widebody</b>": "<b>Supra<br>MK4</b>", "<b>1500 TRX<br>Custom</b>": "<b>1500 TRX</b>",
             '<a class="go" href="https://www.instagram.com/2seriousexoticdeals/">Every deal on Instagram</a>': '<a class="go" href="deals.html">All recent deals</a>',
             'href="#enquire">Structure mine</a>': 'href="apply.html">Structure mine</a>',
             '<a class="go" href="#enquire">Request exact terms</a>': '<a class="go" href="calculator.html">Open full calculator</a>',
             '<a class="cut" href="#">Get approved today</a><a class="cut ghost" href="#">Request a quote</a>': '<a class="cut" href="apply.html">Get approved today</a><a class="cut ghost" href="calculator.html">Price a lease</a>',
             '<a class="cut" href="#enquire">Enquire</a>': '<a class="cut" href="collection.html">View collection</a>',
             }
    for a, b in swaps.items():
        body = body.replace(a, b)
    page("index.html", "2Serious Exotic", "Exotic and luxury car leasing from Fort Lauderdale.", body)

def build_collection():
    types = ["All", "Supercar", "Hypercar", "Grand tourer", "SUV & truck", "Modern classic"]
    filt = "".join(f'<button type="button" data-f="{t}" aria-pressed="{str(t=="All").lower()}">{t}</button>' for t in types)
    cards = "\n".join(vcard(c) for c in COLLECTION)
    body = f"""<section class="phero">
  <img src="{U('photo-1600712242805-5f78671b24da', 2400)}" alt="White Bugatti Chiron" style="object-position:center 55%">
  <div class="in pad">
    <span class="crumb"><a href="index.html">Home</a> &nbsp;/&nbsp; The Collection</span>
    <h1 class="xl">The<br><span class="thin">collection</span></h1>
    <p>Supercars, hypercars, grand tourers, trucks and modern classics. New or pre-owned, from a dealer or a private sale. If it's rare, we can structure it.</p>
  </div>
</section>

<section class="sec pad" id="list">
  <div class="sec-h">
    <div><span class="label mute">{len(COLLECTION)} example structures</span><h2 class="xl">Choose<br><span class="thin">your class</span></h2></div>
    <p class="lead">Every figure below is an example of how we might structure that car. Your real numbers depend on the vehicle, your profile and the lender.</p>
  </div>
  <div class="filters" role="group" aria-label="Filter by class">{filt}</div>
  <div class="cgrid2" id="cars">
{cards}
  </div>
  <p class="fine" style="font-size:11px;color:#6A6A6A;margin-top:18px">Illustrative pricing, not current offers, except the McLaren Artura Spider, which reflects an actual client deal. All terms subject to credit approval.</p>
</section>

<div class="pad">
  <div class="nums words">
    <div><b>Any year</b><span class="label mute">2007 Gallardo to 2025 Artura</span></div>
    <div><b>Any seller</b><span class="label mute">Dealer or private party</span></div>
    <div><b>Any use</b><span class="label mute">Personal, business, rental</span></div>
    <div><b>Not listed?</b><span class="label mute">Send us the car</span></div>
  </div>
</div>

{cta_band(U('photo-1592198084033-aade902d1aae', 2400), 'Red Ferrari F8 Tributo at golden hour')}"""
    page("collection.html", "The Collection · 2Serious Exotic", "Exotic cars we lease: Lamborghini, Ferrari, McLaren, Bentley, Rolls-Royce, Bugatti and more.", body)

def build_deals():
    body = f"""<section class="phero">
  <img src="img/artura.jpg" alt="Orange McLaren Artura" style="object-position:center 60%">
  <div class="in pad">
    <span class="crumb"><a href="index.html">Home</a> &nbsp;/&nbsp; Deals</span>
    <h1 class="xl">Recently<br><span class="thin">delivered</span></h1>
    <p>Real cars, real clients, real structures. From a 2007 Gallardo Spyder to a 2025 McLaren Artura, here's what's leaving the desk.</p>
  </div>
  <span class="credit">{cr('artura')}</span>
</section>

<section class="sheet pad" id="deal">
  <div class="intro">
    <span class="label mute">Featured deal · September 2026</span>
    <h2 class="xl">2025 McLaren<br><span class="thin">Artura Spider</span></h2>
    <p>Techlux convertible, 4,691 miles. Structured over 60 months with a balloon, so the client keeps capital working and can pay off the lease at any time.</p>
    <div><span class="label mute">Total monthly</span><div class="mo">$3,894<small>/ MO</small></div></div>
    <a class="cut" href="apply.html">Structure mine</a>
  </div>
  {ARTURA_SHEET}
</section>

<section class="delivered pad">
  <div class="dhead">
    <div style="display:grid;gap:24px"><span class="label mute">The desk this season</span><h2 class="xl">From Gallardo<br><span class="thin">to TRX</span></h2></div>
    <a class="go" href="https://www.instagram.com/2seriousexoticdeals/">Every deal on Instagram</a>
  </div>
  {delivered_grid()}
  <p style="font-size:11px;color:#6A6A6A;margin:18px 0 0">Photos show the same models as client vehicles, not the client cars themselves. See <a href="credits.html" style="text-decoration:underline">photo credits</a>.</p>
</section>

<section class="split flip">
  <div class="img"><img src="img/supra.jpg" alt="Blue Toyota Supra A80" loading="lazy"></div>
  <div class="txt pad">
    <span class="label mute">Not just new exotics</span>
    <h2 class="xl">Older, rarer,<br><span class="thin">still structured</span></h2>
    <p>Banks often won't touch a 2007 Gallardo or a modified Supra. We will. Residuals follow how collectible cars actually hold value, so older and specialty vehicles can be leased too.</p>
    <ul>
      <li><span>Oldest recent deal</span><span>2007 Lamborghini Gallardo Spyder</span></li>
      <li><span>Trucks & builds</span><span>RAM TRX, custom builds</span></li>
      <li><span>JDM & tuner</span><span>Toyota Supra MK4</span></li>
    </ul>
  </div>
</section>

{cta_band(U('photo-1571607388263-1044f9ea01dd', 2400), 'Lamborghini Aventador S with doors raised at sunset')}"""
    page("deals.html", "Deals · 2Serious Exotic", "Recent 2Serious Exotic lease deals, including a full McLaren Artura deal sheet.", body)

FAQ = [
    ("What are standard lease terms?", "Our leases typically run 24 to 60 months, with flexible mileage options starting as low as 2,000 miles per year. Terms can be tailored for collectors, rental operators or business owners."),
    ("What's the minimum down payment?", "Most structures require 15–20% down, depending on the vehicle, your profile and the deal structure. For qualified clients, we can design creative alternatives to a standard down payment."),
    ("How are residual values set?", "Residuals are tailored to the real-world depreciation curves of exotic vehicles, not cookie-cutter numbers from traditional banks. That keeps things fair and flexible when it's time to upgrade or exit."),
    ("Can I exit my lease early?", "Yes. Whether you choose an open-end or closed-end lease, we offer early exit and trade-out options for clients who want to upgrade or change vehicles before the end of the term. Each structure has different benefits, and we'll match the flexibility to your goals and your car."),
    ("Can I lease an older or pre-owned exotic?", "Yes. Recent deals include a 2007 Lamborghini Gallardo Spyder and a 2016 Ferrari 488. Tell us the car and we'll tell you how it can be structured."),
    ("What is a balloon payment?", "A balloon is a set amount due at the end of the term, which lowers your monthly payment. You can pay off the lease, including the balloon, at any time. On our McLaren Artura deal, a $63,700 balloon kept the payment at $3,894 a month over 60 months."),
]

def build_leasing():
    faq = "\n".join(f"<details{' open' if i==0 else ''}><summary>{q}</summary><p>{a}</p></details>" for i, (q, a) in enumerate(FAQ))
    body = f"""<section class="phero">
  <img src="{U('photo-1631295868223-63265b40d9e4', 2400)}" alt="Rolls-Royce Wraith under palm trees" style="object-position:center 65%">
  <div class="in pad">
    <span class="crumb"><a href="index.html">Home</a> &nbsp;/&nbsp; How Leasing Works</span>
    <h1 class="xl">Leasing,<br><span class="thin">engineered</span></h1>
    <p>A lease built for exotics looks different from one built for a sedan. Here's how we structure them, and why the numbers come out better.</p>
  </div>
</section>

<section class="sec pad">
  <div class="sec-h">
    <div><span class="label mute">Two structures</span><h2 class="xl">Open-end<br><span class="thin">or closed-end</span></h2></div>
    <p class="lead">Both come with early exit and trade-out options. The difference is who carries the residual at the end, and how much flexibility you want along the way.</p>
  </div>
  <div class="compare">
    <article>
      <span class="best">Best for business owners & operators</span>
      <h3>Open-end</h3>
      <p>Lower payments in exchange for taking on the end-of-term value. Often paired with a balloon, so more of your capital stays in the business.</p>
      <ul><li>Lower monthly payment</li><li>Optional balloon to reduce payments further</li><li>Pay off at any time, including the balloon</li><li>Flexible mileage</li></ul>
    </article>
    <article>
      <span class="best">Best for drivers who want certainty</span>
      <h3>Closed-end</h3>
      <p>A fixed payment and a known exit. Hand the car back at the end of the term, or trade into the next one.</p>
      <ul><li>Predictable monthly cost</li><li>Walk away or trade up at term end</li><li>Early exit and trade-out options</li><li>Mileage from 2,000 a year</li></ul>
    </article>
  </div>
</section>

<section class="split">
  <div class="img"><img src="{U('photo-1618418721668-0d1f72aa4bab', 1800)}" alt="Bentley Flying Spur at night" loading="lazy"></div>
  <div class="txt pad">
    <span class="label mute">The residual</span>
    <h2 class="xl">Where the<br><span class="thin">savings live</span></h2>
    <p>Your payment mostly covers the car's drop in value over the term. Banks use generic residual tables, which assume a Lamborghini loses value like a family car. We set residuals on how exotics actually depreciate, so you pay for less of the car.</p>
    <ul>
      <li><span>Terms</span><span>24–60 months</span></li>
      <li><span>Mileage</span><span>From 2,000 / yr</span></li>
      <li><span>Typical down</span><span>15–20%</span></li>
    </ul>
  </div>
</section>

<section class="sec pad">
  <div class="sec-h"><div><span class="label mute">The process</span><h2 class="xl">Inquiry<br><span class="thin">to keys</span></h2></div><p class="lead">One point of contact from the first call to delivery.</p></div>
  <ol class="steps">
    <li><h3>Tell us the car</h3><p>New, pre-owned, dealer or private sale. Share the vehicle and how you plan to use it.</p></li>
    <li><h3>We structure it</h3><p>We shop the deal across our lenders and set the term, mileage, residual and down payment.</p></li>
    <li><h3>Approve &amp; sign</h3><p>Quick turnaround on approval, with every number laid out before you sign.</p></li>
    <li><h3>Drive, then decide</h3><p>Upgrade, trade out early, or pay it off. The exit is planned from day one.</p></li>
  </ol>
</section>

<div class="pad"><div class="nums words">
  <div><b>Collectors</b><span class="label mute">Low miles, long terms</span></div>
  <div><b>Operators</b><span class="label mute">Rental fleet structures</span></div>
  <div><b>Owners</b><span class="label mute">Business-use leases</span></div>
  <div><b>Drivers</b><span class="label mute">Personal leases</span></div>
</div></div>

<section class="sec pad">
  <div class="faq">
    <div style="display:grid;gap:24px;align-content:start"><span class="label mute">FAQ</span><h2 class="xl" style="font-size:clamp(32px,4.4vw,68px)">Straight<br><span class="thin">answers</span></h2><p class="lead">Something not covered? Call 954.594.3642 and you'll speak to us directly.</p></div>
    <div>{faq}</div>
  </div>
</section>

{cta_band(U('photo-1592198084033-aade902d1aae', 2400), 'Red Ferrari F8 Tributo at golden hour')}"""
    page("leasing.html", "How Leasing Works · 2Serious Exotic", "Open-end and closed-end exotic car leases, residuals, balloons and FAQ.", body)

def fld(id, label, val, pre="", suf="", note="", wide=False):
    style = ' style="grid-column:1/-1"' if wide else ""
    return f'<div class="fld"{style}><label for="{id}">{label}</label><div class="in">{f"<i>{pre}</i>" if pre else ""}<input id="{id}" inputmode="decimal" value="{val}">{f"<i>{suf}</i>" if suf else ""}</div><small id="{id}-n">{note}</small></div>'

def build_calculator():
    body = f"""<section class="phero short">
  <div class="in pad">
    <span class="crumb"><a href="index.html">Home</a> &nbsp;/&nbsp; Calculator</span>
    <h1 class="xl">Lease<br><span class="thin">calculator</span></h1>
    <p>Every field a real deal sheet uses. Start from the McLaren Artura deal below or enter your own numbers. A value above 0.1 in the rate field is read as APR.</p>
  </div>
</section>

<section class="pad" style="padding-block:40px 120px">
  <div class="filters" role="group" aria-label="Start from an example" id="presets">
    <button type="button" data-p="artura" aria-pressed="true">McLaren Artura (client deal)</button>
    <button type="button" data-p="huracan" aria-pressed="false">Huracán EVO</button>
    <button type="button" data-p="cullinan" aria-pressed="false">Rolls-Royce Cullinan</button>
    <button type="button" data-p="trx" aria-pressed="false">RAM TRX</button>
  </div>
  <div class="fcalc">
    <form id="fc" novalidate>
      <span class="grp">Vehicle</span>
      {fld('msrp','MSRP / vehicle price','234,327.50','$')}
      {fld('cap','Selling price / cap cost','234,327.50','$')}
      <span class="grp">Structure</span>
      <div class="fld"><label for="term">Term</label><div class="in"><select id="term"><option>24</option><option>36</option><option>39</option><option>48</option><option selected>60</option></select><i>months</i></div><small></small></div>
      <div class="fld"><label for="miles">Miles per year</label><div class="in"><select id="miles"><option>2,000</option><option selected>3,500</option><option>5,000</option><option>7,500</option><option>10,000</option><option>12,000</option></select></div><small></small></div>
      {fld('resid','Residual / balloon','27.1842','','%','')}
      {fld('mf','Money factor or APR','0.00693','','','')}
      <span class="grp">At signing</span>
      {fld('down','Down payment / cap reduction','54,527.13','$','','')}
      {fld('trade','Trade-in value','0','$')}
      {fld('fees','Other due at signing','11,578.72','$','','Taxes, title, lien, bank fees, last month')}
      {fld('tax','Sales tax on payment','7.5','','%','')}
    </form>
    <div class="out" aria-live="polite">
      <span class="label mute">Estimated monthly payment</span>
      <div class="pay" id="fpay">$0</div>
      <div class="bar" aria-hidden="true"><span id="bd" style="background:var(--white)"></span><span id="br" style="background:var(--gold)"></span><span id="bt" style="background:#444"></span></div>
      <dl>
        <div><dt><i style="background:var(--white)"></i>Depreciation</dt><dd id="o-dep"></dd></div>
        <div><dt><i style="background:var(--gold)"></i>Rent charge</dt><dd id="o-rent"></dd></div>
        <div><dt><i style="background:#444"></i>Sales tax</dt><dd id="o-tax"></dd></div>
        <div><dt>Base payment, before tax</dt><dd id="o-base"></dd></div>
        <div><dt>Due at signing (est.)</dt><dd id="o-das"></dd></div>
        <div class="tot"><dt>Total lease cost</dt><dd id="o-total"></dd></div>
      </dl>
      <a class="cut" href="apply.html">Get real numbers on this car</a>
      <p style="margin:0;font-size:11px;color:#6A6A6A">Estimates only. All terms subject to credit approval and may change without notice at the discretion of 2Serious Exotic LLC. Example presets other than the Artura use illustrative pricing.</p>
    </div>
  </div>
</section>

{cta_band(U('photo-1612825173281-9a193378527e', 2400), 'Orange Lamborghini Huracán EVO')}"""
    page("calculator.html", "Lease Calculator · 2Serious Exotic", "Exotic car lease calculator with money factor, residual, tax and due at signing.", body)

def build_apply():
    body = f"""<section class="phero short">
  <div class="in pad">
    <span class="crumb"><a href="index.html">Home</a> &nbsp;/&nbsp; Get Approved</span>
    <h1 class="xl">Get<br><span class="thin">approved</span></h1>
    <p>Four short steps. We'll review your request and come back with a structure, usually the same day.</p>
  </div>
</section>

<section class="pad" style="padding-block:50px 130px">
  <div class="apply">
    <aside>
      <div style="display:grid;gap:12px"><span class="label mute">Prefer to talk?</span><a href="tel:+19545943642" style="font:200 clamp(30px,3vw,44px)/1 var(--wide);font-stretch:125%">954.594.3642</a></div>
      <div style="display:grid;gap:12px"><span class="label mute">Based in</span><span>Fort Lauderdale, Florida</span></div>
      <div style="display:grid;gap:12px"><span class="label mute">What you'll need</span><ul style="margin:0;padding-left:18px;color:#BDBDBD;display:grid;gap:6px"><li>The car you want, or a link to it</li><li>Driver's license</li><li>Business details if leasing through a company</li></ul></div>
      <div style="display:grid;gap:12px"><span class="label mute">Your information</span><span class="mute" style="font-size:13px">Used only to structure your lease. Submitting doesn't affect your credit until you approve a credit check.</span></div>
    </aside>
    <div>
      <div class="progress" id="prog">
        <div class="now"><span></span><b>01 Vehicle</b></div>
        <div><span></span><b>02 You</b></div>
        <div><span></span><b>03 Structure</b></div>
        <div><span></span><b>04 Review</b></div>
      </div>
      <form class="aform" id="af" novalidate>
        <fieldset data-step="0" style="display:contents;border:0">
          <div class="fld wide"><label for="a-car">Vehicle you want</label><div class="in"><input id="a-car" value="2025 McLaren Artura Spider" placeholder="Year, make, model"></div><small>Or paste a listing link</small></div>
          <div class="fld"><label for="a-cond">Condition</label><div class="in"><select id="a-cond"><option>Pre-owned</option><option>New</option></select></div></div>
          <div class="fld"><label for="a-price">Approximate price</label><div class="in"><i>$</i><input id="a-price" inputmode="decimal" value="235,000"></div></div>
          <div class="wide"><span class="label mute" style="display:block;margin-bottom:14px">How will it be used?</span>
            <div class="choice">
              <label><input type="radio" name="use" checked><b>Personal</b><span>Daily or weekend driver</span></label>
              <label><input type="radio" name="use"><b>Business</b><span>Leased through a company</span></label>
              <label><input type="radio" name="use"><b>Rental fleet</b><span>For an operator</span></label>
            </div>
          </div>
        </fieldset>
        <fieldset data-step="1" style="display:none;border:0" hidden>
          <div class="fld"><label for="a-first">First name</label><div class="in"><input id="a-first" autocomplete="given-name"></div></div>
          <div class="fld"><label for="a-last">Last name</label><div class="in"><input id="a-last" autocomplete="family-name"></div></div>
          <div class="fld"><label for="a-email">Email</label><div class="in"><input id="a-email" type="email" autocomplete="email"></div></div>
          <div class="fld"><label for="a-phone">Phone</label><div class="in"><input id="a-phone" type="tel" autocomplete="tel"></div></div>
          <div class="fld wide"><label for="a-state">State</label><div class="in"><input id="a-state" value="Florida"></div></div>
        </fieldset>
        <fieldset data-step="2" style="display:none;border:0" hidden>
          <div class="fld"><label for="a-term">Preferred term</label><div class="in"><select id="a-term"><option>24 months</option><option>36 months</option><option>48 months</option><option selected>60 months</option></select></div></div>
          <div class="fld"><label for="a-miles">Miles per year</label><div class="in"><select id="a-miles"><option>2,000</option><option selected>3,500</option><option>5,000</option><option>7,500</option><option>10,000+</option></select></div></div>
          <div class="fld"><label for="a-down">Down payment available</label><div class="in"><i>$</i><input id="a-down" inputmode="decimal" value="55,000"></div></div>
          <div class="fld"><label for="a-trade">Trade-in?</label><div class="in"><select id="a-trade"><option>No</option><option>Yes</option></select></div></div>
          <div class="fld wide"><label for="a-notes">Anything else</label><textarea id="a-notes" placeholder="Timing, balloon preference, current lease to exit…"></textarea></div>
        </fieldset>
        <fieldset data-step="3" style="display:none;border:0" hidden>
          <div class="wide" id="review" style="display:grid;gap:0"></div>
        </fieldset>
        <div class="formnav">
          <button type="button" class="go" id="back" hidden>Back</button>
          <button type="submit" class="cut" id="next">Continue</button>
        </div>
        <p class="notice" id="sent" hidden></p>
      </form>
    </div>
  </div>
</section>"""
    page("apply.html", "Get Approved · 2Serious Exotic", "Apply for an exotic car lease with 2Serious Exotic.", body)

def build_credits():
    rows = "\n".join(f'<tr><td>{k.replace("-", " ").title()}</td><td>{v["author"]}</td><td>{v["license"]}</td><td><a href="{v["source"]}">{v["title"].replace("File:", "")}</a></td></tr>' for k, v in CREDITS.items())
    body = f"""<section class="phero short"><div class="in pad"><span class="crumb"><a href="index.html">Home</a> &nbsp;/&nbsp; Photo credits</span><h1 class="xl">Photo<br><span class="thin">credits</span></h1><p>Model photos from Wikimedia Commons, used under the licenses below. Other photography from Unsplash under the Unsplash License.</p></div></section>
<section class="pad" style="padding-block:40px 130px"><div class="tablewrap"><table class="ctable"><thead><tr><th>Vehicle</th><th>Author</th><th>License</th><th>Source</th></tr></thead><tbody>
{rows}
</tbody></table></div></section>"""
    page("credits.html", "Photo Credits · 2Serious Exotic", "Photo credits.", body)

if __name__ == "__main__":
    build_home(); build_collection(); build_deals(); build_leasing(); build_calculator(); build_apply(); build_credits()
    print("built")
