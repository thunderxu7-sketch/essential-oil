"""Consumer pages shared by preview and public builds."""
from html import escape as E
from activities import teaser
from videos import video_section


def consumer_pages(page, product, date):
    product_path = '/products/afu-lavender-essential-oil-10ml/'
    guide = '/guides/choosing-lavender-essential-oil/'
    faq = '/faq/'
    name = E(product['name'])
    source = f'''<details class="source-details"><summary>产品信息来源</summary><p>商品名称与 10ml 规格参考 <a href="{E(product['source'])}" target="_blank" rel="noopener">CNPP 商品介绍</a>，阅读日期：{date}。该来源不是实时店铺报价；¥99 为本站设定的参考价格。当前包装、成分表与使用说明请到店铺查看。</p></details>'''
    crumb = lambda label: f'<nav class="crumb" aria-label="面包屑"><a href="/">首页</a> / {label}</nav>'
    pages = {}

    home = f'''<section class="hero consumer-hero">
      <img src="/assets/evening.png" width="1536" height="1024" fetchpriority="high" alt="薰衣草与无品牌瓶子的概念场景，非阿芙商品包装">
      <div class="hero-content"><p class="eyebrow">精油选购 · 晚间活动</p><h1>把夜晚，<br>还给自己。</h1>
        <p class="headline">想试试薰衣草精油？先看清楚再选。</p>
        <p class="intro">这里介绍阿芙薰衣草精油 10ml，整理选购时要问的问题，也准备了两个可以和朋友一起玩的晚间小活动。</p>
        <div class="actions"><a class="btn" href="{product_path}">查看产品与参考价 →</a><a class="btn hero-secondary" href="/activities/">去玩晚间活动</a></div>
      </div><span class="caption">AI 氛围图 · 图中瓶子非阿芙商品包装</span>
    </section>
    <section class="band"><div class="container featured-product">
      <div><p class="eyebrow">产品介绍</p><h2>{name}</h2><p>阿芙 AFU 的薰衣草单方精油。比较商品时，请确认是 10ml 单瓶，还是包含其他产品的套装。</p>
        <div class="product-tags"><span>阿芙 AFU</span><span>薰衣草单方精油</span><span>10ml 单瓶</span></div>
      </div><div class="product-summary"><p class="small">本站参考价</p><p class="consumer-price">¥99 <small>/ 10ml</small></p>
        <p class="reference">按参考价折算 ¥9.90 / ml。<br>实际支付金额、优惠与运费请查看店铺结算页。</p>
        <div class="actions"><a class="btn" href="{product_path}">查看规格 →</a><a class="btn light" href="{guide}">第一次怎么选</a></div>
      </div>
    </div></section>'''
    home += video_section()
    home += teaser()
    home += f'''<section class="container home-help"><h2>买之前，你可能想问</h2><div class="help-links">
      <a href="{faq}#price"><strong>¥99 是现在的到手价吗？</strong><span>它是参考价，实际以店铺结算页为准。 →</span></a>
      <a href="{guide}#label"><strong>买回来应该怎么用？</strong><span>先确认这一款的适用方式、用量和稀释要求。 →</span></a>
    </div></section>'''
    pages['/'] = page('/', '晚间留白｜阿芙薰衣草精油 10ml、选购指南与晚间活动', '了解阿芙薰衣草精油 10ml 和参考价 ¥99，查看选购问题、香气科普视频，参加五行主题签和六题晚间偏好测试。', home)

    body = f'''<article class="container">{crumb('薰衣草精油')}
      <div class="product-intro"><div><p class="eyebrow">产品规格</p><h1>阿芙薰衣草精油</h1><p class="lead">10ml 单瓶。先确认商品规格，再问清楚你打算采用的用法。</p>
        <div class="product-tags"><span>阿芙 AFU</span><span>薰衣草单方精油</span><span>10ml</span></div>
        <div class="actions"><a class="btn" href="#questions">看看该问客服什么 →</a><a class="btn light" href="{faq}#buy">在哪里购买</a></div>
      </div><aside class="product-summary"><p class="small">本站参考价 · 10ml 单瓶</p><p class="consumer-price">¥99</p><p>折合 ¥9.90 / ml</p><p class="reference">这是参考价格，不代表店铺当前到手价。实际优惠、运费和库存请到店铺确认。</p></aside></div>
      <section class="section content"><h2>商品信息</h2><dl class="facts">
        <div><dt>商品名称</dt><dd>{name}</dd></div><div><dt>品牌</dt><dd>阿芙 AFU</dd></div>
        <div><dt>产品类型</dt><dd>薰衣草单方精油</dd></div><div><dt>规格</dt><dd>10ml / 瓶</dd></div>
        <div><dt>参考价格</dt><dd>¥99，按此折算 ¥9.90 / ml</dd></div><div><dt>包装与用法</dt><dd>查看店铺当前商品图、标签与随附说明</dd></div>
      </dl>{source}</section>
      <section id="questions" class="section"><h2>把这三个问题问清楚</h2><p class="reference">可以将下面的问题发给你准备购买的店铺客服。</p><ol class="buyer-questions">
        <li><h3>我选的这一项包含什么？</h3><p>“这个规格是 10ml 单瓶吗？有没有其他产品或赠品？能否发当前包装正反面的照片？”</p></li>
        <li><h3>能不能用于我准备的场景？</h3><p>“我准备搭配这款设备或按这个方式使用，请问是否适用？标签上的用量、稀释要求和限制是什么？”</p></li>
        <li><h3>收到后怎样核对？</h3><p>“产品的保质期、开封后保存说明是什么？如果规格或包装与订单不一致，怎样处理？”</p></li>
      </ol></section>
      <section class="section product-cta"><h2>继续了解</h2><p>第一次买，可以按类型、价格、说明和售后逐项检查。</p><div class="actions"><a class="btn" href="{guide}">阅读四步选购指南 →</a><a class="btn light" href="{faq}">查看价格与购买问答</a></div></section>
    </article>'''
    pages[product_path] = page(product_path, '阿芙薰衣草精油 10ml｜规格、参考价 ¥99 与选购问题｜晚间留白', product['description'], body, product=True)

    body = f'''<article class="container content">{crumb('新手指南')}<p class="eyebrow">新手选购</p><h1>第一次选精油，<br>检查这四件事。</h1><p class="lead">先确认你要买的产品类型，再比较规格、用法和售后。下面以阿芙薰衣草精油 10ml 为例。</p>
      <div class="contents"><strong>四步检查</strong><ul><li><a href="#type">看产品类型</a></li><li><a href="#size">比较规格与价格</a></li><li><a href="#label">问清使用说明</a></li><li><a href="#seller">确认店铺与售后</a></li></ul></div>
      <section id="type" class="section"><h2>1. 商品全名是什么？</h2><p>别只看“薰衣草”三个字。单方精油、复方精油、基础油和纯露是不同类型；看完整名称和成分表，确认自己选的是哪一种。</p><p>本站介绍的是阿芙薰衣草单方精油 10ml，不是按摩油或纯露。</p></section>
      <section id="size" class="section"><h2>2. 比较的是同一规格吗？</h2><p>确认单瓶还是套装，再比较结算金额、赠品和运费。容量不同时，可将金额除以毫升数，便于比较。</p><div class="guide-product"><h3>阿芙薰衣草精油 · 10ml</h3><p>本站参考价 <strong>¥99</strong>，折合 <strong>¥9.90 / ml</strong>。这个折算不包含运费，也不代表当前店铺报价。</p><a href="{product_path}">查看商品信息 →</a></div></section>
      <section id="label" class="section"><h2>3. 准备怎么用？</h2><p>把自己的具体场景告诉客服：准备搭配什么设备、采用什么方式。请对方确认这一款是否适用，并提供当前使用说明。</p><p>重点查看适用方式、用量、是否需要稀释、使用限制和保存要求。不确定的内容先问清楚，再决定是否购买。</p></section>
      <section id="seller" class="section"><h2>4. 出现问题找谁？</h2><p>检查店铺经营主体、品牌授权和退换货规则。下单前确认发货安排及运费，收货后核对规格、包装和标签。</p></section>
      <div class="actions"><a class="btn" href="{product_path}">查看产品规格</a><a class="btn light" href="{faq}#buy">查看购买方式</a></div>
    </article>'''
    pages[guide] = page(guide, '薰衣草精油怎么选？四步新手选购指南｜晚间留白', '以阿芙薰衣草精油 10ml 为例，检查商品类型、同规格价格、使用说明与售后。本站参考价 ¥99，实际以店铺为准。', body)

    answers = [
        ('spec', '这瓶精油是多少毫升？', '这里介绍的是阿芙薰衣草精油 10ml 单瓶。下单时请确认所选规格，单瓶和套装可能有不同的价格与内容。'),
        ('price', '参考价 ¥99 是到手价吗？', '¥99 是本站设定的参考价格，不是实时店铺报价。实际优惠、运费和支付金额以结算页为准。按这个参考价折算，每毫升为 ¥9.90。'),
        ('use', '在哪里看具体用法？', '请查看店铺当前商品标签和使用说明，确认适用方式、用量、稀释要求及限制。可以先向客服说明自己打算怎么用，请对方核对这一款是否适用。'),
        ('buy', '在哪里购买？', '可在常用购物平台搜索“阿芙 薰衣草精油 10ml”，核对店铺主体、品牌授权、商品规格与售后规则后下单。本站介绍产品，不办理销售或收款。'),
        ('test', '测试结果是在推荐适合我的精油吗？', '不是。两个活动提供晚间偏好和小行动建议，不用于判断某款精油是否适合你。购买仍需要结合实际使用场景与商品说明。'),
        ('sleep', '精油可以治疗失眠吗？', '精油不作为失眠治疗方式。本站的阅读、音乐等建议是生活活动；涉及健康问题时，请寻求专业帮助。'),
        ('official', '晚间留白是阿芙官网吗？', '不是。晚间留白是独立生活方式网站，不是阿芙官方网站或授权店铺。品牌名称用于介绍对应产品。'),
    ]
    body = f'''<article class="container content">{crumb('常见问题')}<p class="eyebrow">价格 · 使用 · 活动</p><h1>常见问题</h1><p class="lead">关于这瓶精油、购买方式和两个活动的说明。</p><div class="faq">{''.join(f'<details id="{key}" {"open" if key in ("price", "buy") else ""}><summary>{q}</summary><p>{answer}</p></details>' for key, q, answer in answers)}</div><div class="actions"><a class="btn" href="{product_path}">查看阿芙薰衣草精油</a><a class="btn light" href="/activities/">参加晚间活动</a></div></article>'''
    pages[faq] = page(faq, '精油与晚间活动常见问题｜价格、使用和购买｜晚间留白', '阿芙薰衣草精油 10ml 的参考价格、购买方式、使用说明，以及五行签和晚间偏好测试的常见问题。', body)

    body = f'''<article class="container content">{crumb('关于晚间留白')}<h1>关于晚间留白</h1><p class="lead">这里整理精油选购信息和香气科普视频，也提供两个免费的晚间小活动。</p>
      <section class="section"><h2>网站与产品的关系</h2><p>晚间留白是独立生活方式网站，不是阿芙官方网站或授权销售店铺。本站介绍阿芙薰衣草精油 10ml，购买请到你确认的店铺完成。</p><p>¥99 为本站设定的参考价格。商品名称与规格的来源见下方，当前包装、成分和用法请向店铺核对。</p>{source}<p class="reference">首页主视觉为 AI 氛围图，图中无品牌瓶子不代表阿芙商品包装。其他商品卡使用规格文字，不展示模拟包装。</p></section>
      <section class="section"><h2>活动怎样给出结果？</h2><p>五行签根据你选的画面提供一张主题卡，不计算命理或五行属性。六题晚间偏好测试按本次选择给出建议，不是心理诊断或固定性格分类。</p><p>活动无需登录或提交手机号、出生信息。答案只在当前页面使用，刷新即清除。下载和分享由你主动选择。网站托管服务可能保留基础访问日志。</p></section>
      <section class="section"><h2>视频来源与隐私</h2><p>视频、封面与作者头像来自哔哩哔哩公开页面，保留作者署名和原视频链接，不表示作者与品牌有合作关系。点击观看后才加载第三方播放器，播放和创作者主页适用原平台的隐私规则。</p></section>
      <div class="actions"><a class="btn" href="/activities/">查看两个活动 →</a><a class="btn light" href="{product_path}">查看产品介绍</a></div>
    </article>'''
    pages['/about/'] = page('/about/', '关于晚间留白｜产品信息来源、活动规则与隐私说明', '晚间留白是介绍阿芙薰衣草精油、香气科普与晚间活动的独立网站。查看商品信息来源、活动规则和隐私说明。', body, kind='AboutPage')
    return pages
