'use client';
import { useCallback, useEffect, useRef, useState } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { Euler } from 'three';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { loadBundle, type AssetBundle } from './asset-loader';
import { initPhysics, WalkEngine } from './walk-engine';

type Controls = { keys: Set<string>; yaw: number; pitch: number };
type Mode = 'inspect' | 'walk';
const doorNames: Record<string, string> = {O01:'Acceso',O02:'Dormitorio 3',O03:'Dormitorio 1',O04:'Dormitorio 2',O05:'Baño',O06:'Logia'};

function Scene({bundle,engine,mode,paused,controls,onStatus}:{bundle:AssetBundle;engine:WalkEngine;mode:Mode;paused:boolean;controls:React.RefObject<Controls>;onStatus:(text:string)=>void}) {
  const {camera}=useThree();
  const timer=useRef(0);
  useEffect(()=>{
    bundle.scene.traverse(o=>{if(o.userData.inspection_hide)o.visible=mode==='walk';});
    if(mode==='inspect'){camera.position.set(17,14,12);camera.lookAt(6.3,0,-1.8);}
  },[bundle,camera,mode]);
  useFrame((_,delta)=>{
    const input=controls.current;
    const f=Number(input.keys.has('KeyW')||input.keys.has('ArrowUp'))-Number(input.keys.has('KeyS')||input.keys.has('ArrowDown'));
    const r=Number(input.keys.has('KeyD'))-Number(input.keys.has('KeyA'));
    if(mode==='walk'&&!paused){
      if(input.keys.has('ArrowLeft'))input.yaw+=Math.min(delta,.1)*1.4;
      if(input.keys.has('ArrowRight'))input.yaw-=Math.min(delta,.1)*1.4;
    }
    engine.advance(delta,{x:-Math.sin(input.yaw)*f+Math.cos(input.yaw)*r,z:-Math.cos(input.yaw)*f-Math.sin(input.yaw)*r,paused:mode!=='walk'||paused});
    for(const door of engine.doors){
      const pivot=bundle.scene.getObjectByName(door.data.pivot_name||'');
      if(pivot)pivot.rotation.y=engine.doorPose(door.data,door.fraction).angle;
    }
    if(mode==='walk'){
      const eye=engine.eye;camera.position.set(eye.x,eye.y,eye.z);camera.quaternion.setFromEuler(new Euler(input.pitch,input.yaw,0,'YXZ'));
    }
    timer.current+=delta;
    if(timer.current>.2){timer.current=0;const door=engine.nearestDoor();onStatus(engine.message||(door?'E · '+doorNames[door.data.opening||'']:'W A S D · Moverse'));}
  });
  const roomLights=(bundle.collision.rooms||[]).filter(r=>!['SHAFT','CIRCULATION'].includes(r.id)).map(room=>{
    const ps=room.rings_xy_m.flat();const x=(Math.min(...ps.map(p=>p[0]))+Math.max(...ps.map(p=>p[0])))/2;
    const y=(Math.min(...ps.map(p=>p[1]))+Math.max(...ps.map(p=>p[1])))/2;
    return <pointLight key={room.id} position={[x,2.27,-y]} intensity={mode==='walk'?10:0} distance={7} decay={2} color="#fff5df" />;
  });
  return <>
    <primitive object={bundle.scene}/>
    <ambientLight intensity={mode==='walk'?.5:1.4}/>
    <directionalLight position={[3,15,4]} intensity={3} castShadow shadow-mapSize={[2048,2048]} shadow-camera-left={-18} shadow-camera-right={18} shadow-camera-top={18} shadow-camera-bottom={-18} shadow-bias={-.0002} shadow-normalBias={.025}/>
    {roomLights}
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
  const viewport=useRef<HTMLDivElement>(null);
  const controls=useRef<Controls>({keys:new Set(),yaw:Math.PI/2,pitch:0});
  const onStatus=useCallback((s:string)=>setStatus(previous=>previous===s?previous:s),[]);
  useEffect(()=>{
    const abort=new AbortController();let owned:WalkEngine|undefined;
    setError('');setBundle(null);setEngine(null);
    Promise.all([loadBundle('/models/manifest.json',abort.signal),initPhysics()]).then(([asset])=>{
      if(abort.signal.aborted)return;
      owned=new WalkEngine(asset.collision);setBundle(asset);setEngine(owned);
    }).catch(reason=>{if(!abort.signal.aborted)setError(reason instanceof Error?reason.message:'No se pudo cargar el departamento.');});
    return()=>{abort.abort();owned?.dispose();};
  },[attempt]);
  const pause=useCallback(()=>{controls.current.keys.clear();setPaused(true);if(document.pointerLockElement)document.exitPointerLock();},[]);
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
  const enter=()=>{
    if(!engine)return;
    setTab('model');setMode('walk');setPaused(false);controls.current.keys.clear();
    const canvas=viewport.current?.querySelector('canvas');
    if(canvas)void canvas.requestPointerLock()?.catch(()=>{setPaused(false);setStatus('Usa las flechas para mirar y avanzar.');});
  };
  const inspect=()=>{pause();setMode('inspect');};
  return <main className="t7-workspace">
    <header className="t7-header"><div><p>LOS ALTOS DE ALGARROBO</p><h1>DepartamentoT7</h1></div><span className="t7-stage">Recorrido del departamento</span></header>
    <Tabs value={tab} onValueChange={value=>{setTab(String(value));if(value==='plan')inspect();}} className="min-h-0 flex-1 gap-0">
      <div className="t7-toolbar">
        <TabsList><TabsTrigger value="model">Vista 3D</TabsTrigger><TabsTrigger value="plan">Plano de referencia</TabsTrigger></TabsList>
        <div className="flex flex-wrap gap-2">
          {mode==='walk'&&<Button variant="outline" className="h-10 px-4" onClick={inspect}>Vista general</Button>}
          {mode==='walk'&&<Button variant="outline" className="h-10 px-4" onClick={()=>{pause();if(engine?.reset()){controls.current.yaw=Math.PI/2;controls.current.pitch=0;}}}>Volver al acceso</Button>}
          <Button className="h-10 px-4" disabled={!engine} onClick={mode==='walk'&&!paused?pause:enter}>{mode==='walk'?(paused?'Continuar':'Pausar'):'Recorrer departamento'}</Button>
        </div>
      </div>
      <TabsContent value="model" className="t7-viewport">
        <div ref={viewport} className="t7-canvas">
          {bundle&&engine&&<Canvas shadows dpr={[1,1.75]} camera={{position:[17,14,12],fov:mode==='walk'?65:45,near:.03,far:100}}>
            <color attach="background" args={['#172c3c']}/><Scene bundle={bundle} engine={engine} mode={mode} paused={paused} controls={controls} onStatus={onStatus}/>
          </Canvas>}
        </div>
        {!bundle&&<div className="t7-loading" role="status"><p>{error||'Cargando el departamento…'}</p>{error&&<Button onClick={()=>setAttempt(attempt+1)}>Reintentar</Button>}</div>}
        {mode==='inspect'&&<div className="t7-caption"><strong>Tres dormitorios · Baño accesible · Logia</strong><span>Arrastra para girar y revisar la distribución</span></div>}
        {mode==='walk'&&paused&&<div className="t7-pause"><h2>Recorrido en pausa</h2><p>W A S D para moverte · Ratón para mirar<br/>E para abrir o cerrar · Esc para pausar</p><Button className="h-11 px-7" onClick={enter}>Continuar recorrido</Button></div>}
        {mode==='walk'&&!paused&&<><span className="t7-crosshair" aria-hidden="true">+</span><p className="t7-walk-status">{status}</p></>}
      </TabsContent>
      <TabsContent value="plan" className="t7-plan"><img src="/reference/planta-t7.png" alt="Planta original T7, con tres dormitorios, baño longitudinal, cocina y logia separadas, estar y comedor; acceso superior derecho."/></TabsContent>
    </Tabs>
    <footer className="t7-footer"><span>{mode==='walk'?'Altura de los ojos: 1,60 m':'Vista de inspección con techo y vecinos ocultos'}</span><span>Referencia: 76,66 m² · Modelo: {bundle?.collision.area_m2?.toFixed(2)||'—'} m² exteriores</span></footer>
  </main>;
}
