"""Generate Coremagna favicon set + Google Business logo.

Design: dark (#0A0A0A) rounded square, centered teal (#00D4AA) bold "C".
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DARK = (10, 10, 10, 255)        # #0A0A0A
TEAL = (0, 212, 170, 255)       # #00D4AA
FONT_PATH = r"C:\Windows\Fonts\ariblk.ttf"  # Arial Black


def make_icon(size, supersample=8):
    """Render a single square icon at `size` px with an anti-aliased C."""
    S = size * supersample
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded-square dark background
    radius = int(S * 0.22)
    draw.rounded_rectangle([0, 0, S - 1, S - 1], radius=radius, fill=DARK)

    # Centered teal "C"
    font = ImageFont.truetype(FONT_PATH, int(S * 0.72))
    bbox = draw.textbbox((0, 0), "C", font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (S - w) / 2 - bbox[0]
    y = (S - h) / 2 - bbox[1]
    draw.text((x, y), "C", font=font, fill=TEAL)

    return img.resize((size, size), Image.LANCZOS)


def main():
    img_dir = os.path.join(ROOT, "images")
    os.makedirs(img_dir, exist_ok=True)

    # PNG favicons
    make_icon(32).save(os.path.join(ROOT, "favicon-32x32.png"))
    make_icon(16).save(os.path.join(ROOT, "favicon-16x16.png"))
    make_icon(180).save(os.path.join(ROOT, "apple-touch-icon.png"))

    # Multi-size .ico
    ico = make_icon(48)
    ico.save(os.path.join(ROOT, "favicon.ico"),
             sizes=[(16, 16), (32, 32), (48, 48)])

    # Google Business Profile logo 512x512
    make_icon(512).save(os.path.join(img_dir, "google-business-logo.png"))

    print("Generated: favicon-32x32.png, favicon-16x16.png, "
          "apple-touch-icon.png, favicon.ico, images/google-business-logo.png")


if __name__ == "__main__":
    main()
