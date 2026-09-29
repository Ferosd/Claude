# -*- coding: utf-8 -*-
"""Urun videolari portfolyosu (product-videos.html) medya + sayfa pipeline'i.

Kullanim (repo kokunden):
    python scripts/build_product_wall.py --src "C:/Users/tarka/Downloads/Örnek videolar"
    # yerel onizleme: publish:false olanlar dahil hepsi, repoya dokunmadan
    python scripts/build_product_wall.py --src "..." --all --out <klasor> --page-out <klasor>/product-videos-preview.html

Yaptigi is:
 1. scripts/product-wall.json'daki her is icin (publish: true olanlar, --all ile hepsi):
      <slug>.mp4           tam surum, ses varsa sesli, uzun kenar <= 1280, en fazla 30 fps (lightbox oynaticisi)
      <slug>-loop.webp     sessiz hareketli WebP dongu, varsayilan 6 sn, ~240 bin piksel, kaynak fps'in yarisi
                           (en fazla 15). Duvarda kare gorunurken oynar.
      <slug>-poster.webp   dongunun ilk karesi, uzun kenar <= 960 (dongu yuklenene kadar ve lightbox'ta)
    Kayit alanlari: loop_start / loop_len (sn), crop ("w:h:x:y", ornegin videoya gomulu yaziyi kesmek icin),
    label (kare etiketi, bos ise style'dan), desc, sector.
    Gorseller (kind: image): <slug>.webp (<= 1600) + <slug>-thumb.webp (<= 900)
 2. Banner (hero): bitmis video -> hero-final.mp4 (sessiz) + poster, ayni videodan 4 cekim karesi,
    istege bagli urun fotografi -> hero-photo.webp
 3. Sayfada isaretler arasini yeniden yazar: WALL, HERO-PHOTO, HERO-SHOTS, HERO-FINAL, VIDEO-LD.
    Secilen is yoksa WALL'a dokunmaz (bos yer tutucular kalir).
Cikti dosyasi kaynaktan yeniyse tekrar kodlanmaz; --force ile zorlanir.
Dosya adlarinda musteri/marka adi kullanma: slug public URL olur.
"""
import argparse, datetime, html, json, os, re, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://coremagna.com'
URL = '/videos/products'

STYLES = {  # style -> tile label
    'ugc': 'UGC video', 'product': 'Product shot', 'motion': 'Motion',
    'ads': 'Ad', 'posters': 'Poster', 'marketplace': 'Marketplace',
}
RATIOS = [(9, 16), (2, 3), (3, 4), (4, 5), (1, 1), (5, 4), (4, 3), (3, 2), (16, 9), (21, 9)]
SHOT_LABELS = ['Hook', 'Detail', 'In use', 'End card']
IMAGE_EXT = ('.jpg', '.jpeg', '.png', '.webp')


def ffmpeg(*args):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-y', *args], capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    if r.returncode:
        sys.exit('ffmpeg hata verdi:\n' + r.stderr)


def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                          'stream=codec_type,width,height,r_frame_rate:format=duration',
                          '-of', 'json', path], capture_output=True, check=True,
                         text=True, encoding='utf-8').stdout
    d = json.loads(out)
    v = next(s for s in d['streams'] if s['codec_type'] == 'video')
    num, den = (v.get('r_frame_rate') or '30/1').split('/')
    return {'w': int(v['width']), 'h': int(v['height']),
            'fps': float(num) / float(den) if float(den) else 30.0,
            'dur': float(d.get('format', {}).get('duration', 0) or 0),
            'audio': any(s['codec_type'] == 'audio' for s in d['streams'])}


def fit(w, h, cap):
    """Scale so the long side is at most cap; both sides even (x264 needs that)."""
    k = min(1.0, cap / float(max(w, h)))
    return max(2, int(round(w * k / 2)) * 2), max(2, int(round(h * k / 2)) * 2)


def ratio_label(w, h):
    r = w / float(h)
    best = min(RATIOS, key=lambda p: abs(p[0] / float(p[1]) - r))
    return '%d:%d' % best


