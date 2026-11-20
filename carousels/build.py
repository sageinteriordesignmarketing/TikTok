"""Builds Sage carousel templates (1080x1350) as one HTML file; render.js screenshots each slide."""
import html

PHOTOS = {
    "linen": "Sage-interior-design-marketing-agency.jpg",
    "magazine": "KYRARAWS-442.jpg",
    "tablet": "KYRARAWS-429.jpg",
    "moodboard": "Sage-interior-design-marketing.jpg",
    "sofa": "interior-design-marketing-agency.jpg",
    "chair": "Office-interior-design-digitalmarketing-agency.jpg",
}

CSS = """
:root { --linen:#F4EFE8; --sand:#E8DFD3; --sand2:#D9CCBB; --taupe:#7A6A58; --espresso:#2A231E; --ink:#1B1714; --paper:#FFFDF9;
  --serif:"Cormorant Garamond", Georgia, serif; --sans:"Montserrat", Arial, sans-serif; }
* { box-sizing:border-box; margin:0; padding:0; }
body { background:#999; font-family:var(--sans); }
.slide { width:1080px; height:1350px; position:relative; overflow:hidden; display:flex; flex-direction:column; padding:84px 90px 0; margin:20px; }
.light { background:var(--linen); color:var(--ink); }
.sand { background:var(--sand); color:var(--ink); }
.dark { background:var(--espresso); color:var(--linen); }
.photo { color:var(--paper); background:var(--espresso); }
.photo > img.bg { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
.photo::after { content:""; position:absolute; inset:0; background:linear-gradient(180deg, rgba(27,23,20,.25) 0%, rgba(27,23,20,.35) 40%, rgba(27,23,20,.85) 100%); }
.photo > * { position:relative; z-index:2; }
.top { display:flex; justify-content:space-between; align-items:center; }
.top img { height:46px; }
.series { font:500 19px var(--sans); letter-spacing:.32em; text-transform:uppercase; opacity:.75; }
.body { flex:1; display:flex; flex-direction:column; justify-content:center; gap:34px; }
.body.bottom { justify-content:flex-end; padding-bottom:70px; }
.kicker { font:600 20px var(--sans); letter-spacing:.34em; text-transform:uppercase; color:var(--taupe); }
.dark .kicker, .photo .kicker { color:#CBB9A3; }
h1 { font-family:var(--serif); font-weight:500; font-size:118px; line-height:1.0; letter-spacing:-.015em; font-variant-numeric:lining-nums; }
h1.md { font-size:94px; } h1.sm { font-size:78px; }
h1 em, .em { font-style:italic; font-weight:400; color:var(--taupe); }
.dark h1 em, .photo h1 em, .dark .em { color:#CBB9A3; }
p.lead { font-family:var(--serif); font-size:46px; line-height:1.3; max-width:22ch; font-weight:400; }
p.copy { font:400 32px/1.55 var(--sans); max-width:30ch; }
.dark p.copy { color:rgba(244,239,232,.86); }
.rule { width:120px; height:2px; background:currentColor; opacity:.5; }
.foot { display:flex; justify-content:space-between; align-items:center; padding:30px 0 46px; border-top:1px solid currentColor; border-color:rgba(122,106,88,.35); font:500 18px var(--sans); letter-spacing:.3em; text-transform:uppercase; opacity:.8; }
.ticker { position:absolute; left:0; right:0; bottom:0; height:64px; background:var(--ink); color:var(--linen); overflow:hidden; display:flex; align-items:center; z-index:3; }
.light .ticker, .sand .ticker { background:var(--espresso); }
.dark .ticker { background:var(--linen); color:var(--espresso); }
.ticker span { white-space:nowrap; font:500 19px var(--sans); letter-spacing:.34em; text-transform:uppercase; transform:translateX(-120px); }
.has-ticker .foot { margin-bottom:64px; }
.big { font-family:var(--serif); font-weight:500; font-size:400px; line-height:.82; letter-spacing:-.04em; font-variant-numeric:lining-nums; }
.big small { font-size:.45em; letter-spacing:-.02em; }
.stamp { display:inline-block; border:2px solid currentColor; padding:12px 26px; font:600 22px var(--sans); letter-spacing:.32em; text-transform:uppercase; align-self:flex-start; }
.strike { text-decoration:line-through; text-decoration-thickness:3px; text-decoration-color:var(--taupe); }
.num { font-family:var(--serif); font-size:150px; line-height:.85; font-weight:500; color:var(--taupe); font-variant-numeric:lining-nums; }
.dark .num { color:#CBB9A3; }
.cols { display:grid; grid-template-columns:1fr 1fr; border-top:2px solid currentColor; }
.cols > div { padding:36px 34px 0 0; display:flex; flex-direction:column; gap:22px; }
.cols > div + div { padding-left:34px; border-left:1px solid rgba(122,106,88,.45); }
.cols .lab { font:600 22px var(--sans); letter-spacing:.3em; text-transform:uppercase; color:var(--taupe); }
.cols .them { font-family:var(--serif); font-size:66px; line-height:1.1; color:var(--taupe); }
.dark .cols .them { color:#A89886; }
.dark .cols .lab { color:#CBB9A3; }
.cols .us { font-family:var(--serif); font-size:66px; line-height:1.1; font-weight:500; }
.fill { color:var(--taupe); }
.dark .fill, .photo .fill { color:#CBB9A3; }
.card { background:var(--paper); color:var(--ink); padding:44px 48px; display:flex; flex-direction:column; gap:18px; }
.handle { font:500 22px var(--sans); letter-spacing:.2em; text-transform:uppercase; }
.saveicon { width:70px; height:86px; border:3px solid currentColor; border-bottom:none; position:relative; }
.saveicon::after { content:""; position:absolute; left:-3px; right:-3px; bottom:-26px; height:52px; background:linear-gradient(135deg, transparent 49%, currentColor 49%, currentColor 53%, transparent 53%), linear-gradient(225deg, transparent 49%, currentColor 49%, currentColor 53%, transparent 53%); background-size:50% 100%; background-repeat:no-repeat; background-position:left, right; }
.label-row { display:flex; gap:22px; align-items:baseline; }

.cover { background:var(--linen); color:var(--ink); }
.cover .cimg { position:absolute; left:0; top:0; width:100%; height:700px; object-fit:cover; }
.cover::before { content:""; position:absolute; left:0; top:0; right:0; height:220px; background:linear-gradient(180deg, rgba(27,23,20,.45), rgba(27,23,20,0)); z-index:1; }
.cover > .top { position:relative; z-index:2; color:var(--paper); }
.cover .series { opacity:.95; }
.cover .body { position:relative; z-index:2; justify-content:flex-start; padding-top:660px; padding-bottom:0; gap:26px; }
.cover .kicker { color:var(--taupe); }
.cover h1 { font-size:84px; line-height:1.04; }
.cover h1 em, .cover .fill { color:var(--taupe); }
.cover .stamp { color:var(--ink); }
h1.sm { font-size:92px; line-height:1.03; }
p.copy { font-size:36px; line-height:1.5; max-width:28ch; }
p.lead { font-size:56px; line-height:1.25; }
.kicker { font-size:22px; }
.body { gap:40px; }
"""

