#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from activities import ACTIVITY_PATHS, ASSETS
from demos import DEMO_FILES
from videos import VIDEO_ASSETS
import json
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
CONFIG=json.loads((ROOT/'seo/site.json').read_text())
ORIGIN=CONFIG['origin'];BASE=CONFIG['base_path'];PUBLIC=ROOT/'public'
PATHS=['/','/products/afu-lavender-essential-oil-10ml/','/guides/choosing-lavender-essential-oil/','/faq/','/about/']+ACTIVITY_PATHS
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.meta={};self.canonical=[];self.refs=[];self.ids=set();self.schemas=[];self.h1=0;self.title='';self.intitle=False;self.injson=False;self.buffer='';self.feed(text)
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if t=='h1':self.h1+=1
        if t=='title':self.intitle=True
        if t=='meta':self.meta[a.get('name',a.get('property',''))]=a.get('content','')
        if t=='link' and a.get('rel')=='canonical':self.canonical.append(a['href'])
        for k in ['href','src']:
            if k in a:self.refs.append(a[k])
        if t=='script':
            if a.get('src'):
                assert a.get('type')=='module' and a['src'] in [BASE+'/assets/activities.js',BASE+'/assets/videos.js']
            else:
                assert a.get('type')=='application/ld+json','Only structured data may be inline'
                self.injson=True;self.buffer=''
    def handle_data(self,d):
        if self.intitle:self.title+=d
        if self.injson:self.buffer+=d
    def handle_endtag(self,t):
        if t=='title':self.intitle=False
        if t=='script' and self.injson:self.schemas.append(json.loads(self.buffer));self.injson=False
pages={}
for path in PATHS:
    raw=(PUBLIC/path.strip('/')/'index.html').read_text();p=Page(raw);pages[path]=p
    assert p.h1==1 and p.title and p.meta['description']
    assert p.canonical==[ORIGIN+BASE+path]
    assert p.meta['robots'].startswith('index,')
    assert p.meta['og:url']==p.canonical[0]
    assert 'noindex' not in raw
    assert len(p.schemas)==1 and '晚间留白' in raw
home=(PUBLIC/'index.html').read_text()
assert home.count('class="video-card"')==3 and home.count('data-author-avatar')==3
assert '<iframe' not in home, 'Player must only load after a user chooses a video'
assert 'src="'+BASE+'/assets/videos.js"' in home
assert len({p.title for p in pages.values()})==len(PATHS)
for path,p in pages.items():
    for ref in p.refs:
        u=urlsplit(ref)
        if u.scheme:continue
        if u.path:
            assert u.path.startswith(BASE+'/'),ref
            local=u.path[len(BASE):]
        else:local=path
        f=PUBLIC/local.lstrip('/')
        if local.endswith('/'):
            assert local in pages,(path,ref)
            if u.fragment:assert unquote(u.fragment) in pages[local].ids,(path,ref)
        else:assert f.is_file(),ref
for obj in pages[PATHS[1]].schemas[0]['@graph']:
    if obj['@type']=='Product':
        assert obj['size']=='10ml'
        assert not {'offers','aggregateRating','review','image','sku','gtin'}.intersection(obj)
locations=[e.text for e in ET.parse(PUBLIC/'sitemap.xml').findall('.//{*}loc')]
assert locations==[ORIGIN+BASE+p for p in PATHS]
assert 'Sitemap: '+ORIGIN+BASE+'/sitemap.xml' in (PUBLIC/'robots.txt').read_text()
assert 'OAI-SearchBot\nAllow: /' in (PUBLIC/'robots.txt').read_text()
assert 'noindex' in (PUBLIC/'404.html').read_text()
assert (PUBLIC/'.nojekyll').exists()
expected={Path(p.lstrip('/'))/'index.html' for p in PATHS}|{Path(p) for p in ['assets/evening.png','assets/public.css','404.html','robots.txt','sitemap.xml','llms.txt','.nojekyll']}
expected|={Path('assets')/name for name in ASSETS + VIDEO_ASSETS}
expected|=DEMO_FILES
for route in ['mini','admin']:
    raw=(PUBLIC/route/'index.html').read_text()
    assert 'noindex, follow' in raw and f'data-route="{route}"' in raw
    assert f'href="{BASE}/demo-assets/style.css"' in raw
    assert f'src="{BASE}/demo-assets/app.js"' in raw
    assert f'data-base="{BASE}"' in raw
app=(PUBLIC/'demo-assets/app.js').read_text()
assert not any(t in app for t in ['function plan()', 'function website()', '宣发策划案.md', 'product-reference.jpg'])
assert 'evening-pages-demo-v1' in app and 'storage' in app
assert '../assets/evening.png' in (PUBLIC/'demo-assets/style.css').read_text()
actual={p.relative_to(PUBLIC) for p in PUBLIC.rglob('*') if p.is_file()}
assert actual==expected,(actual-expected,expected-actual)
print('PASS: 8 indexable pages with static introductions and optional activity interactions; GitHub Pages subpath links, assets, canonical, JSON-LD, sitemap and isolated static mini/admin demos.')