def fresh(out, src, force):
    return (not force) and os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src)


def iso_duration(sec):
    sec = int(round(sec))
    m, s = divmod(sec, 60)
    return 'PT%s%dS' % ('%dM' % m if m else '', s)


def crop_filter(item):
    return 'crop=%s,' % item['crop'] if item.get('crop') else ''


def webp_loop(src, out, item, meta, w, h, start, length):
    """Animated WebP via Pillow: much faster than ffmpeg's libwebp_anim, same encoder."""
    from PIL import Image
    fps = min(15, max(8, int(meta['fps'] / 2)))
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', '%.3f' % start, '-t', '%.3f' % length, '-i', src,
                          '-vf', '%sfps=%d,scale=%d:%d:flags=lanczos' % (crop_filter(item), fps, w, h),
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    size = w * h * 3
    frames = [Image.frombytes('RGB', (w, h), raw[i:i + size]) for i in range(0, len(raw) - size + 1, size)]
    if not frames:
        sys.exit('Dongu icin kare cikmadi: ' + src)
    frames[0].save(out, 'WEBP', save_all=True, append_images=frames[1:], duration=int(round(1000.0 / fps)),
                   loop=0, quality=int(item.get('loop_q', 62)), method=6)


def encode_video(src, out_dir, slug, meta, item, force):
    full = os.path.join(out_dir, slug + '.mp4')
    loop = os.path.join(out_dir, slug + '-loop.webp')
    post = os.path.join(out_dir, slug + '-poster.webp')
    if item.get('crop'):
        cw, ch = (int(v) for v in item['crop'].split(':')[:2])
        meta = dict(meta, w=cw, h=ch)
    crop = crop_filter(item)
    fps = ',fps=30' if meta['fps'] > 30.5 else ''
    fw, fh = fit(meta['w'], meta['h'], 1280)
    # the loop gets a pixel budget instead of a side cap, so tall and wide tiles weigh about the same
    k = min(1.0, (240000.0 / (meta['w'] * meta['h'])) ** 0.5, 720.0 / max(meta['w'], meta['h']))
    lw, lh = max(2, int(round(meta['w'] * k / 2)) * 2), max(2, int(round(meta['h'] * k / 2)) * 2)
    qw, qh = fit(meta['w'], meta['h'], 960)
    start = float(item.get('loop_start', 0))
    length = min(float(item.get('loop_len', 6)), max(1.0, meta['dur'] - start))
    if not fresh(full, src, force):
        audio = ['-c:a', 'aac', '-b:a', '128k'] if meta['audio'] and not item.get('mute') else ['-an']
        ffmpeg('-i', src, '-vf', '%sscale=%d:%d%s' % (crop, fw, fh, fps), '-c:v', 'libx264', '-preset', 'medium',
               '-crf', '23', '-profile:v', 'high', '-pix_fmt', 'yuv420p', *audio,
               '-movflags', '+faststart', full)
    if not fresh(loop, src, force):
        webp_loop(src, loop, item, meta, lw, lh, start, length)
    if not fresh(post, src, force):
        from PIL import Image
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', '%.3f' % start, '-i', src, '-frames:v', '1',
                              '-vf', '%sscale=%d:%d:flags=lanczos' % (crop, qw, qh), '-f', 'rawvideo',
                              '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
        Image.frombytes('RGB', (qw, qh), raw[:qw * qh * 3]).save(post, 'WEBP', quality=78, method=6)
    return {'w': fw, 'h': fh, 'pw': qw, 'ph': qh, 'dur': meta['dur']}


def encode_image(src, out_dir, slug, force):
    from PIL import Image
    full = os.path.join(out_dir, slug + '.webp')
    thumb = os.path.join(out_dir, slug + '-thumb.webp')
    with Image.open(src) as im:
        im = im.convert('RGB')
        fw, fh = fit(im.width, im.height, 1600)
        tw, th = fit(im.width, im.height, 900)
        if not fresh(full, src, force):
            im.resize((fw, fh), Image.LANCZOS).save(full, 'WEBP', quality=82, method=6)
        if not fresh(thumb, src, force):
            im.resize((tw, th), Image.LANCZOS).save(thumb, 'WEBP', quality=80, method=6)
    return {'w': fw, 'h': fh, 'pw': tw, 'ph': th}


