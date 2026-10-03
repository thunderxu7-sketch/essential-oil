export const PREVIEW_KEY = 'evening-video-live-preview-v1';
export function liveUrl(value) {
  try { const u = new URL(value); return u.protocol === 'https:' && u.hostname === 'live.bilibili.com' && /^\/[1-9]\d*\/?$/.test(u.pathname) && !u.username && !u.password && !u.port && !u.search && !u.hash ? u.href : ''; } catch { return ''; }
}
export function liveState(author, overrides = {}, now = Date.now()) {
  const live = Object.hasOwn(overrides, author.id) ? overrides[author.id] : author.live;
  const expires = Date.parse(live?.expiresAt);
  const url = liveUrl(live?.url);
  return {active: live?.enabled === true && !!url && Number.isFinite(expires) && expires > now, url, expires};
}
export function readOverrides(storage) {
  try { const data = JSON.parse(storage.getItem(PREVIEW_KEY)); return data && typeof data === 'object' && !Array.isArray(data) ? data : {}; } catch { return {}; }
}
