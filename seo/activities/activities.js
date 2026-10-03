import {elements, profiles, questions, scoreQuiz, dailyElement, quizEvidence} from './model.mjs';
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
let answers=[],step=0,choice=null,result=null,resultDate='',previewUrl='';
const start=document.querySelector('#start');start.hidden=false;start.addEventListener('click',begin);
function focusHost(){host.tabIndex=-1;host.focus({preventScroll:true});host.scrollIntoView({behavior:'auto',block:'start'});}
function begin(){if(previewUrl){URL.revokeObjectURL(previewUrl);previewUrl='';}answers=[];step=0;choice=null;result=null;renderQuestion();}
function renderQuestion(){
 const isElements=kind==='elements';
 const opts=isElements?['木 · 一片绿意','火 · 一盏灯光','土 · 熟悉的角落','金 · 一张白纸','水 · 一段音乐'].map((label,profile)=>({label,profile})):questions[step].options;
 const selected=isElements?choice:answers[step];
 host.innerHTML=`<div class="progress-meta"><span>${isElements?'选择今日画面':`第 ${step+1} / ${questions.length} 题`}</span><span>${isElements?date():'按今晚的想法选择'}</span></div><progress class="quiz-progress" max="${isElements?1:questions.length}" value="${isElements?0:step}" aria-label="已完成题数"></progress><form id="question-form"><fieldset class="options"><legend>${isElements?'此刻，你更喜欢哪个画面？':questions[step].title}</legend>${opts.map(({label,profile})=>`<label class="option"><input type="radio" name="answer" value="${profile}" ${selected===profile?'checked':''} required><span>${label}</span></label>`).join('')}</fieldset><div class="quiz-nav"><button type="button" class="reset-button" id="previous" ${isElements||step===0?'hidden':''}>← 上一题</button><button type="submit" class="btn" id="next" ${selected==null?'disabled':''}>${isElements?'查看这张签':step===questions.length-1?'查看我的结果':'下一题 →'}</button></div></form>`;
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
 const evidence=kind==='elements'?`<p class="choice-note">你选的画面：${['一片绿意','一盏灯光','熟悉的角落','一张白纸','一段音乐'][choice]}。日期只记录领取时间。</p>`:`<aside class="answer-evidence"><h3>本次回答依据</h3><p>六题中有 ${computed.scores[computed.index]} 题选择了这一类安排。${computed.tied?'有多种偏好并列；采用了你最近一道选中的并列类型。':'它是本次回答中出现最多的偏好。'}</p><ul>${quizEvidence(answers).slice(0,2).map(e=>`<li>在“${e.context}”时，你选择了“${e.answer}”。</li>`).join('')}</ul><p>这是今晚的选择，换一天回答可能不同。</p></aside>`;
 host.innerHTML=`<div class="result-head"><p class="eyebrow">${kind==='elements'?'今日主题签 · '+resultDate:'本次晚间偏好'}</p><div class="result-seal" style="color:${result.color}">${result.symbol}</div><h2>${result.name}</h2><p class="result-line">${result.line}</p><p class="result-text">${result.text}</p></div>${evidence}<h3 class="section">可以照这三步做</h3><ol class="ritual-list">${result.tasks.map(t=>`<li>${t}</li>`).join('')}</ol><div class="result-actions"><button class="btn" id="save-card" type="button">保存结果卡</button><button class="btn secondary" id="copy-share" type="button">${kind==='elements'?'邀请朋友领签':'邀请朋友测测'}</button><button class="reset-button" id="restart" type="button">${kind==='elements'?'换个画面':'重新测试'}</button></div><p class="feedback" id="feedback" role="status" aria-live="polite"></p><textarea id="share-fallback" class="share-fallback" aria-label="发给朋友的话" readonly hidden></textarea><div class="card-preview" id="card-preview" hidden><h3>你的结果卡</h3><p>手机上可长按图片保存，或点击下方下载。</p><img id="result-card-image" alt="本次活动结果卡"><div class="result-actions"><a class="btn" id="result-card-download">下载图片</a><button type="button" class="reset-button" id="close-card-preview">收起图片</button></div></div><div class="product-bridge"><h3>精油选购资料</h3><p>如果你正在了解薰衣草精油，可以继续看选购指南和阿芙 10ml 的规格。本次活动结果不用于判断产品是否适合你。</p><p class="reference">阿芙薰衣草精油 10ml · 本站参考价 ¥99</p><a href="${guideUrl}">先看选购指南 →</a><a href="${productUrl}">查看商品规格</a></div><p style="margin-top:24px"><a href="${otherUrl}">${kind==='elements'?'再做六题晚间偏好测试':'再领一张五行主题签'} →</a></p>`;
 document.querySelector('#restart').addEventListener('click',begin);
 document.querySelector('#copy-share').addEventListener('click',copyShare);
 document.querySelector('#save-card').addEventListener('click',saveCard);
 document.querySelector('#close-card-preview').addEventListener('click',()=>{document.querySelector('#card-preview').hidden=true;document.querySelector('#save-card').focus();});
 focusHost();
}
function caption(){return `${kind==='elements'?'我的今日五行主题签':'我的本次晚间偏好'}：${result.name}\n${result.line}\n${kind==='elements'?'五行文化主题娱乐，不计算五行属性。':'依据本次六题选择，非心理诊断或固定性格分类。'}\n${kind==='elements'?'也来选个画面领签':'也来看看今晚的偏好'}：${inviteUrl}`;}
async function copyShare(){
 const text=caption();const feedback=document.querySelector('#feedback');
 try{if(!navigator.clipboard?.writeText)throw new Error();await navigator.clipboard.writeText(text);feedback.textContent='已复制邀请文案和链接。';}
 catch{const area=document.querySelector('#share-fallback');area.hidden=false;area.value=text;area.focus();area.select();feedback.textContent='请长按或选中文案，手动复制。';}
}
async function saveCard(){
 const button=document.querySelector('#save-card');button.disabled=true;
 try{
  if(document.fonts?.ready)await document.fonts.ready;
  const canvas=document.createElement('canvas');canvas.width=1000;canvas.height=1300;
  const c=canvas.getContext('2d');if(!c)throw new Error();
  c.fillStyle='#f8f4f9';c.fillRect(0,0,1000,1300);c.strokeStyle='#cbbbd3';c.lineWidth=2;c.strokeRect(40,40,920,1220);
  c.fillStyle='#766181';c.textAlign='center';c.font='20px sans-serif';c.fillText('晚 间 留 白',500,115);
  c.strokeStyle=result.color;c.beginPath();c.arc(500,290,105,0,Math.PI*2);c.stroke();c.fillStyle=result.color;c.font='100px serif';c.fillText(result.symbol,500,325);
  c.font='50px serif';c.fillText(result.name,500,480);c.font='29px serif';c.fillText(result.line,500,550);
  c.font='24px sans-serif';c.fillStyle='#65546f';c.fillText('可以照这三步做',500,655);
  result.tasks.forEach((t,i)=>{c.font='24px sans-serif';c.fillText(`${i+1}. ${t}`,500,725+i*60,850);});
  c.font='23px sans-serif';c.fillText('晚间留白 · 免费小活动',500,1010);
  c.font='18px sans-serif';c.fillText(kind==='elements'?`五行文化主题娱乐 · 不计算属性 · ${resultDate}`:'本次六题偏好 · 非心理诊断',500,1080);
  c.font='16px sans-serif';c.fillText('邀请朋友也来选一选',500,1140);
  c.fillText(activityUrl.href,500,1190,860);
  const blob=await new Promise(resolve=>canvas.toBlob(resolve,'image/png'));if(!blob)throw new Error();
  if(previewUrl)URL.revokeObjectURL(previewUrl);
  previewUrl=URL.createObjectURL(blob);
  const preview=document.querySelector('#card-preview'),link=document.querySelector('#result-card-download');
  document.querySelector('#result-card-image').src=previewUrl;
  link.href=previewUrl;link.download=`晚间留白-${result.id}-${resultDate}.png`;
  preview.hidden=false;link.click();preview.scrollIntoView({block:'start',behavior:'auto'});
  document.querySelector('#feedback').textContent='图片已生成并发起下载。若未保存，可长按下方图片或点击下载。';
 }catch{document.querySelector('#feedback').textContent='当前浏览器无法保存图片，请使用邀请按钮复制链接。';}
 finally{button.disabled=false;}
}
