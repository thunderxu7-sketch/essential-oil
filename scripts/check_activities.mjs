import assert from 'node:assert/strict';
import {scoreQuiz,dailyElement,profiles,questions,quizEvidence} from '../seo/activities/model.mjs';
for(const q of questions){
 assert.equal(q.options.length,profiles.length);
 assert.deepEqual(q.options.map(o=>o.profile).sort(),[0,1,2,3]);
 assert(q.context&&q.title&&q.options.every(o=>o.label));
}
for(let i=0;i<profiles.length;i++)assert.equal(scoreQuiz(Array(6).fill(i)).index,i);
assert.equal(scoreQuiz([0,1,0,1,2,2]).index,2);
assert.equal(scoreQuiz([0,0,1,1,0,1]).index,1);
assert.equal(scoreQuiz([0,1,0,1,2,2]).tied,true);
assert.throws(()=>scoreQuiz([0,1]));assert.throws(()=>scoreQuiz([0,0,0,0,0,8]));
for(let n=0;n<4**6;n++){
 let v=n;const answers=Array.from({length:6},()=>{const a=v%4;v=Math.floor(v/4);return a;});
 const r=scoreQuiz(answers),evidence=quizEvidence(answers);
 assert.equal(r.scores[r.index],Math.max(...r.scores));assert.equal(r.scores.reduce((a,b)=>a+b,0),6);
 assert.equal(evidence.length,r.scores[r.index]);
 const expected=questions.flatMap((q,i)=>answers[i]===r.index?[{context:q.context,answer:q.options.find(o=>o.profile===r.index).label}]:[]);
 assert.deepEqual(evidence,expected);
}
// Selecting the first displayed option in every question no longer means a single type.
const firsts=questions.map(q=>q.options[0].profile);
assert(new Set(firsts).size>1);
for(let i=0;i<5;i++){
 const r=dailyElement(i,'2026-10-04');assert.deepEqual(r,{index:i});
 assert.deepEqual(r,dailyElement(i,'2026-10-05'));
}
assert.throws(()=>dailyElement(-1,'2026-10-04'));assert.throws(()=>dailyElement(5,'2026-10-04'));assert.throws(()=>dailyElement(0,'invalid'));
console.log('PASS: 4,096 quiz combinations, displayed-option mappings, ties, answer evidence, and five theme signs without fabricated percentages.');
