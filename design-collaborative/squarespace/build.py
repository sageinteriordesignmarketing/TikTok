#!/usr/bin/env python3
"""Turn homepage-concept.html into Squarespace-ready paste files.

  python3 squarespace/build.py      (run from design-collaborative/)

Writes:
  squarespace/1-code-block.html            paste into ONE Code Block on the draft page
  squarespace/2-homepage-header-injection.html   paste at launch into the real homepage's Page Header Code Injection

What it does to the concept:
  * wraps the page in <div id="dc-home"> and prefixes every CSS selector with #dc-home,
    so Squarespace's site styles can't leak in and this CSS can't leak out
  * adds a reset for elements Squarespace styles directly (p, h1-h3, a, li...)
  * hides the native header/footer on this page only and makes its section full-bleed
  * swaps local image paths for the photos already in the site's Squarespace library,
    with responsive srcset sizes (Squarespace CDN ?format=...w)
  * drops the preview-only script
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = (ROOT / "homepage-concept.html").read_text()
CDN = dict(l.split("\t") for l in (ROOT / "squarespace/image-map.tsv").read_text().strip().splitlines())
SCOPE = "#dc-home"

# ---------------------------------------------------------------- CSS scoping
css = re.search(r"<style>(.*?)</style>", SRC, re.S).group(1)
css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
css = css.replace("/* PREVIEW-ONLY */", "")
css = re.sub(r"\.pv-toast[^{]*\{[^}]*\}", "", css)


def scope_selector(sel: str) -> str:
    sel = sel.strip()
    if not sel:
        return sel
    if sel == ":root" or sel == "body":
        return SCOPE
    if sel == "html":
        return None
    if sel.startswith(".dc-js"):
        rest = sel[len(".dc-js"):].strip()
        return f".dc-js {SCOPE} {rest}" if rest else ".dc-js"
    if sel.startswith("*") or sel[0].isalpha() or sel.startswith(":") or sel.startswith("[") or sel.startswith("."):
        if sel.startswith(".dc-hero") and False:
            pass
        return f"{SCOPE} {sel}"
    return f"{SCOPE} {sel}"


def scope_block(text: str) -> str:
    out, i = [], 0
    while i < len(text):
        j = text.find("{", i)
        if j == -1:
            break
        head = text[i:j].strip()
        # find matching brace
        depth, k = 0, j
        while k < len(text):
            if text[k] == "{": depth += 1
            elif text[k] == "}":
                depth -= 1
                if depth == 0: break
            k += 1
        body = text[j + 1:k]
        if head.startswith("@keyframes"):
            out.append(f"{head}{{{body}}}")
        elif head.startswith("@media"):
            out.append(f"{head}{{{scope_block(body)}}}")
        else:
            sels = [scope_selector(s) for s in head.split(",")]
            sels = [s for s in sels if s]
            if sels:
                out.append(",".join(sels) + "{" + body.strip() + "}")
        i = k + 1
    return "\n".join(out)


scoped = scope_block(css)
# Squarespace's own heading/paragraph rules can override spacing; make the design's margins win (still page-scoped)
scoped = re.sub(r"(margin(?:-top|-bottom|-left|-right|-inline|-block)?:[^;{}!]+)(?=[;}])", r"\1!important", scoped)

squarespace_css = f"""
/* ---- Squarespace integration (this page only) ---- */
body:has({SCOPE}){{background:#F8F5F2}}
body:has({SCOPE}) #header,body:has({SCOPE}) header#header,body:has({SCOPE}) #footer-sections,body:has({SCOPE}) .sqs-announcement-bar-dropzone{{display:none!important}}
.page-section:has({SCOPE}){{padding:0!important;min-height:0!important}}
.page-section:has({SCOPE}) .content-wrapper,.page-section:has({SCOPE}) .content{{padding:0!important;max-width:none!important;width:100%!important}}
.page-section:has({SCOPE}) .section-background{{display:none!important}}
.fluid-engine:has({SCOPE}){{display:block!important}}
.fe-block:has({SCOPE}),.sqs-block:has({SCOPE}),.sqs-block-content:has({SCOPE}){{padding:0!important;margin:0!important;transform:none!important}}
{SCOPE}{{position:relative;width:100%;isolation:isolate}}
/* reset elements Squarespace styles directly; the design's class rules (higher specificity) take over */
{SCOPE} :is(p,h1,h2,h3,h4,li,a,span,address,figcaption,button,ul,ol,figure){{font:inherit;letter-spacing:inherit;text-transform:inherit;color:inherit;margin:0;padding:0;line-height:inherit;text-decoration:none;border:0;background:none;max-width:none}}
{SCOPE} button{{cursor:pointer}}
{SCOPE} img{{max-width:100%;height:auto}}
"""

# ---------------------------------------------------------------- markup
body = re.search(r"<body>(.*?)<script>", SRC, re.S).group(1)
body = re.sub(r'<div class="pv-toast".*?</div>\s*', "", body, flags=re.S)


def img_sub(m):
    tag = m.group(0)
    src = re.search(r'src="images/([^"]+)"', tag).group(1)
    url = CDN[src.strip()].strip()
    if src.endswith(".png"):
        return tag.replace(f'src="images/{src}"', f'src="{url}?format=750w"')
    sizes = '(max-width: 960px) 100vw, 60vw'
    if 'fetchpriority="high"' in tag or 'dc-slide' in tag:
        sizes = '100vw'
    srcset = f'{url}?format=750w 750w, {url}?format=1500w 1500w, {url}?format=2500w 2500w'
    return tag.replace(f'src="images/{src}"', f'src="{url}?format=1500w" srcset="{srcset}" sizes="{sizes}"')


body = re.sub(r"<img\b[^>]*>", img_sub, body)
# full-bleed sections get 100vw sizes
for cls in ("dc-slide", "dc-place", "dc-close"):
    pass

js = re.findall(r"<script>(.*?)</script>", SRC, re.S)
main_js = [s for s in js if "SITE SCRIPT" in s][0].split("/* PREVIEW-ONLY")[0]
early_js = "document.documentElement.classList.add('dc-js');setTimeout(function(){if(!window.dcReady)document.documentElement.classList.remove('dc-js')},3000);"

fonts = re.search(r'(<link rel="preconnect" href="https://fonts.googleapis.com">.*?rel="stylesheet">)', SRC, re.S).group(1)
fonts = re.sub(r"family=Figtree:wght@[0-9;]+&", "", fonts)  # Proxima Nova is already loaded by the live site

code_block = f"""<!-- ============================================================
  DESIGN COLLABORATIVE · HOMEPAGE v4  (generated by squarespace/build.py — edit the concept, then rebuild)
  Paste this whole file into ONE Code Block. Display Source: off. See INSTALL.md.
============================================================= -->
{fonts}
<script>{early_js}</script>
<style>
{squarespace_css}
{scoped}
</style>
<div id="dc-home">
{body.strip()}
</div>
<script>{main_js.strip()}</script>
"""
(ROOT / "squarespace/1-code-block.html").write_text(code_block)

head = re.search(r'(<!-- Structured data.*?</script>)', SRC, re.S).group(1)
(ROOT / "squarespace/2-homepage-header-injection.html").write_text(
    "<!-- AT LAUNCH ONLY: paste into the real homepage > Settings > Advanced > Page Header Code Injection.\n"
    "     Do not add to the hidden draft page (it would duplicate the business markup). -->\n" + head.split("-->", 1)[1].strip() + "\n")
print("code block:", len(code_block) // 1024, "KB")