TICK = "Sage &nbsp;✦&nbsp; Interior Design Marketing &nbsp;✦&nbsp; Booked projects, not likes &nbsp;✦&nbsp; "

slides = []  # (template_id, index, html)

def slide(tid, theme, series, inner, n, total, ticker=False, photo=None, bottom=False, nofoot=False):
    if photo: theme = "cover"
    logo = "logo-ink.png" if theme in ("light", "sand") else "logo-white.png"
    bg = f'<img class="cimg" src="{PHOTOS[photo]}" alt="">' if photo else ""
    cls = f"slide {theme}" + (" has-ticker" if ticker else "")
    swipe = "Swipe →" if n < total else "@sageinteriordesignmarketing"
    foot = "" if nofoot else f'<div class="foot"><span>{n:02d} / {total:02d}</span><span>{swipe}</span></div>'
    tk = f'<div class="ticker"><span>{TICK*6}</span></div>' if ticker else ""
    h = f'''<section class="{cls}" id="{tid}-{n:02d}">{bg}
  <div class="top"><img src="{logo}" alt="Sage"><span class="series">{series}</span></div>
  <div class="body{' bottom' if bottom else ''}">{inner}</div>
  {foot}{tk}
</section>'''
    slides.append((tid, n, h))

# ---------------- 0 · MYTH VS TRUTH ----------------
T, S = "0-myth-vs-truth", "Myth vs. truth"
slide(T, "photo", S, '''<span class="stamp">The myth</span>
<h1 class="md">“High-end clients don’t come from <em>Instagram.</em>”</h1>''', 1, 5, photo="tablet", bottom=True, ticker=True)
slide(T, "light", S, '''<p class="kicker">Half true</p>
<h1 class="sm">Most luxury clients won’t find you by <em>scrolling.</em></h1>
<div class="rule"></div>
<p class="copy">That part is real. Your best clients still arrive through people they trust.</p>''', 2, 5)
slide(T, "dark", S, '''<p class="kicker">What’s actually true</p>
<h1 class="sm">Almost every referral checks your Instagram <em>before they call.</em></h1>
<div class="rule"></div>
<p class="copy">Your page is where a warm introduction becomes a booked consultation, or quietly goes cold.</p>''', 3, 5)
slide(T, "sand", S, '''<p class="kicker">What to do instead</p>
<h1 class="sm">Post the projects you want <em>more of.</em></h1>
<p class="copy">Then make booking a call one tap from your bio, so a referral never has to search for the next step.</p>''', 4, 5)
slide(T, "dark", S, '''<p class="kicker">Before your next referral looks you up</p>
<h1 class="md">Save this, then look at your grid like a <em>stranger would.</em></h1>''', 5, 5, ticker=True)