def tile_html(item, dims, kind):
    e = lambda v: html.escape(str(v), quote=True)
    slug, style = item['slug'], item['style']
    label = item.get('label') or STYLES[style]
    ar = '%.4f' % (dims['w'] / float(dims['h']))
    common = ('style="--ar:%s" data-style="%s" data-kind="%s" data-title="%s" data-label="%s" data-ratio="%s"'
              % (ar, style, kind, e(item['title']), e(label), ratio_label(dims['w'], dims['h'])))
    for key in ('desc', 'sector'):
        if item.get(key):
            common += '\n         data-%s="%s"' % (key, e(item[key]))
    if kind == 'video':
        m, sec = divmod(int(round(dims['dur'])), 60)
        head = ('<a class="tile" href="%s/%s.mp4" %s\n         data-dur="%d:%02d" data-anim="%s/%s-loop.webp">'
                % (URL, slug, common, m, sec, URL, slug))
        img = '%s/%s-poster.webp' % (URL, slug)
    else:
        head = '<a class="tile" href="%s/%s.webp" %s>' % (URL, slug, common)
        img = '%s/%s-thumb.webp' % (URL, slug)
    return ('      %s\n'
            '        <span class="tile-media"><img src="%s" alt="" loading="lazy" decoding="async" width="%d" height="%d"></span>\n'
            '        <span class="tile-label"><span class="tile-title">%s</span><span class="tile-kind">%s</span></span>\n'
            '      </a>\n') % (head, img, dims['pw'], dims['ph'], e(item['title']), e(label))


def video_ld(item, dims):
    label = item.get('label') or STYLES[item['style']]
    return {
        '@type': 'VideoObject',
        'name': item['title'],
        'description': item.get('desc') or '%s by Coremagna: %s.' % (label, item['title']),
        'thumbnailUrl': '%s%s/%s-poster.webp' % (SITE, URL, item['slug']),
        'contentUrl': '%s%s/%s.mp4' % (SITE, URL, item['slug']),
        'uploadDate': item.get('date') or datetime.date.today().isoformat(),
        'duration': iso_duration(dims['dur']),
        'width': dims['w'], 'height': dims['h'],
    }


def replace_block(page, name, body):
    start, end = '<!-- %s:START -->\n' % name, '<!-- %s:END -->' % name
    i, j = page.find(start), page.find(end)
    if i < 0 or j < i:
        sys.exit('Sayfada %s isaretleri bulunamadi' % name)
    return page[:i + len(start)] + body + page[j:]


