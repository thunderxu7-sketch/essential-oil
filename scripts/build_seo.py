#!/usr/bin/env python3
"""Build crawlable HTML. No JavaScript execution or external packages required."""
from activities import ACTIVITY_PATHS, ASSETS, activity_pages
from consumer_pages import consumer_pages
from demos import DEMO_FILES, build_demos
from videos import VIDEO_ASSETS, build_videos
import argparse
import html
import ipaddress
import json
import re
from pathlib import Path
import shutil
from urllib.parse import urlsplit
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parents[1]
PRODUCT_PATH = '/products/afu-lavender-essential-oil-10ml/'
GUIDE_PATH = '/guides/choosing-lavender-essential-oil/'
FAQ_PATH = '/faq/'
ABOUT_PATH = '/about/'
PUBLIC_PATHS = ['/', PRODUCT_PATH, GUIDE_PATH, FAQ_PATH, ABOUT_PATH] + ACTIVITY_PATHS
E = html.escape


def validate_origin(value):
    value = value.strip().rstrip('/')
    if not value:
        return ''
    u = urlsplit(value)
    if u.scheme != 'https' or not u.hostname or u.username or u.password or u.path or u.query or u.fragment or u.port:
        raise ValueError('正式域名必须是纯 HTTPS origin，不含路径、端口、账户或查询参数。')
    host = u.hostname.lower()
    try:
        ipaddress.ip_address(host)
        raise ValueError('请使用已确认的公开域名，不使用 IP 地址。')
    except ValueError as ex:
        if str(ex).startswith('请使用'):
            raise
    if '.' not in host or host.endswith(('.localhost', '.local', '.test', '.invalid', '.example')) or host in ('example.com','example.org','example.net'):
        raise ValueError('请使用真实生产域名，不使用本地或示例域名。')
    return value


