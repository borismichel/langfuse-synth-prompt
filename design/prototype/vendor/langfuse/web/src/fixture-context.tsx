// LOCAL FIXTURE ADAPTER — not upstream Langfuse source.
import {createContext,useContext} from 'react'; export const FixtureContext=createContext<any>(null); export const useFixture=()=>useContext(FixtureContext);
