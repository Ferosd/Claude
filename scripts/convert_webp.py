from PIL import Image
import os

jobs = [
    ("PI Firm — $250K Kayıp.jpg",        "images/pi-firm-250k.webp"),
    ("FlowWorks — 28 Saat Tasarruf.jpg", "images/flowworks-28-saat.webp"),
    ("Tate Law — %654 Arama.jpeg",       "images/tate-law-654.webp"),
    ("Clio — No-show düşüşü.jpg",         "images/clio-no-show.webp"),
    ("LawRato — %80 Conversion.jpg",      "images/lawrato-80-conversion.webp"),
]

MAX_W = 1600
for src, dst in jobs:
    if not os.path.exists(src):
        print("MISSING:", src); continue
    img = Image.open(src)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    if img.width > MAX_W:
        h = round(img.height * MAX_W / img.width)
        img = img.resize((MAX_W, h), Image.LANCZOS)
    img.save(dst, "WEBP", quality=80, method=6)
    print(f"{dst}  {os.path.getsize(dst)//1024} KB  ({img.size[0]}x{img.size[1]})")
