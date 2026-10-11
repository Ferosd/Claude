# Shared pieces of the three service pages: head, nav, footer, scripts, JSON-LD and
# small HTML helpers. build.py puts them together with one page_*.py module each.
import json, os, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://coremagna.com'
CAL = 'https://calendar.app.google/XDGM8XJ9zEdqugKr9'
TODAY = '2026-10-11'
TODAY_LONG = '11 October 2026'
MAIL_B64 = 'ZmVyaXQxQGNvcmVtYWduYS5jb20='

ICONS = json.load(open(os.path.join(HERE, 'icons.json'), encoding='utf-8'))


def sprite(names):
    out = ['<!-- Phosphor icon sprite (regular weight) -->',
           '<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">']
    for n in sorted(set(names)):
        body = ICONS['i-' + n]
        out.append('<symbol id="i-%s" viewBox="0 0 256 256">%s</symbol>' % (n, body))
    out.append('</svg>')
    return '\n'.join(out)


def ic(name, cls='ic'):
    return '<svg class="%s" aria-hidden="true"><use href="#i-%s"/></svg>' % (cls, name)


def esc(s):
    return html.escape(s, quote=True)


HEAD = '''<!DOCTYPE html>
<!-- Built by scripts/service-pages/build.py from page_{{MODULE}}.py, parts.py and base.css.
     Change those and run the build. A hand edit here is lost the next time it runs. -->
<html lang="en">
<head>
<meta charset="UTF-8">
<script>document.documentElement.classList.add('js');try{if(localStorage.getItem('theme')==='light')document.documentElement.setAttribute('data-theme','light')}catch(e){}</script>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TITLE}}</title>
<meta name="description" content="{{DESC}}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="Ferit Patefe">
<link rel="canonical" href="{{URL}}">
<meta property="og:title" content="{{OG_TITLE}}">
<meta property="og:description" content="{{OG_DESC}}">
<meta property="og:type" content="website">
<meta property="og:url" content="{{URL}}">
<meta property="og:image" content="{{OG_IMAGE}}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{{OG_ALT}}">
<meta property="og:site_name" content="Coremagna">
<meta property="og:locale" content="en_GB">
<meta property="article:modified_time" content="{{TODAY}}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{{OG_IMAGE}}">
<meta name="twitter:title" content="{{OG_TITLE}}">
<meta name="twitter:description" content="{{OG_DESC}}">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-7MDPMWZ158"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-7MDPMWZ158');
</script>
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="shortcut icon" href="/favicon.ico">
<link rel="stylesheet" href="/fonts/fonts.css">
<link rel="stylesheet" href="/motion.css">
<style>
{{CSS}}
</style>

<script type="application/ld+json">
{{JSONLD}}
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

{{SPRITE}}

<!-- ── NAVIGATION ── -->
<nav id="mainNav" class="pre-entrance" aria-label="Main navigation">
  <div class="nav-inner">
    <a href="/" class="logo" aria-label="Coremagna home">
      <span class="logo-core">Core</span><span class="logo-magna">magna</span><span class="logo-dot" aria-hidden="true"></span>
    </a>
    <ul class="nav-links" role="list">
      <li><a href="/industries">Industries</a></li>
      <li><a href="/real-estate-videos">Video Tours</a></li><li><a href="/product-videos">Product Videos</a></li>
      <li><a href="/demo">Work</a></li>
      <li><a href="/about">About</a></li>
      <li><a href="/blog/">Blog</a></li>
      <li><a href="/#faq">FAQ</a></li><li><a href="/#contact">Contact</a></li>
    </ul>
    <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">
      <svg class="icon-sun" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M120,40V16a8,8,0,0,1,16,0V40a8,8,0,0,1-16,0Zm72,88a64,64,0,1,1-64-64A64.07,64.07,0,0,1,192,128Zm-16,0a48,48,0,1,0-48,48A48.05,48.05,0,0,0,176,128ZM58.34,69.66A8,8,0,0,0,69.66,58.34l-16-16A8,8,0,0,0,42.34,53.66Zm0,116.68-16,16a8,8,0,0,0,11.32,11.32l16-16a8,8,0,0,0-11.32-11.32ZM192,72a8,8,0,0,0,5.66-2.34l16-16a8,8,0,0,0-11.32-11.32l-16,16A8,8,0,0,0,192,72Zm5.66,114.34a8,8,0,0,0-11.32,11.32l16,16a8,8,0,0,0,11.32-11.32ZM48,128a8,8,0,0,0-8-8H16a8,8,0,0,0,0,16H40A8,8,0,0,0,48,128Zm80,80a8,8,0,0,0-8,8v24a8,8,0,0,0,16,0V216A8,8,0,0,0,128,208Zm112-88H216a8,8,0,0,0,0,16h24a8,8,0,0,0,0-16Z"/></svg>
      <svg class="icon-moon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M233.54,142.23a8,8,0,0,0-8-2,88.08,88.08,0,0,1-109.8-109.8,8,8,0,0,0-10-10,104.84,104.84,0,0,0-52.91,37A104,104,0,0,0,136,224a103.09,103.09,0,0,0,62.52-20.88,104.84,104.84,0,0,0,37-52.91A8,8,0,0,0,233.54,142.23Z"/></svg>
    </button>
    <a href="{{CAL}}" target="_blank" rel="noopener noreferrer" class="btn-primary nav-cta" data-loc="nav">Book a Call</a>
    <button class="hamburger" id="hamburger" aria-label="Open menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>

<!-- Mobile nav overlay -->
<div class="mobile-nav" id="mobileNav" aria-hidden="true">
  <ul role="list">
    <li><a href="/industries">Industries</a></li>
    <li><a href="/real-estate-videos">Video Tours</a></li><li><a href="/product-videos">Product Videos</a></li>
    <li><a href="/demo">Work</a></li>
    <li><a href="/about">About</a></li>
    <li><a href="/blog/">Blog</a></li>
    <li><a href="/#faq">FAQ</a></li><li><a href="/#contact">Contact</a></li>
    <li><a href="{{CAL}}" target="_blank" rel="noopener noreferrer" class="btn-primary" data-loc="mobile-nav">Book a Call</a></li>
  </ul>
</div>

<main id="main">
'''

