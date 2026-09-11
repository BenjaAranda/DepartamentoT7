'use client';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, OrthographicCamera } from '@react-three/drei';
import { Euler, Object3D, PCFShadowMap } from 'three';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { loadBundle, disposeScene, type AssetBundle } from './asset-loader';
import { initPhysics, WalkEngine } from './walk-engine';
import { useT7Tools, type T7Actions } from './webmcp';

type Controls = { keys: Set<string>; yaw: number; pitch: number; command?:{f:number;r:number;left:number;finish:()=>void} };
type Mode = 'inspect' | 'top' | 'walk';
type Metrics = {frames:number[];drawCalls:number;triangles:number;textures:number;geometries:number;renderer:string;width:number;height:number};
const nextPaint=()=>new Promise<void>(resolve=>requestAnimationFrame(()=>requestAnimationFrame(()=>resolve())));
const doorNames: Record<string, string> = {O01:'Acceso',O02:'Dormitorio 3',O03:'Dormitorio 1',O04:'Dormitorio 2',O05:'Baño',O06:'Logia'};
function CeilingLight({position,active,lightweight}:{position:[number,number,number];active:boolean;lightweight:boolean}){
  const target=useMemo(()=>{const o=new Object3D();o.position.set(position[0],0,position[2]);return o;},[position]);
  const resolution=lightweight?512:1024;
  return <><primitive object={target}/><spotLight position={position} target={target} intensity={active?15:0} distance={6} angle={1.35} penumbra={.65} decay={2} color="#fff1d6" castShadow={active} shadow-mapSize={[resolution,resolution]} shadow-camera-near={.15} shadow-camera-far={6} shadow-bias={-.001} shadow-normalBias={.02}/></>;
}

function Scene({bundle,engine,mode,paused,controls,onStatus,metrics,lightweight}:{bundle:AssetBundle;engine:WalkEngine;mode:Mode;paused:boolean;controls:React.RefObject<Controls>;onStatus:(text:string)=>void;metrics:React.RefObject<Metrics>;lightweight:boolean}) {
  const {camera,gl,size}=useThree();
  const timer=useRef(0);
  useEffect(()=>{gl.shadowMap.autoUpdate=false;gl.shadowMap.needsUpdate=true;},[gl,bundle,mode,lightweight]);
  useEffect(()=>{
    bundle.scene.traverse(o=>{if(o.userData.inspection_hide)o.visible=mode==='walk';});
    if(mode==='inspect'){camera.position.set(14,10,8);camera.lookAt(6.3,0,-1.8);}
  },[bundle,camera,mode]);
  useFrame((_,delta)=>{
    if(engine.disposed)return;
    const input=controls.current;
    const f=input.command?.f??(Number(input.keys.has('KeyW')||input.keys.has('ArrowUp'))-Number(input.keys.has('KeyS')||input.keys.has('ArrowDown')));
    const r=input.command?.r??(Number(input.keys.has('KeyD'))-Number(input.keys.has('KeyA')));
    if(mode==='walk'&&!paused){
      if(input.keys.has('ArrowLeft'))input.yaw+=Math.min(delta,.1)*1.4;
      if(input.keys.has('ArrowRight'))input.yaw-=Math.min(delta,.1)*1.4;
    }
    engine.advance(delta,{x:-Math.sin(input.yaw)*f+Math.cos(input.yaw)*r,z:-Math.cos(input.yaw)*f-Math.sin(input.yaw)*r,paused:mode!=='walk'||paused});
    if(mode==='walk'&&!paused&&input.command){input.command.left-=Math.min(delta,.1);if(input.command.left<=0){input.command.finish();input.command=undefined;}}
    if(mode==='walk'&&!paused&&!document.hidden&&delta<.25){metrics.current.frames.push(delta*1000);if(metrics.current.frames.length>12000)metrics.current.frames.shift();}
    Object.assign(metrics.current,{drawCalls:gl.info.render.calls,triangles:gl.info.render.triangles,textures:gl.info.memory.textures,geometries:gl.info.memory.geometries,width:size.width,height:size.height});
    if(!metrics.current.renderer){const ctx=gl.getContext(),ext=ctx.getExtension('WEBGL_debug_renderer_info');metrics.current.renderer=ext?String(ctx.getParameter(ext.UNMASKED_RENDERER_WEBGL)):String(ctx.getParameter(ctx.RENDERER));}
    for(const door of engine.doors){
      const pivot=bundle.scene.getObjectByName(door.data.pivot_name||'');
      const angle=engine.doorPose(door.data,door.fraction).angle;
      if(pivot&&Math.abs(pivot.rotation.y-angle)>1e-8){pivot.rotation.y=angle;gl.shadowMap.needsUpdate=true;}
    }
    if(mode==='walk'){
      const eye=engine.eye;camera.position.set(eye.x,eye.y,eye.z);camera.quaternion.setFromEuler(new Euler(input.pitch,input.yaw,0,'YXZ'));
    }
    timer.current+=delta;
    if(timer.current>.2){timer.current=0;const door=engine.nearestDoor();onStatus(engine.message||(door?'E · '+(door.data.label||doorNames[door.data.opening||'']):'W A S D · Moverse'));}
  });
  const roomLights=(bundle.collision.finishes?.lights||[]).map(light=><CeilingLight key={light.id+(lightweight?'lite':'full')} position={light.position} active={mode==='walk'} lightweight={lightweight}/>);
  return <>
    <primitive object={bundle.scene}/>
    <hemisphereLight args={['#dfedfa','#d3d9dc',mode==='walk'?.85:2.2]}/>
    <directionalLight position={[3,15,8]} intensity={mode==='walk'?0:3} castShadow={mode==='inspect'} shadow-mapSize={[2048,2048]} shadow-camera-left={-18} shadow-camera-right={18} shadow-camera-top={18} shadow-camera-bottom={-18} shadow-bias={-.0005} shadow-normalBias={.02}/>
    {roomLights}
    {mode==='top'&&<OrthographicCamera makeDefault position={[6.3,20,-1.8]} rotation={[-Math.PI/2,0,0]} zoom={Math.min(size.width/14.5,size.height/7.8)} near={.1} far={50}/>}
    {mode==='inspect'&&<OrbitControls makeDefault target={[6.3,0,-1.8]} minDistance={5} maxDistance={32} maxPolarAngle={Math.PI/2-.04}/>}
  </>;
}

