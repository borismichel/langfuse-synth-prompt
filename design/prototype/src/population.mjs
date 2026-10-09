// Authored aggregate preview. No representative fixture is extrapolated into a measured trend.
import {modelPolicy,modelFor,costFor} from './model.mjs';
export const usage=[540,325,215,240,240,120,80,100,240];
export const versions=[{version:1,n:77,input:800,output:240,latency:1480},{version:3,n:135,input:770,output:215,latency:1370},{version:5,n:154,input:720,output:190,latency:1200},{version:6,n:97,input:690,output:180,latency:1060},{version:7,n:77,input:680,output:180,latency:1040}].map(v=>({...v,cost:costFor(modelFor('PR-01'),v.input,v.output).total,recordCounts:{Pass:v.n,Fail:0,'Not applicable':0},styleMedian:0}));
const weights=Array.from({length:28},(_,i)=>[13,14,15,15,14,11,10][i%7]);
const total=weights.reduce((a,b)=>a+b,0);
export const days=weights.map((v,i)=>({day:i-28,n:Math.floor(v/total*360)}));
for(let i=0,missing=360-days.reduce((s,d)=>s+d.n,0);i<missing;i++)days[i].n++;
export const hours=[{label:'00–09',n:90},{label:'09–17',n:144},{label:'17–24',n:126}];
export const lengths=[{label:'2 turns',n:144},{label:'3 turns',n:144},{label:'5 turns',n:72}];
export const promptAverages=[
 {input:680,output:180},
 {input:420,output:110},
 {input:510,output:140},
 {input:260,output:16},
 {input:320,output:32},
 {input:1300,output:210},
 {input:480,output:75},
 {input:500,output:125},
 {input:900,output:190}
].map((p,index)=>{const model=modelFor('PR-'+String(index+1).padStart(2,'0')),prices=modelPolicy.models[model];return {...p,model,rate:[prices.input_per_million,prices.output_per_million],syntheticCostMultiplier:modelPolicy.synthetic_cost_multiplier,cost:costFor(model,p.input,p.output).total};});
