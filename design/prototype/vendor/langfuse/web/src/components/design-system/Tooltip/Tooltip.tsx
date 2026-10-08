// LOCAL FIXTURE ADAPTER — not upstream Langfuse source.
export function Tooltip({label,children}:any){return children({getTriggerProps:()=>({title:typeof label==='string'?label:undefined})});}