export default function Simulator(){
  const [bundle,setBundle]=useState<AssetBundle|null>(null);
  const [engine,setEngine]=useState<WalkEngine|null>(null);
  const [error,setError]=useState('');
  const [attempt,setAttempt]=useState(0);
  const [mode,setMode]=useState<Mode>('inspect');
  const [paused,setPaused]=useState(true);
  const [status,setStatus]=useState('');
  const [tab,setTab]=useState('model');
  const [loading,setLoading]=useState('Cargando el departamento…');
  const [help,setHelp]=useState(false);
  const [touch,setTouch]=useState(false);
  const [lightweight,setLightweight]=useState(false);
  const [info,setInfo]=useState(false);
  const [notice,setNotice]=useState('');
  const viewport=useRef<HTMLDivElement>(null);
  const controls=useRef<Controls>({keys:new Set(),yaw:Math.PI/2,pitch:0});
  const drag=useRef<{id:number;x:number;y:number}|null>(null);
  const touchStarted=useRef(0);
  const metrics=useRef<Metrics>({frames:[],drawCalls:0,triangles:0,textures:0,geometries:0,renderer:'',width:0,height:0});
  const onStatus=useCallback((s:string)=>setStatus(previous=>previous===s?previous:s),[]);
  useEffect(()=>{
    const abort=new AbortController();let owned:WalkEngine|undefined;let ownedAsset:AssetBundle|undefined;
    setError('');setBundle(null);setEngine(null);
    Promise.all([loadBundle('/models/manifest.json',abort.signal,setLoading),initPhysics()]).then(([asset])=>{
      if(abort.signal.aborted){disposeScene(asset.scene);return;}
      ownedAsset=asset;
      owned=new WalkEngine(asset.collision);setBundle(asset);setEngine(owned);
    }).catch(reason=>{if(!abort.signal.aborted)setError(reason instanceof Error?reason.message:'No se pudo cargar el departamento.');});
    return()=>{abort.abort();owned?.dispose();if(ownedAsset)disposeScene(ownedAsset.scene);};
  },[attempt]);
  const pause=useCallback(()=>{controls.current.keys.clear();controls.current.command?.finish();controls.current.command=undefined;drag.current=null;setPaused(true);if(document.pointerLockElement)document.exitPointerLock();},[]);
  useEffect(()=>{const coarse=matchMedia('(pointer:coarse)').matches;setTouch(coarse);setLightweight(coarse);},[]);
  useEffect(()=>{
    const keydown=(e:KeyboardEvent)=>{
      if(mode!=='walk'||paused)return;
      if(['KeyW','KeyA','KeyS','KeyD','ArrowUp','ArrowDown','ArrowLeft','ArrowRight','KeyE'].includes(e.code))e.preventDefault();
      controls.current.keys.add(e.code);
      if(e.code==='KeyE'&&!e.repeat)engine?.interact();
      if(e.code==='Escape')pause();
    };
    const keyup=(e:KeyboardEvent)=>controls.current.keys.delete(e.code);
    const move=(e:MouseEvent)=>{if(mode==='walk'&&!paused&&document.pointerLockElement){controls.current.yaw-=e.movementX*.002;controls.current.pitch=Math.max(-1.35,Math.min(1.35,controls.current.pitch-e.movementY*.002));}};
    const lock=()=>{if(!document.pointerLockElement){controls.current.keys.clear();setPaused(true);}};
    const visibility=()=>{if(document.hidden)pause();};
    window.addEventListener('keydown',keydown);window.addEventListener('keyup',keyup);window.addEventListener('mousemove',move);window.addEventListener('blur',pause);
    document.addEventListener('pointerlockchange',lock);document.addEventListener('visibilitychange',visibility);
    return()=>{window.removeEventListener('keydown',keydown);window.removeEventListener('keyup',keyup);window.removeEventListener('mousemove',move);window.removeEventListener('blur',pause);document.removeEventListener('pointerlockchange',lock);document.removeEventListener('visibilitychange',visibility);};
  },[engine,mode,paused,pause]);
  const enter=(lockPointer=true)=>{
    if(!engine)return;
    setTab('model');setMode('walk');setPaused(false);setHelp(false);setInfo(false);controls.current.keys.clear();
    const canvas=viewport.current?.querySelector('canvas');
    if(canvas&&lockPointer&&!touch)void canvas.requestPointerLock()?.catch(()=>{setPaused(false);setStatus('Arrastra para mirar o usa las flechas.');});
  };
  const inspect=()=>{pause();setMode('inspect');};
  const reset=()=>{pause();if(engine?.reset()){controls.current.yaw=Math.PI/2;controls.current.pitch=0;}};
  const fullscreen=async()=>{
    const target=viewport.current?.closest('main');
    if(!target?.requestFullscreen){setNotice('Este navegador no dispone de pantalla completa.');return;}
    try{if(document.fullscreenElement)await document.exitFullscreen();else await target.requestFullscreen();setNotice('');}
    catch{setNotice('Este navegador no permite activar pantalla completa.');}
  };
  const state=()=>{
    const sorted=[...metrics.current.frames].sort((a,b)=>a-b),sum=sorted.reduce((a,b)=>a+b,0);
    return {revision:bundle?.revision,mode,paused,eye:engine?.eye,yaw_degrees:controls.current.yaw*180/Math.PI,pitch_degrees:controls.current.pitch*180/Math.PI,area_m2:bundle?.collision.area_m2,useful_area_m2:bundle?.collision.useful_area_m2,doors:engine?.doors.map(d=>({id:d.data.id,label:d.data.label||doorNames[d.data.opening||''],fraction:d.fraction,blocked:d.blocked})),performance:{frames:sorted.length,measured_seconds:sum/1000,average_fps:sum?sorted.length*1000/sum:0,p95_frame_ms:sorted[Math.floor(sorted.length*.95)]||0,draw_calls:metrics.current.drawCalls,triangles:metrics.current.triangles,textures:metrics.current.textures,geometries:metrics.current.geometries,renderer:metrics.current.renderer,viewport:[metrics.current.width,metrics.current.height],dpr:devicePixelRatio,load_ms:bundle?.loadMs,asset_bytes:bundle?.bytes}};
  };
  const actions=useRef<T7Actions>({state:()=>({}),view:async()=>({}),look:async()=>({}),move:async()=>({}),interact:async()=>({}),pause:async()=>({}),reset:async()=>({})});
  actions.current={state,view:async view=>{if(!engine)throw new Error('El departamento todavía carga.');if(view==='walk')enter(false);else{pause();setTab('model');setMode(view as Mode);}await nextPaint();return actions.current.state();},look:async(yaw,pitch)=>{if(mode!=='walk')throw new Error('Primero inicia el recorrido.');controls.current.yaw=yaw*Math.PI/180;controls.current.pitch=pitch*Math.PI/180;await nextPaint();return actions.current.state();},move:async(direction,seconds)=>{if(mode!=='walk'||paused||!engine)throw new Error('Inicia o reanuda el recorrido antes de moverte.');if(controls.current.command)throw new Error('Ya hay un movimiento en curso.');await new Promise<void>((resolve,reject)=>{const timeout=window.setTimeout(()=>{controls.current.command=undefined;reject(new Error('Movimiento interrumpido.'));},8000);controls.current.command={f:direction==='forward'?1:direction==='back'?-1:0,r:direction==='right'?1:direction==='left'?-1:0,left:seconds,finish:()=>{clearTimeout(timeout);resolve();}};});await nextPaint();return actions.current.state();},interact:async()=>{if(mode!=='walk'||paused||!engine)throw new Error('Primero reanuda el recorrido.');if(!engine.nearestDoor())throw new Error('No hay una puerta al alcance.');engine.interact();await new Promise(resolve=>setTimeout(resolve,1050));return actions.current.state();},pause:async()=>{pause();await nextPaint();return actions.current.state();},reset:async()=>{reset();await nextPaint();return actions.current.state();}};
  useT7Tools(actions);
  return <main className="t7-workspace">
    <header className="t7-header"><div><p>LOS ALTOS DE ALGARROBO</p><h1>DepartamentoT7</h1></div><div className="flex gap-2"><Button variant="ghost" onClick={()=>{pause();setTab('model');setInfo(false);setHelp(!help);}}>Ayuda</Button><Button variant="ghost" onClick={()=>{pause();setTab('model');setHelp(false);setInfo(!info);}}>Información</Button><Button variant="ghost" onClick={()=>void fullscreen()}>Pantalla completa</Button></div></header>
    {notice&&<p className="t7-notice" role="status">{notice}<button onClick={()=>setNotice('')} aria-label="Cerrar aviso">×</button></p>}
    <Tabs value={tab} onValueChange={value=>{setTab(String(value));if(value==='plan')inspect();}} className="min-h-0 flex-1 gap-0">
      <div className="t7-toolbar">
        <TabsList><TabsTrigger value="model">Vista 3D</TabsTrigger><TabsTrigger value="plan">Plano de referencia</TabsTrigger></TabsList>
        <div className="flex flex-wrap gap-2">
          <Button variant="outline" className="h-10 px-4" aria-pressed={mode==='inspect'} onClick={()=>{setTab('model');inspect();}}>Isométrica</Button>
          <Button variant="outline" className="h-10 px-4" aria-pressed={mode==='top'} onClick={()=>{pause();setTab('model');setMode('top');}}>Planta 3D</Button>
          {mode==='walk'&&<Button variant="outline" className="h-10 px-4" onClick={reset}>Volver al acceso</Button>}
          <Button className="h-10 px-4" disabled={!engine} onClick={()=>mode==='walk'&&!paused?pause():enter()}>{mode==='walk'?(paused?'Continuar':'Pausar'):'Recorrer departamento'}</Button>
        </div>
      </div>
      <TabsContent value="model" className="t7-viewport">
        <div ref={viewport} className="t7-canvas" onPointerDown={e=>{if(mode==='walk'&&!paused&&!document.pointerLockElement&&(e.target as HTMLElement).tagName==='CANVAS'){drag.current={id:e.pointerId,x:e.clientX,y:e.clientY};e.currentTarget.setPointerCapture(e.pointerId);}}} onPointerMove={e=>{if(drag.current?.id===e.pointerId){controls.current.yaw-=(e.clientX-drag.current.x)*.005;controls.current.pitch=Math.max(-1.35,Math.min(1.35,controls.current.pitch-(e.clientY-drag.current.y)*.005));drag.current={id:e.pointerId,x:e.clientX,y:e.clientY};}}} onPointerUp={()=>{drag.current=null;}} onPointerCancel={()=>{drag.current=null;}}>
          {bundle&&engine&&<Canvas shadows={{type:PCFShadowMap}} dpr={lightweight?1:[1,1.75]} camera={{position:[17,14,12],fov:mode==='walk'?65:45,near:.03,far:100}}>
            <color attach="background" args={['#172c3c']}/><Scene bundle={bundle} engine={engine} mode={mode} paused={paused} controls={controls} onStatus={onStatus} metrics={metrics} lightweight={lightweight}/>
          </Canvas>}
        </div>
        {!bundle&&<div className="t7-loading" role="status"><p>{error||loading}</p>{error&&<Button onClick={()=>setAttempt(attempt+1)}>Reintentar</Button>}</div>}
        {mode==='inspect'&&<div className="t7-caption"><strong>Tres dormitorios · Baño accesible · Logia</strong><span>Arrastra para girar y revisar la distribución</span></div>}
        {mode==='walk'&&paused&&!help&&!info&&<div className="t7-pause"><h2>Recorrido en pausa</h2><p>W A S D para moverte · Ratón o arrastre para mirar<br/>E para abrir o cerrar · Esc para pausar</p><Button className="h-11 px-7" onClick={()=>enter()}>Continuar recorrido</Button></div>}
        {mode==='walk'&&!paused&&<><span className="t7-crosshair" aria-hidden="true">+</span><p className="t7-walk-status">{status}</p></>}
        {mode==='walk'&&!paused&&touch&&<div className="t7-touch"><div className="t7-pad">{[['KeyW','Avanzar','↑'],['KeyA','Izquierda','←'],['KeyS','Retroceder','↓'],['KeyD','Derecha','→']].map(([key,label,arrow])=><button key={key} aria-label={label} onPointerDown={e=>{e.preventDefault();touchStarted.current=performance.now();e.currentTarget.setPointerCapture(e.pointerId);controls.current.keys.add(key);}} onPointerUp={()=>controls.current.keys.delete(key)} onPointerCancel={()=>{touchStarted.current=-Infinity;controls.current.keys.delete(key);}} onLostPointerCapture={()=>controls.current.keys.delete(key)} onClick={e=>{if((e.detail===0||performance.now()-touchStarted.current<150)&&!controls.current.command)controls.current.command={f:key==='KeyW'?1:key==='KeyS'?-1:0,r:key==='KeyD'?1:key==='KeyA'?-1:0,left:.12,finish:()=>{}};}}>{arrow}</button>)}</div><button className="t7-use" onClick={()=>engine?.interact()}>Abrir / cerrar</button></div>}
        {help&&<aside className="t7-panel"><button onClick={()=>setHelp(false)} aria-label="Cerrar ayuda">×</button><h2>Recorre a tu ritmo</h2><p>W A S D o flechas para caminar. Ratón o arrastre para mirar. Pulsa E cerca de una puerta o un armario.</p><p>Esc pausa el recorrido. Las vistas de inspección permiten revisar la distribución.</p><label><input type="checkbox" checked={touch} onChange={e=>setTouch(e.target.checked)}/> Mostrar controles en pantalla</label><label><input type="checkbox" checked={lightweight} onChange={e=>setLightweight(e.target.checked)}/> Modo ligero</label></aside>}
        {info&&<aside className="t7-panel"><button onClick={()=>setInfo(false)} aria-label="Cerrar información">×</button><h2>Sobre este modelo</h2><p>Referencia documental: 76,66 m² edificados. Contorno del modelo: 77,10 m². Tolerancia acordada: ±0,50 m².</p><p>Superficie útil: {bundle?.collision.useful_area_m2?.toFixed(2)} m². Terraza excluida. Altura de ojos: 1,60 m.</p><p>Plano aproximado a partir de la lámina 20; alturas no acotadas propuestas. No constituye un plano de obra.</p><p>Medición local: {state().performance.average_fps.toFixed(0)} FPS · {(bundle?.loadMs||0).toFixed(0)} ms de carga · {((bundle?.bytes||0)/1e6).toFixed(2)} MB.</p></aside>}
      </TabsContent>
      <TabsContent value="plan" className="t7-plan"><img src="/reference/planta-t7.png" alt="Planta original T7, con tres dormitorios, baño longitudinal, cocina y logia separadas, estar y comedor; acceso superior derecho."/></TabsContent>
    </Tabs>
    <footer className="t7-footer"><span>{mode==='walk'?'Altura de los ojos: 1,60 m':'Vista de inspección con techo y vecinos ocultos'}</span><span>Referencia: 76,66 m² · Modelo: {bundle?.collision.area_m2?.toLocaleString('es-CL',{minimumFractionDigits:2,maximumFractionDigits:2})||'—'} m² exteriores</span></footer>
  </main>;
}
