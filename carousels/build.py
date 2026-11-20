"""Sage carousel templates v2: photography-led editorial system. 1080x1350 slides."""

CSS = """
:root { --linen:#F4EFE8; --paper:#FBF8F3; --sand:#E8DFD3; --taupe:#8A7763; --espresso:#2A231E; --ink:#1B1714;
  --serif:"Cormorant Garamond", Georgia, serif; --sans:"Montserrat", Arial, sans-serif; }
* { box-sizing:border-box; margin:0; padding:0; }
body { background:#888; }
.slide { width:1080px; height:1350px; position:relative; overflow:hidden; margin:20px; color:var(--paper); background:var(--espresso); font-family:var(--sans); }
.slide > img.bg { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
.shade::after { content:""; position:absolute; inset:0; background:radial-gradient(ellipse at center, rgba(30,24,20,.42) 0%, rgba(30,24,20,.7) 100%); z-index:1; }
.blur > img.bg { filter:blur(6px) brightness(.6) saturate(.85); transform:scale(1.06); }
.layer { position:absolute; inset:0; z-index:2; display:flex; flex-direction:column; align-items:center; text-align:center; padding:78px 96px 70px; }
.mark { font:500 22px var(--sans); letter-spacing:.62em; text-transform:uppercase; padding-left:.62em; opacity:.92; }
.center { flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:38px; width:100%; }
.kicker { font:500 21px var(--sans); letter-spacing:.42em; text-transform:uppercase; padding-left:.42em; opacity:.9; }
h1 { font-family:var(--serif); font-style:italic; font-weight:500; font-size:128px; line-height:.96; letter-spacing:-.02em; font-variant-numeric:lining-nums; text-wrap:balance; }
h1.md { font-size:104px; }
h1 .up { font-style:normal; }
.pill { border:1.5px solid currentColor; border-radius:999px; padding:20px 44px; font:500 19px var(--sans); letter-spacing:.32em; text-transform:uppercase; }
.line { font-family:var(--serif); font-size:54px; line-height:1.22; max-width:19ch; }
.foot { width:100%; display:flex; justify-content:space-between; font:500 17px var(--sans); letter-spacing:.34em; text-transform:uppercase; opacity:.8; }
.big { font-family:var(--serif); font-style:italic; font-weight:500; font-size:420px; line-height:.8; letter-spacing:-.04em; font-variant-numeric:lining-nums; }
.big small { font-size:.42em; }
.hair { width:1px; height:90px; background:currentColor; opacity:.6; }
.sheet { position:relative; background:var(--paper); color:var(--ink); width:860px; box-shadow:0 40px 80px -30px rgba(0,0,0,.65); padding:58px 64px 60px; text-align:left; display:flex; flex-direction:column; gap:26px; }
.sheet.tilt { transform:rotate(-2deg); }
.sheet .mast { display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--ink); padding-bottom:16px; }
.sheet .mast b { font:500 20px var(--sans); letter-spacing:.5em; }
.sheet .mast span { font:500 15px var(--sans); letter-spacing:.3em; text-transform:uppercase; color:var(--taupe); }
.sheet .k { font:600 17px var(--sans); letter-spacing:.34em; text-transform:uppercase; color:var(--taupe); }
.sheet h2 { font-family:var(--serif); font-weight:500; font-size:76px; line-height:1.02; letter-spacing:-.015em; font-variant-numeric:lining-nums; }
.sheet h2 em { color:var(--taupe); }
.sheet p.b { font:400 29px/1.6 var(--sans); color:#3A322C; }
.sheet .no { font-family:var(--serif); font-style:italic; font-size:110px; line-height:.85; color:var(--taupe); font-variant-numeric:lining-nums; }
.cmp { display:grid; grid-template-columns:1fr 1fr; border-top:1px solid var(--ink); }
.cmp div { padding:26px 26px 0 0; display:flex; flex-direction:column; gap:14px; }
.cmp div + div { padding-left:26px; border-left:1px solid #D9CCBB; }
.cmp .l { font:600 16px var(--sans); letter-spacing:.32em; text-transform:uppercase; color:var(--taupe); }
.cmp .t { font-family:var(--serif); font-size:52px; line-height:1.08; color:#A39280; }
.cmp .s { font-family:var(--serif); font-size:52px; line-height:1.08; font-weight:500; }
.fill { opacity:.78; }
.sheet .fill { color:var(--taupe); opacity:1; }
"""

slides = []

def frame(tid, n, total, photo, inner, mode, series):
    swipe = "Swipe" if n < total else "@sageinteriordesignmarketing"
    slides.append(f'''<section class="slide {mode}" id="{tid}-{n:02d}"><img class="bg" src="{photo}" alt="">
<div class="layer"><div class="mark">Sage</div><div class="center">{inner}</div>
<div class="foot"><span>No. {n:02d}</span><span>{series}</span><span>{swipe}</span></div></div></section>''')

