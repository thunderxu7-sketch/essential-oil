export const elements = [
 {id:'wood',symbol:'木',name:'木 · 生长签',color:'#527560',line:'给自己一点慢慢生长的空间。',text:'今晚的灵感是向外舒展。试着把注意力放在一件小小的新事上，不必马上看见成果。',tasks:['看看窗外，寻找一种今天没留意的颜色。','翻开想读的书，只读一页。','写下一个可以慢慢完成的小愿望。']},
 {id:'fire',symbol:'火',name:'火 · 微光签',color:'#aa6755',line:'热爱可以很小，也可以很亮。',text:'今晚的灵感是表达。给喜欢的事留一点位置，把值得纪念的普通瞬间留下来。',tasks:['放一首喜欢的歌。','拍下房间里让你喜欢的一角。','给朋友分享一件今天的小事。']},
 {id:'earth',symbol:'土',name:'土 · 安放签',color:'#998054',line:'把日子放稳，把自己接住。',text:'今晚的灵感是安放。熟悉的日常也可以有新鲜感，从一件容易完成的小事开始。',tasks:['整理桌面的一小块地方。','准备明天会用到的一件物品。','为自己留十分钟不赶时间的空白。']},
 {id:'metal',symbol:'金',name:'金 · 留白签',color:'#7d7d88',line:'少一点安排，多一点自己。',text:'今晚的灵感是做减法。没有必要填满每段时间，给真正想做的事留出位置。',tasks:['关掉一个暂时不需要的页面。','从待办中划去一件不着急的事。','留出一处干净的桌面。']},
 {id:'water',symbol:'水',name:'水 · 听雨签',color:'#58738c',line:'不用急着回答，先听见自己。',text:'今晚的灵感是倾听。允许想法暂时没有结论，用你喜欢的节奏和自己待一会儿。',tasks:['选一段喜欢的音乐，完整听完。','在纸上写下此刻想到的一句话。','找个舒服的位置，读几页书。']}
];
export const profiles = [
 {id:'quiet',symbol:'月',name:'静处收藏家',color:'#77648c',line:'你的留白，藏在安静的小角落。',text:'这次选择中，你更常偏向独处与低干扰的场景。今晚可以给自己留一段不被安排的时间；这不代表你总是内向。',tasks:['挑一个不用回复消息的十分钟。','选一本书、一段音乐或一张白纸。','结束时写下一个想保留的瞬间。']},
 {id:'connect',symbol:'光',name:'暖意联络员',color:'#ac7160',line:'一句有人接住的话，就是今晚的微光。',text:'这次选择中，你更常偏向分享与陪伴。一次轻松的交流可能正合你今晚的心意；也可以选择暂时独处。',tasks:['问问一位朋友有没有空聊几分钟。','分享一件小事，而不是急着解决问题。','聊完后给自己留一点收尾的时间。']},
 {id:'explore',symbol:'风',name:'灵感漫游者',color:'#557665',line:'给夜晚开一扇小窗，让新鲜感进来。',text:'这次选择中，你更常偏向新鲜体验与自由探索。换一种小小的日常方式，就可以是今晚的主题。',tasks:['换一本书、一个歌单或一个观察角度。','随手画下一个新的想法。','选择其中最轻的一件事，试十分钟。']},
 {id:'order',symbol:'屿',name:'日常筑岛师',color:'#99804f',line:'一件小事归位，一座小岛亮灯。',text:'这次选择中，你更常偏向有序与明确的安排。让一件小事有始有终，可以成为你的晚间仪式；不必要求事事完美。',tasks:['只选一处很小的地方整理。','写下明天最先做的一件事。','到约定的时间就停下，留一些空白。']}
];
export const questions = [
 {title:'一天结束，突然多出半小时，你最想？',options:['一个人安静待会儿','找熟悉的人聊聊天','试试收藏的新鲜事','把手边的小事收个尾']},
 {title:'理想的晚间角落，更像哪一幅画面？',options:['一盏灯，一本书','一张可以围坐的小桌','随时能涂画的灵感墙','清爽、有序的桌面']},
 {title:'忙了一天后，哪句话更合你心意？',options:['这会儿不用回应任何人','我想和你分享今天','来换个角度看日常','今天的事就到这里']},
 {title:'给晚间选一个小任务，你会选？',options:['独自听完一张专辑','与朋友交换一张照片','随手试一个新点子','整理一个抽屉']},
 {title:'计划临时取消，你更愿意怎么用这段空白？',options:['享受不用安排的时间','问问朋友是否有空','随兴探索一个新主题','完成一直想做的小整理']},
 {title:'今晚结束时，你最想留下哪种感受？',options:['有一段时间只属于我','有人和我分享了日常','发现了一点新的可能','给今天画了一个句号']}
];
export function scoreQuiz(answers) {
 if(answers.length!==questions.length||answers.some(a=>!Number.isInteger(a)||a<0||a>=profiles.length)) throw new Error('请完成全部题目');
 const scores=profiles.map((_,i)=>answers.filter(a=>a===i).length);
 const high=Math.max(...scores);const tied=scores.map((n,i)=>n===high?i:-1).filter(i=>i>=0);
 const winner=[...answers].reverse().find(a=>tied.includes(a));
 return {index:winner,scores,tied:tied.length>1};
}
export function dailyElement(choice,date) {
 if(!Number.isInteger(choice)||choice<0||choice>=5||!/^\d{4}-\d{2}-\d{2}$/.test(date)) throw new Error('请选择一个意象');
 const seed=[...date].reduce((n,c)=>n+c.charCodeAt(0),0);
 const scores=elements.map((_,i)=>1+(seed+i*7)%4);scores[choice]+=6;
 const total=scores.reduce((a,b)=>a+b,0);const shares=scores.map(n=>Math.floor(n/total*100));
 let left=100-shares.reduce((a,b)=>a+b,0);for(let i=0;left>0;i++,left--)shares[(choice+i)%5]++;
 return {index:choice,shares};
}