# ---------------- 1 · CLIENT CASE STUDY ----------------
T, S = "1-case-study", "Client case study"
slide(T, "photo", S, '''<p class="kicker">Case study</p>
<h1 class="md">How <span class="fill">[Studio name]</span> booked <em>[result]</em> from Instagram</h1>''', 1, 5, photo="linen", bottom=True, ticker=True)
slide(T, "light", S, '''<p class="kicker">Where she started</p>
<h1 class="sm"><span class="fill">[One line on her situation]</span></h1>
<div class="rule"></div>
<p class="copy"><span class="fill">[Two sentences: what she was doing, and what wasn’t working. Use her words from the discovery call.]</span></p>''', 2, 5)
slide(T, "dark", S, '''<p class="kicker">What we did</p>
<h1 class="sm"><span class="fill">[The one change that mattered most]</span></h1>
<div class="rule"></div>
<p class="copy"><span class="fill">[Two sentences on the strategy. Name the approach, not a list of deliverables.]</span></p>''', 3, 5)
slide(T, "sand", S, '''<p class="kicker">The result · <span class="fill">[time frame]</span></p>
<div class="big"><span class="fill">[00]</span></div>
<p class="lead"><span class="fill">[What the number means, in one line]</span></p>''', 4, 5)
slide(T, "dark", S, '''<p class="kicker">Want this for your studio?</p>
<h1 class="md">Book a discovery call. <em>Link in bio.</em></h1>
<p class="copy">Results vary by studio. Shared with <span class="fill">[client]</span>’s permission.</p>''', 5, 5, ticker=True)

# ---------------- 2 · BIG STAT (ready to post: public Atlanta results) ----------------
T, S = "2-big-stat", "Three months"
slide(T, "photo", S, '''<p class="kicker">One Atlanta designer</p>
<h1 class="md">Three months of Instagram with Sage. <em>Here’s what changed.</em></h1>''', 1, 6, photo="magazine", bottom=True, ticker=True)
slide(T, "light", S, '''<div class="big">+534<small>%</small></div>
<p class="lead">More people reached in her first three months.</p>''', 2, 6)
slide(T, "dark", S, '''<div class="big">+539<small>%</small></div>
<p class="lead">More engagement, from people who actually stopped to look.</p>''', 3, 6)
slide(T, "sand", S, '''<div class="big">+610</div>
<p class="lead">New followers in her market.</p>''', 4, 6)
slide(T, "dark", S, '''<div class="big">3</div>
<p class="lead">New leads in three months, after years of relying on referrals alone.</p>''', 5, 6)
slide(T, "light", S, '''<p class="kicker">Your work is already good enough</p>
<h1 class="md">Your Instagram should <em>prove it.</em></h1>
<p class="copy">Book a discovery call through the link in bio.</p>''', 6, 6, ticker=True)

