"""Original activity templates; shared by local preview and public site builds."""
ACTIVITY_PATHS=['/activities/','/activities/five-elements/','/activities/evening-personality/']
ASSETS=['activities.css','activities.js','model.mjs']

def teaser():
    return '''<section class="container"><p class="eyebrow">FIND YOUR EVENING</p><h2>今晚，你想怎样留白？</h2><div class="grid two"><article class="box"><p class="eyebrow">01 / 五行文化灵感</p><h3>抽一张今日五行留白签</h3><p>从一个意象开始，把金木水火土变成今晚的小小仪式。</p><p><a href="/activities/five-elements/">领取今日签 →</a></p></article><article class="box"><p class="eyebrow">02 / 趣味心理测试</p><h3>找到你的晚间充电方式</h3><p>6 道生活情境题，遇见此刻更喜欢的自己。</p><p><a href="/activities/evening-personality/">开始探索 →</a></p></article></div></section>'''

def activity_pages(page):
    pages={}
    hub='''<section class="container"><p class="eyebrow">EVENING LAB / 晚间灵感实验室</p><h1>先认识今晚的自己。</h1><p class="lead">不急着安排下一件事。选一个小活动，给夜晚一个属于自己的开场。</p></section>'''+teaser()+'''<section class="container"><h2>从灵感到一段自己的时间</h2><p>生成结果卡 → 选择一个晚间小行动 → 邀请朋友体验。对香气感兴趣时，再了解阿芙薰衣草精油 10ml 的规格与标签。</p><p class="reference">两个活动均为娱乐与生活方式灵感，不评价健康状态，也不据此判断产品适用性。无需登录，答案仅在当前页面使用。</p><p><a href="/products/afu-lavender-essential-oil-10ml/">查看产品资料</a></p></section>'''
    pages[ACTIVITY_PATHS[0]]=page(ACTIVITY_PATHS[0],'晚间灵感活动：五行留白签与晚间充电测试｜晚间留白','体验今日五行留白签和六题晚间偏好测试，生成分享卡与晚间小行动，进一步了解阿芙薰衣草精油资料。',hub)
    for kind,path,kicker,title,description,mark in [
      ('elements',ACTIVITY_PATHS[1],'DAILY FIVE ELEMENTS','今日五行留白签','金木水火土，五种生活意象。选一个此刻向往的画面，领取今天的留白灵感。','木'),
      ('personality',ACTIVITY_PATHS[2],'YOUR EVENING PERSONALITY','你的晚间充电方式','6 道情境题，约 1 分钟。看看此刻的你，更想怎样把夜晚还给自己。','月')]:
        disclaimer='五行文化主题娱乐，以所选意象与本地日期生成灵感，不作命理、体质或运势判断。' if kind=='elements' else '原创趣味心理测试，探索当下生活偏好；不是经验证的心理量表，不提供心理诊断或人格定论。'
        action='领取今日签' if kind=='elements' else '开始测试'
        method='你选择的意象决定主签；本地日期为五行灵感配色占比增加变化。同一天、同一意象的结果相同，占比仅为创意表达。' if kind=='elements' else '每题四个选项分别对应四种偏好，各计一票。最高票成为结果；并列时以你最近一道选择了并列类型的答案决定，并在结果中说明。结果不含常模、置信度或健康评分。'
        catalog='木 · 生长、火 · 微光、土 · 安放、金 · 留白、水 · 听雨。五种意象对应不同的晚间小行动。' if kind=='elements' else '静处收藏家：独处与低干扰；暖意联络员：分享与陪伴；灵感漫游者：新鲜与探索；日常筑岛师：有序与收尾。'
        body=f'''<link rel="stylesheet" href="/assets/activities.css"><div class="activity-shell" data-activity="{kind}"><section class="activity-hero container"><div><nav class="crumb" aria-label="面包屑"><a href="/activities/">晚间灵感活动</a> / {'五行留白签' if kind=='elements' else '晚间充电测试'}</nav><p class="eyebrow">{kicker}</p><h1>{title}</h1><p class="lead">{description}</p><p class="activity-tag">无需登录 · 免费体验 · 可保存分享卡</p></div><div class="orbit" aria-hidden="true"><span>{mark}</span><i>金</i><i>木</i><i>水</i><i>火</i><i>土</i></div></section><section class="container activity-stage"><div id="experience" class="experience"><p class="eyebrow">A MOMENT FOR YOURSELF</p><h2>为今晚，留一点空白。</h2><p>{disclaimer}</p><button type="button" class="btn" id="start" hidden>{action} →</button><noscript><p>互动需要启用 JavaScript。你仍可阅读下方玩法说明和产品资料。</p></noscript></div><p class="reference">{disclaimer}答案只用于当前页面计算，刷新即清除，不上传出生信息或答题记录。保存或分享由你主动操作。</p></section><section class="container activity-explainer"><details><summary>这份结果是怎样生成的？</summary><p>{method}</p></details><details><summary>有哪些结果？</summary><p>{catalog}</p></details><p class="reference">活动由晚间留白独立制作。产品了解入口为阿芙薰衣草精油 10ml 资料页；本活动不代表品牌官方，也不承诺香气能改变运势、性格或健康。</p></section></div><script type="module" src="/assets/activities.js"></script>'''
        pages[path]=page(path,title+'：发现今晚的灵感｜晚间留白',description+' '+disclaimer,body)
    return pages
