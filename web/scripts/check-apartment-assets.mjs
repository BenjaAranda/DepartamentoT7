import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {Box3,Vector3} from 'three';
const root=path.resolve('..'),dir=path.join(root,'web/public/models');
const manifest=JSON.parse(fs.readFileSync(path.join(dir,'manifest.json')));
const geometry=JSON.parse(fs.readFileSync(path.join(root,'validation/e04/geometry-check.json')));
assert.equal(manifest.revision,geometry.revision);
const digest=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
for(const [name,hash] of Object.entries(manifest.hashes)){
 const p=path.join(root,name.endsWith('.blend')?'blender':name.endsWith('.glb')?'assets/interchange':'assets/colliders',name);
 assert.equal(digest(p),hash);
 if(!name.endsWith('.blend'))assert.equal(digest(path.join(dir,name)),hash);
}
const raw=fs.readFileSync(path.join(dir,manifest.model));
const {scene}=await new GLTFLoader().parseAsync(raw.buffer.slice(raw.byteOffset,raw.byteOffset+raw.byteLength),'');
scene.updateMatrixWorld(true);
let meshes=0,maxError=0;
scene.traverse(o=>{if(o.isMesh)meshes++;if(o.userData.revision)assert.equal(o.userData.revision,manifest.revision)});
for(const w of geometry.walls){
 const o=scene.getObjectByName(w.id);assert.ok(o,w.id);const b=new Box3().setFromObject(o);
 const actual=[b.min.x,-b.max.z,b.max.x,-b.min.z];
 const error=Math.max(...actual.map((n,i)=>Math.abs(n-w.expected_rect_xy_m[i])));maxError=Math.max(maxError,error);assert.ok(error<.001,w.id);
}
let floorArea=0;
scene.getObjectByName('T7Floor').traverse(o=>{
 if(!o.isMesh)return;
 const g=o.geometry,p=g.attributes.position,idx=g.index;
 const count=idx?idx.count:p.count;
 for(let i=0;i<count;i+=3){
  const points=[0,1,2].map(j=>new Vector3().fromBufferAttribute(p,idx?idx.getX(i+j):i+j).applyMatrix4(o.matrixWorld));
  if(points.every(q=>Math.abs(q.y)<1e-5))floorArea+=points[1].clone().sub(points[0]).cross(points[2].clone().sub(points[0])).length()/2;
 }
});
assert.ok(Math.abs(floorArea-77.1)<1e-4);
for(const name of ['T7Ceiling','T7Slab','NeighbourNorth','NeighbourEast','CommonCorridor','UpperT6Mass2','UpperT6Mass3','UpperT6Mass4'])assert.ok(scene.getObjectByName(name),name);
for(const d of geometry.doors){
 const pivot=scene.getObjectByName(d.pivot_name);assert.ok(pivot);if(d.category!=='wardrobe')assert.ok(d.clear_span_m>.7);
 const origin=pivot.localToWorld(new Vector3()),tip=pivot.localToWorld(new Vector3(1,0,0));
 const expected=new Vector3(Math.cos(d.base_rotation_y),0,-Math.sin(d.base_rotation_y));
 assert.ok(tip.sub(origin).normalize().distanceTo(expected)<1e-5,'Door basis mismatch: '+d.id);
}
const report={revision:manifest.revision,hashes_match:true,wall_glb_max_error_m:maxError,measured_glb_floor_m2:floorArea,area_delta_m2:floorArea-76.66,meshes,context_present:true,door_pivots:geometry.doors.length,glb_bytes:raw.length};
fs.writeFileSync(path.join(root,'validation/e04/glb-check.json'),JSON.stringify(report,null,2)+'\n');console.log(report);
