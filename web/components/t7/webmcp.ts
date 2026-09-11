import {useEffect} from 'react';
export type T7Actions={state:()=>unknown;view:(view:string)=>Promise<unknown>;look:(yaw:number,pitch:number)=>Promise<unknown>;move:(direction:string,seconds:number)=>Promise<unknown>;interact:()=>Promise<unknown>;pause:()=>Promise<unknown>;reset:()=>Promise<unknown>};
type Tool={name:string;description:string;inputSchema:object;annotations:{readOnlyHint:boolean};execute:(input:unknown)=>unknown|Promise<unknown>};
type Registry={registerTool:(tool:Tool,options:{signal:AbortSignal})=>void|Promise<void>};
function object(input:unknown,allowed:string[]){
 if(!input||typeof input!=='object'||Array.isArray(input)||Object.keys(input).some(k=>!allowed.includes(k)))throw new Error('Argumentos no válidos.');return input as Record<string,unknown>;
}
export function useT7Tools(actions:React.RefObject<T7Actions>){
 useEffect(()=>{
  const context=(document as Document&{modelContext?:Registry}).modelContext;if(!context?.registerTool)return;
  const lifecycle=new AbortController();
  const schema=(properties:object,required:string[]=[])=>({type:'object',properties,required,additionalProperties:false});
  const tools:Tool[]=[
   {name:'read_apartment_state',description:'Read current view, visitor position, doors and local performance measurements.',inputSchema:schema({}),annotations:{readOnlyHint:true},execute:input=>{object(input,[]);return actions.current.state();}},
   {name:'set_apartment_view',description:'Switch the visible apartment to overview, top-down plan, or first-person walking. Walking resumes at the current safe position.',inputSchema:schema({view:{type:'string',enum:['inspect','top','walk']}},['view']),annotations:{readOnlyHint:false},execute:input=>{const a=object(input,['view']);if(!['inspect','top','walk'].includes(String(a.view)))throw new Error('Vista desconocida.');return actions.current.view(String(a.view));}},
   {name:'look_around_apartment',description:'Turn the first-person camera. Yaw in degrees: 90 west, 0 toward the top of the architectural plan. Pitch -60 to 60.',inputSchema:schema({yaw_degrees:{type:'number',minimum:-360,maximum:360},pitch_degrees:{type:'number',minimum:-60,maximum:60}},['yaw_degrees','pitch_degrees']),annotations:{readOnlyHint:false},execute:input=>{const a=object(input,['yaw_degrees','pitch_degrees']);if(typeof a.yaw_degrees!=='number'||!Number.isFinite(a.yaw_degrees)||Math.abs(a.yaw_degrees)>360||typeof a.pitch_degrees!=='number'||!Number.isFinite(a.pitch_degrees)||Math.abs(a.pitch_degrees)>60)throw new Error('Ángulo no válido.');return actions.current.look(a.yaw_degrees,a.pitch_degrees);}},
   {name:'move_in_apartment',description:'Walk forward, backward or sideways with the same collision controller as WASD. Runs for 0.1–3 seconds, stops at obstacles and returns the actual resulting position. Requires an active unpaused walk.',inputSchema:schema({direction:{type:'string',enum:['forward','back','left','right']},seconds:{type:'number',minimum:.1,maximum:3}},['direction','seconds']),annotations:{readOnlyHint:false},execute:input=>{const a=object(input,['direction','seconds']);if(!['forward','back','left','right'].includes(String(a.direction))||typeof a.seconds!=='number'||!Number.isFinite(a.seconds)||a.seconds<.1||a.seconds>3)throw new Error('Movimiento no válido.');return actions.current.move(String(a.direction),a.seconds);}},
   {name:'interact_with_nearby_door',description:'Toggle the nearest reachable door or wardrobe leaf, using the same action as E. The safety motor stops at obstacles.',inputSchema:schema({}),annotations:{readOnlyHint:false},execute:input=>{object(input,[]);return actions.current.interact();}},
   {name:'pause_apartment_walk',description:'Pause walking and release the pointer.',inputSchema:schema({}),annotations:{readOnlyHint:false},execute:input=>{object(input,[]);return actions.current.pause();}},
   {name:'return_to_apartment_entrance',description:'Use the visible return-to-entrance action. Reset only succeeds when the entrance is free and leaves the walk paused.',inputSchema:schema({}),annotations:{readOnlyHint:false},execute:input=>{object(input,[]);return actions.current.reset();}},
  ];
  for(const tool of tools)try{void Promise.resolve(context.registerTool(tool,{signal:lifecycle.signal})).catch(()=>{});}catch{/* Browsers without the optional bridge retain all visible controls. */}
  return()=>lifecycle.abort();
 },[actions]);
}
