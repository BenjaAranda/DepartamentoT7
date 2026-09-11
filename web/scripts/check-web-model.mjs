import './node-gltf.mjs';
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'three/addons/libs/meshopt_decoder.module.js';
import {Box3,Vector3} from 'three';
const manifest=JSON.parse(fs.readFileSync('public/models/manifest.json'));
const loader=new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
const load=async path=>{const b=fs.readFileSync(path);return (await loader.parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),'')).scene;};
const source=await load('../assets/interchange/departamento-t7.glb'),web=await load('public/models/'+manifest.model);
source.updateMatrixWorld(true);web.updateMatrixWorld(true);
let maxError=0,meshes=0;
source.traverse(o=>{
 const counterpart=web.getObjectByName(o.name);assert.ok(counterpart,o.name);
 if(!o.isMesh)return;meshes++;
 const a=new Box3().setFromObject(o),b=new Box3().setFromObject(counterpart);
 const error=Math.max(...a.min.toArray().map((n,i)=>Math.abs(n-b.min.getComponent(i))),...a.max.toArray().map((n,i)=>Math.abs(n-b.max.getComponent(i))));
 maxError=Math.max(maxError,error);assert.ok(error<.001,'Compressed bounds mismatch '+o.name+': '+error);
});
const data=JSON.parse(fs.readFileSync('public/models/departamento-t7.json'));
for(const door of data.doors){const pivot=web.getObjectByName(door.pivot_name);const origin=pivot.localToWorld(new Vector3());assert.ok(origin.distanceTo(new Vector3(...door.pivot))<.00001);const direction=pivot.localToWorld(new Vector3(1,0,0)).sub(origin).normalize();assert.ok(direction.distanceTo(new Vector3(Math.cos(door.base_rotation_y),0,-Math.sin(door.base_rotation_y)))<.00001);}
for(const [name,hash] of Object.entries(manifest.hashes)){
 const path=name.endsWith('.blend')?'../blender/'+name:'public/models/'+name;
 assert.equal(createHash('sha256').update(fs.readFileSync(path)).digest('hex'),hash,name);
}
const report={revision:manifest.revision,compressed_meshes:meshes,maximum_bounds_deviation_m:maxError,pivots_preserved:data.doors.length,all_hashes_match:true};
fs.writeFileSync('../validation/e09/web-glb-check.json',JSON.stringify(report,null,2)+'\n');console.log(report);
