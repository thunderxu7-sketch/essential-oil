#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
CONFIG=json.loads((ROOT/'seo/site.json').read_text())
ORIGIN=CONFIG['origin'];BASE=CONFIG['base_path'];PUBLIC=ROOT/'public'
PATHS=['/','/products/afu-lavender-essential-oil-10ml/','/guides/choosing-lavender-essential-oil/','/faq/','/about/']
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
            assert a.get('type')=='application/ld+json','Public pages must not depend on JavaScript'
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
    assert len(p.schemas)==1 and '阿芙' in raw
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
actual={p.relative_to(PUBLIC) for p in PUBLIC.rglob('*') if p.is_file()}
assert actual==expected,(actual-expected,expected-actual)
print('PASS: 5 indexable static pages; GitHub Pages subpath links, assets, canonical, JSON-LD, sitemap and public-only artifact.')
