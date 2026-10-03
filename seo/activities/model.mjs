export const elements = [
 {id:'wood',symbol:'木',name:'木 · 试一件新事',color:'#527560',line:'挑一件一直想试的小事，今天先做一点。',text:'你选了绿意。这张签借“生长”的意象，建议你从一个小尝试开始，不必今天就完成。',tasks:['从收藏里挑一本书或一篇文章。','读一页或一小段，看到想停的地方就停。','把下次想继续看的位置记下来。']},
 {id:'fire',symbol:'火',name:'火 · 和人聊聊',color:'#aa6755',line:'找一个有空的朋友，聊聊今天的一件事。',text:'你选了灯光。这张签借“温暖”的意象，建议你留几分钟与熟悉的人聊聊天。',tasks:['先问问朋友现在有没有空。','分享今天发生的一件小事。','约定聊到什么时候，结束后收好手机。']},
 {id:'earth',symbol:'土',name:'土 · 收好明天',color:'#998054',line:'先收好明天要用的东西，今晚就到这里。',text:'你选了熟悉的角落。这张签借“安放”的意象，建议你先准备好明天的一件物品。',tasks:['想想明天出门最先会用到什么。','把钥匙、包或要带的东西放到固定位置。','核对一次就好，剩下的事明天再做。']},
 {id:'metal',symbol:'金',name:'金 · 清一小处',color:'#7d7d88',line:'只整理眼前这一小块，不用收拾整个房间。',text:'你选了白纸。这张签借“做减法”的意象，建议你清出一块真正用得上的空间。',tasks:['挑桌面上手掌大小的一块位置。','把不属于这里的东西放回原处。','五分钟到了就停，今天先做到这里。']},
 {id:'water',symbol:'水',name:'水 · 听完一首',color:'#58738c',line:'选一首想听的歌，从头到尾听完。',text:'你选了音乐。这张签借“流动”的意象，建议你用一首歌的时间歇一会儿。',tasks:['选一首歌，暂时关掉自动切歌。','坐到舒服的位置，先不刷其他内容。','听完后记下歌名，想听时再找出来。']}
];
export const profiles = [
 {id:'quiet',symbol:'静',name:'安静独处型',color:'#77648c',line:'先给自己十分钟，不用回复消息。',text:'本次回答更常选择独自完成、少被打断的安排。可以从一段安静的阅读或音乐开始；这不是固定性格分类。',tasks:['选一个这会儿不需要交流的位置。','把消息提醒静音十分钟。','读几页书或听一首歌，结束后再看消息。']},
 {id:'connect',symbol:'聊',name:'朋友陪伴型',color:'#ac7160',line:'先问朋友有没有空，再分享今天的小事。',text:'本次回答更常选择聊天、分享和一起做事。今晚可以约一次短聊，不需要把每个问题都聊出答案。',tasks:['问一位熟悉的朋友有没有空。','选一件今天的事，互相说几句。','留意对方是否方便继续，聊完各自休息。']},
 {id:'explore',symbol:'试',name:'新鲜探索型',color:'#557665',line:'从收藏里挑一个新点子，试十分钟。',text:'本次回答更常选择换个方式、尝试新内容。挑一个容易开始的小尝试，比再收藏十个链接更具体。',tasks:['从收藏里只挑一个想试的内容。','准备好手边材料，先做十分钟。','记下做到了哪一步，再决定要不要继续。']},
 {id:'order',symbol:'整',name:'整理收尾型',color:'#99804f',line:'只收好一件事，剩下的明天再做。',text:'本次回答更常选择整理、准备和完成手边的事。今晚可以用一个明确的小任务结束，不用把全部待办清空。',tasks:['只选一小处整理，或准备一件明天要用的物品。','给它留五分钟，不额外增加任务。','做完就停，把其他待办留到明天。']}
];
export const questions = [
 {context:'突然空出的半小时',title:'晚饭后突然空出半小时，你先做什么？',options:[{profile:2,label:'试试收藏了很久的新内容'},{profile:0,label:'一个人坐一会儿，不看消息'},{profile:3,label:'收好手边没做完的小事'},{profile:1,label:'找熟悉的人聊聊今天'}]},
 {context:'朋友发来邀约',title:'朋友问你今晚要不要见面，你更想怎么安排？',options:[{profile:1,label:'找个能坐下聊天的地方'},{profile:3,label:'先确认时间，把手头的事收完'},{profile:2,label:'一起去一家没去过的小店'},{profile:0,label:'今晚自己待着，改天再约'}]},
 {context:'桌面上还没收好的东西',title:'回家看到桌面有点乱，你会先做哪件事？',options:[{profile:3,label:'用五分钟把东西放回原处'},{profile:0,label:'先坐下来休息，暂时不处理'},{profile:1,label:'问家里人今天怎么样，边聊边收'},{profile:2,label:'试着换个摆法，放上喜欢的小物'}]},
 {context:'想留下的一张照片',title:'给今天留一张照片，你会选哪一张？',options:[{profile:0,label:'窗边安静的一角'},{profile:2,label:'路上第一次留意到的小细节'},{profile:1,label:'和朋友或家人一起的画面'},{profile:3,label:'刚整理好的桌面'}]},
 {context:'只剩十分钟',title:'只剩十分钟，手机上有这些内容，你先点开？',options:[{profile:2,label:'一段想试试的新教程'},{profile:1,label:'朋友发来的语音消息'},{profile:3,label:'明天要带的东西清单'},{profile:0,label:'一首可以安静听完的歌'}]},
 {context:'准备结束今晚',title:'准备结束今晚，你更愿意做哪件事？',options:[{profile:3,label:'把明天最先要用的东西放好'},{profile:1,label:'和熟悉的人互道晚安'},{profile:0,label:'放下手机，自己安静待会儿'},{profile:2,label:'记下一个刚想到的新点子'}]}
];
export function scoreQuiz(answers) {
 if(answers.length!==questions.length||answers.some(a=>!Number.isInteger(a)||a<0||a>=profiles.length)) throw new Error('请完成全部题目');
 const scores=profiles.map((_,i)=>answers.filter(a=>a===i).length);
 const high=Math.max(...scores);const tied=scores.map((n,i)=>n===high?i:-1).filter(i=>i>=0);
 const winner=[...answers].reverse().find(a=>tied.includes(a));
 return {index:winner,scores,tied:tied.length>1};
}
export function quizEvidence(answers) {
 const {index}=scoreQuiz(answers);
 return questions.flatMap((q,i)=>answers[i]===index?[{context:q.context,answer:q.options.find(o=>o.profile===index).label}]:[]);
}
export function dailyElement(choice,date) {
 if(!Number.isInteger(choice)||choice<0||choice>=elements.length||!/^\d{4}-\d{2}-\d{2}$/.test(date)) throw new Error('请选择一个画面');
 return {index:choice};
}
