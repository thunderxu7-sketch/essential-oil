# 晚间留白 · 生活灵感与精油选购

面向消费者的晚间生活灵感、趣味活动与阿芙薰衣草精油 10ml 介绍。
本项目非品牌官方网站或销售店铺，不提供价格、库存、疗效或官方身份承诺。

网站：https://thunderxu7-sketch.github.io/essential-oil/

## 开发与发布

无需第三方依赖，Python 3.12 或更高版本即可生成静态 HTML：

```sh
python3 scripts/build_seo.py --release --output public
python3 scripts/check_pages.py
```

向 main 分支推送后，GitHub Actions 自动构建、校验并部署 public 目录。
公开仓库包含消费者网站与静态小程序 / 后台演示源文件，不包含内部策划文档、真实用户数据或第三方商品参考图。

- seo/site.json：域名、项目路径和产品事实。
- seo/public.css：样式。
- seo/assets/evening.png：AI 概念静物，非真实产品包装。
- scripts/build_seo.py：静态页面、结构化数据、站点地图与资料索引生成。
- scripts/check_pages.py：校验项目子路径、资源、链接与搜索元数据。

## 搜索收录

消费者内容页均包含正文并允许收录；小程序与后台演示为 noindex，不进入 sitemap。canonical 和 sitemap 使用正式 Pages 项目网址。
站点地图：https://thunderxu7-sketch.github.io/essential-oil/sitemap.xml

项目目录下的 robots.txt 不是域名根目录 robots.txt，不能控制整个 github.io 站点的爬虫规则；不修改账号下其他网站的根路径配置。可在 Search Console / Bing Webmaster Tools 验证项目网址后直接提交上述站点地图。
llms.txt 仅为可选资料导航，不保证 AI 搜索引用。没有提交搜索引擎所有权验证或宣称已收录。

GitHub Pages 不执行 _headers / _redirects。页面自带正确的 meta robots 和 canonical，404.html 由 Pages 用于未找到的路径。

## 内容维护

具名来源和资料核验日期保留在正文。修改商品信息时同步核对正文、schema 和数据来源。
没有真实报价和评价时，不添加 Offer、AggregateRating 或 Review 标记；Product 用于实体描述，不宣称商品富摘要资格。

## 晚间引流活动

- `/activities/`：活动入口。
- `/activities/five-elements/`：今日五行留白签，借鉴五行校准项目的每日主题与分享卡体验，采用原创意象规则。
- `/activities/evening-personality/`：六题趣味晚间偏好测试，非心理诊断。

支持结果卡 PNG 下载、邀请文案复制、重测、产品及另一个活动跳转。无账号、追踪采集或答题上传；UTM 仅标识链接来源，并不代表统计服务已接入。活动说明、玩法规则与结果类型在静态 HTML 内可读取。

活动资源位于 `seo/activities/`，模板为 `scripts/activities.py`；使用 `node scripts/check_activities.mjs` 校验计分与每日分布规则。

公开内容由 `scripts/consumer_pages.py` 生成。首页聚焦生活场景与活动参与，产品页提供规格、参考价及选购入口；资料来源在可展开区，网站身份与隐私在关于页面。

## 小程序与后台

- https://thunderxu7-sketch.github.io/essential-oil/mini/
- https://thunderxu7-sketch.github.io/essential-oil/admin/

GitHub Pages 上的浏览器交互演示，不执行服务器逻辑或真实支付。演示订单、权益、内容编辑与活动状态存储在当前浏览器；同一浏览器的页面共享演示状态，不跨用户共享。后台无需登录，因为不连接真实业务数据；不得将真实客户、凭据或内部数据填入演示。

`seo/demos/` 为独立体验资源，`scripts/demos.py` 生成两个入口，不发布内部策划或原始演示中的非授权参考图。

## 首页科普视频与直播头像

首页 `/#learn` 展示三条经原页面核对的公开 B 站视频，保留封面、作者头像、署名和原视频入口。视频不复制到本仓库；点击后按需加载官方嵌入播放器，平台或网络限制导致不可播放时可前往原站。

- 数据：`seo/videos/videos.json`，包含原视频标题、BV 号、作者主页和头像。标题和署名以原平台为准，不代表品牌合作或作者授权代言。
- 后台“视频与作者”：设置直播间和状态截止时间、预览直播头像圈、导出 `videos.json`。只接受有效的 B 站直播间 HTTPS 链接，预览最长 24 小时，到期恢复普通头像；没有确认开播的作者不标注“直播中”。
- 保存仅同步同一浏览器的首页预览，首页显示预览提示；对所有访客生效需把导出文件替换为 `seo/videos/videos.json` 后提交部署。没有连接平台开播接口，也没有服务器发布接口。生产初始配置均不启用直播。
- 校验：`node scripts/check_videos.mjs` 验证来源字段、直播链接、有效期与状态覆盖规则。

## 移动端布局

官网、小程序 H5、后台与两个活动均提供手机布局。已在浏览器 320、390、430 像素宽度检查五个入口，无整页横向溢出；官网的产品、指南、问答、关于和活动入口也通过 320 像素检查。

小程序在手机上使用整页滚动，底部导航固定并为内容预留空间；桌面保留模拟手机外框。后台五个菜单换行展示，表单与视频管理按窄屏排布，宽表格只在自身容器内横向滚动。活动按钮、视频关闭按钮与主要导航扩大触控区域；表单文字采用 16px，页面包含安全区设置。

浏览器验证了小程序场景与结果切换、七日格子、后台活动编辑弹窗、内容表格、五行结果与完整六题心理测试。此验证为响应式浏览器检查，未宣称实机平台认证。
