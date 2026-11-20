"""Sage carousel templates v4: type-led brand studio aesthetic. 1080x1350."""
import urllib.parse

def svg_uri(svg):
    return "url(\"data:image/svg+xml," + urllib.parse.quote(svg) + "\")"

GRAIN = svg_uri("<svg xmlns='http://www.w3.org/2000/svg' width='260' height='260'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .4 0 0 0 0 .37 0 0 0 0 .33 0 0 0 .32 0'/></filter><rect width='100%' height='100%' filter='url(#n)'/></svg>")
FIBER = svg_uri("<svg xmlns='http://www.w3.org/2000/svg' width='600' height='600'><filter id='f'><feTurbulence type='fractalNoise' baseFrequency='.02 .3' numOctaves='3' seed='5'/><feColorMatrix values='0 0 0 0 .45 0 0 0 0 .42 0 0 0 0 .38 0 0 0 .12 0'/></filter><rect width='100%' height='100%' filter='url(#f)'/></svg>")

CSS = """
:root { --paper:#EAE6DF; --cream:#F6F2EA; --ink:#1E1B18; --mute:#8C857C; --black:#0E0D0C;
  --serif:"Cormorant Garamond", Georgia, serif; --script:"Italianno", "Pinyon Script", cursive; --sans:"Montserrat", Arial, sans-serif; }
* { box-sizing:border-box; margin:0; padding:0; }
body { background:#999; }
.slide { width:1080px; height:1350px; position:relative; overflow:hidden; margin:20px; color:var(--ink); font-family:var(--sans); }
.paper { background-color:var(--paper); background-image:GRAIN, FIBER; }
.black { background:var(--black); color:var(--cream); }
.img { position:absolute; overflow:hidden; } .img img { width:100%; height:100%; object-fit:cover; display:block; }
.folio { position:absolute; left:80px; right:80px; display:flex; justify-content:space-between; font:500 15px var(--sans); letter-spacing:.42em; text-transform:uppercase; z-index:9; }
.folio.t { top:64px; } .folio.b { bottom:60px; justify-content:center; letter-spacing:.3em; }
.poster { position:absolute; left:80px; right:80px; top:0; bottom:0; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; z-index:5; }
.ln { display:flex; align-items:baseline; justify-content:center; gap:16px; flex-wrap:wrap; line-height:1; }
.sc { font:500 19px var(--sans); letter-spacing:.32em; text-transform:uppercase; }
.rc { font-family:var(--serif); font-weight:300; text-transform:uppercase; letter-spacing:.02em; font-size:92px; line-height:1; font-variant-numeric:lining-nums; }
.rl { font-family:var(--serif); font-weight:400; font-size:80px; line-height:1.05; letter-spacing:-.01em; font-variant-numeric:lining-nums; }
.scr { font-family:var(--script); font-size:120px; line-height:.8; font-weight:400; }
.giant { position:absolute; font-family:var(--serif); font-weight:300; text-transform:uppercase; line-height:.8; letter-spacing:-.02em; white-space:nowrap; z-index:2; font-variant-numeric:lining-nums; }
.body { font:400 27px/1.65 var(--sans); max-width:30ch; }
.mute { color:var(--mute); }
.card { position:absolute; background-color:var(--cream); background-image:GRAIN; color:var(--ink); box-shadow:0 30px 60px -30px rgba(0,0,0,.8); display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; z-index:5; }
.rule { width:90px; height:1px; background:currentColor; opacity:.45; }
.phone { position:absolute; width:440px; height:900px; border-radius:66px; background:#111; padding:16px; box-shadow:0 40px 70px -30px rgba(0,0,0,.7); z-index:5; }
.phone .scr2 { width:100%; height:100%; border-radius:52px; background:var(--cream); overflow:hidden; display:flex; flex-direction:column; }
.phone .notch { width:120px; height:30px; border-radius:20px; background:#111; margin:14px auto 0; }
.phone .hdr { padding:26px 28px 14px; display:flex; flex-direction:column; gap:6px; }
.phone .hdr b { font:600 17px var(--sans); letter-spacing:.06em; }
.phone .hdr span { font:400 13px var(--sans); color:var(--mute); }
.phone .grid { display:grid; grid-template-columns:repeat(3,1fr); gap:3px; padding:0 0 0; }
.phone .grid img { width:100%; aspect-ratio:4/5; object-fit:cover; display:block; }
.strike { text-decoration:line-through; text-decoration-thickness:1.5px; }
.fill { color:var(--mute); }
"""
CSS = CSS.replace("GRAIN", GRAIN).replace("FIBER", FIBER)

