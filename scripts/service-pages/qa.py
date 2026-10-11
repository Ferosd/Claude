# Checks the generated service pages (and the new home page section) against the
# site rules in CLAUDE.md and a few SEO basics. Prints findings; exits 1 if any.
#   python scripts/service-pages/qa.py
import html, json, os, re, sys
from html.parser import HTMLParser

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGES = ['ai-visibility', 'ad-creative-testing', 'expert-content']
BANNED = ['leverage', 'seamless', 'elevate', 'unleash', 'next-gen', 'cutting-edge', 'robust', 'synergy', 'harness',
          'unlock potential', 'john doe', 'acme corp', 'lorem ipsum']
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
problems = []


def bad(page, msg):
    problems.append('%s: %s' % (page, msg))


class P(HTMLParser):
    """Collects headings, links, images and visible text."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.heads, self.links, self.imgs, self.text, self.ids, self.faq = [], [], [], [], [], set(), []
        self.cur = None
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        if tag in ('script', 'style', 'svg'):
            self.skip += 1
        if tag in ('h1', 'h2', 'h3', 'h4'):
            self.cur = [tag, '']
        if tag == 'button' and 'faq-q' in a.get('class', ''):
            self.cur = ['faq', '']
        if tag == 'a':
            self.links.append(a)
        if tag in ('img', 'video', 'source'):
            self.imgs.append((tag, a))

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'svg'):
            self.skip -= 1
        if self.cur and (tag == self.cur[0] or (self.cur[0] == 'faq' and tag == 'button')):
            (self.faq if self.cur[0] == 'faq' else self.heads).append((self.cur[0], ' '.join(self.cur[1].split())))
            self.cur = None

    def handle_data(self, data):
        if self.skip:
            return
        self.text.append(data)
        if self.cur:
            self.cur[1] += data


def exists(path):
    path = path.split('#')[0].split('?')[0]
    if path in ('', '/'):
        return True
    p = os.path.join(REPO, path.lstrip('/').replace('/', os.sep))
    return os.path.isfile(p) or os.path.isfile(p + '.html') or os.path.isfile(os.path.join(p, 'index.html'))


def check_headings(page, heads, faq):
    for tag, t in heads + faq:
        if re.search(r'[.,:;\u2014\u2013]', t):
            bad(page, 'punctuation in %s: %r' % (tag, t))
        for m in re.finditer(r'(\S*)-(\S*)', t):
            if not (m.group(1) and m.group(2)):
                bad(page, 'loose hyphen in %s: %r' % (tag, t))


def check_page(slug):
    path = os.path.join(REPO, slug + '.html')
    raw = open(path, encoding='utf-8').read()
    p = P()
    p.feed(raw)
    text = ' '.join(' '.join(p.text).split())

    title = re.search(r'<title>(.*?)</title>', raw).group(1)
    desc = html.unescape(re.search(r'<meta name="description" content="(.*?)">', raw).group(1))
    if len(html.unescape(title)) > 60:
        bad(slug, 'title is %d characters' % len(html.unescape(title)))
    if not 110 <= len(desc) <= 160:
        bad(slug, 'description is %d characters' % len(desc))
    if 'rel="canonical" href="https://coremagna.com/%s"' % slug not in raw:
        bad(slug, 'canonical missing')

    h1 = [h for h in p.heads if h[0] == 'h1']
    if len(h1) != 1:
        bad(slug, '%d h1 elements' % len(h1))
    last = 1
    for tag, t in p.heads:
        lvl = int(tag[1])
        if lvl > last + 1:
            bad(slug, 'heading level jumps to %s: %r' % (tag, t))
        last = lvl
    check_headings(slug, p.heads, p.faq)

    low = text.lower()
    for w in BANNED:
        if re.search(r'(?<![a-z])' + re.escape(w) + r'(?![a-z])', low):
            bad(slug, 'banned word in copy: ' + w)
    if re.search(r'[\u2014\u2013]', text):
        bad(slug, 'dash character in copy: ' + ', '.join(sorted(set(re.findall(r'.{20}[\u2014\u2013].{20}', text))))[:200])
    if re.search('[\U0001F300-\U0001FAFF\u2600-\u27BF]', raw):
        bad(slug, 'emoji or pictograph character')

    for a in p.links:
        h = a.get('href', '')
        if h.startswith('/'):
            if '.html' in h:
                bad(slug, '.html link: ' + h)
            if not exists(h):
                bad(slug, 'internal link target missing: ' + h)
            if '#' in h and h.split('#')[0] in ('/' + s for s in PAGES):
                other = open(os.path.join(REPO, h.split('#')[0].lstrip('/') + '.html'), encoding='utf-8').read()
                if 'id="%s"' % h.split('#')[1] not in other:
                    bad(slug, 'anchor missing on target: ' + h)
        elif h.startswith('#') and len(h) > 1:
            if h[1:] not in p.ids:
                bad(slug, 'in-page anchor missing: ' + h)
        elif h.startswith('http'):
            if a.get('target') == '_blank' and 'noopener' not in a.get('rel', ''):
                bad(slug, 'external link without rel=noopener: ' + h)
            if 'calendar.app.google' not in h and a.get('target') != '_blank':
                bad(slug, 'external link opens in the same tab: ' + h)
        elif h not in ('#',):
            bad(slug, 'odd href: %r' % h)
    for tag, a in p.imgs:
        for k in ('src', 'poster'):
            v = a.get(k)
            if v and v.startswith('/') and not exists(v):
                bad(slug, 'asset missing: ' + v)
        if tag == 'img':
            if 'alt' not in a:
                bad(slug, 'img without alt: ' + a.get('src', ''))
            if not (a.get('width') and a.get('height')):
                bad(slug, 'img without dimensions: ' + a.get('src', ''))

    css = re.search(r'<style>(.*?)</style>', raw, re.S).group(1)
    body_css = re.sub(r':root\s*\{.*?\}|\[data-theme="light"\]\s*\{.*?\}', '', css, count=2, flags=re.S)
    for m in re.finditer(r'#[0-9a-fA-F]{3,8}\b', body_css):
        bad(slug, 'hard-coded colour in CSS: ' + body_css[max(0, m.start() - 50):m.end()].replace('\n', ' '))
    if re.search(r'transition\s*:\s*all', css):
        bad(slug, 'transition: all')
    for m in re.finditer(r'font-size\s*:\s*([\d.]+)rem', css):
        if float(m.group(1)) > 4:
            bad(slug, 'font-size above 4rem')
    for m in re.finditer(r'font-size\s*:\s*(\d+)px', css):
        if int(m.group(1)) > 64:
            bad(slug, 'font-size above 64px')

    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
        d = json.loads(block)
        types = [n['@type'] for n in d['@graph']]
        for need in ('WebPage', 'Service', 'BreadcrumbList', 'VideoObject', 'Organization', 'Person'):
            if need not in types:
                bad(slug, 'JSON-LD lacks ' + need)
        if 'FAQPage' in types:
            bad(slug, 'JSON-LD has FAQPage')
        v = [n for n in d['@graph'] if n['@type'] == 'VideoObject'][0]
        for k in ('name', 'description', 'thumbnailUrl', 'contentUrl', 'uploadDate', 'duration'):
            if not v.get(k):
                bad(slug, 'VideoObject lacks ' + k)
        for k in ('thumbnailUrl', 'contentUrl'):
            if not exists(v[k].replace('https://coremagna.com', '')):
                bad(slug, 'VideoObject file missing: ' + v[k])
        for o in [n for n in d['@graph'] if n['@type'] == 'Service'][0]['offers']:
            if ('$' + format(int(o['price']), ',')) not in text and o['price'] != '0':
                bad(slug, 'offer price not shown on page: ' + o['price'])
    og = re.search(r'property="og:image" content="https://coremagna.com(.*?)"', raw).group(1)
    if not exists(og):
        bad(slug, 'og:image missing: ' + og)

    answer = re.search(r'<div class="answer rv">(.*?)</div>', raw, re.S).group(1)
    first = re.sub(r'<[^>]+>', '', re.search(r'<p>(.*?)</p>', answer, re.S).group(1))
    words = len(html.unescape(first).split())
    total = len(text.split())
    print('%-22s title %2d  desc %3d  h2 %2d  faq %2d  words %4d  first answer %3d words  links %d' % (
        slug, len(html.unescape(title)), len(desc), sum(1 for h in p.heads if h[0] == 'h2'), len(p.faq), total, words,
        len(p.links)))
    return p


for s in PAGES:
    check_page(s)

# The new section and footer column on the home page.
raw = open(os.path.join(REPO, 'index.html'), encoding='utf-8').read()
sec = re.search(r'<section id="new-services".*?</section>', raw, re.S).group(0)
p = P()
p.feed(sec)
check_headings('index#new-services', p.heads, [])
for a in p.links:
    if not exists(a['href']):
        bad('index#new-services', 'link target missing: ' + a['href'])
for tag, a in p.imgs:
    for k in ('src', 'poster', 'srcset'):
        if a.get(k) and not exists(a[k]):
            bad('index#new-services', 'asset missing: ' + a[k])
t = ' '.join(' '.join(p.text).split())
if re.search(r'[\u2014\u2013]', t):
    bad('index#new-services', 'dash character in copy')
for w in BANNED:
    if w in t.lower():
        bad('index#new-services', 'banned word: ' + w)
for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
    json.loads(block)
print('index#new-services     headings %d  links %d' % (len(p.heads), len(p.links)))

print()
print('\n'.join(problems) if problems else 'no problems found')
sys.exit(1 if problems else 0)
