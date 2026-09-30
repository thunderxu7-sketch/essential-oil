"""Original activity templates; shared by local preview and public site builds."""
ACTIVITY_PATHS=['/activities/','/activities/five-elements/','/activities/evening-personality/']
ASSETS=['activities.css','activities.js','model.mjs']

def teaser():
    return '''<section class="container"><p class="eyebrow">FIND YOUR EVENING</p><h2>今晚，你想怎样留白？</h2><div class="grid two"><article class="box"><p class="eyebrow">01 / 五行文化灵感</p><h3>抽一张今日五行留白签</h3><p>从一个意象开始，把金木水火土变成今晚的小小仪式。</p><p><a href="/activities/five-elements/">领取今日签 →</a></p></article><article class="box"><p class="eyebrow">02 / 趣味心理测试</p><h3>找到你的晚间充电方式</h3><p>6 道生活情境题，遇见此刻更喜欢的自己。</p><p><a href="/activities/evening-personality/">开始探索 →</a></p></article></div></section>'''

def activity_pages(page):
    pages={}
    hub='''<section class="container"><p class="eyebrow">YOUR EVENING / 今晚属于你</p><h1>今晚，和自己待一会儿。</h1><p class="lead">一张签，六道题。没有标准答案，只有你此刻喜欢的样子。</p></section>'''+teaser()+'''<section class="container"><h2>把喜欢的小事，留给今晚。</h2><div class="grid"><article class="box"><h3>发现一点自己</h3><p>跟着第一直觉选择，遇见一个属于今晚的灵感。</p></article><article class="box"><h3>挑一件小事去做</h3><p>从结果卡里选一个行动。读书、听歌，或整理一个角落。</p></article><article class="box"><h3>也邀请朋友来看看</h3><p>保存你的卡片，和朋友聊聊彼此喜欢的晚间方式。</p></article></div><div class="actions"><a class="btn light" href="/products/afu-lavender-essential-oil-10ml/">认识阿芙薰衣草精油 →</a></div><p class="reference">活动免费，无需登录。仅供娱乐与自我探索，答案刷新即清除。</p></section>'''
    pages[ACTIVITY_PATHS[0]]=page(ACTIVITY_PATHS[0],'晚间灵感活动：五行留白签与晚间充电测试｜晚间留白','体验今日五行留白签和六题晚间偏好测试，生成分享卡与晚间小行动，发现适合自己的晚间小行动，并认识阿芙薰衣草精油。',hub)
    for kind,path,kicker,title,description,mark in [
      ('elements',ACTIVITY_PATHS[1],'DAILY FIVE ELEMENTS','今日五行留白签','金木水火土，五种生活意象。选一个此刻向往的画面，领取今天的留白灵感。','木'),
      ('personality',ACTIVITY_PATHS[2],'YOUR EVENING PERSONALITY','你的晚间充电方式','6 道情境题，约 1 分钟。看看此刻的你，更想怎样把夜晚还给自己。','月')]:
        disclaimer='五行文化主题娱乐，签文供生活灵感参考。' if kind=='elements' else '趣味自我探索，结果描述当下偏好，不作心理诊断。'
        invitation='绿意、微光、留白……选一个喜欢的画面，看看今天是哪一张签。' if kind=='elements' else '不用想太久，跟着第一直觉，遇见今晚的自己。'
        action='领取今日签' if kind=='elements' else '开始测试'
        method='你选择的意象决定主签；本地日期为五行灵感配色占比增加变化。同一天、同一意象的结果相同，占比仅为创意表达。' if kind=='elements' else '每题四个选项分别对应四种偏好，各计一票。最高票成为结果；并列时以你最近一道选择了并列类型的答案决定，并在结果中说明。每次回答都可能不同，选择最贴近此刻的答案就好。'
        catalog='木 · 生长、火 · 微光、土 · 安放、金 · 留白、水 · 听雨。五种意象对应不同的晚间小行动。' if kind=='elements' else '静处收藏家：独处与低干扰；暖意联络员：分享与陪伴；灵感漫游者：新鲜与探索；日常筑岛师：有序与收尾。'
        body=f'''<link rel="stylesheet" href="/assets/activities.css"><div class="activity-shell" data-activity="{kind}"><section class="activity-hero container"><div><nav class="crumb" aria-label="面包屑"><a href="/activities/">晚间灵感活动</a> / {'五行留白签' if kind=='elements' else '晚间充电测试'}</nav><p class="eyebrow">{kicker}</p><h1>{title}</h1><p class="lead">{description}</p><p class="activity-tag">无需登录 · 免费体验 · 可保存分享卡</p></div><div class="orbit" aria-hidden="true"><span>{mark}</span><i>金</i><i>木</i><i>水</i><i>火</i><i>土</i></div></section><section class="container activity-stage"><div id="experience" class="experience"><p class="eyebrow">A MOMENT FOR YOURSELF</p><h2>为今晚，留一点空白。</h2><p>{invitation}</p><button type="button" class="btn" id="start" hidden>{action} →</button><noscript><p>互动需要启用 JavaScript。你可以先阅读下方活动介绍，或认识薰衣草精油。</p></noscript></div><p class="reference">{disclaimer} 无需登录，答案刷新即清除。</p></section><section class="container activity-explainer"><details><summary>关于这张结果卡</summary><p>{method}</p></details><details><summary>有哪些结果？</summary><p>{catalog}</p></details><p class="reference">结果只是一份晚间灵感，请按自己的喜好选择行动。<a href="/about/">了解活动与隐私</a></p></section></div><script type="module" src="/assets/activities.js"></script>'''
        pages[path]=page(path,title+'：发现今晚的灵感｜晚间留白',description+' '+disclaimer,body)
    return pages
