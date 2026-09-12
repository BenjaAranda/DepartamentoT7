import fs from 'node:fs';
import assert from 'node:assert/strict';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {Box3,Vector3} from 'three';
import {WalkEngine,initPhysics} from '../components/t7/walk-engine.ts';
const data=JSON.parse(fs.readFileSync('public/models/departamento-t7.json'));
const raw=fs.readFileSync('public/models/departamento-t7.glb');
const {scene}=await new GLTFLoader().parseAsync(raw.buffer.slice(raw.byteOffset,raw.byteOffset+raw.byteLength),'');
scene.updateMatrixWorld(true);
const boxOf=name=>{const ob=scene.getObjectByName(name);assert.ok(ob,name);return new Box3().setFromObject(ob);};
const obstacles=data.colliders.filter(c=>['Architecture','Carpentry'].includes(c.category)).map(c=>({id:c.id,box:new Box3(new Vector3(...c.center).sub(new Vector3(...c.size).multiplyScalar(.5)),new Vector3(...c.center).add(new Vector3(...c.size).multiplyScalar(.5)))}));
const overlap=(a,b)=>[0,1,2].map(i=>Math.min(a.max.getComponent(i),b.max.getComponent(i))-Math.max(a.min.getComponent(i),b.min.getComponent(i)));
const violations=[],checks=[];
for(const item of data.inventory){
 const bounds=new Box3();
 for(const name of item.mesh_names){
  const actual=boxOf(name);bounds.union(actual);
  for(const obstacle of obstacles)if(overlap(actual,obstacle.box).every(d=>d>.002))violations.push({mesh:name,obstacle:obstacle.id,overlap_m:overlap(actual,obstacle.box)});
 }
 if(item.type==='chair'){
  const a=item.rotation*Math.PI/180,offset=new Vector3(-Math.sin(a)*item.use_offset_local_y,0,-Math.cos(a)*item.use_offset_local_y);
  const used=bounds.clone().translate(offset);
  for(const obstacle of obstacles)if(overlap(used,obstacle.box).every(d=>d>.002))violations.push({mesh:item.id+' use position',obstacle:obstacle.id});
 }
 checks.push({id:item.id,type:item.type,room:item.room,bounds:[bounds.min.toArray(),bounds.max.toArray()],mesh_count:item.mesh_names.length});
}
const count=(room,type)=>data.inventory.filter(i=>i.room===room&&i.type===type).length;
for(const room of ['D1','D2','D3']){
 assert.equal(count(room,'bed'),1);assert.equal(count(room,'wardrobe'),1);
 const wardrobe=data.inventory.find(i=>i.room===room&&i.type==='wardrobe');
 assert.equal(data.doors.filter(d=>d.opening===wardrobe.id).length,2);
 for(const suffix of ['Back','Jamb-1','Jamb1','Plinth','Crown','Shelf','Rail'])assert.ok(wardrobe.mesh_names.includes(wardrobe.id+'_'+suffix));
}
assert.equal(count('D1','nightstand'),2);assert.equal(count('D2','nightstand'),1);assert.equal(count('D3','nightstand'),1);
assert.equal(count('D2','desk'),0);assert.equal(count('DINING','chair'),4);
const facing=[];
for(const [aId,bId] of [['Living_Sofa','Living_TV'],['D1_Bed','D1_TV']]){
 const a=data.inventory.find(i=>i.id===aId),b=data.inventory.find(i=>i.id===bId);
 const direction=b.center.map((v,i)=>v-a.center[i]);const length=Math.hypot(...direction);const dot=a.forward_xy.reduce((s,v,i)=>s+v*direction[i]/length,0);
 const opposed=a.forward_xy.reduce((s,v,i)=>s+v*b.forward_xy[i],0);
 assert.ok(dot>.999&&opposed<-.999);facing.push({a:aId,b:bId,direction_dot:dot,opposed_dot:opposed});
}
await initPhysics();const engine=new WalkEngine(data),sweeps=[];
for(const door of engine.doors){
 // Place the visitor away from the sweep, then exercise the actual motor.
 engine.body.setTranslation({x:13.5,y:.83,z:-3},true);engine.world.step();
 engine.setDoor(door.data.id,true);for(let i=0;i<65;i++)engine.step({x:0,z:0,paused:true});
 const opened=door.fraction,blocked=door.blocked;
 engine.setDoor(door.data.id,false);for(let i=0;i<65;i++)engine.step({x:0,z:0,paused:true});
 sweeps.push({id:door.data.id,opened_fraction:opened,closed_fraction:door.fraction,blocked});
}
engine.dispose();
const decorViolations=[];
const artSupports=[];
for(const name of data.finishes?.decorations||[]){
 const b=boxOf(name);
 for(const o of obstacles)if(overlap(b,o.box).every(d=>d>.002))decorViolations.push({mesh:name,obstacle:o.id});
 if(name.startsWith('Art_')&&name.endsWith('_Frame')){
  const size=b.getSize(new Vector3()),center=b.getCenter(new Vector3());
  const normal=[0,1,2].sort((a,c)=>size.getComponent(a)-size.getComponent(c))[0],axes=[0,1,2].filter(a=>a!==normal);
  let backed=true;
  for(const u of [-1,0,1])for(const v of [-1,0,1]){
   const p=center.clone();p.setComponent(axes[0],center.getComponent(axes[0])+u*(size.getComponent(axes[0])/2-.01));p.setComponent(axes[1],center.getComponent(axes[1])+v*(size.getComponent(axes[1])/2-.01));
   const supported=[-1,1].some(sign=>{const behind=p.clone();behind.setComponent(normal,center.getComponent(normal)+sign*(size.getComponent(normal)/2+.04));return obstacles.some(o=>/^W\d/.test(o.id)&&o.box.containsPoint(behind));});
   backed&&=supported;
  }
  artSupports.push({mesh:name,backed_by_solid_wall:backed});
 }
}
const report={revision:data.revision,inventory_count:checks.length,checks,facing,wall_penetrations:violations,decoration_penetrations:decorViolations,art_supports:artSupports,chair_use_offset_m:.15,door_sweeps:sweeps};
const out=process.argv[2]||'../validation/e06';fs.mkdirSync(out,{recursive:true});fs.writeFileSync(out+'/furniture-check.json',JSON.stringify(report,null,2)+'\n');
console.log({inventory:checks.length,violations,sweeps});
assert.equal(violations.length,0,'Furniture intersects architecture');
assert.deepEqual(decorViolations,[],'Decoration intersects architecture');
assert.ok(artSupports.every(a=>a.backed_by_solid_wall),'Wall art covers an opening or lacks support');
assert.ok(sweeps.every(s=>s.opened_fraction>.999&&s.closed_fraction<.001&&!s.blocked),'Blocked leaf');
import './node-gltf.mjs';