slides = []
def add(tid, n, total, series, inner, bg="paper", tone="ink"):
    col = "var(--cream)" if tone == "light" else "var(--ink)"
    slides.append(f'''<section class="slide {bg}" id="{tid}-{n:02d}">{inner}
<div class="folio t" style="color:{col}"><span>Sage</span><span>{series}</span></div>
<div class="folio b" style="color:{col}"><span>{n:02d} / {total:02d}</span></div></section>''')

def poster(lines, extra=""):
    return f'<div class="poster" style="gap:26px">{"".join(f"<div class=ln>{l}</div>" for l in lines)}{extra}</div>'

def sc(t, c=""): return f'<span class="sc {c}">{t}</span>'
def rc(t, s=92, c=""): return f'<span class="rc {c}" style="font-size:{s}px">{t}</span>'
def rl(t, s=80, c=""): return f'<span class="rl {c}" style="font-size:{s}px">{t}</span>'
def scr(t, s=120, c=""): return f'<span class="scr {c}" style="font-size:{s}px">{t}</span>'

def phone(left, top, photos, name="yourstudio"):
    imgs = "".join(f'<img src="{p}" alt="">' for p in photos)
    return f'''<div class="phone" style="left:{left}px;top:{top}px"><div class="scr2"><div class="notch"></div>
<div class="hdr"><b>{name}</b><span>Interior design studio</span></div><div class="grid">{imgs}</div></div></div>'''

GRID = ["living.jpg", "dining.jpg", "bedroom.jpg", "kitchen.jpg", "library.jpg", "bath.jpg", "stair.jpg", "powder.jpg", "stilllife.jpg", "terrace.jpg", "house.jpg", "dining.jpg", "bedroom.jpg", "living.jpg", "kitchen.jpg"]

# ============ 0 MYTH VS TRUTH: giant cropped word + type posters ============
T, S, N = "0-myth-vs-truth", "Myth vs. Truth", 5
add(T, 1, N, S, f'''<div class="giant" style="left:-40px;top:150px;font-size:430px;opacity:.9">Myth</div>
<div class="poster" style="top:560px;gap:22px">
<div class="ln">{sc("the myth")}</div>
<div class="ln">{rl("“High-end clients", 84)}</div>
<div class="ln">{rl("don’t come from", 84)}{scr("Instagram.”", 140)}</div></div>''')
add(T, 2, N, S, poster([
    sc("it’s") + scr("half true", 150),
    rc("Most luxury clients", 84),
    sc("won’t find you by") + scr("scrolling.", 130),
], f'<div class="rule" style="margin-top:30px"></div><p class="body mute" style="margin-top:18px">Your best clients still arrive through people they trust.</p>'))
add(T, 3, N, S, poster([
    sc("what’s") + scr("actually", 140) + sc("true"),
    rc("Almost every referral", 80),
    rl("checks your Instagram", 76),
    scr("before they call.", 150),
], f'<p class="body mute" style="margin-top:34px">Your page is where a warm introduction becomes a booked consultation, or goes cold.</p>'), "paper")
add(T, 4, N, S, f'''<div class="img" style="left:0;right:0;top:0;height:760px"><img src="stilllife.jpg" alt=""></div>
<div class="poster" style="top:760px;gap:22px">
<div class="ln">{sc("what to do instead")}</div>
<div class="ln">{rl("Post the projects you want", 64)}</div><div class="ln">{scr("more of.", 140)}</div></div>''', "paper", "light")
add(T, 5, N, S, f'''<div class="card" style="left:150px;right:150px;top:300px;bottom:300px;gap:26px;padding:60px">
{sc("before your next referral looks you up")}<div class="rule"></div>
<div class="rl" style="font-size:72px">Look at your grid</div><div class="scr" style="font-size:110px">like a stranger would.</div>
<div class="rule"></div>{sc("save this")}</div>''', "black", "light")

