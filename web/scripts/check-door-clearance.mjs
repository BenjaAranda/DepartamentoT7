import './node-gltf.mjs';
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {Box3,Vector3} from 'three';
import {WalkEngine,initPhysics} from '../components/t7/walk-engine.ts';

const data=JSON.parse(fs.readFileSync('public/models/departamento-t7.json'));
await initPhysics();const engine=new WalkEngine(data);
const raw=fs.readFileSync('public/models/departamento-t7.glb');
const {scene}=await new GLTFLoader().parseAsync(raw.buffer.slice(raw.byteOffset,raw.byteOffset+raw.byteLength),'');
scene.updateMatrixWorld(true);const obstacles=[...data.colliders];
scene.traverse(object=>{
 if(!object.isMesh||data.doors.some(d=>object.name.startsWith(d.id+'_')))return;
 const box=new Box3().setFromObject(object);
 obstacles.push({id:object.name,center:box.getCenter(new Vector3()).toArray(),size:box.getSize(new Vector3()).toArray()});
});
const shape=(door,f)=>{const p=engine.doorPose(door,f);return {id:door.id,center:[p.position.x,p.position.y,p.position.z],size:door.size,angle:p.angle};};
function intersects(a,b){
 if(Math.min(a.center[1]+a.size[1]/2,b.center[1]+b.size[1]/2)-Math.max(a.center[1]-a.size[1]/2,b.center[1]-b.size[1]/2)<=.002)return false;
 const axes=o=>[[Math.cos(o.angle),-Math.sin(o.angle)],[Math.sin(o.angle),Math.cos(o.angle)]];
 const aa=axes(a),ba=axes(b),delta=[b.center[0]-a.center[0],b.center[2]-a.center[2]];
 const dot=(x,y)=>x[0]*y[0]+x[1]*y[1];
 for(const axis of [...aa,...ba]){
  const radius=(o,own)=>Math.abs(dot(axis,own[0]))*o.size[0]/2+Math.abs(dot(axis,own[1]))*o.size[2]/2;
  if(radius(a,aa)+radius(b,ba)-Math.abs(dot(delta,axis))<=.002)return false;
 }
 return true;
}
const ids=['P03','P04','P05','P06'],violations=[],checks=[];
for(const id of ids){
 const door=data.doors.find(d=>d.id===id);
 for(let step=0;step<=90;step++)for(const collider of obstacles){
  // Include each leaf's own jambs, unlike the runtime's frame-contact exception.
  if(intersects(shape(door,step/90),{...collider,angle:0}))violations.push({id,fraction:step/90,obstacle:collider.id});
 }
 const closed=shape(door,0),open=shape(door,1);
 assert.ok(open.center[2]>closed.center[2]+door.size[0]*.45,`${id} must open into its room, toward -Y in Blender`);
 checks.push({id,samples:91,opens_inward:true,includes_own_jambs:true});
}
const d2=data.doors.find(d=>d.id==='P04'),bath=data.doors.find(d=>d.id==='P05');
let pairChecks=0;
for(let a=0;a<=90;a++)for(let b=0;b<=90;b++){pairChecks++;if(intersects(shape(d2,a/90),shape(bath,b/90)))violations.push({pair:['P04','P05'],fractions:[a/90,b/90]});}
const report={revision:data.revision,checks,independent_bath_bedroom2_angle_pairs:pairChecks,violations,passed:violations.length===0};
fs.mkdirSync('../validation/door-fix',{recursive:true});fs.writeFileSync('../validation/door-fix/clearance.json',JSON.stringify(report,null,2)+'\n');
console.log(report);engine.dispose();assert.deepEqual(violations,[],'Door intersects wall, jamb, furniture or adjacent door');
