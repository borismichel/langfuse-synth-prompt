import portfolio from './data/portfolio.json' with {type:'json'};
import product from './data/product.json' with {type:'json'};
import examples from './data/examples.json' with {type:'json'};
import extras from './data/dataset-extras.json' with {type:'json'};
import modelPolicy from './data/model-policy.json' with {type:'json'};
export {portfolio,product,examples,extras,modelPolicy};
export const rootNameByPrompt={'PR-01':'explain-product','PR-02':'explain-fees','PR-03':'guide-application','PR-04':'classify-service-intent','PR-05':'rewrite-service-query','PR-06':'summarize-conversation','PR-07':'extract-document-fields','PR-08':'draft-customer-message','PR-09':'prepare-handoff-note'};
export const environmentFor=stage=>stage==='experiment'?'experiment':stage==='control'?'staging':'production';
export function sessionLabel(state,id){const first=state.traces.find(t=>t.sessionId===id);return first?`${first.root.name} · ${first.caseId}`:'New conversation';}
export function modelFor(promptId,stage='history'){return stage==='experiment'?modelPolicy.experiment_model:modelPolicy.model_by_prompt[promptId];}
export function costFor(model,input,output,multiplier=modelPolicy.synthetic_cost_multiplier){const prices=modelPolicy.models[model];return {input:input*prices.input_per_million*multiplier/1e6,output:output*prices.output_per_million*multiplier/1e6,total:(input*prices.input_per_million+output*prices.output_per_million)*multiplier/1e6};}
export const definitions=[
 ['E-01','dark_side_delivery','The Dark Side of Customer Service','reply','0 ordinary; 0.5 isolated theatrical wording; 1 recognisable theatrical voice, at most one restrained space metaphor.'],
 ['E-02','record_fidelity','Record fidelity','reply','Correct requested facts and material conditions. Honest uncertainty passes; Not applicable when no factual issue applies. Failure to answer an answerable factual question is Fail.'],
 ['E-03','claim_support','Grounded claims','reply','Every substantive claim is supported by the supplied record. Not applicable when no substantive claim exists.'],
 ['E-04','respectful_tone','Respectful tone','reply','No insult, threat, contempt or mockery aimed at the user.'],
 ['E-05','user_contradiction','User contradiction','input','Conflicting factual self-report without acknowledging correction. Explicit corrections are not contradictions.'],
 ['E-06','expressed_frustration','Expressed frustration','input','Explicit agitation in the current message. Quoting someone else is not evidence of the speaker’s frustration.'],
 ['E-07','user_profanity','User profanity','input','Profanity in the current message, including quotations. Comments distinguish direct from quoted.'],
 ['E-08','user_disagreement','User disagreement','input','Challenges a preceding assistant assertion. Correcting one’s own statement is not disagreement with the assistant.'],
 ['E-09','intent_correct','Intent correctness','reply','Selected intent equals the authored label.'],
 ['E-10','query_constraints_preserved','Query constraints','reply','Preserves material entities, amounts, deposit type and period.'],
 ['E-11','handoff_fidelity','Handoff fidelity','reply','Preserves facts, correction, uncertainty and unresolved work; invents no action.'],
 ['E-12','extraction_match','Extraction match','reply','Fields equal the authored expected object, including missing fields as null.'],
 ['F-01','user-thumbs','Customer feedback','feedback','Explicit thumbs up or down with an optional comment on the saved request root. Separate from inferred E-08 disagreement; one submission per reply.']
].map(([id,name,title,subject,rubric])=>({id,name,title,subject,rubric,dataType:id==='F-01'?'BOOLEAN':['E-02','E-03'].includes(id)?'CATEGORICAL':'NUMERIC',revision:['E-02','E-03'].includes(id)?'r2':'r1',producer:id==='F-01'?'Human feedback': ['E-09','E-12'].includes(id)?'Proposed deterministic check':'Proposed LLM judge'}));
export const byDef=id=>definitions.find(d=>d.id===id);
export const factualCategories=['Pass','Fail','Not applicable'];
export function scoreDisplay(id,value){
 if(byDef(id)?.dataType!=='CATEGORICAL')return value??'Pending';
 if(value===1)return 'Pass';
 if(value===0)return 'Fail';
 if(value===null)return 'Not applicable';
 if(factualCategories.includes(value))return value;
 if(value===undefined)return 'Pending';
 throw new Error(`Invalid authored factual outcome: ${id}=${value}`);
}
export function categoryCounts(records,id){
 return Object.fromEntries(factualCategories.map(category=>[category,records.filter(r=>r.definitionId===id&&r.status==='complete'&&r.stringValue===category).length]));
}
const zeroInput={'E-05':0,'E-06':0,'E-07':0,'E-08':0};
const asText=value=>typeof value==='string'?value:JSON.stringify(value);
const baseTime=Date.parse('2026-10-08T09:00:00Z');
export function systemFor(promptId,version){
 if(promptId==='PR-01')return version===9?product.prompt_comparison.candidate_system:product.prompt_comparison.baseline_system;
 const p=portfolio.prompts.find(p=>p.id===promptId);return p.current_system_prompt_proposal||`${p.purpose} Use only the supplied source. Preserve conditions and unknowns. ${p.input_output}.`;
}
export function makeTrace({id,sessionId,caseId,promptId='PR-01',version=7,user,reply,prior=[],source=product.source,stage='history',expected={},seconds=0,comment=''}){
 const p=portfolio.prompts.find(p=>p.id===promptId),rootId=id+'-root',genId=id+'-reply';
 const startTime=new Date(baseTime+(stage==='history'?-86400000:0)+seconds*1000),endTime=new Date(+startTime+1040);
 const context={current_user_message:user,prior_messages:prior,reference_context:source};
 const model=modelFor(promptId,stage),usageDetails={input:680,output:version===9?215:180},multiplier=stage==='live-demo'?1:modelPolicy.synthetic_cost_multiplier;
 const common={traceId:id,sessionId,startTime,endTime,level:'DEFAULT',children:[],metadata:{application_id:p.application_id,environment:environmentFor(stage),evidence_kind:'fixture',evaluation_mode:'preview',fixture_stage:stage,fixture_case_id:caseId,model_policy_revision:modelPolicy.revision}};
 const gen={...common,id:genId,parentObservationId:rootId,type:'GENERATION',name:'generate-response',promptId,promptName:p.name,promptVersion:version,model,usageDetails,costDetails:costFor(model,usageDetails.input,usageDetails.output,multiplier),input:[{role:'system',content:systemFor(promptId,version)+'\n\nReference context: '+JSON.stringify(source)},...prior,{role:'user',content:user}],output:{role:'assistant',content:reply},metadata:{...common.metadata,prompt_name:p.name,prompt_version:version,resolved_version:version,prompt_label:stage==='live-demo'?'production':undefined,evaluation_subject:'assistant_reply',...context,assistant_reply:reply,cost_source:'authored fixture estimate',synthetic_cost_multiplier:multiplier},children:[]};
 const root={...common,id:rootId,parentObservationId:null,isRootObservation:true,type:'AGENT',name:rootNameByPrompt[promptId],input:{role:'user',content:user},output:{role:'assistant',content:reply},metadata:{...common.metadata,evaluation_subject:'user_input',...context},children:[gen]};
 const trace={id,rootId,genId,sessionId,caseId,promptId,version,user,reply,prior,stage,startTime,endTime,root,nodes:[root,gen],expected,comment};
 return trace;
}
export function traceScores(trace,{outputOnly=false}={}){
 return Object.entries(trace.expected).filter(([id])=>!outputOnly||byDef(id).subject==='reply').map(([id,value])=>{
 const def=byDef(id),observationId=def.subject==='input'?trace.rootId:trace.genId;
 let reason=trace.comment||'Assessed against the supplied case and evaluation criteria.';
 if(def.subject==='input'){
  reason=id==='E-05'?(value?'An unacknowledged factual self-report conflicts with prior context.':'No unacknowledged conflict; an explicit correction is a valid update.'):
  id==='E-06'?(value?'The current user explicitly expresses frustration.':'No direct expression of frustration; a quotation alone does not establish it.'):
  id==='E-07'?(value?(trace.caseId==='C-07'?'Quoted profanity is present; not directed abuse.':'Direct profanity is present in the current user message.'):'No profanity in the current user message.'):
  value?'The user challenges the preceding assistant answer. This does not prove that answer was wrong.':'No challenge to an assistant assertion; self-correction alone does not qualify.';
 }
 return {id:`${trace.id}:${id}:${def.revision}`,definitionId:id,revision:def.revision,name:def.name,value:def.dataType==='CATEGORICAL'?undefined:value,stringValue:def.dataType==='CATEGORICAL'?scoreDisplay(id,value):undefined,dataType:def.dataType,authoredValue:value,source:'API',observationId,traceId:trace.id,sessionId:trace.sessionId,caseId:trace.caseId,promptId:trace.promptId,stage:trace.stage,producer:def.producer,evidence:'Authored fixture; no evaluator executed',status:'complete',applicability:value===null?'not_applicable':'applicable',comment:reason, timestamp:trace.endTime};
 });
}
export function caseTrace(c,version,id,stage='history',override={}){
 return makeTrace({id,sessionId:id+'-session',caseId:c.id,user:c.input.user_message,prior:c.input.conversation_history,reply:version===9?c.candidate_output:c.baseline_output,version,stage,expected:version===9?c.expected_candidate_scores:c.expected_baseline_scores,comment:c.score_comment,...override});
}
export function referenceSession(){
 let prior=[];return product.conversation.turns.map((t,i)=>{
 const trace=makeTrace({id:'REFERENCE-'+t.id,sessionId:'SESSION-01',caseId:t.id,version:9,user:t.user,reply:t.assistant,prior:[...prior],stage:'reference-session',seconds:t.after_seconds,expected:t.expected_scores,comment:'Response assessed against the supplied product information and evaluation criteria.'});
 prior.push({role:'user',content:t.user},{role:'assistant',content:t.assistant});return trace;
 });
}
export function flowTrace(){
 const id='FLOW-01',sessionId='FLOW-01-session',rootId=id+'-root';
 const source=product.source,common={traceId:id,sessionId,level:'DEFAULT',children:[]};
 const nodes=[['PR-04','fees'],['PR-05','monthly fee waiver own-account transfer'],['TOOL',source],['PR-09',examples.cases.find(c=>c.id==='PC-09').expected_output]].map(([pid,out],i)=>{
  const p=portfolio.prompts.find(p=>p.id===pid),operation=p?.operation_id||'SIM-LOOKUP',model=p?modelFor(pid):undefined;
  return {...common,id:id+'-'+operation,parentObservationId:rootId,type:p?'GENERATION':'TOOL',name:p?'generate-response':'retrieve-product-context',promptId:p?.id,promptName:p?.name,promptVersion:p?7:undefined,model,...(p?{usageDetails:{input:680,output:180},costDetails:costFor(model,680,180)}:{}),startTime:new Date(baseTime-86400000+i*700),endTime:new Date(baseTime-86400000+i*700+650),input:i===0?{role:'user',content:portfolio.multi_prompt_example.user_request}:i===1?{role:'user',content:portfolio.multi_prompt_example.user_request}:i===2?{query:'monthly fee waiver own-account transfer'}:{intent:'fees',reference:source,account_ledger:'unavailable',user_request:portfolio.multi_prompt_example.user_request},output:pid==='PR-04'?{intent:out}:out,metadata:{operation_id:operation,environment:'production',evidence_kind:'fixture',evaluation_mode:'preview',source_id:'SRC-01',...(p?{prompt_name:p.name,prompt_version:7,resolved_version:7,cost_source:'authored fixture estimate',synthetic_cost_multiplier:modelPolicy.synthetic_cost_multiplier}:{} )}};
 });
 const root={...common,id:rootId,isRootObservation:true,type:'AGENT',name:'review-service-request',startTime:new Date(baseTime-86400000),endTime:new Date(baseTime-86400000+3000),input:{role:'user',content:portfolio.multi_prompt_example.user_request},output:{role:'assistant',content:nodes[3].output},metadata:{environment:'production',evidence_kind:'fixture',evaluation_mode:'preview'},children:nodes};
 return {id,sessionId,caseId:'FLOW-01',rootId,genId:nodes[3].id,root,nodes:[root,...nodes],stage:'history',expected:{},user:portfolio.multi_prompt_example.user_request,reply:nodes[3].output};
}
export function initialState(){
 const traces=[...product.cases.map(c=>caseTrace(c,7,'HISTORY-'+c.id)),...product.negative_controls.map(c=>caseTrace(product.cases.find(x=>x.id===c.case_id),9,c.id,'control',{caseId:c.id,reply:c.output,expected:c.expected,comment:c.reason})),...referenceSession()];
 for(const c of examples.cases){traces.push(makeTrace({id:'HISTORY-'+c.id,sessionId:'HISTORY-'+c.id+'-session',caseId:c.id,promptId:c.prompt_id,user:asText(c.input),reply:c.expected_output,source:c.source||product.source,stage:'history',expected:c.expected_scores}));}
 const flow=flowTrace();traces.push(flow);
 const scores=traces.flatMap(t=>traceScores(t));
 for(const [pid,eid] of [['PR-04','E-09'],['PR-05','E-10'],['PR-09','E-11']]){
  const node=flow.nodes.find(n=>n.promptId===pid);scores.push(...traceScores({...flow,expected:{[eid]:1},genId:node.id,promptId:pid,comment:'The operation output preserves the supplied request and reference.'}));
 }
 return {production:7,candidate:null,role:'member',traces,scores,experiment:null,pending:null,chatSessions:{'PR-01':null,'PR-02':null,'PR-03':null},serial:0,notice:'',audit:[]};
}
export function transition(state,action){
 const s={...state,notice:''};
 switch(action.type){
 case 'role':return {...s,role:action.role};
 case 'save':
  if(s.candidate&&action.text!==s.candidate.text)return {...s,notice:'Version 9 already exists. Reset this local rehearsal to try a different draft; existing versions remain immutable.'};
  if(!action.text?.trim())return {...s,notice:'A prompt needs instructions before it can be saved.'};
  return {...s,candidate:{version:9,text:action.text,label:'staging',fixtureMatches:action.text.trim()===product.prompt_comparison.candidate_system.trim()},notice:'Version 9 saved to staging. Production has not moved.'};
 case 'startExperiment':
  if(!s.candidate)return {...s,notice:'Save a candidate before running an experiment.'};
  if(!s.candidate.fixtureMatches)return {...s,notice:'This prototype has authored outcomes for the supplied candidate only. Restore it to rehearse; custom text needs a real model run in the implementation.'};
  return {...s,experiment:{status:'pending',scenario:action.scenario||'expected',traces:[]},notice:'Comparison queued. Complete the run to inspect outcomes.'};
 case 'finishExperiment':{
  if(s.experiment?.status!=='pending')return s;
  const run=++s.serial,ids=[];const added=[];
  for(const c of product.cases)for(const version of [7,9]){
   const id=`EXP-${run}-v${version}-${c.id}`,override={};
   if(version===9&&s.experiment.scenario==='mixed'&&c.id==='C-02'){const control=product.negative_controls[0];Object.assign(override,{reply:control.output,expected:control.expected,comment:control.reason});}
   if(version===9&&s.experiment.scenario==='flat')Object.assign(override,{reply:c.baseline_output,expected:c.expected_baseline_scores,comment:'The candidate output retains an ordinary speaking style.'});
   added.push(caseTrace(c,version,id,'experiment',override));ids.push(id);
  }
  return {...s,traces:[...s.traces,...added],scores:[...s.scores,...added.flatMap(t=>traceScores(t,{outputOnly:true}))],experiment:{...s.experiment,status:'complete',traces:ids,run},notice:'Experiment complete. Inspect the results; the next decision belongs to the presenter.'};
 }
 case 'promote':
  if(s.role!=='admin')return {...s,notice:'Production is protected. A member can edit staging; only the simulated admin can move production.'};
  if(!s.candidate)return {...s,notice:'Create a staging version first.'};
  return {...s,production:9,audit:[...s.audit,{action:'promotion',from:s.production,to:9,role:s.role}],notice:'Production now points to v9. The next request resolves v9; previous calls keep their recorded versions.'};
 case 'newSession':if(s.pending)return {...s,notice:'Finish the pending request before starting a new conversation.'};return {...s,chatSessions:{...s.chatSessions,[action.promptId]:null},notice:'New conversation ready.'};
 case 'send':{
  if(s.pending)return {...s,notice:'Finish the pending request first.'};
  if(action.promptId==='PR-01'&&s.production===9&&!s.candidate?.fixtureMatches)return {...s,notice:'The promoted text has no matching response fixture. Restore the supplied candidate, or defer real execution to authoring.'};
  const pid=action.promptId,existing=s.chatSessions[pid],priorTraces=s.traces.filter(t=>t.sessionId===existing),prior=priorTraces.flatMap(t=>[{role:'user',content:t.user},{role:'assistant',content:t.reply}]);
  const n=s.serial+1,sessionId=existing||`LIVE-${pid}-${n}`,version=pid==='PR-01'?s.production:7;
  let user=action.text.trim(),reply,expected,caseId,source=product.source;
  const turn=product.conversation.turns.find(t=>t.user===user),c=product.cases.find(c=>c.input.user_message===user);
  if(pid==='PR-01'){
   if(turn){reply=version===9?turn.assistant:({ 'T-01':product.cases[0].baseline_output,'T-02':product.cases.find(c=>c.id==='C-04').baseline_output,'T-03':product.cases.find(c=>c.id==='C-05').baseline_output,'T-04':'You need valid photo ID and proof of address dated within the last three months. Processing takes two working days after complete documents arrive.'}[turn.id]);expected={...turn.expected_scores,'E-01':version===9?1:0};caseId=turn.id;}
   else if(c){reply=version===9?c.candidate_output:c.baseline_output;expected=version===9?c.expected_candidate_scores:c.expected_baseline_scores;caseId=c.id;}
  }else{const c=examples.cases.find(c=>c.prompt_id===pid);if(user===c.input||user===c.control_input){reply=user===c.input?c.expected_output:c.control_output;expected={...c.expected_scores,...zeroInput};caseId=c.id;}}
  if(reply===undefined)return {...s,notice:'This local prototype recognises the supplied example messages. Choose a suggestion to continue; no model was called.'};
  // Only replay input labels whose required context is actually present.
  expected={...expected};if(!prior.length){expected['E-05']=0;expected['E-08']=0;}
  const trace=makeTrace({id:`LIVE-REQUEST-${n}`,sessionId,caseId,promptId:pid,version,user,reply,prior,source,stage:'live-demo',seconds:n*24,expected,comment:'Response assessed against the supplied product information and evaluation criteria.'});
  return {...s,serial:n,pending:{trace,phase:'fetch'},chatSessions:{...s.chatSessions,[pid]:sessionId},notice:`Resolving the production label for this request (v${version}).`};
 }
 case 'receive':{
  if(s.pending?.phase!=='fetch')return s;
  return {...s,traces:[...s.traces,s.pending.trace],pending:{...s.pending,phase:'evaluation'},notice:'Reply recorded in the session. Input and reply evaluations are pending.'};
 }
 case 'evaluate':{
  if(s.pending?.phase!=='evaluation')return s;
  return {...s,scores:[...s.scores,...traceScores(s.pending.trace)],pending:null,notice:'Both evaluation tracks are now visible on their own observations.'};
 }
 case 'feedback':{
  const trace=s.traces.find(t=>t.id===action.traceId);if(!trace)return {...s,notice:'Reply is not saved yet.'};
  if(![0,1].includes(action.value)||typeof action.value!=='number'||(action.comment!==undefined&&typeof action.comment!=='string')||(action.comment||'').length>1000)return {...s,notice:'Choose thumbs up or down and a comment of at most 1,000 characters.'};
  const id=trace.id+':F-01',comment=(action.comment||'').trim(),existing=s.scores.find(r=>r.id===id);
  if(existing)return {...s,notice:existing.value===action.value&&existing.comment===comment?'Feedback already saved on this reply.':'Feedback has already been submitted for this reply.'};
  const record={id,definitionId:'F-01',revision:byDef('F-01').revision,name:'user-thumbs',value:action.value,dataType:'BOOLEAN',source:'API',traceId:trace.id,observationId:trace.rootId,sessionId:trace.sessionId,caseId:trace.caseId,stage:trace.stage,producer:'Human feedback',signal_source:'explicit-user-feedback',evidence:'Local prototype interaction',comment,status:'complete',timestamp:new Date()};
  return {...s,scores:[...s.scores,record],notice:'Feedback saved on the request root for this reply.'};
 }
 case 'reset':return initialState();
 default:return s;
 }
}
export const recordsFor=(state,observationId)=>state.scores.filter(r=>r.observationId===observationId);
export function visibleTotals(state){return {records:new Set(state.scores.map(r=>r.id)).size,definitions:new Set(state.scores.map(r=>r.definitionId)).size,observations:new Set(state.traces.flatMap(t=>t.nodes.map(n=>n.id))).size,traces:state.traces.length};}
export function coverage(state){return [
 {id:'P-01',feature:'Prompt portfolio & version links',purpose:'Find nine prompts; inspect the actual resolved version.',scoreIds:[],evidence:portfolio.prompts.map(p=>p.id),fidelity:'Prompt portfolio and trace links'},
 {id:'P-02',feature:'Paired experiment',purpose:'Compare the same eight inputs without a release gate.',scoreIds:state.scores.filter(r=>r.stage==='experiment').map(r=>r.id),evidence:state.traces.filter(t=>t.stage==='experiment').map(t=>t.id),fidelity:'Paired output comparison'},
 {id:'P-03',feature:'Multi-prompt provenance',purpose:'Each generation keeps its own prompt; lookup has none.',scoreIds:state.scores.filter(r=>r.traceId==='FLOW-01').map(r=>r.id),evidence:['FLOW-01'],fidelity:'Prompt references and operation details'},
 {id:'P-04a',feature:'What the chatbot hears',purpose:'Distinct contradiction, frustration, profanity and disagreement.',scoreIds:state.scores.filter(r=>byDef(r.definitionId)?.subject==='input').map(r=>r.id),evidence:product.cases.map(c=>c.id),fidelity:'Request input scores'},
 {id:'P-04b',feature:'What the chatbot says',purpose:'Style, facts, grounding and tone on reply generations.',scoreIds:state.scores.filter(r=>byDef(r.definitionId)?.subject==='reply'&&r.stage!=='experiment'&&['PR-01','PR-02','PR-03'].includes(r.promptId)).map(r=>r.id),evidence:['SESSION-01','CTRL-01','CTRL-02','CTRL-03'],fidelity:'Reply generation scores'},
 {id:'PH-01',feature:'Background task quality',purpose:'Task-specific checks for the six background prompt families.',scoreIds:state.scores.filter(r=>r.promptId&&!['PR-01','PR-02','PR-03'].includes(r.promptId)&&r.traceId!=='FLOW-01').map(r=>r.id),evidence:examples.cases.filter(c=>!['PR-02','PR-03'].includes(c.prompt_id)).map(c=>c.id),fidelity:'Task-specific outputs and checks'},
 {id:'P-04c',feature:'Protected promotion & session',purpose:'Admin moves production; new calls resolve that version.',scoreIds:[],evidence:['PR-01/v7','PR-01/v9','SESSION-01'],fidelity:'Protected promotion and conversation replay'},
 {id:'F-01',feature:'Customer feedback',purpose:'One stable root target per saved reply.',scoreIds:state.scores.filter(r=>r.definitionId==='F-01').map(r=>r.id),evidence:state.scores.filter(r=>r.definitionId==='F-01').map(r=>r.observationId),fidelity:'Explicit user feedback'}
 ];}
