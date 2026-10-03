import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {liveState, liveUrl, readOverrides} from '../seo/videos/video-model.mjs';
const catalog = JSON.parse(await readFile(new URL('../seo/videos/videos.json', import.meta.url), 'utf8'));
assert.equal(catalog.videos.length, 3);
assert.equal(new Set(catalog.videos.map(v => v.id)).size, 3);
for (const v of catalog.videos) {
  assert.match(v.bvid, /^BV\w{10}$/);
  assert.equal(v.url, `https://www.bilibili.com/video/${v.bvid}/`);
  assert.equal(v.author.url, `https://space.bilibili.com/${v.author.id}/`);
  assert.ok(v.author.name && v.author.avatar.startsWith('https://i2.hdslb.com/bfs/face/'));
  assert.ok(v.originalTitle && v.cover.startsWith('https://'));
}
const now = Date.parse('2026-10-03T12:00:00Z');
const author = {id:'test',live:{enabled:true,url:'https://live.bilibili.com/12345',expiresAt:'2026-10-03T12:01:00Z'}};
assert.equal(liveState(author,{},now).active,true);
assert.equal(liveState(author,{},now+60000).active,false,'expires at the exact cutoff');
assert.equal(liveState(author,{test:{enabled:false}},now).active,false,'preview can end a published live');
assert.equal(liveState({...author,live:{...author.live,expiresAt:''}},{},now).active,false);
assert.equal(liveState({...author,live:{...author.live,url:'javascript:alert(1)'}},{},now).active,false);
for(const u of ['http://live.bilibili.com/123','https://live.bilibili.com.evil.com/123','https://evil@live.bilibili.com/123','https://live.bilibili.com:444/123','https://live.bilibili.com/blackboard/123','https://live.bilibili.com/123?url=bad']) assert.equal(liveUrl(u),'');
assert.deepEqual(readOverrides({getItem:()=>'{invalid'}),{});
assert.deepEqual(readOverrides({getItem:()=> '[]'}),{});
console.log('PASS: attributed video catalog; valid live-room URLs; expiry and preview override behavior.');
