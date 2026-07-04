"""Generate Google Business Profile cover + business photo for Coremagna.

Brand: bg #0A0A0A, teal #00D4AA, white #FFFFFF, grey #888888.
Dark, minimal, professional. Uses Arial Bold/Regular (DejaVu not present).
Rendered at 2x then downscaled (LANCZOS) for crisp anti-aliased text.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "images")

BG = (10, 10, 10)        # #0A0A0A
TEAL = (0, 212, 170)     # #00D4AA
WHITE = (255, 255, 255)
GREY = (136, 136, 136)   # #888888
DIM = (102, 102, 102)    # #666666

BOLD = r"C:\Windows\Fonts\arialbd.ttf"
REG = r"C:\Windows\Fonts\arial.ttf"

S = 3  # supersample factor


def f(path, size):
    return ImageFont.truetype(path, size * S)


def tracked(draw, xy, text, font, fill, spacing):
    """Draw text with extra letter-spacing (spacing in design px)."""
    x, y = xy[0] * S, xy[1] * S
    sp = spacing * S
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        w = draw.textbbox((0, 0), ch, font=font)[2]
        x += w + sp


def text(draw, xy, s, font, fill):
    draw.text((xy[0] * S, xy[1] * S), s, font=font, fill=fill)


def logo(draw, right_x, y, fsize):
    """Right-aligned CORE+MAGNA+dot logo. right_x = right edge (design px)."""
    fb = f(BOLD, fsize)
    rx = right_x * S
    yy = y * S
    fs = fsize * S
    dot_r = max(3, fs // 7)
    gap = dot_r * 3
    core = draw.textbbox((0, 0), "CORE", font=fb)[2]
    magna = draw.textbbox((0, 0), "MAGNA", font=fb)[2]
    total = core + magna + gap + dot_r * 2
    x = rx - total
    draw.text((x, yy), "CORE", font=fb, fill=WHITE)
    draw.text((x + core, yy), "MAGNA", font=fb, fill=TEAL)
    cy = yy + fs // 2
    dx = x + core + magna + gap
    draw.ellipse([dx, cy - dot_r, dx + dot_r * 2, cy + dot_r], fill=TEAL)


def teal_gradient_line(draw, x0, x1, y, h):
    """Horizontal teal->bg gradient line (design px)."""
    x0, x1, y, h = x0 * S, x1 * S, y * S, h * S
    span = x1 - x0
    for i in range(span):
        t = i / span
        r = int(TEAL[0] + (BG[0] - TEAL[0]) * t)
        g = int(TEAL[1] + (BG[1] - TEAL[1]) * t)
        b = int(TEAL[2] + (BG[2] - TEAL[2]) * t)
        draw.rectangle([x0 + i, y, x0 + i + 1, y + h], fill=(r, g, b))


def rect(draw, box, fill):
    draw.rectangle([v * S for v in box], fill=fill)


def ellipse(draw, box, fill):
    draw.ellipse([v * S for v in box], fill=fill)


def canvas(W, H):
    img = Image.new("RGB", (W * S, H * S), BG)
    return img, ImageDraw.Draw(img)


def finish(img, W, H, name):
    img = img.resize((W, H), Image.LANCZOS)
    out = os.path.join(IMG, name)
    img.save(out, compress_level=1)
    return out, img.size


# ---------------------------------------------------------------- COVER
def make_cover():
    W, H = 1080, 608
    img, d = canvas(W, H)

    # left column (~55%)
    lx = 64
    tracked(d, (lx, 96), "— AI AUTOMATION AGENCY", f(BOLD, 18), TEAL, 4)
    text(d, (lx, 150), "Stop Losing", f(BOLD, 64), WHITE)
    text(d, (lx, 230), "Leads.", f(BOLD, 64), TEAL)
    text(d, (lx, 332), "AI systems that capture, qualify and follow", f(REG, 20), GREY)
    text(d, (lx, 362), "up — 24/7", f(REG, 20), GREY)

    # right column (~45%)
    rx = 600
    logo(d, W - 64, 70, 22)
    services = [
        ("AI Chatbots", "24/7 lead capture"),
        ("Lead Scoring", "AI scores 0-100"),
        ("AI Automation", "respond in 30 seconds"),
        ("Voice AI Agent", "calls leads automatically"),
    ]
    sy, step = 200, 78
    nb, nd = f(BOLD, 24), f(REG, 18)
    for name, desc in services:
        br = 6
        ellipse(d, [rx, sy + 8, rx + br * 2, sy + 8 + br * 2], TEAL)
        tx = rx + br * 2 + 18
        text(d, (tx, sy), name, nb, WHITE)
        text(d, (tx, sy + 32), desc, nd, GREY)
        sy += step

    teal_gradient_line(d, 0, W, H - 4, 2)
    return finish(img, W, H, "gbp-cover.png")


# ---------------------------------------------------------------- STAT / SQUARE
def make_stat():
    W, H = 1080, 1080
    img, d = canvas(W, H)
    lx = 80

    tracked(d, (lx, 70), "— WHAT WE BUILD", f(BOLD, 16), TEAL, 4)
    logo(d, W - 80, 64, 18)

    hb = f(BOLD, 72)
    text(d, (lx, 130), "4 Systems.", hb, WHITE)
    text(d, (lx, 218), "Zero Manual", hb, WHITE)
    text(d, (lx, 306), "Work.", hb, TEAL)

    text(d, (lx, 412), "Built for law firms, dental clinics and estate", f(REG, 18), GREY)
    text(d, (lx, 438), "agents in UK & AU", f(REG, 18), GREY)

    boxes = [
        ("01", "AI Chatbot", "Engages visitors & captures leads 24/7"),
        ("02", "Lead Scoring", "AI scores every enquiry 0-100"),
        ("03", "Ad Automation", "Automated response in under 30 seconds"),
        ("04", "Voice AI Agent", "Human voice, instant response, zero staff"),
    ]
    by, bh = 510, 118
    nb, nd, numf = f(BOLD, 30), f(REG, 19), f(BOLD, 20)
    for num, name, desc in boxes:
        rect(d, [lx, by + 8, lx + 3, by + bh - 18], TEAL)
        tx = lx + 28
        text(d, (tx, by + 6), num, numf, TEAL)
        text(d, (tx, by + 34), name, nb, WHITE)
        text(d, (tx, by + 74), desc, nd, GREY)
        by += bh

    text(d, (lx, H - 56), "coremagna.com", f(REG, 14), DIM)
    return finish(img, W, H, "gbp-stat.png")


if __name__ == "__main__":
    os.makedirs(IMG, exist_ok=True)
    for fn in (make_cover, make_stat):
        path, size = fn()
        kb = os.path.getsize(path) / 1024
        print(f"{os.path.relpath(path, ROOT)}  {size[0]}x{size[1]}  {kb:.1f} KB")
