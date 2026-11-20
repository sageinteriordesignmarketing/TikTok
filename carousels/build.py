"""Sage carousel templates v3: each series has its own textured editorial treatment. 1080x1350."""
import random, urllib.parse

random.seed(7)

def svg_uri(svg):
    return "url(\"data:image/svg+xml," + urllib.parse.quote(svg) + "\")"

GRAIN = svg_uri("<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .5 0 0 0 0 .45 0 0 0 0 .4 0 0 0 .55 0'/></filter><rect width='100%' height='100%' filter='url(#n)'/></svg>")
PLASTER = svg_uri("<svg xmlns='http://www.w3.org/2000/svg' width='1080' height='1350'><filter id='p'><feTurbulence type='fractalNoise' baseFrequency='.006' numOctaves='5' seed='3'/><feColorMatrix values='0 0 0 0 .55 0 0 0 0 .48 0 0 0 0 .4 0 0 0 .35 0'/></filter><rect width='100%' height='100%' filter='url(#p)'/></svg>")
LINEN = svg_uri("<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'><filter id='a'><feTurbulence type='fractalNoise' baseFrequency='.012 .9' numOctaves='2' seed='4'/><feColorMatrix values='0 0 0 0 .45 0 0 0 0 .4 0 0 0 0 .34 0 0 0 .5 0'/></filter><filter id='b'><feTurbulence type='fractalNoise' baseFrequency='.9 .012' numOctaves='2' seed='9'/><feColorMatrix values='0 0 0 0 .45 0 0 0 0 .4 0 0 0 0 .34 0 0 0 .45 0'/></filter><rect width='100%' height='100%' filter='url(#a)'/><rect width='100%' height='100%' filter='url(#b)'/></svg>")

def deckle(w, h, j=7, step=14):
    pts = []
    for x in range(0, w + 1, step): pts.append((x, random.uniform(0, j)))
    for y in range(0, h + 1, step): pts.append((w - random.uniform(0, j), y))
    for x in range(w, -1, -step): pts.append((x, h - random.uniform(0, j)))
    for y in range(h, -1, -step): pts.append((random.uniform(0, j), y))
    return "polygon(" + ",".join(f"{x:.0f}px {y:.0f}px" for x, y in pts) + ")"

