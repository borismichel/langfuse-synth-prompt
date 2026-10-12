// Exercise actual rendering and async submission with deliberately delayed responses.
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const {runInNewContext} = require('node:vm');
class Node {
  constructor(tag, text='') { this.tag=tag; this.text=text; this.children=[]; this.value=''; }
  set textContent(text) { this.text=text; this.children=[]; }
  get textContent() { return this.text+this.children.map(n=>n.textContent).join(''); }
  set innerHTML(_) { throw Error('User content must stay inert'); }
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren(...nodes) { this.children=nodes; this.text=''; }
  setAttribute() {} removeAttribute() {} focus() { this.focused=true; }
}
const all=n=>[n,...n.children.flatMap(all)];
const source=readFileSync(process.env.COMPANION_JS || 'src/synth/companion/static/app.js','utf8');
function setup() {
  const nodes={}; const requests=[];
  const context={
    document:{body:{dataset:{}},getElementById:id=>nodes[id] ||= new Node('div'),
      createElement:tag=>new Node(tag),createTextNode:text=>new Node('#text',text),querySelectorAll:()=>[]},
    location:{search:''},URLSearchParams,crypto:{randomUUID:()=> 'request-id'},
    fetch:(url,options)=>new Promise((resolve,reject)=>requests.push({url,options,reject,
      answer:body=>resolve({ok:true,json:async()=>body})}))
  };
  runInNewContext(source.slice(0,source.indexOf("$('save-feedback').onclick"))+`\nbots=[{id:'PR-01',title:'Product guide',suggestions:[]}];render();`,context);
  return {nodes,requests,send:context.send};
}
const tick=()=>new Promise(resolve=>setImmediate(resolve));
const users=nodes=>all(nodes.transcript).filter(n=>n.className==='chat-message user-message').map(n=>n.children[1].textContent);
(async()=>{
  const {nodes,requests,send}=setup();
  const question='<img src=x onerror=alert(1)>\nWhat is the fee?';
  nodes.message.value=question;
  const first=send(question);
  assert.deepEqual(users(nodes),[question],'User message appears before session creation completes');
  assert.equal(nodes.message.value,'','Composer clears immediately');
  assert.equal(nodes.transcript.children.at(-1).textContent,'Thinking…');
  assert.ok(!nodes.transcript.textContent.includes('Let’s make sense'));
  await send('duplicate'); assert.equal(requests.length,1,'Busy state prevents duplicate submits');
  requests[0].answer({session_id:'session',token:'token'}); await tick();
  assert.deepEqual(users(nodes),[question],'Pending message survives session creation');
  assert.equal(JSON.parse(requests[1].options.body).message,question);
  requests[1].answer({user:question,reply:'The fee is €4.',status:'complete'}); await first;
  assert.deepEqual(users(nodes),[question],'Canonical turn replaces pending bubble without duplication');
  assert.ok(nodes.transcript.textContent.includes('The fee is €4.'));
  assert.ok(!nodes.transcript.textContent.includes('Thinking…'));
  assert.equal(nodes.message.disabled,false);
  const second=send('And eligibility?'); await tick();
  assert.deepEqual(users(nodes),[question,'And eligibility?'],'Earlier history stays visible');
  requests[2].reject(Error('Connection lost')); await second;
  assert.deepEqual(users(nodes),[question],'Failed request does not invent a saved turn');
  assert.equal(nodes.message.value,'And eligibility?','Draft is restored for retry');
  assert.equal(nodes.notice.textContent,'Connection lost');
  const third=send('Try again'); await tick();
  requests[3].answer({user:'Try again',reply:'',status:'failed',error:'Model unavailable'}); await third;
  assert.deepEqual(users(nodes),[question,'Try again']);
  assert.ok(nodes.transcript.textContent.includes('Model unavailable'));
  const fresh=setup(); const failed=fresh.send('First question');
  fresh.requests[0].reject(Error('Session unavailable')); await failed;
  assert.deepEqual(users(fresh.nodes),[]);
  assert.equal(fresh.nodes.message.value,'First question');
  assert.equal(fresh.nodes.message.disabled,false);
  console.log('Pending chat passed: immediate user bubble, cleared composer, history, inert text, no duplicates, session/turn failure recovery.');
})().catch(error=>{console.error(error);process.exitCode=1});
