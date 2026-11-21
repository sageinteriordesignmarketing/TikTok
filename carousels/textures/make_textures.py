"""Paper textures with embossed / pressed names for Instagram reveal posts (1080x1350).

python3 make_textures.py                      -> Sage logo set + blank textures
python3 make_textures.py "Studio Name"        -> client name versions (cream emboss + olive press)
"""
import sys, os, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FONTS = os.environ.get("FONT_DIR", os.path.join(HERE, "fonts"))
BRAND = os.path.join(HERE, "..", "..", "case-studies", "brand")
rng = np.random.default_rng(7)


def blur(a, r):
    """Gaussian blur a float array in [0,1] through PIL (keeps numpy-only deps)."""
    lo, hi = float(a.min()), float(a.max())
    span = hi - lo or 1.0
    im = Image.fromarray(np.uint8((a - lo) / span * 255))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(r)), dtype=np.float32) / 255 * span + lo


def noise(scale, amount):
    n = rng.standard_normal((H, W)).astype(np.float32)
    return (blur(n, scale) if scale else n) * amount


def paper(base, grain=6.0, mottle=7.0, fibers=900, fiber_tone=(-14, 10), specks=140):
    img = np.ones((H, W, 3), np.float32) * np.array(base, np.float32)
    tone = noise(0, grain) + noise(2, grain * 1.2) + noise(40, mottle * 3) + noise(120, mottle * 4)
    img += tone[..., None]
    # fibers: short thin curved strokes, lighter and darker
    layer = Image.new("L", (W, H), 128)
    d = ImageDraw.Draw(layer)
    for _ in range(fibers):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        ang, ln = rng.uniform(0, np.pi), rng.uniform(6, 28)
        pts = []
        for t in np.linspace(0, 1, 6):
            ang += rng.normal(0, 0.25)
            x += np.cos(ang) * ln / 5
            y += np.sin(ang) * ln / 5
            pts.append((x, y))
        d.line(pts, fill=int(128 + rng.uniform(*fiber_tone) * 3), width=1)
    for _ in range(specks):
        x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0.6, 1.8)
        d.ellipse([x - r, y - r, x + r, y + r], fill=int(128 - rng.uniform(25, 60)))
    f = (np.asarray(layer.filter(ImageFilter.GaussianBlur(0.5)), np.float32) - 128) / 3
    img += f[..., None]
    return img


def text_mask(lines, font_file, size, wght, tracking=0.0, leading=1.0, max_w=880):
    """Render centred lines into a W x H mask; shrinks to fit max_w."""
    while True:
        font = ImageFont.truetype(font_file, size)
        try:
            font.set_variation_by_axes([wght])
        except Exception:
            pass
        widths = []
        for ln in lines:
            w = sum(font.getlength(c) for c in ln) + tracking * size * (len(ln) - 1)
            widths.append(w)
        if max(widths) <= max_w or size < 20:
            break
        size = int(size * 0.94)
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    asc, desc = font.getmetrics()
    lh = size * leading
    y = (H - lh * len(lines)) / 2 + (lh - asc - desc) / 2
    for ln, w in zip(lines, widths):
        x = (W - w) / 2
        for c in ln:
            d.text((x, y), c, font=font, fill=255)
            x += font.getlength(c) + tracking * size
        y += lh
    return np.asarray(m, np.float32) / 255