CSS = """
:root { --linen:#F1EBE2; --paper:#FBF8F2; --sand:#E6DCCD; --plaster:#E9E1D5; --taupe:#8A7763; --espresso:#2A231E; --ink:#1B1714;
  --serif:"Cormorant Garamond", Georgia, serif; --sans:"Montserrat", Arial, sans-serif; }
* { box-sizing:border-box; margin:0; padding:0; }
body { background:#888; }
.slide { width:1080px; height:1350px; position:relative; overflow:hidden; margin:20px; font-family:var(--sans); color:var(--ink); }
.abs { position:absolute; inset:0; }
.cover-img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
.grain::before { content:""; position:absolute; inset:0; background-image:GRAIN; opacity:.55; mix-blend-mode:multiply; z-index:5; pointer-events:none; }
.grain.lt::before { mix-blend-mode:soft-light; opacity:.7; }
.shade { position:absolute; inset:0; background:radial-gradient(ellipse at center, rgba(30,24,20,.38) 0%, rgba(30,24,20,.72) 100%); }
.mark { position:absolute; top:70px; left:0; right:0; text-align:center; font:500 22px var(--sans); letter-spacing:.62em; padding-left:.62em; z-index:6; }
.foot { position:absolute; left:90px; right:90px; bottom:62px; display:flex; justify-content:space-between; font:500 17px var(--sans); letter-spacing:.34em; text-transform:uppercase; opacity:.8; z-index:6; }
.k { font:500 20px var(--sans); letter-spacing:.4em; text-transform:uppercase; }
.it { font-family:var(--serif); font-style:italic; font-weight:500; letter-spacing:-.02em; line-height:.98; font-variant-numeric:lining-nums; text-wrap:balance; }
.rm { font-family:var(--serif); font-weight:500; letter-spacing:-.015em; line-height:1.04; font-variant-numeric:lining-nums; text-wrap:balance; }
.rm em, .it em { color:var(--taupe); }
.body { font:400 31px/1.6 var(--sans); }
.pill { display:inline-block; border:1.5px solid currentColor; border-radius:999px; padding:18px 40px; font:500 18px var(--sans); letter-spacing:.3em; text-transform:uppercase; }
.fill { color:var(--taupe); }
.light-text { color:#FBF8F2; } .light-text .rm em, .light-text .it em { color:#D9C6AC; }

/* T0 myth vs truth: plaster wall, inset frame */
.plaster { background-color:var(--plaster); background-image:PLASTER; }
.frame { position:absolute; inset:44px; border:1px solid rgba(27,23,20,.35); z-index:4; pointer-events:none; }
.frame.lt { border-color:rgba(251,248,242,.45); }
.mv { position:absolute; left:110px; right:110px; top:0; bottom:0; display:flex; flex-direction:column; justify-content:center; gap:34px; z-index:6; }
.mv .tag { font-family:var(--serif); font-style:italic; font-size:150px; line-height:.85; color:var(--taupe); }
.quote { font-family:var(--serif); font-size:360px; line-height:.5; color:var(--taupe); opacity:.5; height:120px; }
.struck { position:relative; display:inline; background-image:linear-gradient(transparent 52%, rgba(138,119,99,.9) 52%, rgba(138,119,99,.9) 55%, transparent 55%); }

/* T1 case study: arch */
.linenbg { background-color:var(--linen); background-image:LINEN; }
.arch { overflow:hidden; border-radius:999px 999px 0 0; }
.arch img { width:100%; height:100%; object-fit:cover; display:block; }
.archline { border:1.5px solid var(--taupe); border-radius:999px 999px 0 0; }

/* T2 big stat: double rule frame */
.dbl { position:absolute; inset:40px; border:1px solid rgba(251,248,242,.55); z-index:4; }
.dbl::after { content:""; position:absolute; inset:10px; border:1px solid rgba(251,248,242,.35); }
.stat { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:34px; text-align:center; z-index:6; color:#FBF8F2; padding:0 120px; }
.big { font-family:var(--serif); font-style:italic; font-weight:500; font-size:420px; line-height:.8; letter-spacing:-.04em; font-variant-numeric:lining-nums; }
.big small { font-size:.42em; }

/* T3 mistakes: espresso, outline numerals */
.esp { background:var(--espresso); color:#F1EBE2; }
.outline { font-family:var(--serif); font-style:italic; font-weight:500; font-size:520px; line-height:.75; color:transparent; -webkit-text-stroke:2px rgba(217,198,172,.55); letter-spacing:-.04em; font-variant-numeric:lining-nums; }
.sq { position:absolute; overflow:hidden; } .sq img { width:100%; height:100%; object-fit:cover; display:block; }

/* T4 brand breakdown: magazine spread */
.spread { position:absolute; inset:0; display:grid; grid-template-columns:44% 56%; }
.spread .ph { position:relative; overflow:hidden; } .spread .ph img { width:100%; height:100%; object-fit:cover; display:block; }
.spread .tx { background-color:var(--paper); background-image:GRAIN; position:relative; padding:200px 70px 160px 64px; display:flex; flex-direction:column; gap:28px; }
.runhead { font:500 16px var(--sans); letter-spacing:.34em; text-transform:uppercase; color:var(--taupe); border-bottom:1px solid var(--ink); padding-bottom:14px; }
.drop::first-letter { font-family:var(--serif); font-size:112px; float:left; line-height:.82; padding:6px 12px 0 0; color:var(--taupe); }
.band { position:absolute; left:0; right:0; bottom:0; background-color:var(--paper); background-image:GRAIN; padding:56px 90px 120px; z-index:6; }

/* T5 checklist: index card on linen */
.card { justify-content:center; position:absolute; left:120px; right:120px; top:230px; bottom:230px; background-color:var(--paper); background-image:repeating-linear-gradient(transparent 0 63px, rgba(138,119,99,.18) 63px 64px); box-shadow:0 26px 50px -24px rgba(42,35,30,.5); padding:70px 70px; display:flex; flex-direction:column; gap:30px; z-index:6; }
.card .no { font-family:var(--serif); font-style:italic; font-size:44px; color:var(--taupe); }
.box { width:58px; height:58px; border:2px solid var(--ink); position:relative; }
.box::after { content:""; position:absolute; left:16px; top:4px; width:16px; height:32px; border-right:3px solid var(--taupe); border-bottom:3px solid var(--taupe); transform:rotate(45deg); }

/* T6 split comparison */
.split { position:absolute; inset:0; display:grid; grid-template-columns:1fr 1fr; }
.split .side { position:relative; overflow:hidden; }
.split .side img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
.split .side.them img { filter:grayscale(1) brightness(.75) contrast(.9); }
.split .side .ov { position:absolute; inset:0; background:linear-gradient(180deg, rgba(27,23,20,.35), rgba(27,23,20,.78)); }
.split .side .txt { position:absolute; left:56px; right:50px; bottom:190px; color:#FBF8F2; display:flex; flex-direction:column; gap:22px; }
.vs { position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); width:118px; height:118px; border-radius:50%; background:var(--paper); color:var(--ink); display:flex; align-items:center; justify-content:center; font-family:var(--serif); font-style:italic; font-size:44px; z-index:7; }
.split::after { content:""; position:absolute; left:50%; top:0; bottom:0; width:1px; background:rgba(251,248,242,.6); }

/* T7 solution selling: deckle-edged letter on plaster */
.letter { position:absolute; left:110px; right:110px; top:200px; bottom:190px; background-color:var(--paper); background-image:GRAIN; padding:86px 80px; display:flex; flex-direction:column; gap:30px; z-index:6; filter:drop-shadow(0 20px 26px rgba(42,35,30,.28)); }
.sig { font-family:var(--serif); font-style:italic; font-size:40px; color:var(--taupe); margin-top:auto; }
"""
CSS = CSS.replace("GRAIN", GRAIN).replace("PLASTER", PLASTER).replace("LINEN", LINEN)

