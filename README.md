# 晚间留白 · 产品资料网站

阿芙薰衣草精油 10ml 的独立产品资料、选购指南与常见问题。
本项目非品牌官方网站或销售店铺，不提供价格、库存、疗效或官方身份承诺。

网站：https://thunderxu7-sketch.github.io/essential-oil/

## 开发与发布

无需第三方依赖，Python 3.12 或更高版本即可生成静态 HTML：

```sh
python3 scripts/build_seo.py --release --output public
python3 scripts/check_pages.py
```

向 main 分支推送后，GitHub Actions 自动构建、校验并部署 public 目录。
公开仓库只包含产品网站源文件，不包含内部策划、模拟后台、小程序数据或第三方商品参考图。

- seo/site.json：域名、项目路径和产品事实。
- seo/public.css：样式。
- seo/assets/evening.png：AI 概念静物，非真实产品包装。
- scripts/build_seo.py：静态页面、结构化数据、站点地图与资料索引生成。
- scripts/check_pages.py：校验项目子路径、资源、链接与搜索元数据。

## 搜索收录

所有公开 HTML 均包含正文并允许收录。canonical 和 sitemap 使用正式 Pages 项目网址。
站点地图：https://thunderxu7-sketch.github.io/essential-oil/sitemap.xml

项目目录下的 robots.txt 不是域名根目录 robots.txt，不能控制整个 github.io 站点的爬虫规则；不修改账号下其他网站的根路径配置。可在 Search Console / Bing Webmaster Tools 验证项目网址后直接提交上述站点地图。
llms.txt 仅为可选资料导航，不保证 AI 搜索引用。没有提交搜索引擎所有权验证或宣称已收录。

GitHub Pages 不执行 _headers / _redirects。页面自带正确的 meta robots 和 canonical，404.html 由 Pages 用于未找到的路径。

## 内容维护

具名来源和资料核验日期保留在正文。修改商品信息时同步核对正文、schema 和数据来源。
没有真实报价和评价时，不添加 Offer、AggregateRating 或 Review 标记；Product 用于实体描述，不宣称商品富摘要资格。