# ============ 1 CASE STUDY: cream card on black, photo pages ============
T, S, N = "1-case-study", "Case Study", 5
add(T, 1, N, S, f'''<div class="card" style="left:230px;right:230px;top:260px;bottom:260px;gap:30px">
{sc("client case study")}<div class="rc fill" style="font-size:74px">[Studio Name]</div>
<div class="scr" style="font-size:110px">the story</div><div class="rule"></div>{sc("sage interior design marketing")}</div>''', "black", "light")
for n, (photo, k, h, b) in enumerate([
    ("bedroom.jpg", "where she started", "[One line on her situation]", "[Two sentences in her words from the discovery call.]"),
    ("kitchen.jpg", "what we did", "[The one change that mattered most]", "[Two sentences on the strategy, not a list of deliverables.]"),
], start=2):
    add(T, n, N, S, f'''<div class="img" style="left:80px;top:150px;width:440px;height:600px"><img src="{photo}" alt=""></div>
<div style="position:absolute;left:580px;right:80px;top:170px;display:flex;flex-direction:column;gap:24px;z-index:5">
{sc(k, "mute")}<div class="rl fill" style="font-size:64px">{h}</div></div>
<div style="position:absolute;left:80px;right:80px;top:830px;border-top:1px solid var(--ink);padding-top:30px;z-index:5"><p class="body fill" style="max-width:40ch;font-size:32px">{b}</p></div>''')
add(T, 4, N, S, poster([sc("the result"), f'<span class="rc fill" style="font-size:300px;font-weight:300">[00]</span>', scr("[what it means]", 120, "fill"), sc("[time frame]", "mute")]))
add(T, 5, N, S, f'''<div class="img" style="left:0;right:0;top:0;height:800px"><img src="terrace.jpg" alt=""></div>
<div class="poster" style="top:800px;gap:20px"><div class="ln">{sc("want this for")}{scr("your studio?", 130)}</div>
<div class="ln">{sc("book a discovery call · link in bio", "mute")}</div></div>''')

# ============ 2 BIG STAT: thin numerals, script word ============
T, S, N = "2-big-stat", "Three Months", 6
add(T, 1, N, S, f'''<div class="img" style="left:0;right:0;top:0;height:800px"><img src="bedroom.jpg" alt=""></div>
<div class="poster" style="top:800px;gap:18px"><div class="ln">{sc("one atlanta designer")}</div>
<div class="ln">{rc("Three months", 96)}</div><div class="ln">{scr("of Instagram", 130)}</div></div>''')
for n, (num, word, line) in enumerate([
    ("+534%", "reach", "in her first three months"),
    ("+539%", "engagement", "from people who stopped to look"),
    ("+610", "followers", "new, in her market"),
    ("3", "new leads", "after years of relying on referrals alone"),
], start=2):
    bg, tone = ("black", "light") if n % 2 else ("paper", "ink")
    add(T, n, N, S, poster([sc("three months with sage", "mute"),
        f'<span class="rc" style="font-size:{340 if len(num)>3 else 520}px;font-weight:300;letter-spacing:-.03em">{num}</span>',
        scr(word, 160), sc(line)]), bg, tone)
add(T, 6, N, S, poster([sc("your work is already"), scr("good enough", 150), rc("Your Instagram", 84), rl("should prove it.", 80)],
    f'<div class="rule" style="margin-top:30px"></div><p class="sc mute" style="margin-top:20px">book a discovery call · link in bio</p>'))