slides = []
def add(tid, n, total, series, inner, cls="", tone="dark", col_left=None):
    col = "#FBF8F2" if tone == "light" else "#1B1714"
    swipe = "Swipe" if n < total else "@sageinteriordesignmarketing"
    pos = f"left:{col_left}px;right:70px;text-align:left;padding-left:0;" if col_left else ""
    fpos = f"left:{col_left}px;right:70px;" if col_left else ""
    slides.append(f'''<section class="slide {cls}" id="{tid}-{n:02d}">{inner}
<div class="mark" style="color:{col};{pos}">SAGE</div>
<div class="foot" style="color:{col};{fpos}"><span>No. {n:02d}</span><span>{series}</span><span>{swipe}</span></div></section>''')

def photo_cover(tid, total, series, photo, kicker, title, pill, extra=""):
    add(tid, 1, total, series, f'''<img class="cover-img" src="{photo}" alt=""><div class="shade"></div>{extra}
<div class="stat light-text"><p class="k">{kicker}</p><h1 class="it" style="font-size:124px">{title}</h1><span class="pill">{pill}</span></div>''', "grain lt", "light")

# ============ T0 MYTH VS TRUTH: plaster wall ============
T, S, N = "0-myth-vs-truth", "Myth vs. Truth", 5
add(T, 1, N, S, '''<div class="frame"></div><div class="mv"><p class="k" style="color:var(--taupe)">The myth</p>
<div class="quote">“</div><h1 class="rm" style="font-size:112px"><span class="struck">High-end clients don’t come from Instagram.</span></h1>
<p class="k" style="color:var(--taupe)">Half true. Swipe</p></div>''', "plaster grain")
for n, (tag, h, b) in enumerate([
    ("Half true.", "Most luxury clients won’t find you by <em>scrolling.</em>", "That part is real. Your best clients still arrive through people they trust."),
    ("Actually,", "almost every referral checks your Instagram <em>before they call.</em>", "Your page is where a warm introduction becomes a booked consultation, or quietly goes cold."),
    ("Instead,", "post the projects you want <em>more of.</em>", "Then make booking a call one tap from your bio, so a referral never has to search for the next step."),
], start=2):
    add(T, n, N, S, f'''<div class="frame"></div><div class="mv"><p class="tag">{tag}</p><h2 class="rm" style="font-size:90px">{h}</h2>
<div style="width:110px;height:1px;background:var(--ink);opacity:.5"></div><p class="body" style="max-width:27ch">{b}</p></div>''', "plaster grain")
add(T, 5, N, S, '''<img class="cover-img" src="KYRARAWS-429.jpg" alt=""><div class="shade"></div><div class="frame lt"></div>
<div class="stat"><p class="k">Before your next referral looks you up</p><h1 class="it" style="font-size:112px">Look at your grid like a stranger would.</h1><span class="pill">Save this</span></div>''', "grain lt", "light")