FOOT = '''
</main>

<!-- ── FOOTER ── -->
<footer>
  <div class="container">
    <div class="footer-inner">
      <div>
        <div class="footer-logo">Core<span>magna</span></div>
        <p class="footer-tagline">AI automation for service businesses.</p>
        <div class="footer-social">
          <a href="https://linkedin.com/in/ferit-patefe" class="social-icon" aria-label="LinkedIn" target="_blank" rel="noopener noreferrer">
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
          </a>
        </div>
      </div>
      <div class="footer-col">
        <h3>Services</h3>
        <ul>
          <li><a href="/ai-visibility"{{CUR_1}}>AI Visibility</a></li>
          <li><a href="/ad-creative-testing"{{CUR_2}}>Ad Creative Testing</a></li>
          <li><a href="/expert-content"{{CUR_3}}>Expert Content</a></li>
          <li><a href="/real-estate-videos">Video Tours</a></li>
          <li><a href="/product-videos">Product Videos</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h3>Company</h3>
        <ul>
          <li><a href="/industries">Industries</a></li>
          <li><a href="/about">About</a></li>
          <li><a href="/demo">Work</a></li>
          <li><a href="/blog/">Blog</a></li>
          <li><a href="/#faq">FAQ</a></li><li><a href="/#contact">Contact</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h3>Connect</h3>
        <ul>
          <li><a href="#" onclick="this.href='mailto:'+atob('{{MAIL}}')" rel="nofollow">ferit1@coremagna.com</a></li>
          <li><a href="https://linkedin.com/in/ferit-patefe" target="_blank" rel="noopener noreferrer">LinkedIn</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2026 Coremagna. All rights reserved. · <a href="/privacy">Privacy</a> · <a href="/terms">Terms</a></p>
      <p>AI Automation · CRM Systems · Chatbots</p>
    </div>
  </div>
</footer>

<script>
function track(name,params){if(typeof gtag==='function')gtag('event',name,params||{});}
const PAGE='{{PAGE}}';

/* Nav scroll + hamburger */
(function(){
  const nav=document.getElementById('mainNav');
  const hamburger=document.getElementById('hamburger');
  const mobileNav=document.getElementById('mobileNav');
  let menuOpen=false;
  window.addEventListener('scroll',()=>{nav.classList.toggle('scrolled',window.scrollY>40);},{passive:true});
  hamburger.addEventListener('click',()=>{
    menuOpen=!menuOpen;hamburger.classList.toggle('open',menuOpen);hamburger.setAttribute('aria-expanded',String(menuOpen));
    mobileNav.setAttribute('aria-hidden',String(!menuOpen));mobileNav.classList.toggle('visible',menuOpen);document.body.style.overflow=menuOpen?'hidden':'';
  });
  mobileNav.querySelectorAll('a').forEach(a=>{a.addEventListener('click',()=>{menuOpen=false;hamburger.classList.remove('open');hamburger.setAttribute('aria-expanded','false');mobileNav.setAttribute('aria-hidden','true');mobileNav.classList.remove('visible');document.body.style.overflow='';});});
  setTimeout(()=>{nav.classList.remove('pre-entrance');nav.classList.add('entered');},0);
})();

/* Booking clicks and the obfuscated mail links */
(function(){
  document.querySelectorAll('a[href^="https://calendar.app.google"]').forEach(a=>{
    a.addEventListener('click',()=>track('cta_click',{page:PAGE,location:a.dataset.loc||'page'}));
  });
  document.querySelectorAll('.js-mail').forEach(a=>{
    const set=()=>{a.href='mailto:'+atob('{{MAIL}}')+'?subject='+encodeURIComponent(a.dataset.subject||'{{MAIL_SUBJECT}}')+(a.dataset.body?'&body='+encodeURIComponent(a.dataset.body):'');};
    a.addEventListener('pointerenter',set,{once:true});
    a.addEventListener('focus',set,{once:true});
    a.addEventListener('click',()=>{set();track('cta_click',{page:PAGE,location:'email'});});
  });
})();

/* Sections fade up as they enter the viewport. The hidden state is only
   switched on here, so the page reads normally if this script never runs. */
(function(){
  const els=document.querySelectorAll('.rv');
  if(!els.length||!('IntersectionObserver' in window)||window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.documentElement.classList.add('rv-on');
  const io=new IntersectionObserver(es=>es.forEach(e=>{
    if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target);}
  }),{rootMargin:'0px 0px -6% 0px',threshold:0.05});
  els.forEach(el=>io.observe(el));
})();

/* Explainer video: count the first play */
(function(){
  document.querySelectorAll('video[data-video]').forEach(v=>{
    v.addEventListener('play',()=>track('video_play',{page:PAGE,video:v.dataset.video}),{once:true});
  });
})();
{{PAGE_JS}}
/* FAQ accordion */
(function(){
  document.querySelectorAll('.faq-item').forEach(item=>{
    const q=item.querySelector('.faq-q');
    const a=item.querySelector('.faq-a');
    q.addEventListener('click',()=>{
      const open=item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(other=>{
        if(other!==item){other.classList.remove('open');other.querySelector('.faq-a').style.maxHeight=null;other.querySelector('.faq-q').setAttribute('aria-expanded','false');}
      });
      if(open){item.classList.remove('open');a.style.maxHeight=null;q.setAttribute('aria-expanded','false');}
      else{item.classList.add('open');a.style.maxHeight=a.scrollHeight+'px';q.setAttribute('aria-expanded','true');}
    });
  });
})();

/* Theme toggle (the stored theme is applied in the head, before first paint) */
(function(){
  const btn=document.getElementById('themeToggle');
  if(btn)btn.addEventListener('click',function(){
    const isLight=document.documentElement.getAttribute('data-theme')==='light';
    if(isLight){document.documentElement.removeAttribute('data-theme');localStorage.setItem('theme','dark');}
    else{document.documentElement.setAttribute('data-theme','light');localStorage.setItem('theme','light');}
  });
})();
</script>
</body>
</html>
'''