def build(output, origin='', release=False, base_path=None):
    config = json.loads((ROOT/'seo/site.json').read_text())
    origin = validate_origin(origin or config['origin'])
    base_path = config.get('base_path', '') if base_path is None else base_path
    base_path = base_path.rstrip('/')
    if base_path and not re.fullmatch(r'/[A-Za-z0-9_-]+', base_path):
        raise ValueError('项目路径必须是 /仓库名称。')
    if release and not origin:
        raise ValueError('发布构建缺少正式域名。使用 --origin https://你的域名，或填写 seo/site.json 的 origin。')
    output = Path(output).resolve()
    if output in (ROOT, ROOT.parent, Path('/')):
        raise ValueError('输出目录不能是项目根目录或其父目录。')
    if release and output == ROOT/'dist':
        raise ValueError('发布目录必须与本地演示 dist 分开，例如 publish。')
    if release and output.exists():
        allowed = {Path(path.strip('/'))/'index.html' for path in PUBLIC_PATHS} | DEMO_FILES
        allowed |= {Path('assets')/name for name in ASSETS + VIDEO_ASSETS}
        allowed |= {Path(path) for path in ['assets/public.css','assets/evening.png','404.html','robots.txt','sitemap.xml','llms.txt','.nojekyll']}
        if any(x.relative_to(output) not in allowed for x in output.rglob('*') if x.is_file()):
            raise ValueError('发布目录含演示或内部文件，请指定干净目录。')
    output.mkdir(parents=True, exist_ok=True)
    (output/'assets').mkdir(exist_ok=True)
    shutil.copy2(ROOT/'seo/public.css', output/'assets/public.css')
    # Concept visual is identified as artwork. No unlicensed product reference image in the public build.
    shutil.copy2(ROOT/'seo/assets/evening.png', output/'assets/evening.png')
    for name in ASSETS:
        shutil.copy2(ROOT/'seo/activities'/name, output/'assets'/name)
    build_videos(ROOT, output)
    p=config['product']; date=config['reviewed_date']; site=config['name']
    indexable=release and bool(origin)
    robots='index, follow, max-image-preview:large' if indexable else 'noindex, follow'
    absolute=lambda path:origin+base_path+path
    def with_base(content):
        return re.sub(r'((?:href|src)=")/(?!/)', lambda m:m.group(1)+base_path+'/', content) if base_path else content
    def link(path,label):return f'<a href="{E(path)}">{E(label)}</a>'
    identity='晚间留白，陪你发现属于自己的生活灵感。'
    nav=[('/', '首页'),(PRODUCT_PATH,'薰衣草精油'),(GUIDE_PATH,'新手指南'),(ACTIVITY_PATHS[0],'晚间活动'),(FAQ_PATH,'常见问题')]
    def page(path,title,desc,body,kind='WebPage',product=False):
        current=absolute(path)
        graph=[{'@type':'WebSite','@id':absolute('/#website'),'name':site,'url':absolute('/'),'inLanguage':'zh-CN','description':identity},
               {'@type':kind,'@id':current+'#page','url':current,'name':title,'description':desc,'inLanguage':'zh-CN','isPartOf':{'@id':absolute('/#website')}}]
        if product:
            graph[1]['mainEntity']={'@id':current+'#product'}
            graph.append({'@type':'Product','@id':current+'#product','name':p['name'],'alternateName':p['alternateName'],'brand':{'@type':'Brand','name':p['brand']},'category':p['category'],'size':p['size'],'description':p['description'],'url':current})
        if path != '/':
            graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':site,'item':absolute('/')},{'@type':'ListItem','position':2,'name':title.split('｜')[0],'item':current}]})
        schema=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')
        canon=f'<link rel="canonical" href="{E(current)}"><meta property="og:url" content="{E(current)}">' if origin else ''
        # Preview-only support for previous local demo bookmarks. Omitted from deployment builds.
        legacy='<script>if(["#plan","#website","#mini","#admin"].includes(location.hash))location.replace("/demo/"+location.hash);</script>' if path=='/' and not release else ''
        header=''.join(f'<a href="{u}"'+(' aria-current="page"' if u==path else '')+f'>{label}</a>' for u,label in nav)
        return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="robots" content="{robots}">
{canon}<meta property="og:type" content="website"><meta property="og:locale" content="zh_CN"><meta property="og:site_name" content="晚间留白"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<link rel="stylesheet" href="/assets/public.css"><script type="application/ld+json">{schema}</script>{legacy}</head>
<body><a class="skip" href="#main">跳至正文</a><header class="header"><a class="brand" href="/">晚间留白<small>EVENING, YOURS.</small></a><nav aria-label="主导航">{header}</nav></header><main id="main">{body}</main><footer class="footer"><p>{identity}</p><nav aria-label="页脚">{link(ABOUT_PATH,'关于晚间留白')}{link(PRODUCT_PATH,'认识精油')}{link(FAQ_PATH,'选购与使用问答')}</nav><p>产品价格与使用说明以店铺页面和商品标签为准。</p></footer></body></html>'''
    pages=consumer_pages(page,p,date)
    pages.update(activity_pages(page))
    for path,content in pages.items():
        target=output/path.strip('/')/'index.html' if path!='/' else output/'index.html'
        target.parent.mkdir(parents=True,exist_ok=True);target.write_text(with_base(content))
    build_demos(ROOT, output, base_path)
    (output/'404.html').write_text(with_base('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="robots" content="noindex"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>页面未找到｜晚间留白</title><link rel="stylesheet" href="/assets/public.css"><main class="container"><h1>页面未找到</h1><p>地址可能已变更，欢迎从产品资料页继续阅读。</p><a href="/">返回首页</a></main></html>'))
    # Do not robots-block demo URLs: noindex must remain readable if someone hosts dist accidentally.
    txt='User-agent: *\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n'
    if indexable:
        txt+='\nSitemap: '+absolute('/sitemap.xml')+'\n'
        (output/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+xml_escape(absolute(path))+'</loc></url>' for path in PUBLIC_PATHS)+'</urlset>\n')
    elif (output/'sitemap.xml').exists():
        (output/'sitemap.xml').unlink()
    (output/'robots.txt').write_text(txt)
    (output/'llms.txt').write_text('# 晚间留白\n\n> 晚间生活灵感、趣味自我探索与精油选购指南。独立网站，非阿芙官方网站或店铺。\n\n## 产品资料\n'+''.join(f'- [{label}]({absolute(path)})\n' for path,label in [(PRODUCT_PATH,p['name']),(GUIDE_PATH,'薰衣草精油选购指南'),(FAQ_PATH,'产品常见问题'),(ABOUT_PATH,'网站身份与信息来源'),(ACTIVITY_PATHS[0],'晚间灵感活动'),(ACTIVITY_PATHS[1],'今日五行留白签'),(ACTIVITY_PATHS[2],'晚间充电方式趣味测试')])+f'\n## 资料边界\n产品索引标注 10ml；资料核验日期 {date}。本站未核验实时价格、库存、单瓶销量或功效，不提供交易。页面正文与来源是信息依据。\n')
    (output/'.nojekyll').write_text('')
    return {'output':str(output),'pages':len(pages),'indexable':indexable,'origin':origin or None,'base_path':base_path,'sitemap':indexable}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--origin',default='')
    parser.add_argument('--output',type=Path,default=ROOT/'public')
    parser.add_argument('--release',action='store_true')
    parser.add_argument('--base-path',default=None)
    args=parser.parse_args()
    try:print(json.dumps(build(args.output,args.origin,args.release,args.base_path),ensure_ascii=False))
    except ValueError as exc:parser.error(str(exc))