def build_hero(hero, src_dir, out_dir, force):
    """Returns {block_name: html} for the hero slots that have media."""
    blocks = {}
    if hero.get('video'):
        src = os.path.join(src_dir, hero['video'])
        meta = probe(src)
        fw, fh = fit(meta['w'], meta['h'], 1280)
        final = os.path.join(out_dir, 'hero-final.mp4')
        poster = os.path.join(out_dir, 'hero-final-poster.jpg')
        fps = ',fps=30' if meta['fps'] > 30.5 else ''
        if not fresh(final, src, force):
            ffmpeg('-i', src, '-vf', 'scale=%d:%d%s' % (fw, fh, fps), '-an', '-c:v', 'libx264',
                   '-preset', 'medium', '-crf', '24', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', final)
        if not fresh(poster, src, force):
            ffmpeg('-ss', '0.2', '-i', src, '-frames:v', '1', '-vf', 'scale=%d:%d' % fit(meta['w'], meta['h'], 960),
                   '-q:v', '3', poster)
        blocks['HERO-FINAL'] = (
            '          <video src="%s/hero-final.mp4" poster="%s/hero-final-poster.jpg" autoplay muted loop playsinline '
            'preload="metadata" aria-label="%s"></video>\n' % (URL, URL, html.escape(hero.get('alt', 'Finished product video'), quote=True)))
        times = hero.get('shots') or [meta['dur'] * k for k in (0.08, 0.3, 0.55, 0.85)]
        thumbs = []
        for n, t in enumerate(times[:4], 1):
            shot = os.path.join(out_dir, 'hero-shot-%d.jpg' % n)
            if not fresh(shot, src, force):
                ffmpeg('-ss', '%.3f' % t, '-i', src, '-frames:v', '1', '-vf',
                       'scale=%d:%d' % fit(meta['w'], meta['h'], 480), '-q:v', '4', shot)
            thumbs.append('                <span class="sc-thumb"><img src="%s/hero-shot-%d.jpg" alt="" loading="lazy" decoding="async"><em>%s</em></span>\n'
                          % (URL, n, SHOT_LABELS[n - 1]))
        blocks['HERO-SHOTS'] = ''.join(thumbs)
    if hero.get('photo'):
        from PIL import Image
        src = os.path.join(src_dir, hero['photo'])
        out = os.path.join(out_dir, 'hero-photo.webp')
        if not fresh(out, src, force):
            with Image.open(src) as im:
                im = im.convert('RGB')
                im.resize(fit(im.width, im.height, 900), Image.LANCZOS).save(out, 'WEBP', quality=82, method=6)
        blocks['HERO-PHOTO'] = '                <img src="%s/hero-photo.webp" alt="" loading="lazy" decoding="async">\n' % URL
    return blocks


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--src', required=True, help='kaynak dosyalarin klasoru')
    ap.add_argument('--manifest', default=os.path.join(REPO, 'scripts', 'product-wall.json'))
    ap.add_argument('--out', default=os.path.join(REPO, 'videos', 'products'))
    ap.add_argument('--page', default=os.path.join(REPO, 'product-videos.html'))
    ap.add_argument('--page-out', help='sayfayi baska yere yaz (varsayilan: yerinde)')
    ap.add_argument('--all', action='store_true', help='publish:false olanlari da dahil et (onizleme)')
    ap.add_argument('--force', action='store_true', help='ciktilari bastan kodla')
    a = ap.parse_args()

    with open(a.manifest, encoding='utf-8') as f:
        manifest = json.load(f)
    os.makedirs(a.out, exist_ok=True)

    tiles, lds = [], []
    for item in manifest.get('items', []):
        if not (a.all or item.get('publish')):
            continue
        if item['style'] not in STYLES:
            sys.exit('Bilinmeyen style: %s (%s)' % (item['style'], item['slug']))
        src = os.path.join(a.src, item['src'])
        if not os.path.exists(src):
            sys.exit('Kaynak yok: ' + src)
        if src.lower().endswith(IMAGE_EXT):
            dims = encode_image(src, a.out, item['slug'], a.force)
            tiles.append(tile_html(item, dims, 'image'))
        else:
            dims = encode_video(src, a.out, item['slug'], probe(src), item, a.force)
            tiles.append(tile_html(item, dims, 'video'))
            lds.append(video_ld(item, dims))
        print('ok  %-28s %s' % (item['slug'], item['style']))

    with open(a.page, encoding='utf-8', newline='') as f:
        page = f.read()
    nl = '\r\n' if '\r\n' in page else '\n'
    page = page.replace('\r\n', '\n')
    if tiles:
        page = replace_block(page, 'WALL', ''.join(tiles))
    hero = manifest.get('hero') or {}
    if a.all or hero.get('publish'):
        for name, body in build_hero(hero, a.src, a.out, a.force).items():
            page = replace_block(page, name, body)
    ld = ''
    if lds:
        ld = ('<script type="application/ld+json">\n%s\n</script>\n'
              % json.dumps({'@context': 'https://schema.org', '@graph': lds}, ensure_ascii=False, indent=2))
    page = replace_block(page, 'VIDEO-LD', ld)
    out_page = a.page_out or a.page
    with open(out_page, 'w', encoding='utf-8', newline='') as f:
        f.write(page.replace('\n', nl))
    print('%d is, sayfa: %s' % (len(tiles), out_page))


if __name__ == '__main__':
    main()
