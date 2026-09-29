#!/usr/bin/env python3
"""Build crawlable HTML. No JavaScript execution or external packages required."""
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
PUBLIC_PATHS = ['/', PRODUCT_PATH, GUIDE_PATH, FAQ_PATH, ABOUT_PATH]
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
        allowed = {Path(path.strip('/'))/'index.html' for path in PUBLIC_PATHS}
        allowed |= {Path(path) for path in ['assets/public.css','assets/evening.png','404.html','robots.txt','sitemap.xml','llms.txt','.nojekyll']}
        if any(x.relative_to(output) not in allowed for x in output.rglob('*') if x.is_file()):
            raise ValueError('发布目录含演示或内部文件，请指定干净目录。')
    output.mkdir(parents=True, exist_ok=True)
    (output/'assets').mkdir(exist_ok=True)
    shutil.copy2(ROOT/'seo/public.css', output/'assets/public.css')
    # Concept visual is identified as artwork. No unlicensed product reference image in the public build.
    shutil.copy2(ROOT/'seo/assets/evening.png', output/'assets/evening.png')
    p=config['product']; date=config['reviewed_date']; site=config['name']
    indexable=release and bool(origin)
    robots='index, follow, max-image-preview:large' if indexable else 'noindex, follow'
    absolute=lambda path:origin+base_path+path
    def with_base(content):
        return re.sub(r'((?:href|src)=")/(?!/)', lambda m:m.group(1)+base_path+'/', content) if base_path else content
    def link(path,label):return f'<a href="{E(path)}">{E(label)}</a>'
    def refs():return f'''<section class="section" id="sources"><h2>信息来源与核验日期</h2><p class="small">资料核验：<time datetime="{date}">{date}</time>。网页展示可能变化，以下信息不替代商家当前标签和交易页面。</p><ol class="sources"><li><a href="{E(p['source'])}" rel="noopener" target="_blank">CNPP：阿芙精油热卖产品推荐</a>（页面标注 2025-10-24）。用于核对名称、10ml 规格与第三方历史展示价，不是官方实时售价或销量证明。</li><li><a href="https://www.tmtpost.com/3420263.html" rel="noopener" target="_blank">钛媒体：薰衣草精油与香水的产地报道</a>（2018-08-20）。仅用于历史背景，不外推当前销量、产地或批次。</li></ol></section>'''
    def related():return f'<div class="related">{link(PRODUCT_PATH,"查看阿芙薰衣草精油 10ml")}{link(GUIDE_PATH,"阅读薰衣草精油选购指南")}{link(FAQ_PATH,"查看产品常见问题")}</div>'
    identity='本站是晚间留白的独立产品资料与场景提案，非阿芙品牌官方网站，也不是交易店铺。'
    nav=[('/', '首页'),(PRODUCT_PATH,'产品资料'),(GUIDE_PATH,'选购指南'),(FAQ_PATH,'常见问题')]
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
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="robots" content="{robots}">
{canon}<meta property="og:type" content="website"><meta property="og:locale" content="zh_CN"><meta property="og:site_name" content="晚间留白"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<link rel="stylesheet" href="/assets/public.css"><script type="application/ld+json">{schema}</script>{legacy}</head>
<body><a class="skip" href="#main">跳至正文</a><header class="header"><a class="brand" href="/">晚间留白<small>EVENING, YOURS.</small></a><nav aria-label="主导航">{header}</nav></header><main id="main">{body}</main><footer class="footer"><p>{identity}</p><nav aria-label="页脚">{link(ABOUT_PATH,'关于本站与资料来源')}{link(PRODUCT_PATH,'产品规格')}{link(FAQ_PATH,'价格与购买问答')}</nav><p>概念图片不代表商品实际包装。产品的当前价格、库存和使用方式，以商家页面与商品标签为准。</p></footer></body></html>'''
    pages={}
    home=f'''<section class="hero"><img src="/assets/evening.png" width="1536" height="1024" fetchpriority="high" alt="薰衣草与无品牌精油瓶的晚间概念静物，并非阿芙实际包装"><div class="hero-content"><p class="eyebrow">LAVENDER / EVENING RITUAL</p><h1>阿芙薰衣草精油 10ml</h1><p class="headline">把夜晚，还给自己。</p><p class="intro">从认识一瓶精油开始，留一段自己的时间。这里整理产品规格、购买前要核对的信息，以及晚间留白的生活灵感。</p><div class="actions"><a class="btn" href="{PRODUCT_PATH}">了解产品规格</a><a class="btn" href="{GUIDE_PATH}">阅读选购指南</a></div></div><span class="caption">AI 概念视觉 · 非实际商品包装</span></section><section class="container"><p class="eyebrow">KNOW BEFORE YOU CHOOSE</p><h2>先了解，再选择。</h2><p class="lead">阿芙（AFU）薰衣草精油在公开商品索引中标注为 10ml。购买时需要核对同一规格、当前标签、店铺主体和实际结算价。</p><div class="grid section"><article class="box"><div class="number">01</div><h3>产品是什么？</h3><p>查看品牌、名称、容量与资料来源，将已知信息和待核验内容分开。</p><p>{link(PRODUCT_PATH,'查看产品事实表')}</p></article><article class="box"><div class="number">02</div><h3>怎么比较和选购？</h3><p>先确认产品类型与标签，再比较容量、购买成本、适用方式与售后。</p><p>{link(GUIDE_PATH,'查看四步选购指南')}</p></article><article class="box"><div class="number">03</div><h3>价格和使用怎么确认？</h3><p>集中解答历史参考价、使用说明、热销依据和购买渠道的问题。</p><p>{link(FAQ_PATH,'阅读常见问题')}</p></article></div></section><section class="band"><div class="container"><p class="eyebrow">A LITTLE SPACE FOR YOURSELF</p><h2>给晚间，一个简单的开始。</h2><div class="grid"><div><h3>合上电脑</h3><p>为今天的工作画一个句号。</p></div><div><h3>翻开一本书</h3><p>选择一件自己喜欢的小事。</p></div><div><h3>记下一个瞬间</h3><p>让日常留下一点自己的印记。</p></div></div><p class="reference">这些是生活方式灵感，不是精油功效或使用方法；产品使用遵循当前标签。</p></div></section>'''
    pages['/']=page('/','阿芙薰衣草精油 10ml：产品资料与选购指南｜晚间留白','了解阿芙（AFU）薰衣草精油 10ml 的规格、价格核验方法、选购要点与常见问题。晚间留白提供可追溯的独立产品资料，非品牌官方网站。',home)
    intro=f'<nav class="crumb" aria-label="面包屑">{link("/","首页")} / 产品资料</nav>'
    product=f'''<article class="container content">{intro}<p class="eyebrow">PRODUCT FACTS</p><h1>{E(p['name'])}</h1><p class="lead">{E(p['description'])}</p><p class="meta">资料整理：晚间留白 · 核验日期 <time datetime="{date}">{date}</time> · 独立产品资料</p><h2>产品规格一览</h2><dl class="facts"><div><dt>商品名称</dt><dd>{E(p['name'])}</dd></div><div><dt>英文品牌 / 别名</dt><dd>{E(p['alternateName'])}</dd></div><div><dt>品牌</dt><dd>{E(p['brand'])}</dd></div><div><dt>产品类型</dt><dd>{E(p['category'])}，具体以当前标签为准</dd></div><div><dt>标注净含量</dt><dd>10ml</dd></div><div><dt>产品参考价</dt><dd>¥99／10ml（项目策划设定，非实时售价）</dd></div><div><dt>当前售价与库存</dt><dd>本站未提供实时销售报价或库存，购买前向商家核对</dd></div><div><dt>用途与使用方法</dt><dd>按当前商品标签确认，不从产品名称推断用量或接触皮肤方式</dd></div></dl><section class="section"><h2>这款精油多少钱？</h2><p>本项目的产品参考价为 ¥99／10ml，用于宣发策划与演示测算。这是项目设定，不是已核验的店铺实时售价或购买承诺；实际支付金额、运费和优惠条件以商家结算页为准。</p><p>{link(FAQ_PATH+'#price','查看价格核验问答')}</p></section><section class="section"><h2>什么情况下值得进一步了解？</h2><p>如果你正在比较薰衣草精油，希望先看清规格、标签和店铺信息，可以将这款 10ml 产品作为了解对象。是否适合你，仍取决于你希望的使用方式和当前产品说明；本站没有开展实物试用或买家评价抽样，不给出功效、气味偏好或排名保证。</p></section><section class="section"><h2>购买前，确认这四项</h2><ol class="reading"><li>搜索完整名称「阿芙 薰衣草精油 10ml」，核对单瓶、套装与其他规格。</li><li>确认经营主体、授权信息、客服与退换货规则。</li><li>对照当前标签的使用方法和注意事项，不照搬其他精油的用法。</li><li>查看结算页实际金额，并确认发货与售后安排。</li></ol><div class="note">当前未核验官方购买链接，因此本站不设置销售或付款入口。核对店铺时不要只凭商品标题中的“官方”二字判断。</div></section>{refs()}{related()}</article>'''
    pages[PRODUCT_PATH]=page(PRODUCT_PATH,'阿芙薰衣草精油 10ml：规格、价格说明与选购要点｜晚间留白',p['description'],product,product=True)
    guide=f'''<article class="container content"><nav class="crumb" aria-label="面包屑">{link('/','首页')} / 选购指南</nav><p class="eyebrow">CHOOSING YOUR FIRST BOTTLE</p><h1>薰衣草精油怎么选？<br>从四项信息开始核对。</h1><p class="lead">比较薰衣草精油时，先确认产品类型、容量、标签说明和交易条件。以阿芙薰衣草精油 10ml 为例，可以把这些信息放在同一张核对表里，再决定是否购买。</p><p class="meta">资料整理：晚间留白 · <time datetime="{date}">{date}</time> · 产品信息核对指南</p><div class="contents"><strong>本页内容</strong><ul><li>{link('#type','先核对产品类型')}</li><li>{link('#size','比较同规格的实际成本')}</li><li>{link('#label','从标签确认适用方式')}</li><li>{link('#seller','核对店铺与售后')}</li></ul></div><section id="type" class="section"><h2>1. 先核对产品类型</h2><p>不要把名称中都带“薰衣草”的商品直接放在一起排名。比较前先看完整名称、标签和成分说明，确认它是单方精油、复方产品、基础油还是纯露。商品标题中的简称不足以确认使用方式。</p><p>本提案围绕的阿芙薰衣草精油规格为 10ml；相关套装中的销量和价格，需要与单瓶分开核对。</p></section><section id="size" class="section"><h2>2. 比较同规格的实际成本</h2><p>同容量商品可以先比较结算页价格，再看赠品和运费。不同容量需要单独记录。历史推荐价、活动预售价和到手价不是同一个口径，不能混用。</p><div class="table-wrap"><table><caption>购买前的信息核对表</caption><thead><tr><th>核对项</th><th>阿芙薰衣草精油 10ml 的资料状态</th><th>还需要确认什么</th></tr></thead><tbody><tr><td>规格</td><td>第三方索引标注 10ml</td><td>商家当前 SKU 与包装</td></tr><tr><td>价格</td><td>项目参考价 ¥99（策划设定）</td><td>当前结算价、运费和优惠条件</td></tr><tr><td>销量</td><td>没有已核实的实时单瓶销量</td><td>销量字段口径、时间与商品范围</td></tr><tr><td>使用方式</td><td>不凭名称推断</td><td>当前标签与说明</td></tr></tbody></table></div></section><section id="label" class="section"><h2>3. 从标签确认适用方式</h2><p>先确定自己希望怎样使用，再对照产品标签的适用范围和注意事项。不要把单方精油当成已经配好、可以直接使用的按摩油；本站不提供未经产品标签核实的配方、用量或直接上脸建议。</p></section><section id="seller" class="section"><h2>4. 核对店铺与售后</h2><p>保留商品链接和所选规格，核对店铺主体、授权与客服信息。购买前看清退换货条件，收到商品后核对实物标签与订单。若商品信息和宣传不一致，先向商家确认。</p></section><div class="note">这是一份购买信息核对方法，不是实测排名。本站没有实时销量、用户评分或功效证据，因此不使用“最好”“销量第一”等结论。</div>{refs()}{related()}</article>'''
    pages[GUIDE_PATH]=page(GUIDE_PATH,'薰衣草精油怎么选？规格、价格和标签核对指南｜晚间留白','薰衣草精油选购前应核对哪些信息？以阿芙薰衣草精油 10ml 为例，整理产品类型、容量、实际价格、标签说明、店铺主体与售后六类信息。',guide)
    questions=[('spec','阿芙薰衣草精油是多少毫升？','本次参考的公开商品索引标注为 10ml。本页讨论这一规格，购买时仍需确认商家的具体 SKU，避免选成套装或其他容量。'),('price','阿芙薰衣草精油 10ml 多少钱？','本项目设定的产品参考价为 ¥99／10ml，用于宣发策划与演示测算，不是 CNPP 报价或已核验的店铺实时售价。实际支付金额需要在商家结算页确认。本站没有销售或收款服务。'),('use','阿芙薰衣草精油应该怎么用？','具体适用方式、用量和注意事项以当前商品标签为准。不能仅凭“薰衣草精油”名称推断可以直接接触皮肤、加入设备或采用其他使用方式。'),('popular','这款是淘宝热销精油吗？','存在历史报道和第三方热卖推荐线索，但本站尚未核验实时淘宝单瓶销量。相关套装的销量不能当作 10ml 单瓶销量，历史报道不能当作今天的排名。'),('buy','在哪里能购买？','本站暂未核验可直接提供的官方商品链接。可按完整商品名称检索，再核对经营主体、授权信息、所选规格与售后条款，不只凭标题判断官方身份。'),('official','晚间留白是阿芙官方网站吗？','不是。本站是独立产品资料与场景提案，提及阿芙用于标识所讨论的产品，不代表品牌官方、授权经销关系或商家背书。'),('sleep','本站是否承诺助眠或其他功效？','本站没有核验该商品相应功效证据，不承诺改善睡眠、治疗失眠或其他健康效果。晚间阅读与留白只是生活方式灵感。')]
    faq=f'''<article class="container content"><nav class="crumb" aria-label="面包屑">{link('/','首页')} / 常见问题</nav><p class="eyebrow">CLEAR ANSWERS</p><h1>阿芙薰衣草精油<br>常见问题</h1><p class="lead">关于 10ml 规格、价格、使用信息和购买渠道，先分清哪些已经有资料，哪些还需要向商家核实。</p><p class="meta">资料核验：<time datetime="{date}">{date}</time></p><div class="faq">{''.join(f'<details open id="{key}"><summary>{q}</summary><p>{answer}</p></details>' for key,q,answer in questions)}</div>{refs()}{related()}</article>'''
    pages[FAQ_PATH]=page(FAQ_PATH,'阿芙薰衣草精油常见问题：价格、规格、使用与购买｜晚间留白','阿芙薰衣草精油 10ml 是什么规格、参考价如何理解、使用方式怎样确认、哪里购买？查看有来源的解答与尚待商家核验的信息。',faq)
    about=f'''<article class="container content"><nav class="crumb" aria-label="面包屑">{link('/','首页')} / 关于本站</nav><p class="eyebrow">ABOUT THIS INFORMATION</p><h1>关于晚间留白<br>与我们的产品资料</h1><p class="lead">{identity}我们希望帮助读者把商品名称、规格、价格和使用信息看清楚，再做自己的选择。</p><section class="section"><h2>本站提供什么？</h2><p>围绕阿芙薰衣草精油 10ml 整理可追溯的产品资料、购买信息核对指南和常见问题。没有实物试用、买家评分采集或实时交易接口的内容，会明确说明其边界。</p></section><section class="section"><h2>与品牌是什么关系？</h2><p>本项目没有提供品牌授权或经销资质证明，因此不自称阿芙官网、官方店铺或授权商家。品牌名称用于识别所讨论的商品，本站不代表商家作价格、库存或功效承诺。</p></section><section class="section"><h2>内容如何核验？</h2><p>产品信息以具名来源和实际读取日期记录。第三方展示价不当作实时价格，历史报道不当作当前销量，套装不当作单瓶。若后续取得当前标签、商家商品页或实测资料，应更新对应正文和资料日期。</p></section><section class="section"><h2>图片与个人信息</h2><p>站点主视觉为无品牌瓶身的 AI 概念静物，不代表实际商品包装。本站产品资料页面不设置登录、订单表单、追踪脚本或支付功能；具体部署服务仍可能产生基础访问日志。</p></section>{refs()}{related()}</article>'''
    pages[ABOUT_PATH]=page(ABOUT_PATH,'关于晚间留白：网站身份、产品资料与来源说明',identity,about,kind='AboutPage')
    for path,content in pages.items():
        target=output/path.strip('/')/'index.html' if path!='/' else output/'index.html'
        target.parent.mkdir(parents=True,exist_ok=True);target.write_text(with_base(content))
    (output/'404.html').write_text(with_base('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="robots" content="noindex"><meta name="viewport" content="width=device-width,initial-scale=1"><title>页面未找到｜晚间留白</title><link rel="stylesheet" href="/assets/public.css"><main class="container"><h1>页面未找到</h1><p>地址可能已变更，欢迎从产品资料页继续阅读。</p><a href="/">返回首页</a></main></html>'))
    # Do not robots-block demo URLs: noindex must remain readable if someone hosts dist accidentally.
    txt='User-agent: *\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n'
    if indexable:
        txt+='\nSitemap: '+absolute('/sitemap.xml')+'\n'
        (output/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+xml_escape(absolute(path))+'</loc></url>' for path in PUBLIC_PATHS)+'</urlset>\n')
    elif (output/'sitemap.xml').exists():
        (output/'sitemap.xml').unlink()
    (output/'robots.txt').write_text(txt)
    (output/'llms.txt').write_text('# 晚间留白\n\n> 独立产品资料与场景提案，非阿芙官方网站或交易店铺。\n\n## 产品资料\n'+''.join(f'- [{label}]({absolute(path)})\n' for path,label in [(PRODUCT_PATH,p['name']),(GUIDE_PATH,'薰衣草精油选购指南'),(FAQ_PATH,'产品常见问题'),(ABOUT_PATH,'网站身份与信息来源')])+f'\n## 资料边界\n产品索引标注 10ml；资料核验日期 {date}。本站未核验实时价格、库存、单瓶销量或功效，不提供交易。页面正文与来源是信息依据。\n')
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