def logo_mask(path, width, invert_alpha=False):
    im = Image.open(path).convert("RGBA")
    a = im.split()[3]
    s = width / im.width
    if im.height * s > H * 0.7:
        s = H * 0.7 / im.height
    a = a.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    m = Image.new("L", (W, H), 0)
    m.paste(a, ((W - a.width) // 2, (H - a.height) // 2))
    return np.asarray(m, np.float32) / 255


def relief(mask, depth=1.0, soft=3.0, light=(-1, -1)):
    """Directional shading of a raised mask. Positive = lit edge, negative = shadow."""
    h = blur(mask, soft)
    dx, dy = light
    s = 2
    shifted_a = np.roll(np.roll(h, -dy * s, 0), -dx * s, 1)
    shifted_b = np.roll(np.roll(h, dy * s, 0), dx * s, 1)
    return (shifted_b - shifted_a) * depth


def emboss(base_img, mask, strength=60, flat_lift=3):
    """Blind emboss: no ink, just light and shadow on the paper."""
    sh = relief(mask, soft=2.6)
    img = base_img + (sh * strength)[..., None] + (blur(mask, 1.2) * flat_lift)[..., None]
    # soft outer shadow under the raised shape
    halo = blur(mask, 10) - blur(mask, 2)
    img -= (np.clip(np.roll(np.roll(halo, 4, 0), 3, 1), 0, 1) * 10)[..., None]
    return img


def press(base_img, mask, ink, ink_opacity=0.92, strength=42):
    """Ink pressed into cardstock: inked shape sits slightly below the surface."""
    m = blur(mask, 0.7)
    tex = (noise(0, 1.0) + noise(1.2, 1.0)) * 0.06  # ink sits unevenly in the fibres
    a = np.clip(m * (ink_opacity + tex), 0, 1)[..., None]
    img = base_img * (1 - a) + np.array(ink, np.float32) * a
    sh = relief(mask, soft=1.8)
    img -= (sh * strength)[..., None]  # inverted light = debossed
    return img


def save(img, name):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    Image.fromarray(np.uint8(np.clip(img, 0, 255))).save(p, quality=93, subsampling=0)
    print(p)


CREAM = (233, 227, 216)
OLIVE = (112, 104, 60)
ESPRESSO = (52, 44, 38)
INK_CREAM = (238, 232, 218)


def cream():
    return paper(CREAM, grain=5, mottle=5, fibers=1100, fiber_tone=(-12, 8), specks=160)


def olive():
    return paper(OLIVE, grain=9, mottle=4, fibers=2600, fiber_tone=(-10, 10), specks=60)


def espresso():
    return paper(ESPRESSO, grain=6, mottle=4, fibers=1500, fiber_tone=(-8, 8), specks=30)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main():
    serif = os.path.join(FONTS, "CormorantGaramond[wght].ttf")
    sans = os.path.join(FONTS, "Montserrat[wght].ttf")
    if len(sys.argv) > 1:
        name = " ".join(sys.argv[1:])
        words = name.upper().split()
        lines = words if len(words) <= 3 else [" ".join(words[:len(words) // 2]), " ".join(words[len(words) // 2:])]
        save(emboss(cream(), text_mask(lines, serif, 190, 500, tracking=0.04, leading=0.9)), f"{slug(name)}-emboss-cream.jpg")
        save(press(olive(), text_mask([name.upper()], sans, 58, 500, tracking=0.12), INK_CREAM), f"{slug(name)}-press-olive.jpg")
        save(emboss(espresso(), text_mask(lines, serif, 190, 500, tracking=0.04, leading=0.9), strength=45), f"{slug(name)}-emboss-espresso.jpg")
        return
    save(cream(), "texture-cream-paper.jpg")
    save(olive(), "texture-olive-cardstock.jpg")
    save(espresso(), "texture-espresso-paper.jpg")
    logo = os.path.join(BRAND, "logo-ink.png")
    sub = os.path.join(BRAND, "submark-espresso.png")
    save(emboss(cream(), logo_mask(logo, 760)), "sage-logo-emboss-cream.jpg")
    save(press(olive(), logo_mask(logo, 560), INK_CREAM), "sage-logo-press-olive.jpg")
    save(emboss(espresso(), logo_mask(logo, 760), strength=45), "sage-logo-emboss-espresso.jpg")
    save(emboss(cream(), logo_mask(sub, 300)), "sage-submark-emboss-cream.jpg")


if __name__ == "__main__":
    main()
