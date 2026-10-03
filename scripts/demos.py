"""Publish the explicitly requested static mini and admin experiences."""
from html import escape
from pathlib import Path
import shutil

DEMO_FILES={Path(p) for p in ['mini/index.html','admin/index.html','demo-assets/app.js','demo-assets/style.css']}

def build_demos(root, output, base=''):
    target=output/'demo-assets';target.mkdir(exist_ok=True)
    for name in ['app.js','style.css']:
        shutil.copy2(root/'seo/demos'/name,target/name)
    for route,title in [('mini','小程序体验'),('admin','管理后台演示')]:
        directory=output/route;directory.mkdir(exist_ok=True)
        nav=f'<a href="{base}/">官网</a><a href="{base}/activities/">晚间活动</a>'
        if route=='admin':nav+=f'<a href="{base}/mini/">小程序体验</a>'
        else:nav+=f'<a href="{base}/mini/" aria-current="page">小程序体验</a>'
        content=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="robots" content="noindex, follow"><meta name="description" content="晚间留白{title}，浏览器内运行的交互体验，数据仅保存在当前浏览器。"><title>{title} · 晚间留白</title><link rel="stylesheet" href="{base}/demo-assets/style.css"><script defer src="{base}/demo-assets/app.js"></script></head><body data-route="{route}" data-base="{escape(base)}"><header class="shell-header"><a class="wordmark" href="{base}/"><span class="brand-icon">✳</span><span>晚间留白<small>EVENING, YOURS.</small></span></a><nav aria-label="页面导航">{nav}</nav><span class="demo-label">{'H5 体验' if route=='mini' else '演示数据'}</span></header><main id="app"><noscript><h1>{title}</h1><p>请启用 JavaScript 体验本页面。</p></noscript></main><div id="toast" role="status" aria-live="polite"></div><dialog id="modal"><button class="close" aria-label="关闭弹窗">×</button><div id="modal-content"></div></dialog></body></html>'''
        (directory/'index.html').write_text(content)