# ---------------- 3 · MISTAKES ----------------
T, S = "3-mistakes", "Mistakes"
slide(T, "photo", S, '''<p class="kicker">Instagram for interior designers</p>
<h1 class="md">Four mistakes keeping your page <em>from booking projects.</em></h1>''', 1, 6, photo="chair", bottom=True, ticker=True)
for i, (head, why, theme) in enumerate([
    ("You’re posting only when you feel <em>inspired.</em>", "The algorithm and your future clients both reward consistency. Inspiration shows up on its own schedule.", "light"),
    ("You’re only showing <em>finished rooms.</em>", "Clients hire a process, not a photo. Without it, you look like every other portfolio.", "dark"),
    ("Your captions describe <em>the room.</em>", "They can see the room. Tell them what the homeowner was struggling with and what changed.", "sand"),
    ("Your bio sends people to a menu of <em>six links.</em>", "Every extra choice is a chance to leave. Give them one next step.", "dark"),
], start=2):
    slide(T, theme, S, f'''<p class="kicker">Mistake {i-1:02d}</p>
<h1 class="sm">{head}</h1>
<div class="rule"></div>
<p class="copy">{why}</p>''', i, 6)
slide(T, "light", S, '''<p class="kicker">What to do instead</p>
<h1 class="sm">Plan a month ahead, show the process, and give one clear <em>next step.</em></h1>
<p class="copy">Save this for your next content day.</p>''', 6, 6, ticker=True)

# ---------------- 4 · BRAND BREAKDOWN ----------------
T, S = "4-brand-breakdown", "Brand breakdown"
slide(T, "photo", S, '''<p class="kicker">Brand breakdown</p>
<h1 class="md">Why <span class="fill">[Designer]</span>’s Instagram <em>works.</em></h1>''', 1, 5, photo="moodboard", bottom=True, ticker=True)
slide(T, "light", S, '''<p class="kicker">Who they are</p>
<h1 class="sm"><span class="fill">[Studio, city, the kind of work they’re known for]</span></h1>
<div class="rule"></div>
<p class="copy"><span class="fill">[One sentence on why the audience already knows the name.]</span></p>''', 2, 5)
slide(T, "dark", S, '''<p class="kicker">What they do on Instagram</p>
<h1 class="sm"><span class="fill">[The pattern you can see in their last 12 posts]</span></h1>
<div class="rule"></div>
<p class="copy"><span class="fill">[Specifics: formats, who’s on camera, how often, what the captions do.]</span></p>''', 3, 5)
slide(T, "sand", S, '''<p class="kicker">Why it works</p>
<h1 class="sm"><span class="fill">[The strategy underneath it]</span></h1>
<div class="rule"></div>
<p class="copy"><span class="fill">[Tie it to a business result: who it attracts, what it signals to a buyer.]</span></p>''', 4, 5)
slide(T, "dark", S, '''<p class="kicker">What it means for you</p>
<h1 class="sm"><span class="fill">[The one move a smaller studio can copy this month]</span></h1>
<p class="copy">Follow for a new breakdown every week.</p>''', 5, 5, ticker=True)

