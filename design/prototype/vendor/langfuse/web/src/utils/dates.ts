// LOCAL FIXTURE ADAPTER — not upstream Langfuse source.
export const formatIntervalSeconds=(n:number)=>n<1?`${Math.round(n*1000)}ms`:`${n.toFixed(2)}s`;
