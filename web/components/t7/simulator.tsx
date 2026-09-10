'use client';
import { Suspense, useEffect, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { Physics, RigidBody, CuboidCollider } from '@react-three/rapier';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { loadBundle, type AssetBundle } from './asset-loader';
function Model({ bundle, opened }: { bundle: AssetBundle; opened: boolean }) {
  useEffect(() => {
    for (const door of bundle.collision.doors) {
      const pivot = bundle.scene.getObjectByName(door.pivot_name || 'ProofDoorPivot');
      if (pivot) pivot.rotation.y = (door.base_rotation_y || 0) + (opened ? door.swing_radians : 0);
    }
    bundle.scene.traverse(object => { if (object.userData.inspection_hide) object.visible = false; });
  }, [bundle, opened]);
  return <>
    <primitive object={bundle.scene} />
    <Physics timeStep={1 / 60} gravity={[0, -9.81, 0]}>
      <RigidBody type="fixed" colliders={false}>
        {bundle.collision.colliders.map(c => <CuboidCollider key={c.id} name={c.id} position={c.center} args={[c.size[0] / 2, c.size[1] / 2, c.size[2] / 2]} />)}
      </RigidBody>
    </Physics>
  </>;
}
export default function Simulator() {
  const [bundle, setBundle] = useState<AssetBundle | null>(null);
  const [error, setError] = useState('');
  const [attempt, setAttempt] = useState(0);
  const [opened, setOpened] = useState(false);
  useEffect(() => {
    const controller = new AbortController();
    setError('');setBundle(null);
    loadBundle('/models/manifest.json', controller.signal).then(setBundle).catch(reason => {
      if (!controller.signal.aborted) setError(reason instanceof Error ? reason.message : 'No se pudo cargar el modelo.');
    });
    return () => controller.abort();
  }, [attempt]);
  return <main className="t7-workspace">
    <header className="t7-header"><div><p>LOS ALTOS DE ALGARROBO</p><h1>DepartamentoT7</h1></div><span className="t7-stage">Arquitectura</span></header>
    <Tabs defaultValue="model" className="min-h-0 flex-1 gap-0">
      <div className="t7-toolbar"><TabsList><TabsTrigger value="model">Vista 3D</TabsTrigger><TabsTrigger value="plan">Plano de referencia</TabsTrigger></TabsList><Button variant="outline" className="h-10 px-4" disabled={!bundle} onClick={() => setOpened(!opened)}>{opened ? 'Cerrar puertas' : 'Abrir puertas'}</Button></div>
      <TabsContent value="model" className="t7-viewport">
        {bundle && <Canvas shadows dpr={[1, 1.75]} camera={{ position: [17, 14, 12], fov: 45, near: .03, far: 100 }}>
          <color attach="background" args={['#172c3c']} /><ambientLight intensity={1.4} />
          <directionalLight position={[3, 15, 4]} intensity={3} castShadow shadow-mapSize={[2048, 2048]} shadow-camera-left={-18} shadow-camera-right={18} shadow-camera-top={18} shadow-camera-bottom={-18} shadow-bias={-.0002} shadow-normalBias={.025} />
          <Suspense fallback={null}><Model bundle={bundle} opened={opened} /></Suspense>
          <OrbitControls makeDefault target={[6.3, 0, -1.8]} minDistance={5} maxDistance={32} maxPolarAngle={Math.PI / 2 - .04} />
        </Canvas>}
        {!bundle && <div className="t7-loading" role="status"><p>{error || 'Cargando el departamento…'}</p>{error && <Button onClick={() => setAttempt(attempt + 1)}>Reintentar</Button>}</div>}
        <div className="t7-caption"><strong>Tres dormitorios · Baño accesible · Logia</strong><span>Vista de inspección con techo y contexto ocultos</span></div><p className="t7-hint">Arrastra para girar · Rueda para acercarte</p>
      </TabsContent>
      <TabsContent value="plan" className="t7-plan"><img src="/reference/planta-t7.png" alt="Planta original del T7: tres dormitorios a la izquierda, baño longitudinal al centro, cocina y logia separadas, estar y comedor a la derecha; acceso superior derecho." /></TabsContent>
    </Tabs>
    <footer className="t7-footer"><span>Arquitectura en revisión · Mobiliario y recorrido pendientes</span><span>Referencia: 76,66 m² · Modelo: {bundle?.collision.area_m2?.toFixed(2) || '—'} m² exteriores</span></footer>
  </main>;
}