def cover(tid, total, photo, kicker, title, pill, series):
    frame(tid, 1, total, photo, f'<p class="kicker">{kicker}</p><h1>{title}</h1><span class="pill">{pill}</span>', "shade", series)

def sheet(tid, n, total, photo, k, title, body, series, tilt=False, extra=""):
    kk = f'<p class="k">{k}</p>' if k else ""
    inner = f'''<div class="sheet{' tilt' if tilt else ''}"><div class="mast"><b>SAGE</b><span>{series}</span></div>
{extra}{kk}<h2>{title}</h2><p class="b">{body}</p></div>'''
    frame(tid, n, total, photo, inner, "blur", series)

def stat(tid, n, total, photo, num, line, series):
    frame(tid, n, total, photo, f'<div class="big">{num}</div><div class="hair"></div><p class="line">{line}</p>', "shade", series)

def close(tid, n, total, photo, kicker, title, pill, series):
    frame(tid, n, total, photo, f'<p class="kicker">{kicker}</p><h1 class="md">{title}</h1><span class="pill">{pill}</span>', "shade", series)

# ---------------- MYTH VS TRUTH ----------------
T, S, N = "0-myth-vs-truth", "Myth vs. Truth", 5
cover(T, N, "Sage-interior-design-marketing-agency.jpg", "The myth", "“High-end clients don’t come from Instagram.”", "Half true. Keep reading", S)
sheet(T, 2, N, "living.jpg", "Half true", "Most luxury clients won’t find you by <em>scrolling.</em>", "That part is real. Your best clients still arrive through people they trust.", S)
sheet(T, 3, N, "library.jpg", "What’s actually true", "Almost every referral checks your Instagram <em>before they call.</em>", "Your page is where a warm introduction becomes a booked consultation, or quietly goes cold.", S, tilt=True)
sheet(T, 4, N, "stilllife.jpg", "What to do instead", "Post the projects you want <em>more of.</em>", "Then make booking a call one tap from your bio, so a referral never has to search for the next step.", S)
close(T, N, N, "KYRARAWS-429.jpg", "Before your next referral looks you up", "Look at your grid like a stranger would.", "Save this", S)

# ---------------- CASE STUDY ----------------
T, S, N = "1-case-study", "Case Study", 5
cover(T, N, "dining.jpg", "Client case study", '<span class="fill">[Studio name]</span>', '<span class="fill">[The result in four words]</span>', S)
sheet(T, 2, N, "bedroom.jpg", "Where she started", '<span class="fill">[One line on her situation]</span>', '<span class="fill">[Two sentences in her words from the discovery call.]</span>', S)
sheet(T, 3, N, "kitchen.jpg", "What we did", '<span class="fill">[The one change that mattered most]</span>', '<span class="fill">[Two sentences on the strategy, not a list of deliverables.]</span>', S, tilt=True)
stat(T, 4, N, "stair.jpg", '<span class="fill">[00]</span>', '<span class="fill">[What the number means, over what time frame]</span>', S)
close(T, N, N, "terrace.jpg", "Shared with her permission", "Want this for your studio?", "Book a discovery call", S)

# ---------------- BIG STAT (ready) ----------------
T, S, N = "2-big-stat", "Three Months", 6
cover(T, N, "bedroom.jpg", "One Atlanta designer", 'Three months <span class="up">of</span> Instagram', "Here’s what changed", S)
stat(T, 2, N, "living.jpg", "+534<small>%</small>", "more people reached in her first three months", S)
stat(T, 3, N, "library.jpg", "+539<small>%</small>", "more engagement from people who stopped to look", S)
stat(T, 4, N, "dining.jpg", "+610", "new followers in her market", S)
stat(T, 5, N, "bath.jpg", "3", "new leads, after years of relying on referrals alone", S)
close(T, N, N, "powder.jpg", "Your work is already good enough", "Your Instagram should prove it.", "Book a discovery call", S)

# ---------------- MISTAKES ----------------
T, S, N = "3-mistakes", "Mistakes", 6
cover(T, N, "powder.jpg", "Instagram for interior designers", "Four mistakes", "Keeping your page from booking projects", S)
for i, (photo, h, b) in enumerate([
    ("stilllife.jpg", "You’re posting only when you feel <em>inspired.</em>", "Your future clients reward consistency. Inspiration shows up on its own schedule."),
    ("bedroom.jpg", "You’re only showing <em>finished rooms.</em>", "Clients hire a process, not a photo. Without it, you look like every other portfolio."),
    ("kitchen.jpg", "Your captions describe <em>the room.</em>", "They can see the room. Tell them what the homeowner was struggling with and what changed."),
    ("library.jpg", "Your bio sends people to a menu of <em>six links.</em>", "Every extra choice is a chance to leave. Give them one next step."),
], start=2):
    sheet(T, i, N, photo, f"Mistake No. {i-1:02d}", h, b, S, tilt=(i % 2 == 1))
close(T, N, N, "terrace.jpg", "What to do instead", "Plan ahead and keep one next step.", "Save for your next content day", S)

