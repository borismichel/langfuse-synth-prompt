// LOCAL FIXTURE ADAPTER — not upstream Langfuse source.
import {useFixture} from '@/src/fixture-context'; export const useSelectTraceNode=(_source:string)=>useFixture().selectNode;
