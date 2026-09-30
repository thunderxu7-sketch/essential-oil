import {elements, profiles, questions, scoreQuiz, dailyElement} from './model.mjs';
const root=document.querySelector('[data-activity]');
const host=document.querySelector('#experience');
const kind=root.dataset.activity;
const base=new URL('../',import.meta.url);
const path=kind==='elements'?'five-elements':'evening-personality';
const activityUrl=new URL(`activities/${path}/`,base);
const inviteUrl=new URL(activityUrl);inviteUrl.searchParams.set('utm_source','result_share');inviteUrl.searchParams.set('utm_medium','invitation');inviteUrl.searchParams.set('utm_campaign',path);
const productUrl=new URL('products/afu-lavender-essential-oil-10ml/',base);productUrl.searchParams.set('utm_source',path);productUrl.searchParams.set('utm_medium','activity_result');
const guideUrl=new URL('guides/choosing-lavender-essential-oil/',base);
const otherUrl=new URL(`activities/${kind==='elements'?'evening-personality':'five-elements'}/`,base);
const date=()=>{const d=new Date();return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;};
let answers=[],step=0,choice=null,result=null,resultDate='';
const start=document.querySelector('#start');start.hidden=false;start.addEventListener('click',begin);
function focusHost(){host.tabIndex=-1;host.focus({preventScroll:true});host.scrollIntoView({behavior:'auto',block:'start'});}
function begin(){answers=[];step=0;choice=null;result=null;renderQuestion();}
function renderQuestion(){
 const isElements=kind==='elements';
 const opts=isElements?['木 · 一片正在生长的绿意','火 · 一盏温暖的小灯','土 · 一个熟悉的角落','金 · 一张留白的纸','水 · 一段缓缓流动的音乐']:questions[step].options;
 const selected=isElements?choice:answers[step];
 host.innerHTML=`<div class="progress-meta"><span>${isElements?'今日灵感选择':`第 ${step+1} / ${questions.length} 题`}</span><span>${isElements?date():'凭第一直觉选择即可'}</span></div><progress class="quiz-progress" max="${isElements?1:questions.length}" value="${isElements?0:step}" aria-label="已完成题数"></progress><form id="question-form"><fieldset class="options"><legend>${isElements?'此刻，你更向往哪个画面？':questions[step].title}</legend>${opts.map((label,i)=>`<label class="option"><input type="radio" name="answer" value="${i}" ${selected===i?'checked':''} required><span>${label}</span></label>`).join('')}</fieldset><div class="quiz-nav"><button type="button" class="reset-button" id="previous" ${isElements||step===0?'hidden':''}>← 上一题</button><button type="submit" class="btn" id="next" ${selected==null?'disabled':''}>${isElements?'生成今日签':step===questions.length-1?'查看我的结果':'下一题 →'}</button></div></form>`;
 document.querySelector('#question-form').addEventListener('change',()=>{document.querySelector('#next').disabled=false;});
 document.querySelector('#previous').addEventListener('click',()=>{saveAnswer();step--;renderQuestion();});
 document.querySelector('#question-form').addEventListener('submit',e=>{e.preventDefault();saveAnswer();if(isElements||step===questions.length-1)showResult();else{step++;renderQuestion();}});
 focusHost();
}
function saveAnswer(){const value=host.querySelector('input:checked')?.value;if(value===undefined)return;if(kind==='elements')choice=Number(value);else answers[step]=Number(value);}
function showResult(){
 resultDate=date();
 const computed=kind==='elements'?dailyElement(choice,resultDate):scoreQuiz(answers);
 result=(kind==='elements'?elements:profiles)[computed.index];
 const distribution=kind==='elements'?`<div class="score-list" aria-label="五行灵感配色占比">${elements.map((e,i)=>`<div class="score-row" style="--accent:${e.color}"><span>${e.symbol}</span><progress value="${computed.shares[i]}" max="100" aria-label="${e.symbol} ${computed.shares[i]}%"></progress><span>${computed.shares[i]}%</span></div>`).join('')}</div><p class="choice-note">五种意象，组成今天的灵感色谱。</p>`:`<p class="choice-note">你有 ${computed.scores[computed.index]} / ${questions.length} 个选择指向这一偏好。${computed.tied?'你也喜欢不止一种方式，这张卡更贴近你最近的选择。':'跟着今晚的心意就好，明天可以有另一种答案。'}</p>`;
 host.innerHTML=`<div class="result-head"><p class="eyebrow">${kind==='elements'?'YOUR DAILY SIGN / '+resultDate:'YOUR EVENING, YOUR WAY'}</p><div class="result-seal" style="color:${result.color}">${result.symbol}</div><h2>${result.name}</h2><p class="result-line">${result.line}</p><p class="result-text">${result.text}</p></div>${distribution}<h3 class="section">今晚，可以从这三件小事开始</h3><ol class="ritual-list">${result.tasks.map(t=>`<li>${t}</li>`).join('')}</ol><div class="result-actions"><button class="btn" id="save-card" type="button">保存结果卡</button><button class="btn secondary" id="copy-share" type="button">邀请朋友测测</button><button class="reset-button" id="restart" type="button">${kind==='elements'?'换个意象':'重新测试'}</button></div><p class="feedback" id="feedback" role="status" aria-live="polite"></p><textarea id="share-fallback" class="share-fallback" aria-label="发给朋友的话" readonly hidden></textarea><div class="product-bridge"><p class="eyebrow">CONTINUE YOUR EVENING</p><h3>把灵感，带回生活里。</h3><p>想认识一瓶薰衣草精油？看看阿芙薰衣草精油 10ml，了解它的规格与使用说明。</p><p class="reference">参考价 ¥99 · 实际价格以店铺为准</p><a href="${productUrl}">认识这瓶精油 →</a><a href="${guideUrl}">先读选购指南</a></div><p style="margin-top:24px"><a href="${otherUrl}">${kind==='elements'?'再测测你的晚间充电方式':'再领一张五行留白签'} →</a></p>`;
 document.querySelector('#restart').addEventListener('click',begin);
 document.querySelector('#copy-share').addEventListener('click',copyShare);
 document.querySelector('#save-card').addEventListener('click',saveCard);
 focusHost();
}
function caption(){return `${kind==='elements'?'我的今日五行留白签':'我的晚间充电方式'}：${result.name}\n${result.line}\n${kind==='elements'?'五行文化灵感，仅供娱乐。':'原创趣味偏好测试，非心理诊断。'}\n也来找到你的晚间灵感：${inviteUrl}`;}
async function copyShare(){
 const text=caption();const feedback=document.querySelector('#feedback');
 try{if(!navigator.clipboard?.writeText)throw new Error();await navigator.clipboard.writeText(text);feedback.textContent='已复制，发给朋友一起测测吧。';}
 catch{const area=document.querySelector('#share-fallback');area.hidden=false;area.value=text;area.focus();area.select();feedback.textContent='请长按或选中文案，手动复制。';}
}
async function saveCard(){
 const button=document.querySelector('#save-card');button.disabled=true;
 try{
  if(document.fonts?.ready)await document.fonts.ready;
  const canvas=document.createElement('canvas');canvas.width=1000;canvas.height=1300;
  const c=canvas.getContext('2d');if(!c)throw new Error();
  c.fillStyle='#f8f4f9';c.fillRect(0,0,1000,1300);c.strokeStyle='#cbbbd3';c.lineWidth=2;c.strokeRect(40,40,920,1220);
  c.fillStyle='#766181';c.textAlign='center';c.font='20px sans-serif';c.fillText('晚 间 留 白  /  EVENING, YOURS.',500,115);
  c.strokeStyle=result.color;c.beginPath();c.arc(500,290,105,0,Math.PI*2);c.stroke();c.fillStyle=result.color;c.font='100px serif';c.fillText(result.symbol,500,325);
  c.font='50px serif';c.fillText(result.name,500,480);c.font='29px serif';c.fillText(result.line,500,550);
  c.font='24px sans-serif';c.fillStyle='#65546f';c.fillText('今晚的小小仪式',500,655);
  result.tasks.forEach((t,i)=>{c.font='24px sans-serif';c.fillText(`${i+1}. ${t}`,500,725+i*60,850);});
  c.font='23px sans-serif';c.fillText('把夜晚，还给自己。',500,1010);
  c.font='18px sans-serif';c.fillText(kind==='elements'?`五行文化灵感 · 仅供娱乐 · ${resultDate}`:'原创趣味偏好测试 · 非心理诊断',500,1080);
  c.font='16px sans-serif';c.fillText('和朋友一起，发现今晚的自己',500,1140);
  c.fillText(activityUrl.href,500,1190,860);
  const blob=await new Promise(resolve=>canvas.toBlob(resolve,'image/png'));if(!blob)throw new Error();
  const url=URL.createObjectURL(blob);const link=document.createElement('a');link.href=url;link.download=`晚间留白-${result.id}-${resultDate}.png`;document.body.appendChild(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),60000);
  document.querySelector('#feedback').textContent='结果卡已生成并发起下载；可同时邀请朋友测测与链接。';
 }catch{document.querySelector('#feedback').textContent='当前浏览器无法保存图片，请使用“邀请朋友测测”。';}
 finally{button.disabled=false;}
}