PERSON = {
    '@type': 'Person',
    '@id': SITE + '/about#ferit-patefe',
    'name': 'Ferit Patefe',
    'jobTitle': 'Founder',
    'url': SITE + '/about',
    'sameAs': ['https://www.linkedin.com/in/ferit-patefe'],
}
ORG = {
    '@type': 'Organization',
    '@id': SITE + '/#organization',
    'name': 'Coremagna',
    'url': SITE,
    'email': 'ferit1@coremagna.com',
    'founder': {'@id': SITE + '/about#ferit-patefe'},
}
AREAS = ['United Kingdom', 'Ireland', 'Australia', 'New Zealand', 'Canada', 'United States']


def graph(slug, name, title, desc, service, video, crumb):
    """JSON-LD for a service page: WebPage, Service with offers, breadcrumb, video, author.
    No FAQPage on purpose: Google stopped showing FAQ rich results on 7 May 2026."""
    url = '%s/%s' % (SITE, slug)
    g = [
        {
            '@type': 'WebPage',
            '@id': url + '#webpage',
            'url': url,
            'name': title,
            'description': desc,
            'inLanguage': 'en-GB',
            'datePublished': TODAY,
            'dateModified': TODAY,
            'author': {'@id': PERSON['@id']},
            'publisher': {'@id': ORG['@id']},
            'about': {'@id': url + '#service'},
            'primaryImageOfPage': {'@type': 'ImageObject', 'url': '%s/images/og-%s.jpg' % (SITE, slug), 'width': 1200, 'height': 630},
        },
        dict({'@type': 'Service', '@id': url + '#service', 'url': url, 'provider': {'@id': ORG['@id']},
              'areaServed': AREAS}, **service),
        {
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': crumb, 'item': url},
            ],
        },
        dict({'@type': 'VideoObject', 'uploadDate': TODAY, 'width': 1280, 'height': 720}, **video),
        ORG,
        PERSON,
    ]
    return json.dumps({'@context': 'https://schema.org', '@graph': g}, indent=2, ensure_ascii=False)