# ============ T1 CASE STUDY: arches on linen ============
T, S, N = "1-case-study", "Case Study", 5
add(T, 1, N, S, '''<div class="arch" style="position:absolute;left:190px;right:190px;top:150px;height:760px"><img src="dining.jpg" alt=""></div>
<div style="position:absolute;left:90px;right:90px;top:950px;text-align:center;display:flex;flex-direction:column;gap:22px;align-items:center;z-index:6">
<p class="k" style="color:var(--taupe)">Client case study</p><h1 class="it" style="font-size:100px"><span class="fill">[Studio name]</span></h1></div>''', "linenbg grain")
for n, (photo, k, h, b) in enumerate([
    ("bedroom.jpg", "Where she started", "[One line on her situation]", "[Two sentences in her words from the discovery call.]"),
    ("kitchen.jpg", "What we did", "[The one change that mattered most]", "[Two sentences on the strategy, not a list of deliverables.]"),
], start=2):
    add(T, n, N, S, f'''<div class="arch" style="position:absolute;right:90px;top:170px;width:390px;height:620px"><img src="{photo}" alt=""></div>
<div style="position:absolute;left:90px;width:470px;top:240px;display:flex;flex-direction:column;gap:30px;z-index:6">
<p class="k" style="color:var(--taupe)">{k}</p><h2 class="rm" style="font-size:80px"><span class="fill">{h}</span></h2></div>
<div style="position:absolute;left:90px;right:90px;top:870px;border-top:1px solid var(--ink);padding-top:34px;z-index:6"><p class="body fill">{b}</p></div>''', "linenbg grain")
add(T, 4, N, S, '''<div class="archline" style="position:absolute;left:170px;right:170px;top:170px;bottom:230px"></div>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:30px;text-align:center;z-index:6;padding:0 220px">
<p class="k" style="color:var(--taupe)">The result</p><div class="big fill" style="font-size:300px">[00]</div><p class="rm fill" style="font-size:48px;font-weight:400">[What the number means, over what time frame]</p></div>''', "linenbg grain")
add(T, 5, N, S, '''<img class="cover-img" src="terrace.jpg" alt=""><div class="shade"></div>
<div class="stat"><p class="k">Shared with her permission</p><h1 class="it" style="font-size:118px">Want this for your studio?</h1><span class="pill">Book a discovery call</span></div>''', "grain lt", "light")

# ============ T2 BIG STAT: full-bleed photo, double rule ============
T, S, N = "2-big-stat", "Three Months", 6
def stat_slide(n, photo, inner):
    add(T, n, N, S, f'<img class="cover-img" src="{photo}" alt=""><div class="shade"></div><div class="dbl"></div><div class="stat">{inner}</div>', "grain lt", "light")
stat_slide(1, "bedroom.jpg", '<p class="k">One Atlanta designer</p><h1 class="it" style="font-size:132px">Three months of Instagram</h1><span class="pill">Here’s what changed</span>')
for n, (photo, num, line) in enumerate([
    ("living.jpg", "+534<small>%</small>", "more people reached in her first three months"),
    ("library.jpg", "+539<small>%</small>", "more engagement from people who stopped to look"),
    ("dining.jpg", "+610", "new followers in her market"),
    ("bath.jpg", "3", "new leads, after years of relying on referrals alone"),
], start=2):
    stat_slide(n, photo, f'<div class="big">{num}</div><div style="width:1px;height:90px;background:#FBF8F2;opacity:.6"></div><p class="rm" style="font-size:54px;font-weight:400;max-width:18ch">{line}</p>')
stat_slide(6, "powder.jpg", '<p class="k">Your work is already good enough</p><h1 class="it" style="font-size:112px">Your Instagram should prove it.</h1><span class="pill">Book a discovery call</span>')

