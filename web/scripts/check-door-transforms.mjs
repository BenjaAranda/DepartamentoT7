import './node-gltf.mjs';
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'three/addons/libs/meshopt_decoder.module.js';
import {Box3,Vector3} from 'three';
import {applyDoorAngle} from '../components/t7/door-transform.ts';
import {WalkEngine,initPhysics} from '../components/t7/walk-engine.ts';

const data=JSON.parse(fs.readFileSync('public/models/departamento-t7.json'));
const raw=fs.readFileSync('public/models/departamento-t7-web.glb');
const {scene}=await new GLTFLoader().setMeshoptDecoder(MeshoptDecoder).parseAsync(raw.buffer.slice(raw.byteOffset,raw.byteOffset+raw.byteLength),'');
await initPhysics();const engine=new WalkEngine(data);
const checks=[];
for(const door of data.doors){
 const pivot=scene.getObjectByName(door.pivot_name),leaf=scene.getObjectByName(door.leaf_name);
 assert.ok(pivot&&leaf,door.id);const imported=pivot.quaternion.clone();
 let maxError=0,legacyError=0;
 for(let step=0;step<=90;step++){
  const fraction=step/90,pose=engine.doorPose(door,fraction),expected=new Box3();
  for(const x of [-1,1])for(const y of [-1,1])for(const z of [-1,1]){
   const local=new Vector3(x*door.size[0]/2,y*door.size[1]/2,z*door.size[2]/2);
   expected.expandByPoint(new Vector3(Math.cos(pose.angle)*local.x+Math.sin(pose.angle)*local.z+pose.position.x,local.y+pose.position.y,-Math.sin(pose.angle)*local.x+Math.cos(pose.angle)*local.z+pose.position.z));
  }
  pivot.quaternion.copy(imported);pivot.rotation.y=pose.angle;scene.updateMatrixWorld(true);
  const legacy=new Box3().setFromObject(leaf);
  legacyError=Math.max(legacyError,legacy.min.distanceTo(expected.min),legacy.max.distanceTo(expected.max));
  applyDoorAngle(pivot,pose.angle);scene.updateMatrixWorld(true);
  const actual=new Box3().setFromObject(leaf);
  maxError=Math.max(maxError,actual.min.distanceTo(expected.min),actual.max.distanceTo(expected.max));
 }
 assert.ok(maxError<.0002,`${door.id}: visible leaf differs from collider ${maxError}m`);
 checks.push({id:door.id,samples:91,maximum_visual_collider_error_m:maxError,previous_euler_error_m:legacyError});
 applyDoorAngle(pivot,door.base_rotation_y||0);
}
assert.ok(checks.filter(c=>c.previous_euler_error_m>.1).length>=4,'Fixture must reproduce the imported Euler-axis regression');
assert.ok(engine.doors.filter(d=>d.data.opening==='D1_Wardrobe').every(d=>d.fraction===0&&d.target===0),'D1 wardrobe starts closed');
const report={revision:data.revision,checks,wardrobe_d1_initially_closed:true,passed:true};
fs.mkdirSync('../validation/door-fix',{recursive:true});fs.writeFileSync('../validation/door-fix/transforms.json',JSON.stringify(report,null,2)+'\n');
console.log(report);engine.dispose();
