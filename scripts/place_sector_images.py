# -*- coding: utf-8 -*-
"""Sektor gorselleri: WebP donusumu + sayfa yerlesimi.

Kullanim (repo kokunden):  python scripts/place_sector_images.py
 - images/raw/ icindeki kazanan varyantlari images/<slug>.webp'e cevirir (1600px, <=200KB)
 - Her slug'in hedef sayfalarina "problem" bolumunun hemen ustune atmosfer gorseli ekler
 - Idempotent: sayfada ayni webp zaten varsa dokunmaz
"""
import os, sys, io
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(REPO, 'images', 'raw')
OUT = os.path.join(REPO, 'images')

# slug -> (kaynak dosya, alt metni, hedef sayfalar)
IMAGES = {
    'law-night': ('law-night.jpg',
        "Empty solicitor's office at night with a desk phone ringing unanswered",
        ['industries/law-firms-after-hours.html', 'industries/law-firms-enquiry.html']),
    'law-desk': ('law-desk.jpg',
        "Stack of legal case folders on a solicitor's desk under a lamp",
        ['industries/law-firms-intake.html', 'industries/law-firms-followup.html']),
    'dental-reception': ('dental-reception.jpg',
        'Unstaffed dental clinic reception with a phone ringing off its cradle',
        ['industries/clinics-lost-calls.html']),
    'dental-chair': ('dental-chair-v1.jpg',
        'Empty dental treatment chair in a darkened clinic after hours',
        ['industries/clinics-empty-chairs.html', 'industries/clinics-patients-disappear.html']),
    'estate-window': ('estate-window-v1.jpg',
        'Estate agency window display glowing at dusk on a rainy high street',
        ['estate-agents.html', 'industries/real-estate-leads.html']),
    'estate-keys': ('estate-keys-v1.jpg',
        'House keys resting on a signed property contract beside a phone',
        ['industries/real-estate-viewings.html', 'industries/real-estate-noshow.html',
         'industries/real-estate-vendors.html']),
    'salon-chair': ('salon-chair-v1.jpg',
        "Empty styling chair and mirror in a salon prepared for a client who didn't show",
        ['industries/beauty-no-show-clients.html', 'industries/beauty-clients-never-return.html']),
    'salon-phone': ('salon-phone-v1.jpg',
        'Salon phone screen full of unanswered booking messages beside scissors',
        ['industries/beauty-invisible-on-instagram.html', 'industries/beauty-booking-chaos.html']),
    'restaurant-host': ('restaurant-host-v1.jpg',
        'Restaurant host stand phone ringing during a packed dinner service',
        ['industries/restaurants-phone-keeps-ringing.html', 'industries/restaurants-no-repeat-guests.html']),
    'restaurant-empty': ('restaurant-empty-v2.jpg',
        'One empty set table in an otherwise busy candlelit restaurant',
        ['industries/restaurants-empty-tables.html', 'industries/restaurants-bad-reviews-good-food.html']),
}

# Sablon nesillerine gore "problem" bolumu anchor'lari (oncelik sirasiyla)
ANCHORS = ['<!-- S3 THE PROBLEM -->', '<!-- S3 PROBLEM SECTION -->', '<!-- S3: PROBLEM SECTION -->',
           '<!-- ── PROBLEM ── -->', '<!-- S3: PROBLEM -->', '<!-- 3. ROI CALCULATOR -->',
           '<section class="problem-section"']

BLOCK = '''<!-- ── SECTOR IMAGE ── -->
<div style="padding:56px 0 0">
  <div class="container">
    <img src="/images/{slug}.webp" alt="{alt}" loading="lazy" decoding="async" width="{w}" height="{h}" style="width:100%;height:auto;display:block;border-radius:14px;border:1px solid rgba(255,255,255,0.08)">
  </div>
</div>
'''

def to_webp(src_path, dst_path, width=1600, max_kb=200):
    img = Image.open(src_path).convert('RGB')
    if img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    for q in (80, 72, 64, 56, 48):
        buf = io.BytesIO()
        img.save(buf, 'WEBP', quality=q, method=6)
        if buf.tell() <= max_kb * 1024:
            break
    open(dst_path, 'wb').write(buf.getvalue())
    return img.width, img.height, buf.tell() // 1024, q

def main():
    ok, miss = [], []
    for slug, (src_name, alt, pages) in IMAGES.items():
        src = os.path.join(RAW, src_name)
        if not os.path.isfile(src):
            print(f'{slug}: kaynak yok ({src_name}), atlandi'); miss.append(slug); continue
        dst = os.path.join(OUT, f'{slug}.webp')
        w, h, kb, q = to_webp(src, dst)
        print(f'{slug}.webp: {w}x{h}, {kb} KB (q{q})')
        block = BLOCK.format(slug=slug, alt=alt.replace('"', '&quot;'), w=w, h=h)
        for rel in pages:
            path = os.path.join(REPO, rel)
            if not os.path.isfile(path):
                print(f'  {rel}: SAYFA YOK'); continue
            s = open(path, encoding='utf-8').read()
            if f'/images/{slug}.webp' in s:
                print(f'  {rel}: zaten var'); continue
            anchor = next((a for a in ANCHORS if a in s), None)
            if not anchor:
                print(f'  {rel}: ANCHOR YOK, atlandi'); miss.append(rel); continue
            s = s.replace(anchor, block + anchor, 1)
            open(path, 'w', encoding='utf-8').write(s)
            print(f'  {rel}: eklendi ({anchor.strip("<!- >").encode("ascii", "ignore").decode().strip()})')
            ok.append(rel)
    print(f'\nToplam: {len(ok)} sayfa guncellendi' + (f', sorunlu: {miss}' if miss else ''))

if __name__ == '__main__':
    main()
