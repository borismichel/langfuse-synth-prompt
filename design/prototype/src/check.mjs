import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {initialState,transition as t,product,portfolio,visibleTotals,coverage,definitions,recordsFor,systemFor} from './model.mjs';
import {days,hours,lengths,usage,versions} from './population.mjs';
let s=initialState();const initial=visibleTotals(s);
assert.equal(s.production,7);assert.equal(portfolio.prompts.length,9);assert.equal(portfolio.prompts.reduce((n,p)=>n+p.versions.length,0),72);
for(const tr of s.traces){for(const node of tr.nodes){assert.equal(node.sessionId,tr.sessionId);assert.equal(node.traceId,tr.id)}}
assert.equal(new Set(s.scores.map(r=>r.id)).size,s.scores.length);
for(const r of s.scores){const tr=s.traces.find(tr=>tr.id===r.traceId);assert.ok(tr.nodes.some(n=>n.id===r.observationId));assert.ok(definitions.some(d=>d.id===r.definitionId));}
const ref=s.traces.filter(t=>t.sessionId==='SESSION-01');assert.equal(ref.length,4);assert.deepEqual(ref.map(t=>t.prior.length),[0,2,4,6]);assert.equal(s.scores.filter(r=>r.sessionId==='SESSION-01').length,32);
assert.equal(s.scores.find(r=>r.id==='REFERENCE-T-03:E-08:r1').value,1);
assert.equal(s.scores.find(r=>r.id==='HISTORY-C-04:E-05:r1').value,0);
assert.equal(s.scores.find(r=>r.id==='HISTORY-C-06:E-05:r1').value,1);
assert.equal(s.scores.find(r=>r.id==='HISTORY-C-07:E-07:r1').value,1);
assert.equal(s.scores.find(r=>r.id==='HISTORY-C-07:E-06:r1').value,0);
assert.deepEqual(t(s,{type:'finishExperiment'}),s);
s=t(s,{type:'promote'});assert.equal(s.production,7);assert.match(s.notice,/protected/);
s=t(s,{type:'save',text:product.prompt_comparison.candidate_system});assert.equal(s.candidate.fixtureMatches,true);
s=t(s,{type:'startExperiment',scenario:'mixed'});assert.equal(s.experiment.status,'pending');assert.equal(s.scores.length,initial.records);
s=t(s,{type:'finishExperiment'});assert.equal(s.scores.length,initial.records+64);assert.equal(s.experiment.traces.length,16);assert.equal(s.scores.find(r=>r.id===s.experiment.traces.find(id=>id.includes('v9-C-02'))+':E-02:r1').value,0);
s=t(s,{type:'promote'});assert.equal(s.production,7);
s=t(s,{type:'send',promptId:'PR-01',text:product.conversation.turns[0].user});const beforeId=s.pending.trace.id;assert.equal(s.pending.trace.version,7);assert.ok(!s.traces.some(tr=>tr.id===beforeId));
s=t(s,{type:'receive'});assert.ok(!s.scores.some(r=>r.traceId===beforeId));s=t(s,{type:'evaluate'});assert.equal(s.scores.filter(r=>r.traceId===beforeId).length,8);
s=t(s,{type:'role',role:'admin'});s=t(s,{type:'promote'});assert.equal(s.production,9);assert.equal(s.traces.find(tr=>tr.id===beforeId).version,7); // promotion after a failing score is allowed
s=t(s,{type:'newSession',promptId:'PR-01'});let sessionId;
for(const turn of product.conversation.turns){s=t(s,{type:'send',promptId:'PR-01',text:turn.user});assert.equal(s.pending.trace.version,9);sessionId=s.pending.trace.sessionId;s=t(s,{type:'receive'});s=t(s,{type:'evaluate'});}
const live=s.traces.filter(tr=>tr.sessionId===sessionId);assert.equal(live.length,4);assert.deepEqual(live.map(tr=>tr.prior.length),[0,2,4,6]);assert.equal(s.scores.filter(r=>r.sessionId===sessionId).length,32);
const first=live[0],third=live[2];s=t(s,{type:'feedback',traceId:first.id,value:0,comment:'Needs clarity'});const afterFeedback=s.scores.length;s=t(s,{type:'feedback',traceId:first.id,value:1,comment:'Now clear'});assert.equal(s.scores.length,afterFeedback);assert.equal(s.scores.find(r=>r.id===first.id+':F-01').observationId,first.rootId);assert.ok(!recordsFor(s,third.rootId).some(r=>r.definitionId==='F-01'));assert.ok(!recordsFor(s,first.genId).some(r=>r.definitionId==='F-01'));
assert.equal(new Set(coverage(s).flatMap(c=>c.scoreIds)).size,s.scores.length);
assert.equal(coverage(s).find(c=>c.id==='P-04c').scoreIds.length,0);
assert.equal(visibleTotals(s).records,s.scores.length);assert.equal(new Set(s.scores.map(r=>r.id)).size,s.scores.length);
for(const pid of ['PR-02','PR-03']){const {examples}=await import('./model.mjs');s=t(s,{type:'send',promptId:pid,text:examples.cases.find(c=>c.prompt_id===pid).input});assert.ok(s.pending);s=t(s,{type:'receive'});s=t(s,{type:'evaluate'});}
assert.equal(days.reduce((n,d)=>n+d.n,0),360);assert.equal(hours.reduce((n,d)=>n+d.n,0),360);assert.equal(lengths.reduce((n,d)=>n+d.n,0),360);assert.equal(usage.reduce((a,b)=>a+b,0),2100);assert.equal(versions.reduce((n,d)=>n+d.n,0),540);
const reset=t(s,{type:'reset'});assert.deepEqual(visibleTotals(reset),initial);assert.equal(reset.production,7);assert.equal(reset.candidate,null);assert.ok(!reset.scores.some(r=>r.definitionId==='F-01'));
assert.equal(systemFor('PR-02',7),portfolio.prompts.find(p=>p.id==='PR-02').current_system_prompt_proposal);
const provenance=JSON.parse(readFileSync(new URL('../vendor/langfuse/provenance.json',import.meta.url)));
for(const f of provenance.unmodified_files){const bytes=readFileSync(new URL('../vendor/langfuse/'+f.path,import.meta.url));assert.equal(createHash('sha256').update(bytes).digest('hex'),f.sha256,f.path)}
console.log(JSON.stringify({passed:true,initial,afterRehearsal:visibleTotals(s),checks:['source hashes','explicit targets','session propagation/history','pending evaluation','paired experiment 64 outcomes','mixed-score admin promotion','historic version immutability','feedback upsert/isolation','all three bots','population totals','reset']},null,2));

let rerun=t(s,{type:'startExperiment',scenario:'flat'});rerun=t(rerun,{type:'finishExperiment'});assert.equal(new Set(coverage(rerun).flatMap(c=>c.scoreIds)).size,rerun.scores.length);
assert.ok(rerun.scores.filter(r=>rerun.experiment.traces.includes(r.traceId)&&r.definitionId==='E-01').every(r=>r.value===0));
assert.equal(t(s,{type:'save',text:'Changed later'}).candidate.text,s.candidate.text);
let custom=t(initialState(),{type:'save',text:'A new unrelated prompt'});assert.equal(t(custom,{type:'startExperiment'}).experiment,null);
const flow=s.traces.find(x=>x.id==='FLOW-01');assert.deepEqual(flow.nodes.filter(n=>n.type==='GENERATION').map(n=>n.promptId),['PR-04','PR-05','PR-09']);assert.equal(flow.nodes.find(n=>n.type==='TOOL').promptId,undefined);
console.log('Additional checks passed: rerun coverage, non-improvement, immutable versions, unsupported prompt guard, multi-prompt attribution.');
