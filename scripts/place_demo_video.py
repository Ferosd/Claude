# -*- coding: utf-8 -*-
"""Coremagna demo videosu yerlestirme pipeline'i.

Kullanim (repo kokunden):
    python scripts/place_demo_video.py realestate
    python scripts/place_demo_video.py dental --source "C:/path/to/demo-dental.mp4" --poster-time 36.0

Yaptigi is:
 1. Kaynak mp4'ten sesi atarak videos/demo-<sector>.mp4 kopyasini cikarir (re-encode yok)
 2. --poster-time anindan videos/demo-<sector>-poster.jpg uretir
 3. Sektore esli sayfalara "See It Happen" video bolumunu ekler
    (sayfada ayni video zaten varsa dokunmaz — idempotent)

Kaynak varsayilani: ../kling/coremagna-demos/out/demo-<sector>.mp4
"""
import argparse, os, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SRC = os.path.join(os.path.dirname(REPO), 'kling', 'coremagna-demos', 'out')

SECTORS = {
    'law': {
        'headline': '12 seconds from enquiry to booked consultation',
        'aria': 'Demo video: a law firm enquiry goes from website chat to booked consultation and CRM record in 12 seconds',
        'pages': ['industries/law-firms-enquiry.html', 'industries/law-firms-intake.html',
                  'industries/law-firms-after-hours.html'],
    },
    'realestate': {
        'headline': 'Seconds from portal lead to booked viewing',
        'aria': 'Demo video: a Rightmove enquiry becomes a booked viewing with reminders, in seconds',
        'pages': ['estate-agents.html', 'industries/real-estate-leads.html',
                  'industries/real-estate-viewings.html', 'industries/real-estate-noshow.html'],
    },
    'dental': {
        'headline': 'Seconds from enquiry to a booked chair',
        'aria': 'Demo video: an urgent dental enquiry becomes a same-day booked appointment, in seconds',
        'pages': ['dental-clinics.html', 'industries/clinics-lost-calls.html',
                  'industries/clinics-empty-chairs.html'],
    },
    'salon': {
        'headline': 'Seconds from DM to paid booking',
        'aria': 'Demo video: an Instagram enquiry becomes a deposit-paid salon booking with reminders, in seconds',
        'pages': ['industries/beauty-no-show-clients.html', 'industries/beauty-booking-chaos.html'],
    },
}

BLOCK = '''
<!-- ── DEMO VIDEO ── -->
<section aria-label="Watch the system in action" style="padding:64px 0;border-top:1px solid rgba(255,255,255,0.07)">
  <div class="container">
    <span style="font-family:'Cabinet Grotesk',sans-serif;font-size:10px;letter-spacing:0.18em;text-transform:uppercase;color:var(--accent,#00D4AA);font-weight:700;display:block;margin-bottom:8px">See It Happen</span>
    <h2 style="font-family:'Cabinet Grotesk',sans-serif;font-weight:800;font-size:clamp(1.6rem,3vw,2.2rem);line-height:1.05;letter-spacing:-0.02em;color:var(--text,#F0F4F3);max-width:640px;margin:0 0 24px">{headline}</h2>
    <div style="max-width:920px">
      <video src="/videos/demo-{sector}.mp4" poster="/videos/demo-{sector}-poster.jpg" muted autoplay loop playsinline controls preload="metadata" style="width:100%;display:block;border-radius:14px;border:1px solid rgba(0,212,170,0.25)" aria-label="{aria}"></video>
      <p style="font-family:'DM Sans',sans-serif;font-size:12px;color:var(--muted,#9AB0B0);margin-top:10px;line-height:1.6">Real flow, real timer — turn the sound on for the guided walkthrough. <a href="/demo.html" style="color:var(--accent,#00D4AA);text-decoration:none;font-weight:600">Try the same AI live →</a></p>
    </div>
  </div>
</section>
'''

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f'HATA: {" ".join(cmd)}\n{r.stderr[-500:]}')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('sector', choices=SECTORS)
    ap.add_argument('--source', help='kaynak mp4 (varsayilan: kling/coremagna-demos/out/demo-<sector>.mp4)')
    ap.add_argument('--poster-time', type=float, default=38.5, help='poster karesi saniyesi (kronometre ani ideal)')
    ap.add_argument('--headline', help='bolum basligini override et')
    a = ap.parse_args()

    cfg = SECTORS[a.sector]
    src = a.source or os.path.join(DEFAULT_SRC, f'demo-{a.sector}.mp4')
    if not os.path.isfile(src):
        sys.exit(f'Kaynak bulunamadi: {src}')

    vdir = os.path.join(REPO, 'videos')
    os.makedirs(vdir, exist_ok=True)
    dst = os.path.join(vdir, f'demo-{a.sector}.mp4')
    poster = os.path.join(vdir, f'demo-{a.sector}-poster.jpg')

    # Anlatici sesli surum: ses kanali korunur (autoplay yine muted, kullanici acabilir)
    run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-c:v', 'copy', '-c:a', 'copy', dst])
    run(['ffmpeg', '-y', '-v', 'error', '-ss', str(a.poster_time), '-i', src,
         '-frames:v', '1', '-q:v', '3', '-vf', 'scale=1280:-1', poster])
    print(f'video: {dst} ({os.path.getsize(dst)//1024} KB), poster: {poster}')

    block = BLOCK.format(sector=a.sector, headline=a.headline or cfg['headline'], aria=cfg['aria'])
    marker = f'/videos/demo-{a.sector}.mp4'
    for rel in cfg['pages']:
        path = os.path.join(REPO, rel)
        if not os.path.isfile(path):
            print(f'{rel}: SAYFA YOK, atlandi'); continue
        s = open(path, encoding='utf-8').read()
        if marker in s:
            print(f'{rel}: zaten var, atlandi'); continue
        anchor = '\n<!-- ── SYSTEM CROSS-LINKS ── -->'
        if anchor in s:
            s = s.replace(anchor, block + anchor, 1)
        elif '</main>' in s:
            s = s.replace('</main>', block + '</main>', 1)
        else:
            print(f'{rel}: anchor bulunamadi, atlandi'); continue
        open(path, 'w', encoding='utf-8').write(s)
        print(f'{rel}: eklendi')

if __name__ == '__main__':
    main()
