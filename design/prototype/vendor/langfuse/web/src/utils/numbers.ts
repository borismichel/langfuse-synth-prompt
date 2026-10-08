// LOCAL FIXTURE ADAPTER — not upstream Langfuse source.
export const usdFormatter=(n:any)=>`$${Number(n).toFixed(4)}`; export const numberFormatter=(n:number,d=0)=>n.toLocaleString('en',{maximumFractionDigits:d});