# ============ T3 MISTAKES: espresso, outline numerals, photo inset ============
T, S, N = "3-mistakes", "Mistakes", 6
add(T, 1, N, S, '''<div class="outline" style="position:absolute;left:40px;top:150px">4</div>
<div class="sq" style="right:90px;top:200px;width:430px;height:560px"><img src="powder.jpg" alt=""></div>
<div style="position:absolute;left:90px;right:90px;bottom:200px;display:flex;flex-direction:column;gap:26px;z-index:6">
<p class="k" style="color:#D9C6AC">Instagram for interior designers</p><h1 class="it" style="font-size:118px">Four mistakes keeping your page from booking projects.</h1></div>''', "esp grain lt", "light")
for n, (photo, h, b) in enumerate([
    ("stilllife.jpg", "You’re posting only when you feel <em>inspired.</em>", "Your future clients reward consistency. Inspiration shows up on its own schedule."),
    ("bedroom.jpg", "You’re only showing <em>finished rooms.</em>", "Clients hire a process, not a photo. Without it, you look like every other portfolio."),
    ("kitchen.jpg", "Your captions describe <em>the room.</em>", "They can see the room. Tell them what the homeowner was struggling with and what changed."),
    ("library.jpg", "Your bio sends people to a menu of <em>six links.</em>", "Every extra choice is a chance to leave. Give them one next step."),
], start=2):
    add(T, n, N, S, f'''<div class="outline" style="position:absolute;left:50px;top:140px">0{n-1}</div>
<div class="sq" style="right:90px;top:190px;width:300px;height:380px"><img src="{photo}" alt=""></div>
<div style="position:absolute;left:90px;right:90px;top:700px;display:flex;flex-direction:column;gap:30px;z-index:6">
<p class="k" style="color:#D9C6AC">Mistake No. 0{n-1}</p><h2 class="rm light-text" style="font-size:84px">{h}</h2>
<p class="body" style="color:rgba(241,235,226,.85);max-width:30ch">{b}</p></div>''', "esp grain lt", "light")
add(T, 6, N, S, '''<img class="cover-img" src="terrace.jpg" alt=""><div class="shade"></div>
<div class="stat"><p class="k">What to do instead</p><h1 class="it" style="font-size:118px">Plan ahead and keep one next step.</h1><span class="pill">Save for your next content day</span></div>''', "grain lt", "light")

# ============ T4 BRAND BREAKDOWN: magazine spread ============
T, S, N = "4-brand-breakdown", "Brand Insights", 5
add(T, 1, N, S, '''<img class="cover-img" src="stair.jpg" alt="">
<div class="band"><p class="runhead">Brand insights · A marketing breakdown</p>
<h1 class="it" style="font-size:108px;margin-top:26px">Why <span class="fill">[Designer]</span>’s Instagram works</h1></div>''', "grain", "dark")
for n, (photo, k, h, b) in enumerate([
    ("living.jpg", "Who they are", "[Studio, city, the work they’re known for]", "[One sentence on why your audience already knows the name.]"),
    ("dining.jpg", "What they do on Instagram", "[The pattern in their last twelve posts]", "[Formats, who is on camera, how often, what the captions do.]"),
    ("library.jpg", "Why it works", "[The strategy underneath it]", "[Tie it to a business result: who it attracts and what it signals to a buyer.]"),
], start=2):
    add(T, n, N, S, f'''<div class="spread"><div class="ph"><img src="{photo}" alt=""></div>
<div class="tx"><p class="runhead">{k}</p><h2 class="rm" style="font-size:72px"><span class="fill">{h}</span></h2>
<p class="body fill" style="font-size:30px">{b}</p></div></div>''', "", "dark", col_left=539)
add(T, 5, N, S, '''<img class="cover-img" src="house.jpg" alt="">
<div class="band"><p class="runhead">What it means for you</p>
<h1 class="it" style="font-size:96px;margin-top:26px"><span class="fill">[The one move you can copy this month]</span></h1></div>''', "grain", "dark")

# ============ T5 CHECKLIST: index card on linen ============
T, S, N = "5-checklist", "The Audit", 7
add(T, 1, N, S, '''<div class="card" style="justify-content:center;text-align:center;align-items:center"><p class="k" style="color:var(--taupe)">Instagram audit</p>
<h1 class="it" style="font-size:118px">Five things I check first</h1><p class="k" style="color:var(--taupe)">On a designer’s Instagram</p></div>''', "linenbg grain")
for n, (h, b) in enumerate([
    ("Your bio says who you serve and <em>where.</em>", "If a stranger can’t tell in three seconds, they won’t keep scrolling."),
    ("Your last nine posts match the work you <em>want.</em>", "Your grid is a sales pitch. It should sell the projects you want more of."),
    ("A real person shows up <em>on camera.</em>", "Clients hire you, not a mood board. Let them hear you before the first call."),
    ("Your captions give a reason to <em>reach out.</em>", "Every post should leave a client knowing what working with you feels like."),
    ("One link, one <em>next step.</em>", "Send people straight to booking. Don’t make them choose."),
], start=2):
    add(T, n, N, S, f'''<div class="card" style="justify-content:flex-start;padding-top:80px"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:auto"><span class="no">No. 0{n-1} of 05</span><div class="box"></div></div>
<h2 class="rm" style="font-size:96px;margin-top:30px">{h}</h2><p class="body" style="color:#3A322C;font-size:34px;margin-bottom:auto">{b}</p></div>''', "linenbg grain")
add(T, 7, N, S, '''<div class="card" style="justify-content:center;text-align:center;align-items:center">
<svg width="64" height="84" viewBox="0 0 64 84"><path d="M2 2h60v80L32 60 2 82z" fill="none" stroke="#1B1714" stroke-width="3"/></svg>
<h1 class="it" style="font-size:120px">Save this.</h1><p class="body" style="color:#3A322C">Run it on your own page this week, and share it with a designer friend.</p></div>''', "linenbg grain")

