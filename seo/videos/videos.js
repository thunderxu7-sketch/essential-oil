import {PREVIEW_KEY, liveState, readOverrides} from './video-model.mjs';
const section = document.querySelector('.video-section');
const dialog = document.querySelector('#video-dialog');
let catalog, lastTrigger;
// The HTML links remain usable if the catalog, script, or player is unavailable.
try { const response = await fetch(new URL('./videos.json', import.meta.url)); if (response.ok) catalog = await response.json(); } catch {}
function refreshLive() {
  if (!catalog) return;
  let overrides = {};
  try { overrides = readOverrides(localStorage); } catch {}
  document.querySelector('#video-preview-note').hidden = Object.keys(overrides).length === 0;
  for (const v of catalog.videos) {
    const card = document.querySelector(`[data-video-id="${v.id}"]`);
    if (!card) continue;
    const live = liveState(v.author, overrides);
    const avatar = card.querySelector('[data-author-avatar]');
    avatar.classList.toggle('is-live', live.active);
    avatar.href = live.active ? live.url : v.author.url;
    avatar.setAttribute('aria-label', live.active ? `${v.author.name}正在直播，进入直播间` : `查看${v.author.name}的主页`);
    avatar.querySelector('.live-badge').hidden = !live.active;
    card.querySelector('[data-author-status]').textContent = live.active ? '正在直播 · 一起聊聊香气' : '视频创作者 · 哔哩哔哩';
    const room = card.querySelector('.author-room');
    room.hidden = !live.active;
    if (live.active) room.href = live.url; else room.removeAttribute('href');
  }
}
section.addEventListener('click', e => {
  const trigger = e.target.closest('[data-video-play]');
  if (!trigger || !catalog || !dialog.showModal || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
  const video = catalog.videos.find(v => v.id === trigger.closest('[data-video-id]').dataset.videoId);
  if (!video || !/^BV[\w]{10}$/.test(video.bvid)) return;
  e.preventDefault(); lastTrigger = trigger;
  document.querySelector('#video-dialog-title').textContent = video.title;
  document.querySelector('#video-original').href = video.url;
  const frame = document.createElement('iframe');
  frame.src = `https://player.bilibili.com/player.html?bvid=${encodeURIComponent(video.bvid)}&page=1&autoplay=0`;
  frame.title = `${video.originalTitle} — ${video.author.name}`;
  frame.allow = 'fullscreen; picture-in-picture'; frame.referrerPolicy = 'no-referrer';
  document.querySelector('#video-player').replaceChildren(frame); dialog.showModal();
});
document.querySelector('#video-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', e => { if (e.target === dialog) { const r = dialog.getBoundingClientRect(); if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close(); } });
dialog.addEventListener('close', () => { document.querySelector('#video-player').replaceChildren(); lastTrigger?.focus(); });
document.querySelector('#clear-video-preview').addEventListener('click', () => { try { localStorage.removeItem(PREVIEW_KEY); } catch {} refreshLive(); });
section.querySelectorAll('img').forEach(img => { const fallback = () => img.classList.add('image-unavailable'); img.addEventListener('error', fallback); if (img.complete && !img.naturalWidth) fallback(); });
window.addEventListener('storage', e => { if (e.key === PREVIEW_KEY || e.key === null) refreshLive(); });
document.addEventListener('visibilitychange', () => { if (!document.hidden) refreshLive(); });
refreshLive(); setInterval(refreshLive, 15000);
