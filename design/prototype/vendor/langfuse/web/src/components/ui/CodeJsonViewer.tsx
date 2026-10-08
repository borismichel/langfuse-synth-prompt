// LOCAL FIXTURE ADAPTER — not upstream Langfuse source.
export function JSONView({json}:any){return <pre>{JSON.stringify(json,null,2)}</pre>}
