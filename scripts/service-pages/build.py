# Builds the three service pages (/ai-visibility, /ad-creative-testing, /expert-content)
# into the repo root as standalone HTML. The site itself has no build step: the
# output is plain HTML with its CSS inline, like every other page.
#
#   python scripts/service-pages/build.py                  all three pages
#   python scripts/service-pages/build.py ai-visibility    one page
#   python scripts/service-pages/qa.py                     rule and link checks on the output
#
# Copy lives in page_*.py, shared head/nav/footer/scripts in parts.py, shared styles
# in base.css. When the copy changes, set TODAY in parts.py so the "Updated" date,
# dateModified and the Sources line move with it, and update lastmod in sitemap.xml.
import importlib, os, sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from parts import render

MODULES = ['page_ai_visibility', 'page_ad_creative_testing', 'page_expert_content']

only = sys.argv[1] if len(sys.argv) > 1 else ''
for name in MODULES:
    page = importlib.import_module(name).PAGE
    if only and page['slug'] != only:
        continue
    doc = render(page)
    path = os.path.join(REPO, page['slug'] + '.html')
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(doc)
    print('wrote %s.html (%d KB)' % (page['slug'], len(doc.encode('utf-8')) // 1024))
