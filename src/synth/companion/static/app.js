'use strict';
const $ = id => document.getElementById(id);
const base = document.body.dataset.base;
const preview = document.body.dataset.preview === 'true';
const chats = new Map();
let bots = [], current = 'PR-01', busy = false, feedback = null, returnFocus = null;
const params = new URLSearchParams(location.search);
function appearance() {
  const dark = params.get('theme') === 'dark';
  $('app').classList.toggle('dark', dark);
  document.documentElement.style.colorScheme = dark ? 'dark' : 'light';
  $('theme').textContent = dark ? 'Light mode' : 'Dark mode';
  const variant = ['0','1','2'].includes(params.get('layout')) ? params.get('layout') : '0';
  $('workspace').className = 'workspace layout-' + variant;
  $('layout').value = variant;
  history.replaceState(null, '', '?' + params.toString());
}
function notice(message) { $('notice').textContent = message; $('notice').hidden = !message; }
function element(tag, text, className) { const e = document.createElement(tag); if (text !== undefined) e.textContent = text; if (className) e.className = className; return e; }
function replyInline(tag, text) {
  const node = element(tag);
  let offset = 0;
  // A small Markdown subset: never interpret model content as HTML or links.
  for (const match of text.matchAll(/(?<!`)`([^`\n]+)`(?!`)|\*\*([^*\n]+)\*\*/g)) {
    node.append(document.createTextNode(text.slice(offset, match.index)), element(match[1] === undefined ? 'strong' : 'code', match[1] ?? match[2]));
    offset = match.index + match[0].length;
  }
  node.append(document.createTextNode(text.slice(offset)));
  return node;
}
function replyContent(text, className) {
  const content = element('div', undefined, ['reply-content', className].filter(Boolean).join(' '));
  const lines = text.replace(/\r\n?/g, '\n').split('\n');
  const heading = line => /^ {0,3}(#{1,6})\s+(.+?)\s*#*\s*$/.exec(line);
  const listItem = line => /^ {0,3}([-+*]|\d+[.)])\s+(.+)$/.exec(line);
  const rule = line => /^ {0,3}(?:(?:-\s*){3,}|(?:_\s*){3,}|(?:\*\s*){3,})$/.test(line);
  const cells = line => line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(cell => cell.trim());
  const tableHeader = index => {
    if (!lines[index]?.includes('|') || !lines[index + 1]?.includes('|')) return null;
    const header = cells(lines[index]), separator = cells(lines[index + 1]);
    return header.length > 1 && header.length === separator.length && separator.every(cell => /^:?-{3,}:?$/.test(cell)) ? header : null;
  };
  const startsBlock = index => heading(lines[index]) || rule(lines[index]) || listItem(lines[index]) || tableHeader(index);
  for (let index = 0; index < lines.length;) {
    if (!lines[index].trim()) { index++; continue; }
    const title = heading(lines[index]);
    if (title) { content.append(replyInline(title[1].length <= 3 ? 'h3' : 'h4', title[2])); index++; continue; }
    if (rule(lines[index])) { content.append(element('hr')); index++; continue; }
    const header = tableHeader(index);
    if (header) {
      const wrapper = element('div', undefined, 'reply-table-wrap'), table = element('table'), head = element('thead'), row = element('tr'), body = element('tbody');
      header.forEach(cell => { const th = replyInline('th', cell); th.scope = 'col'; row.append(th); });
      head.append(row); table.append(head, body); index += 2;
      while (index < lines.length && lines[index].includes('|')) {
        const values = cells(lines[index]);
        if (values.length !== header.length) break;
        const row = element('tr'); values.forEach(cell => row.append(replyInline('td', cell))); body.append(row); index++;
      }
      wrapper.append(table); content.append(wrapper); continue;
    }
    const firstItem = listItem(lines[index]);
    if (firstItem) {
      const ordered = /^\d/.test(firstItem[1]), list = element(ordered ? 'ol' : 'ul');
      while (index < lines.length) {
        const item = listItem(lines[index]);
        if (!item || /^\d/.test(item[1]) !== ordered || rule(lines[index])) break;
        const li = replyInline('li', item[2]);
        if (ordered) li.value = Number.parseInt(item[1], 10);
        list.append(li); index++;
      }
      content.append(list); continue;
    }
    const paragraph = [lines[index++]];
    while (index < lines.length && lines[index].trim() && !startsBlock(index)) paragraph.push(lines[index++]);
    content.append(replyInline('p', paragraph.join('\n')));
  }
  return content;
}
async function api(path, options = {}, session) {
  const response = await fetch(base + path, {...options, headers: {'Content-Type':'application/json', ...(session ? {'X-Conversation-Token':session.token} : {}), ...options.headers}});
  const data = await response.json();
  if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'The request could not be completed.');
  return data;
}
function setLink(id, url) { const a=$(id); a.setAttribute('aria-disabled', String(!url)); if(url) { a.href=url; a.target='_blank'; a.rel='noopener'; } else a.removeAttribute('href'); }
function updateControls() {
  $('send').disabled = busy || !$('message').value.trim();
  $('new').disabled = busy;
  $('message').disabled = busy;
  document.querySelectorAll('#bots>button,#suggestions button').forEach(b => b.disabled=busy);
  $('transcript').setAttribute('aria-busy', String(busy));
}
function botSpec() { return bots.find(b => b.id === current); }
function render() {
  const bot=botSpec(); if (!bot) return;
  const session=chats.get(current);
  $('bot-title').textContent=bot.title;
  document.querySelectorAll('#bots>button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.bot===current)));
  $('transcript').replaceChildren(); $('suggestions').replaceChildren(); $('inspector').replaceChildren();
  if (!session?.turns.length) {
    const empty=element('div',undefined,'chat-empty');
    empty.append(element('span','✳','welcome-star'),element('h2','Let’s make sense of it.'),element('p',current==='PR-01'?'Ask about the Everyday Account’s monthly fee. We can work through the details together.':current==='PR-02'?'Check how the withdrawal allowance affects a fee.':'Understand which documents you need and when processing starts.'));
    $('transcript').append(empty);
  }
  for (const turn of session?.turns || []) {
    const wrapper=element('div',undefined,'chat-turn');
    const user=element('div',undefined,'chat-message user-message');user.append(element('small','You'),element('p',turn.user));
    const reply=element('div',undefined,'chat-message assistant-message');reply.append(element('small',bot.title),turn.reply ? replyContent(turn.reply,turn.status==='failed'?'error-message':'') : element('p',turn.error || 'Reply in progress…',turn.status==='failed'?'error-message':''));
    if (turn.reply && turn.error) reply.append(element('p',turn.error,'error-message'));
    if(turn.status==='complete') {
      const f=element('div',undefined,'feedback');f.append(element('span','Was this helpful?'));
      for(const value of [1,0]) { const button=element('button',value?'Helpful':'Not helpful');button.setAttribute('aria-pressed',String(turn.feedback?.value===value));button.onclick=()=>openFeedback(session,turn,value,button);f.append(button); }
      reply.append(f);
    }
    wrapper.append(user,reply);$('transcript').append(wrapper);
    if(turn.trace_id) {
      const row=element('div',undefined,'identity-row');
      row.append(element('span',`${turn.prompt_name} · ${turn.prompt_version ? 'v'+turn.prompt_version : 'prompt unresolved'}`),element('code',`Feedback target: ${turn.root_observation_id}`));
      if(turn.observation_url){const a=element('a','Inspect generation ↗','text-button');a.href=turn.observation_url;a.target='_blank';a.rel='noopener';row.append(a);}
      const evaluation=element('button','Check evaluations','text-button');
      const state=element('span',preview?'Fixture preview · evaluators not run':'Evaluations pending','evaluation-note');
      evaluation.onclick=async()=>{evaluation.disabled=true;try{const result=await api(`/api/conversations/${session.session_id}/evaluations/${turn.request_id}`,{},session);state.textContent=result.message || `${result.received}/${result.expected} outcomes · ${result.status}`;if(result.scores?.length){state.textContent=`${result.received}/${result.expected} outcomes · ${result.status}. `+result.scores.map(s=>`${s.name}: ${s.value===null?'N/A':s.value}`).join(' · ');}}catch(e){state.textContent=e.message}finally{evaluation.disabled=false}};
      row.append(evaluation,state);$('inspector').append(row);
    }
  }
  if(busy) $('transcript').append(element('p','Retrieving the managed production prompt and preparing a reply…','pending-inline'));
  bot.suggestions.forEach(s=>{const button=element('button',s.label+' ↗');button.title=s.message;button.onclick=()=>send(s.message);$('suggestions').append(button)});
  const last=[...(session?.turns||[])].reverse().find(t=>t.session_url);
  setLink('session',last?.session_url);
  $('transcript').scrollTop=$('transcript').scrollHeight;
  updateControls();
}
async function ensureSession(){let session=chats.get(current);if(!session){session={...await api('/api/conversations',{method:'POST',body:JSON.stringify({prompt_id:current})}),turns:[]};chats.set(current,session)}return session;}
async function send(text) {
  if(busy||!text.trim())return;
  const original=text;busy=true;notice('');render();
  try{
    const session=await ensureSession();
    const turn=await api(`/api/conversations/${session.session_id}/turns`,{method:'POST',body:JSON.stringify({message:text,request_id:crypto.randomUUID()})},session);
    session.turns.push(turn);$('message').value='';
    if(turn.status==='failed')notice(turn.error);
  }catch(e){notice(e.message);$('message').value=original}
  finally{busy=false;render();$('message').focus()}
}
function openFeedback(session,turn,value,button){feedback={session,turn,value};returnFocus=button;$('feedback-comment').value=turn.feedback?.comment||'';$('feedback-target').textContent='Feedback stays attached to this reply’s saved request root.';$('feedback-dialog').hidden=false;$('feedback-comment').focus()}
function closeFeedback(){feedback=null;$('feedback-dialog').hidden=true;returnFocus?.focus()}
$('save-feedback').onclick=async()=>{if(!feedback)return;$('save-feedback').disabled=true;const {session,turn,value}=feedback;try{const f=await api(`/api/conversations/${session.session_id}/feedback`,{method:'POST',body:JSON.stringify({request_id:turn.request_id,value,comment:$('feedback-comment').value})},session);turn.feedback=f;closeFeedback();render();notice(preview?'Fixture feedback saved locally.':'Feedback submitted to the saved request root.');}catch(e){notice(e.message)}finally{$('save-feedback').disabled=false}};
$('cancel-feedback').onclick=closeFeedback;
$('feedback-dialog').addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();closeFeedback()}if(e.key==='Tab'){const first=$('feedback-comment'),last=$('cancel-feedback');if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}}});
$('composer').onsubmit=e=>{e.preventDefault();send($('message').value)};
$('message').oninput=updateControls;
$('new').onclick=()=>{chats.delete(current);notice('');render();$('message').focus()};
$('theme').onclick=()=>{params.set('theme',params.get('theme')==='dark'?'light':'dark');appearance()};
$('layout').onchange=()=>{params.set('layout',$('layout').value);appearance()};
document.addEventListener('keydown',e=>{if(e.target.matches('input,textarea,select')||!$('feedback-dialog').hidden)return;if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();params.set('layout',String((Number($('layout').value)+(e.key==='ArrowRight'?1:2))%3));appearance()}});
async function connection(){ $('refresh').disabled=true;try{const r=await api('/api/connection');for(const id of ['portfolio','experiments','sessions'])setLink(id,r.links?.[id]);$('health-status').textContent=r.ready?'Connected · managed production prompts refreshed · evaluator rules enabled':r.gaps.join(' ');if(!r.ready&&!preview)notice(r.gaps.join(' '));}catch(e){$('health-status').textContent=e.message}finally{$('refresh').disabled=false}}
$('refresh').onclick=connection;
async function init(){appearance();if(preview){$('mode-label').textContent='PREVIEW · Local fixtures · no model or Langfuse connection';$('footnote').textContent='Fictional product information · authored fixture replies'}try{bots=(await api('/api/catalog')).bots;for(const [i,b] of bots.entries()){const button=element('button');button.dataset.bot=b.id;button.append(element('span','0'+(i+1),'bot-number'));const span=element('span');span.append(element('b',b.title),element('small',['Understand the everyday account','Know what a fee means','Prepare your next step'][i]));button.append(span,element('span','›'));button.onclick=()=>{if(busy)return;current=b.id;notice('');$('message').value='';render()};$('bots').insertBefore(button,$('bots').querySelector('.context-card'));}render();await connection()}catch(e){notice(e.message)}}
init();
