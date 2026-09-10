import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';
import { Box3, Vector3 } from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import RAPIER from '@dimforge/rapier3d-compat';

const root=path.resolve('..');
const dir=path.join(root,'web/public/models');
const manifest=JSON.parse(fs.readFileSync(path.join(dir,'proof-manifest.json')));
const model=JSON.parse(fs.readFileSync(path.join(root,'architecture/model/departamento-t7.json')));
assert.equal(manifest.revision,model.revision);
const digest=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
for(const [name,hash] of Object.entries(manifest.hashes)) {
  const original=path.join(root,name.endsWith('.blend')?'blender':name.endsWith('.glb')?'assets/interchange':'assets/colliders',name);
  assert.equal(digest(original),hash);
  if(!name.endsWith('.blend'))assert.equal(digest(path.join(dir,name)),hash);
}
const bytes=fs.readFileSync(path.join(dir,manifest.model));
const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
gltf.scene.updateMatrixWorld(true);
const box=name=>new Box3().setFromObject(gltf.scene.getObjectByName(name));
const ruler=box('ProofRuler1m').getSize(new Vector3()).x;
assert.ok(Math.abs(ruler-1)<.001);
const eye=box('ProofEyeDatum').getCenter(new Vector3()).y;
assert.ok(Math.abs(eye-1.6)<.001);
const pivot=gltf.scene.getObjectByName('ProofDoorPivot');
assert.ok(Math.abs(pivot.position.x+.425)<.001);
const data=JSON.parse(fs.readFileSync(path.join(dir,manifest.colliders)));
assert.equal(data.revision,manifest.revision);
for(const c of data.colliders){
  const b=box(c.id), center=b.getCenter(new Vector3()), size=b.getSize(new Vector3());
  assert.ok(center.distanceTo(new Vector3(...c.center))<.001,c.id);
  assert.ok(size.distanceTo(new Vector3(...c.size))<.001,c.id);
}
await RAPIER.init();
function route(x,closed,from=1,to=-1){
  const world=new RAPIER.World({x:0,y:-9.81,z:0});
  for(const c of data.colliders)world.createCollider(RAPIER.ColliderDesc.cuboid(...c.size.map(v=>v/2)).setTranslation(...c.center));
  if(closed)world.createCollider(RAPIER.ColliderDesc.cuboid(.425,1.035,.0175).setTranslation(0,1.035,0));
  const body=world.createRigidBody(RAPIER.RigidBodyDesc.kinematicPositionBased().setTranslation(x,.87,from));
  const collider=world.createCollider(RAPIER.ColliderDesc.capsule(.6,.25),body);
  const controller=world.createCharacterController(.01);
  controller.enableSnapToGround(.1);
  for(let i=0;i<180;i++){
    world.step();
    controller.computeColliderMovement(collider,{x:0,y:-.04,z:(to-from)/180});
    const m=controller.computedMovement(),p=body.translation();
    body.setNextKinematicTranslation({x:p.x+m.x,y:p.y+m.y,z:p.z+m.z});
  }
  world.step();const result={...body.translation()};world.free();return result;
}
const through=route(0,false),reverse=route(0,false,-1,1),wall=route(1.2,false),closed=route(0,true);
assert.ok(through.z<-.8 && reverse.z>.8,'Portal must be traversable both ways');
assert.ok(wall.z>.3 && closed.z>.2,'Wall and closed leaf must block');
assert.ok(Math.abs(through.y-.86)<.02,'No falling through floor');
const report={revision:manifest.revision,ruler_m:ruler,eye_m:eye,hashes_match:true,collider_bounds_match:true,portal_both_directions:true,wall_blocks:true,closed_leaf_blocks:true,positions:{through,reverse,wall,closed},runtime:'Three.js GLTFLoader + Rapier 0.19.2, Node; browser appearance checked separately'};
fs.writeFileSync(path.join(root,'validation/e03/exchange-check.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