# ============ 3 MISTAKES: phone mockup ============
T, S, N = "3-mistakes", "Mistakes", 6
add(T, 1, N, S, f'''<div class="giant" style="right:-30px;top:120px;font-size:900px;color:#DAD4CB">4</div>
{phone(110, 230, GRID)}
<div style="position:absolute;left:600px;right:80px;top:470px;display:flex;flex-direction:column;gap:22px;z-index:5">
{sc("four mistakes")}<div class="rl" style="font-size:66px">keeping your page from</div><div class="scr" style="font-size:120px">booking projects</div></div>''')
for n, (h1, h2, b) in enumerate([
    ("Posting only when you feel", "inspired.", "Future clients reward consistency. Inspiration shows up on its own schedule."),
    ("Showing only", "finished rooms.", "Clients hire a process, not a photo. Show how you get there."),
    ("Captions that", "describe the room.", "They can see the room. Tell them what changed for the homeowner."),
    ("A bio with", "a menu of six links.", "Every extra choice is a chance to leave. Give them one next step."),
], start=2):
    bg, tone = ("black", "light") if n % 2 else ("paper", "ink")
    add(T, n, N, S, f'''{phone(600, 220, GRID[n-2:] + GRID[:n-2])}
<div style="position:absolute;left:80px;width:490px;top:330px;display:flex;flex-direction:column;gap:24px;z-index:5">
<div class="rc" style="font-size:180px;font-weight:300;line-height:.8">0{n-1}</div>{sc("you’re")}
<div class="rl" style="font-size:62px">{h1}</div><div class="scr" style="font-size:118px">{h2}</div>
<p class="body" style="font-size:25px;opacity:.75">{b}</p></div>''', bg, tone)
add(T, 6, N, S, poster([sc("what to do"), scr("instead", 150), rc("Plan ahead", 88), rl("and keep one next step.", 68)],
    f'<div class="rule" style="margin-top:30px"></div><p class="sc mute" style="margin-top:20px">save for your next content day</p>'))

# ============ 4 BRAND BREAKDOWN: giant cropped wordmark ============
T, S, N = "4-brand-breakdown", "Brand Insights", 5
add(T, 1, N, S, f'''<div class="giant fill" style="left:-30px;top:200px;font-size:250px">[Designer]</div>
<div class="img" style="left:80px;right:80px;top:520px;height:560px"><img src="stair.jpg" alt=""></div>
<div class="poster" style="top:1080px;bottom:110px;gap:10px"><div class="ln">{sc("brand insights")}{scr("why it works", 110)}</div></div>''')
for n, (photo, k, h, b) in enumerate([
    ("living.jpg", "who they are", "[Studio, city, the work they’re known for]", "[One sentence on why your audience already knows the name.]"),
    ("dining.jpg", "what they do on instagram", "[The pattern in their last twelve posts]", "[Formats, who is on camera, how often, what the captions do.]"),
    ("library.jpg", "why it works", "[The strategy underneath it]", "[Tie it to a business result: who it attracts and what it signals.]"),
], start=2):
    add(T, n, N, S, f'''<div style="position:absolute;left:80px;width:540px;top:0;bottom:0;justify-content:center;display:flex;flex-direction:column;gap:30px;z-index:5">
<div class="sc mute">{k}</div><div class="rl fill" style="font-size:76px">{h}</div><p class="body fill">{b}</p></div>
<div class="img" style="right:0;top:0;bottom:0;width:390px"><img src="{photo}" alt=""></div>''')
add(T, 5, N, S, poster([sc("what it means for"), scr("your studio", 150), f'<span class="rl fill" style="font-size:68px">[The one move you can copy this month]</span>']))

# ============ 5 CHECKLIST: thin numerals and hairlines ============
T, S, N = "5-checklist", "The Audit", 7
add(T, 1, N, S, poster([sc("the"), rc("Five things", 110), sc("i check first on a designer’s"), scr("Instagram", 170)]))
for n, (h1, h2, b) in enumerate([
    ("Your bio says who you serve", "and where.", "If a stranger can’t tell in three seconds, they won’t keep scrolling."),
    ("Your last nine posts match", "the work you want.", "Your grid is a sales pitch for the projects you want more of."),
    ("A real person shows up", "on camera.", "Clients hire you, not a mood board. Let them hear you first."),
    ("Your captions give a reason", "to reach out.", "Leave them knowing what working with you feels like."),
    ("One link,", "one next step.", "Send people straight to booking. Don’t make them choose."),
], start=2):
    add(T, n, N, S, f'''<div class="rc" style="position:absolute;left:70px;top:150px;font-size:420px;font-weight:300;line-height:.8;color:#B9AFA2">{n-1}</div>
<div style="position:absolute;left:80px;right:80px;top:640px;border-top:1px solid var(--ink);padding-top:44px;display:flex;flex-direction:column;gap:18px;z-index:5">
{sc(f"no. {n-1} of 5", "mute")}<div class="rl" style="font-size:72px">{h1}</div><div class="scr" style="font-size:130px">{h2}</div>
<p class="body" style="margin-top:14px;max-width:36ch">{b}</p></div>''')
add(T, 7, N, S, f'''<div class="card" style="left:230px;right:230px;top:300px;bottom:300px;gap:24px">
{sc("run it on your own page")}<div class="scr" style="font-size:170px">save this</div><div class="rule"></div>{sc("and send it to a designer friend", "mute")}</div>''', "black", "light")

