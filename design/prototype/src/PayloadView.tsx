import React,{useState} from 'react';
export const Json=({value}:any)=><pre className="json">{JSON.stringify(value,null,2)}</pre>;
function Structured({value,label='Structured content'}:any){return <section className="payload-data"><small>{label}</small><Json value={value}/></section>}
export function Message({message:m}:any){
 let content=m.content;
 if(m.role==='tool'&&typeof content==='string'){try{content=JSON.parse(content)}catch{}}
 return <article className={'payload-message role-'+m.role}><header><strong>{m.role==='system'?'System':m.role==='user'?'User':m.role==='assistant'?'Assistant':'Tool result'}</strong>{m.tool_call_id&&<code>{m.tool_call_id}</code>}</header>
 {typeof content==='string'?<p className="message-text">{content}</p>:content!=null?<Structured value={content}/>:null}
 {m.tool_calls?.map((call:any)=><section className="tool-invocation" key={call.id}><strong>Tool call · {call.function?.name||call.name}</strong><code>{call.id}</code><Structured label="Arguments" value={typeof call.function?.arguments==='string'?JSON.parse(call.function.arguments):call.arguments}/></section>)}
 </article>
}
export default function PayloadView({value,title}:any){const [raw,setRaw]=useState(false);const messages=Array.isArray(value)&&value.every(m=>m?.role)?value:value?.messages||(value?.role?[value]:null);
 const extra=messages&&value?.messages?Object.fromEntries(Object.entries(value).filter(([k])=>k!=='messages')):null;
 return <section className="payload"><header className="payload-heading"><h3>{title}</h3><button onClick={()=>setRaw(!raw)}>{raw?'Formatted':'Raw JSON'}</button></header>{raw?<Json value={value}/>:messages?<>{messages.map((m:any,i:number)=>m.role==='system'?<details className="system-message" key={i}><summary>System message</summary><Message message={m}/></details>:<Message key={i} message={m}/>)}{extra&&Object.keys(extra).length>0&&<Structured label="Structured input · tool definitions" value={extra}/>}</>:typeof value==='string'?<p className="message-text">{value}</p>:<Structured value={value} label={'Structured '+title.toLowerCase()}/>}</section>
}
