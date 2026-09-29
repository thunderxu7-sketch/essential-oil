import assert from 'node:assert/strict';
import {scoreQuiz,dailyElement,profiles} from '../seo/activities/model.mjs';
for(let i=0;i<profiles.length;i++)assert.equal(scoreQuiz(Array(6).fill(i)).index,i);
assert.equal(scoreQuiz([0,1,0,1,2,2]).index,2);
assert.equal(scoreQuiz([0,0,1,1,0,1]).index,1);
assert.throws(()=>scoreQuiz([0,1]));assert.throws(()=>scoreQuiz([0,0,0,0,0,8]));
for(let n=0;n<4**6;n++){
 let v=n;const answers=Array.from({length:6},()=>{const a=v%4;v=Math.floor(v/4);return a;});
 const r=scoreQuiz(answers);assert.equal(r.scores[r.index],Math.max(...r.scores));assert.equal(r.scores.reduce((a,b)=>a+b,0),6);
}
for(let day=1;day<=31;day++)for(let i=0;i<5;i++){
 const date=`2026-10-${String(day).padStart(2,'0')}`;const r=dailyElement(i,date);
 assert.equal(r.index,i);assert.equal(r.shares.reduce((a,b)=>a+b,0),100);assert.equal(r.shares[i],Math.max(...r.shares));assert.deepEqual(r,dailyElement(i,date));
}
assert.throws(()=>dailyElement(-1,'2026-09-29'));
console.log('PASS: all 4,096 quiz combinations, ties, invalid input, 5 daily signs and distribution totals.');