# ============ 6 SAGE VS AGENCY: two columns, struck-through ============
T, S, N = "6-sage-vs-agency", "Sage vs. Agency", 6
add(T, 1, N, S, poster([sc("what a"), rc("Typical agency", 100), sc("does, and what"), scr("Sage does instead", 140)]))
for n, (t, u) in enumerate([
    ("Posts for you", "Runs a strategy built around the projects you want"),
    ("Reports followers and likes", "Tracks inquiries and booked projects"),
    ("Works with any industry", "Only works with interior designers"),
    ("Hands you a template", "Starts from a discovery call about your studio"),
], start=2):
    bg, tone = ("black", "light") if n % 2 else ("paper", "ink")
    add(T, n, N, S, f'''<div style="position:absolute;left:80px;right:80px;top:300px;bottom:260px;display:grid;grid-template-columns:1fr 1fr;align-items:center;z-index:5">
<div style="padding-right:40px;display:flex;flex-direction:column;gap:28px">{sc("a typical agency")}<div class="rl strike" style="font-size:78px;opacity:.45">{t}</div></div>
<div style="padding-left:40px;border-left:1px solid currentColor;display:flex;flex-direction:column;gap:28px">{scr("Sage", 140)}<div class="rl" style="font-size:78px">{u}</div></div></div>''', bg, tone)
add(T, 6, N, S, f'''<div class="img" style="left:0;right:0;top:0;height:780px"><img src="Sage-interior-design-marketing-agency.jpg" alt=""></div>
<div class="poster" style="top:780px;gap:18px"><div class="ln">{sc("booked projects,")}{scr("not likes", 130)}</div>
<div class="ln">{sc("book a discovery call · link in bio", "mute")}</div></div>''')

# ============ 7 SOLUTION SELLING: letter-style posters ============
T, S, N = "7-solution-selling", "For Designers", 5
add(T, 1, N, S, f'''<div class="img" style="left:0;right:0;top:0;height:780px"><img src="house.jpg" alt=""></div>
<div class="poster" style="top:780px;gap:16px"><div class="ln">{sc("if your")}{scr("referrals", 130)}</div>
<div class="ln">{rc("are slowing down", 72)}</div></div>''')
for n, (k, a, b2, body) in enumerate([
    ("the problem", "You can’t control when", "the next referral comes in.", "A great year can turn into a quiet quarter, and you only find out once the calendar is empty."),
    ("why your current approach won’t fix it", "Posting when you have time", "won’t build a pipeline.", "Clients who don’t know you yet need to see you consistently, long before they’re ready to call."),
    ("how sage fixes it", "A strategy built around", "the projects you want more of.", "Your account manager plans and posts every week. You approve everything, and we report on inquiries, not followers."),
], start=2):
    bg, tone = ("black", "light") if n == 3 else ("paper", "ink")
    add(T, n, N, S, f'''<div style="position:absolute;left:110px;right:110px;top:250px;bottom:200px;display:flex;flex-direction:column;gap:26px;z-index:5">
{sc(k, "mute")}<div class="rl" style="font-size:78px;margin-top:20px">{a}</div><div class="scr" style="font-size:112px">{b2}</div>
<p class="body" style="max-width:34ch;margin-top:10px">{body}</p><div class="scr" style="font-size:70px;margin-top:auto;opacity:.7">Kyra</div></div>''', bg, tone)
add(T, 5, N, S, poster([sc("ready for a"), scr("steadier pipeline?", 140), rc("Let’s talk", 96), rl("about your studio.", 72)],
    f'<div class="rule" style="margin-top:30px"></div><p class="sc mute" style="margin-top:20px">book a discovery call · link in bio</p>'))

head = f'''<!doctype html><html><head><meta charset="utf-8"><title>Sage carousel templates</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,400&family=Italianno&family=Montserrat:wght@400;500;600&display=swap">
<style>{CSS}</style></head><body>'''
open("carousels.html", "w").write(head + "\n".join(slides) + "</body></html>")
print(len(slides), "slides")