# ============ T6 SAGE VS AGENCY: split screen ============
T, S, N = "6-sage-vs-agency", "Sage vs. Agency", 6
photo_cover(T, N, S, "library.jpg", "Before you hire anyone", "What a typical agency does", "And what Sage does instead")
for n, (photo, t, u) in enumerate([
    ("stilllife.jpg", "Posts for you", "Runs a strategy built around the projects you want"),
    ("bedroom.jpg", "Reports followers and likes", "Tracks inquiries and booked projects"),
    ("living.jpg", "Works with any industry", "Only works with interior designers"),
    ("dining.jpg", "Hands you a template", "Starts from a discovery call about your studio"),
], start=2):
    add(T, n, N, S, f'''<div class="split"><div class="side them"><img src="{photo}" alt="" style="object-position:left center"><div class="ov"></div>
<div class="txt"><p class="k" style="font-size:17px;opacity:.75">A typical agency</p><p class="rm" style="font-size:62px;opacity:.75">{t}</p></div></div>
<div class="side"><img src="{photo}" alt="" style="object-position:right center"><div class="ov"></div>
<div class="txt"><p class="k" style="font-size:17px;color:#D9C6AC">Sage</p><p class="it" style="font-size:66px;line-height:1.02">{u}</p></div></div></div><div class="vs">vs.</div>''', "grain lt", "light")
add(T, 6, N, S, '''<img class="cover-img" src="Sage-interior-design-marketing-agency.jpg" alt=""><div class="shade"></div>
<div class="stat"><p class="k">Booked projects, not likes</p><h1 class="it" style="font-size:108px">See what a strategy built for your studio looks like.</h1><span class="pill">Book a discovery call</span></div>''', "grain lt", "light")

# ============ T7 SOLUTION SELLING: deckle letter on plaster ============
T, S, N = "7-solution-selling", "For Designers", 5
photo_cover(T, N, S, "house.jpg", "If this sounds familiar", "Your referrals are slowing down", "And nothing is replacing them")
for n, (k, h, b) in enumerate([
    ("The problem", "You can’t control when the next referral <em>comes in.</em>", "A great year can turn into a quiet quarter, and you only find out once the calendar is empty."),
    ("Why your current approach won’t fix it", "Posting when you have time won’t build a <em>pipeline.</em>", "Clients who don’t know you yet need to see you consistently, long before they’re ready to call."),
    ("How Sage fixes it", "A strategy built around the projects you want <em>more of.</em>", "Your account manager plans and posts every week. You approve everything, and we report on inquiries, not followers."),
], start=2):
    clip = deckle(860, 960)
    add(T, n, N, S, f'''<div class="letter" style="clip-path:{clip}"><p class="k" style="color:var(--taupe);font-size:18px">{k}</p>
<h2 class="rm" style="font-size:92px;margin-top:40px">{h}</h2><p class="body" style="color:#3A322C;font-size:34px">{b}</p><p class="sig">Kyra, founder of Sage</p></div>''', "plaster grain")
add(T, 5, N, S, '''<img class="cover-img" src="terrace.jpg" alt=""><div class="shade"></div>
<div class="stat"><p class="k">Ready for a steadier pipeline?</p><h1 class="it" style="font-size:118px">Let’s talk about your studio.</h1><span class="pill">Book a discovery call</span></div>''', "grain lt", "light")

head = f'''<!doctype html><html><head><meta charset="utf-8"><title>Sage carousel templates</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600&family=Montserrat:wght@400;500;600&display=swap">
<style>{CSS}</style></head><body>'''
open("carousels.html", "w").write(head + "\n".join(slides) + "</body></html>")
print(len(slides), "slides")
