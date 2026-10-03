"""Original activity templates shared by preview and public builds."""
ACTIVITY_PATHS = ['/activities/', '/activities/five-elements/', '/activities/evening-personality/']
ASSETS = ['activities.css', 'activities.js', 'model.mjs']


def teaser():
    return '''<section class="container activity-teaser"><p class="eyebrow">两个免费小活动</p><h2>今晚有十分钟，你想怎么过？</h2><div class="grid two">
      <article class="box"><p class="eyebrow">选一个画面 · 约 30 秒</p><h3>领一张五行主题签</h3><p>绿意、灯光、角落、白纸、音乐。选一个喜欢的画面，拿到一张签和具体行动。</p><p><a href="/activities/five-elements/">选画面，领签 →</a></p></article>
      <article class="box"><p class="eyebrow">回答六题 · 约 1 分钟</p><h3>看看今晚的偏好</h3><p>现在更想独处、聊天、尝试新事，还是整理收尾？用六个生活场景看看你的选择。</p><p><a href="/activities/evening-personality/">开始晚间偏好测试 →</a></p></article>
    </div></section>'''


def activity_pages(page):
    pages = {}
    hub = '''<section class="container"><h1>晚间小活动</h1><p class="lead">两个玩法，都不需要登录。可以自己玩，也可以把结果卡发给朋友。</p></section>''' + teaser() + '''<section class="container activity-how"><h2>拿到结果后</h2><ol><li>看看卡片上的建议，想做就试试，不需要打卡。</li><li>保存卡片，或复制链接邀请朋友一起玩。</li><li>想换个选择，可以重新领取或答题。</li></ol><p class="reference">活动免费，仅供娱乐与偏好探索。答案只在当前页面使用，刷新即清除。结果不用于推荐适合你的精油。</p></section>'''
    pages[ACTIVITY_PATHS[0]] = page(ACTIVITY_PATHS[0], '晚间活动｜五行主题签与六题偏好测试｜晚间留白', '免费体验五行主题签和六题晚间偏好测试，查看具体行动建议，保存结果卡或邀请朋友参加。无需登录。', hub)
    for kind, path, title, description, mark in [
        ('elements', ACTIVITY_PATHS[1], '今日五行主题签', '选一个你喜欢的画面，领取对应的五行主题签。每张签是一件小事和三步建议，想做再开始。', '木'),
        ('personality', ACTIVITY_PATHS[2], '今晚，你更想怎么过？', '六个生活场景，约一分钟。看看本次选择更偏向独处、陪伴、探索还是整理。', '问'),
    ]:
        is_elements = kind == 'elements'
        disclaimer = '五行文化主题娱乐，不计算命理或五行属性。' if is_elements else '原创趣味偏好测试，不作心理诊断或固定性格分类。'
        invitation = '从绿意、灯光、角落、白纸和音乐中选一个画面。' if is_elements else '按今晚的想法作答，不需要选“应该做”的事。'
        action = '选画面，领签' if is_elements else '开始六题测试'
        stage_title = '你喜欢哪一个画面？' if is_elements else '先想想今晚的自己'
        method = '所选画面直接对应一张主题签，日期只标记领取时间。绿意对应木、灯光对应火、熟悉的角落对应土、白纸对应金、音乐对应水。结果不包含属性占比或命理推断。' if is_elements else '每道题的选项分别对应独处、陪伴、探索和整理四种行动偏好，各计一票。最高票成为结果；并列时采用最近一道选中的并列类型。结果会列出本次回答作为依据，不代表固定性格或专业测评。'
        catalog = '木：试一件新事；火：和人聊聊；土：收好明天；金：清一小处；水：听完一首。' if is_elements else '安静独处型、朋友陪伴型、新鲜探索型、整理收尾型。这些名称只概括本次选择。'
        body = f'''<link rel="stylesheet" href="/assets/activities.css"><div class="activity-shell" data-activity="{kind}">
          <section class="activity-hero container"><div><nav class="crumb" aria-label="面包屑"><a href="/activities/">晚间活动</a> / {'五行主题签' if is_elements else '六题偏好测试'}</nav><h1>{title}</h1><p class="lead">{description}</p><p class="activity-tag">无需登录 · 免费 · 可保存结果卡</p></div><div class="orbit" aria-hidden="true"><span>{mark}</span><i>金</i><i>木</i><i>水</i><i>火</i><i>土</i></div></section>
          <section class="container activity-stage"><div id="experience" class="experience"><h2>{stage_title}</h2><p>{invitation}</p><button type="button" class="btn" id="start" hidden>{action} →</button><noscript><p>互动需要启用 JavaScript。下方可以阅读玩法与结果类型。</p></noscript></div><p class="reference">{disclaimer} 答案刷新即清除。</p></section>
          <section class="container activity-explainer"><details><summary>结果是怎样得出的？</summary><p>{method}</p></details><details><summary>有哪些结果？</summary><p>{catalog}</p></details><p class="reference"><a href="/about/">查看网站与隐私说明</a></p></section>
        </div><script type="module" src="/assets/activities.js"></script>'''
        pages[path] = page(path, title + '｜晚间留白', description + ' ' + disclaimer, body)
    return pages
