"""Static, attributed video recommendations; original media stays on Bilibili."""
from html import escape as E
from pathlib import Path
import json
import shutil

VIDEO_ASSETS = ['videos.json', 'videos.js', 'video-model.mjs']

def video_section():
    root = Path(__file__).resolve().parents[1]
    catalog = json.loads((root/'seo/videos/videos.json').read_text())
    cards = []
    for v in catalog['videos']:
        a = v['author']
        cards.append(f'''<article class="video-card" data-video-id="{E(v['id'])}"><a class="video-cover" href="{E(v['url'])}" target="_blank" rel="noopener noreferrer" data-video-play aria-haspopup="dialog" aria-label="播放：{E(v['title'])}"><img src="{E(v['cover'])}" width="1200" height="630" loading="lazy" referrerpolicy="no-referrer" alt="《{E(v['originalTitle'])}》视频封面"><span class="video-topic">{E(v['topic'])}</span><span class="video-play" aria-hidden="true">▶</span><span class="video-platform">BILIBILI · 观看视频</span></a><div class="video-copy"><h3><a href="{E(v['url'])}" target="_blank" rel="noopener noreferrer" data-video-play>{E(v['title'])}</a></h3><p>{E(v['description'])}</p><div class="video-author"><a class="author-avatar" data-author-avatar href="{E(a['url'])}" target="_blank" rel="noopener noreferrer" aria-label="查看{E(a['name'])}的主页"><img src="{E(a['avatar'])}" width="44" height="44" loading="lazy" referrerpolicy="no-referrer" alt="{E(a['name'])}的头像"><span class="author-fallback" aria-hidden="true">{E(a['name'][0])}</span><span class="live-badge" hidden>直播中</span></a><div><a class="author-name" href="{E(a['url'])}" target="_blank" rel="noopener noreferrer">{E(a['name'])}</a><span class="author-status" data-author-status>视频创作者 · 哔哩哔哩</span></div><a class="author-room" hidden target="_blank" rel="noopener noreferrer">去直播间 ↗</a></div></div></article>''')
    return f'''<section class="container video-section" id="learn" aria-labelledby="video-heading"><div class="video-heading"><div><p class="eyebrow">科普视频</p><h2 id="video-heading">香气是怎么来的？</h2></div><p>看萃取实验、调香搭配和香料原理。<br>视频下方可以查看作者与原视频。</p></div><p id="video-preview-note" class="video-preview-note" hidden>当前为本浏览器的直播状态预览，其他访客看到的是已上线配置。<button type="button" id="clear-video-preview">退出预览</button></p><div class="video-grid">{''.join(cards)}</div><p class="reference">精选第三方公开视频，点击观看或前往原平台。创作者保留内容权利；实验演示供了解原理，产品使用请遵循标签。</p><dialog id="video-dialog" class="video-dialog" aria-labelledby="video-dialog-title"><div class="video-dialog-top"><h2 id="video-dialog-title">科普视频</h2><button type="button" id="video-close" aria-label="关闭视频">×</button></div><div id="video-player" class="video-player"></div><p class="video-dialog-note">播放由哔哩哔哩提供。无法播放时，可以<a id="video-original" target="_blank" rel="noopener noreferrer">前往原视频观看 ↗</a>。</p></dialog><script type="module" src="/assets/videos.js"></script></section>'''

def build_videos(root, output):
    for name in VIDEO_ASSETS:
        shutil.copy2(root/'seo/videos'/name, output/'assets'/name)