# ---------------- 5 · CHECKLIST / AUDIT ----------------
T, S = "5-checklist", "The audit"
slide(T, "photo", S, '''<p class="kicker">Instagram audit</p>
<h1 class="md">The five things I check first on a <em>designer’s Instagram.</em></h1>''', 1, 7, photo="sofa", bottom=True, ticker=True)
checks = [
    ("Your bio says who you serve and <em>where.</em>", "If a stranger can’t tell in three seconds, they won’t keep scrolling."),
    ("Your last nine posts match the projects you <em>want.</em>", "Your grid is a sales pitch. It should sell the work you want more of."),
    ("A real person shows up <em>on camera.</em>", "Clients hire you, not a mood board. Let them hear you before the first call."),
    ("Your captions give a reason to <em>reach out.</em>", "Every post should leave a client knowing what working with you feels like."),
    ("There’s one link and one <em>next step.</em>", "Send people straight to booking. Don’t make them choose."),
]
themes = ["light", "dark", "sand", "dark", "light"]
for i, ((h, c), th) in enumerate(zip(checks, themes), start=2):
    slide(T, th, S, f'''<div class="num">{i-1:02d}</div>
<h1 class="sm">{h}</h1>
<div class="rule"></div>
<p class="copy">{c}</p>''', i, 7)
slide(T, "dark", S, '''<div class="saveicon"></div>
<h1 class="md">Save this and run it on your own page <em>this week.</em></h1>
<p class="copy">Share it with a designer friend who needs it.</p>''', 7, 7, ticker=True)

# ---------------- 6 · SAGE VS TYPICAL AGENCY ----------------
T, S = "6-sage-vs-agency", "Sage vs. a typical agency"
slide(T, "photo", S, '''<p class="kicker">Before you hire anyone</p>
<h1 class="md">What a typical agency does, and what <em>Sage does instead.</em></h1>''', 1, 6, photo="linen", bottom=True, ticker=True)
rows = [
    ("Posts for you", "Runs a strategy built around the projects you want"),
    ("Reports followers and likes", "Tracks inquiries and booked projects"),
    ("Works with any industry", "Only works with interior designers"),
    ("Hands you a template", "Starts from a discovery call about your studio"),
]
themes = ["light", "dark", "sand", "dark"]
for i, ((them, us), th) in enumerate(zip(rows, themes), start=2):
    slide(T, th, S, f'''<div class="cols">
  <div><span class="lab">A typical agency</span><p class="them">{them}</p></div>
  <div><span class="lab" style="color:inherit;opacity:.9">Sage</span><p class="us">{us}</p></div>
</div>''', i, 6)
slide(T, "light", S, '''<p class="kicker">Booked projects, not likes</p>
<h1 class="md">See what a strategy built for <em>your studio</em> looks like.</h1>
<p class="copy">Book a discovery call through the link in bio.</p>''', 6, 6, ticker=True)

# ---------------- 7 · SOLUTION SELLING ----------------
T, S = "7-solution-selling", "For designers"
slide(T, "photo", S, '''<p class="kicker">If this sounds familiar</p>
<h1 class="md">Your referrals are slowing down, and nothing is <em>replacing them.</em></h1>''', 1, 5, photo="chair", bottom=True, ticker=True)
slide(T, "light", S, '''<p class="kicker">The problem</p>
<h1 class="sm">You can’t control when the next referral <em>comes in.</em></h1>
<div class="rule"></div>
<p class="copy">A great year can turn into a quiet quarter, and you only find out once the calendar is already empty.</p>''', 2, 5)
slide(T, "dark", S, '''<p class="kicker">Why your current approach won’t fix it</p>
<h1 class="sm">Posting when you have time won’t build a <em>pipeline.</em></h1>
<div class="rule"></div>
<p class="copy">Clients who don’t know you yet need to see you consistently, long before they’re ready to call.</p>''', 3, 5)
slide(T, "sand", S, '''<p class="kicker">How Sage fixes it</p>
<h1 class="sm">A strategy built around the projects you want <em>more of.</em></h1>
<div class="rule"></div>
<p class="copy">Your account manager plans and posts every week. You approve everything, and we report on inquiries, not followers.</p>''', 4, 5)
slide(T, "dark", S, '''<p class="kicker">Ready for a steadier pipeline?</p>
<h1 class="md">Book a discovery call. <em>Link in bio.</em></h1>''', 5, 5, ticker=True)

head = f'''<!doctype html><html><head><meta charset="utf-8"><title>Sage carousel templates</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Montserrat:wght@400;500;600&display=swap">
<style>{CSS}</style></head><body>'''
open("carousels.html", "w").write(head + "\n".join(h for _, _, h in slides) + "</body></html>")
print(len(slides), "slides")
