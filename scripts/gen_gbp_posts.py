"""Generate 3 Google Business Profile post images for Coremagna.

Brand: bg #0A0A0A, teal #00D4AA, white #FFFFFF, grey #888888, dim #666666.
1200x900, centered poster layouts. Rendered at 3x then downscaled (LANCZOS).
DejaVu Sans not installed on this host -> Arial Bold/Regular.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "images")

BG = (10, 10, 10)
TEAL = (0, 212, 170)
WHITE = (255, 255, 255)
GREY = (136, 136, 136)
DIM = (102, 102, 102)
BLACK = (10, 10, 10)

BOLD = r"C:\Windows\Fonts\arialbd.ttf"
REG = r"C:\Windows\Fonts\arial.ttf"

W, H = 1200, 900
S = 3  # supersample


def f(path, size):
    return ImageFont.truetype(path, size * S)


def w_of(d, s, font):
    b = d.textbbox((0, 0), s, font=font)
    return b[2] - b[0]


def center(d, y, s, font, fill):
    """Horizontally centered text at design-y. Returns design height used."""
    fw = w_of(d, s, font)
    d.text(((W * S - fw) / 2, y * S), s, font=font, fill=fill)
    b = d.textbbox((0, 0), s, font=font)
    return (b[3] - b[1]) / S


def logo(d, fsize=20):
    """Top-right COREMAGNA + teal dot."""
    fb = f(BOLD, fsize)
    fs = fsize * S
    redge = (W - 60) * S
    y = 50 * S
    dot_r = max(3, fs // 7)
    gap = dot_r * 3
    core = w_of(d, "CORE", fb)
    magna = w_of(d, "MAGNA", fb)
    total = core + magna + gap + dot_r * 2
    x = redge - total
    d.text((x, y), "CORE", font=fb, fill=WHITE)
    d.text((x + core, y), "MAGNA", font=fb, fill=TEAL)
    cy = y + fs // 2
    dx = x + core + magna + gap
    d.ellipse([dx, cy - dot_r, dx + dot_r * 2, cy + dot_r], fill=TEAL)


def url(d):
    center(d, H - 56, "coremagna.com", f(REG, 16), DIM)


def cta_box(d, cy, label, font, pad_x=44, pad_y=20):
    """Centered teal rounded box with text. cy = design center-y of box."""
    tw = w_of(d, label, font)
    tb = d.textbbox((0, 0), label, font=font)
    th = tb[3] - tb[1]
    bw = tw + pad_x * 2 * S
    bh = th + pad_y * 2 * S
    x0 = (W * S - bw) / 2
    y0 = cy * S - bh / 2
    rad = 14 * S
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=rad, fill=TEAL)
    d.text((x0 + pad_x * S, y0 + pad_y * S - tb[1], ), label, font=font, fill=WHITE)


def canvas():
    img = Image.new("RGB", (W * S, H * S), BG)
    return img, ImageDraw.Draw(img)


def save(img, name):
    img = img.resize((W, H), Image.LANCZOS)
    out = os.path.join(IMG, name)
    img.save(out, compress_level=1)
    kb = os.path.getsize(out) / 1024
    print(f"{os.path.relpath(out, ROOT)}  {img.size[0]}x{img.size[1]}  {kb:.1f} KB")


# tracked (letter-spaced) centered eyebrow
def eyebrow(d, y, text, fsize=22, spacing=5):
    font = f(BOLD, fsize)
    sp = spacing * S
    widths = [w_of(d, ch, font) for ch in text]
    total = sum(widths) + sp * (len(text) - 1)
    x = (W * S - total) / 2
    for ch, wch in zip(text, widths):
        d.text((x, y * S), ch, font=font, fill=TEAL)
        x += wch + sp


# ---------------------------------------------------------------- POST 1
def post1():
    img, d = canvas()
    logo(d)
    eyebrow(d, 150, "— 24/7 LEAD CAPTURE", 22, 5)
    center(d, 270, "Never Miss", f(BOLD, 72), WHITE)
    center(d, 370, "A Lead Again.", f(BOLD, 72), TEAL)
    center(d, 510, "AI chatbots that respond in 30 seconds — day or night",
           f(REG, 22), GREY)

    # 3 inline items with teal bullets
    items = ["Law Firms", "Dental Clinics", "Estate Agents"]
    font = f(BOLD, 24)
    br = 6 * S
    gap_bullet = 16 * S
    gap_item = 48 * S
    seg = []
    for it in items:
        seg.append(br * 2 + gap_bullet + w_of(d, it, font))
    total = sum(seg) + gap_item * (len(items) - 1)
    x = (W * S - total) / 2
    y = 640 * S
    for it, segw in zip(items, seg):
        d.ellipse([x, y + 9 * S, x + br * 2, y + 9 * S + br * 2], fill=TEAL)
        d.text((x + br * 2 + gap_bullet, y), it, font=font, fill=WHITE)
        x += segw + gap_item

    url(d)
    save(img, "gbp-post-1.png")


# ---------------------------------------------------------------- POST 2
def post2():
    img, d = canvas()
    logo(d)
    center(d, 180, "25%", f(BOLD, 120), TEAL)
    center(d, 360, "of estate agent leads get a response", f(REG, 28), WHITE)
    center(d, 425, "The other 75% go to a competitor.", f(REG, 22), GREY)
    cta_box(d, 600, "We fix that. In 7 days.", f(BOLD, 24))
    url(d)
    save(img, "gbp-post-2.png")


# ---------------------------------------------------------------- POST 3
def post3():
    img, d = canvas()
    logo(d)
    eyebrow(d, 170, "— FREE AUDIT", 22, 5)
    center(d, 280, "Where Are Your", f(BOLD, 64), WHITE)
    center(d, 370, "Leads Going?", f(BOLD, 64), TEAL)
    center(d, 500, "Free 30-minute review of your website,", f(REG, 20), GREY)
    center(d, 540, "intake process and response times.", f(REG, 20), GREY)
    cta_box(d, 670, "Book Your Free Audit →", f(BOLD, 22))
    url(d)
    save(img, "gbp-post-3.png")


if __name__ == "__main__":
    os.makedirs(IMG, exist_ok=True)
    post1()
    post2()
    post3()