# ---------------- BRAND BREAKDOWN ----------------
T, S, N = "4-brand-breakdown", "Brand Insights", 5
cover(T, N, "stair.jpg", "Brand insights", 'Why <span class="fill">[Designer]</span>’s Instagram works', "A marketing breakdown", S)
for i, (photo, k, h, b) in enumerate([
    ("living.jpg", "Who they are", "[Studio, city, the work they’re known for]", "[One sentence on why your audience already knows the name.]"),
    ("dining.jpg", "What they do on Instagram", "[The pattern in their last twelve posts]", "[Formats, who is on camera, how often, what the captions do.]"),
    ("library.jpg", "Why it works", "[The strategy underneath it]", "[Tie it to a business result: who it attracts and what it signals to a buyer.]"),
], start=2):
    sheet(T, i, N, photo, k, f'<span class="fill">{h}</span>', f'<span class="fill">{b}</span>', S, tilt=(i == 3))
close(T, N, N, "house.jpg", "What it means for you", '<span class="fill">[The one move you can copy this month]</span>', "Follow for weekly breakdowns", S)

# ---------------- CHECKLIST ----------------
T, S, N = "5-checklist", "The Audit", 7
cover(T, N, "Office-interior-design-digitalmarketing-agency.jpg", "Instagram audit", "Five things I check first", "On a designer’s Instagram", S)
for i, (photo, h, b) in enumerate([
    ("bedroom.jpg", "Your bio says who you serve and <em>where.</em>", "If a stranger can’t tell in three seconds, they won’t keep scrolling."),
    ("dining.jpg", "Your last nine posts match the work you <em>want.</em>", "Your grid is a sales pitch. It should sell the projects you want more of."),
    ("living.jpg", "A real person shows up <em>on camera.</em>", "Clients hire you, not a mood board. Let them hear you before the first call."),
    ("kitchen.jpg", "Your captions give a reason to <em>reach out.</em>", "Every post should leave a client knowing what working with you feels like."),
    ("powder.jpg", "One link, one <em>next step.</em>", "Send people straight to booking. Don’t make them choose."),
], start=2):
    sheet(T, i, N, photo, "", h, b, S, tilt=(i % 2 == 1), extra=f'<div class="no">No. {i-1:02d}</div>')
close(T, N, N, "interior-design-marketing-agency.jpg", "Run it on your own page this week", "Save this.", "Share with a designer friend", S)

# ---------------- SAGE VS AGENCY ----------------
T, S, N = "6-sage-vs-agency", "Sage vs. Agency", 6
cover(T, N, "library.jpg", "Before you hire anyone", "What a typical agency does", "And what Sage does instead", S)
for i, (photo, t, u) in enumerate([
    ("stilllife.jpg", "Posts for you", "Runs a strategy built around the projects you want"),
    ("bedroom.jpg", "Reports followers and likes", "Tracks inquiries and booked projects"),
    ("living.jpg", "Works with any industry", "Only works with interior designers"),
    ("dining.jpg", "Hands you a template", "Starts from a discovery call about your studio"),
], start=2):
    inner = f'''<div class="sheet{' tilt' if i % 2 == 1 else ''}"><div class="mast"><b>SAGE</b><span>{S}</span></div>
<div class="cmp"><div><span class="l">A typical agency</span><p class="t">{t}</p></div><div><span class="l" style="color:var(--ink)">Sage</span><p class="s">{u}</p></div></div></div>'''
    frame(T, i, N, photo, inner, "blur", S)
close(T, N, N, "Sage-interior-design-marketing-agency.jpg", "Booked projects, not likes", "See what a strategy built for your studio looks like.", "Book a discovery call", S)

# ---------------- SOLUTION SELLING ----------------
T, S, N = "7-solution-selling", "For Designers", 5
cover(T, N, "house.jpg", "If this sounds familiar", "Your referrals are slowing down", "And nothing is replacing them", S)
sheet(T, 2, N, "living.jpg", "The problem", "You can’t control when the next referral <em>comes in.</em>", "A great year can turn into a quiet quarter, and you only find out once the calendar is empty.", S)
sheet(T, 3, N, "library.jpg", "Why your current approach won’t fix it", "Posting when you have time won’t build a <em>pipeline.</em>", "Clients who don’t know you yet need to see you consistently, long before they’re ready to call.", S, tilt=True)
sheet(T, 4, N, "kitchen.jpg", "How Sage fixes it", "A strategy built around the projects you want <em>more of.</em>", "Your account manager plans and posts every week. You approve everything, and we report on inquiries, not followers.", S)
close(T, N, N, "terrace.jpg", "Ready for a steadier pipeline?", "Let’s talk about your studio.", "Book a discovery call", S)

head = f'''<!doctype html><html><head><meta charset="utf-8"><title>Sage carousel templates</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600&family=Montserrat:wght@400;500;600&display=swap">
<style>{CSS}</style></head><body>'''
open("carousels.html", "w").write(head + "\n".join(slides) + "</body></html>")
print(len(slides), "slides")