def offer(name, price, desc, unit=None):
    o = {'@type': 'Offer', 'name': name, 'price': str(price), 'priceCurrency': 'USD', 'description': desc}
    if unit:
        o['priceSpecification'] = {'@type': 'UnitPriceSpecification', 'price': str(price), 'priceCurrency': 'USD',
                                   'unitText': unit}
    return o


def table(caption, heads, rows, us=None):
    """Comparison table. heads are the column titles; each row is a list whose first cell is the
    row header. us is the index of the column to highlight. Every cell carries data-label so the
    table can stack into blocks on a phone."""
    cls = lambda i: ' class="is-us"' if i == us else ''
    out = ['<div class="tbl-wrap rv">', '  <table class="tbl">']
    if caption:
        out.append('    <caption>%s</caption>' % caption)
    out.append('    <thead><tr>%s</tr></thead>' % ''.join(
        '<th scope="col"%s>%s</th>' % (cls(i), h) for i, h in enumerate(heads)))
    out.append('    <tbody>')
    for r in rows:
        cells = ['<th scope="row">%s</th>' % r[0]]
        cells += ['<td data-label="%s"%s>%s</td>' % (heads[i], cls(i), c) for i, c in enumerate(r[1:], 1)]
        out.append('      <tr>%s</tr>' % ''.join(cells))
    out += ['    </tbody>', '  </table>', '</div>']
    return '\n'.join(out)


def faq_html(items):
    out = []
    for q, a in items:
        out.append('''        <div class="faq-item">
          <button class="faq-q" aria-expanded="false">%s<span class="faq-icon" aria-hidden="true"></span></button>
          <div class="faq-a"><div class="faq-a-inner">%s</div></div>
        </div>''' % (q, a))
    return '\n'.join(out)


def render(page):
    base_css = open(os.path.join(HERE, 'base.css'), encoding='utf-8').read().rstrip()
    css = base_css + '\n\n' + page['css'].strip()
    doc = (HEAD + page['body'].strip('\n') + '\n' + FOOT)
    cur = {1: '', 2: '', 3: ''}
    cur[page['n']] = ' aria-current="page"'
    rep = {
        '{{TITLE}}': esc(page['title']), '{{DESC}}': esc(page['desc']), '{{URL}}': '%s/%s' % (SITE, page['slug']),
        '{{OG_TITLE}}': esc(page['og_title']), '{{OG_DESC}}': esc(page['og_desc']),
        '{{OG_IMAGE}}': '%s/images/og-%s.jpg' % (SITE, page['slug']), '{{OG_ALT}}': esc(page['og_alt']),
        '{{TODAY}}': TODAY, '{{CSS}}': css, '{{JSONLD}}': page['jsonld'], '{{SPRITE}}': sprite(page['icons']),
        '{{PAGE}}': page['slug'], '{{PAGE_JS}}': '\n' + page.get('js', '').strip('\n') + '\n',
        '{{MAIL_SUBJECT}}': page['mail_subject'], '{{MAIL}}': MAIL_B64, '{{CAL}}': CAL,
        '{{CUR_1}}': cur[1], '{{CUR_2}}': cur[2], '{{CUR_3}}': cur[3], '{{TODAY_LONG}}': TODAY_LONG,
        '{{MODULE}}': page['slug'].replace('-', '_'),
    }
    for k, v in rep.items():
        doc = doc.replace(k, v)
    left = re.findall(r'\{\{[A-Z_0-9]+\}\}', doc)
    assert not left, left
    return doc
