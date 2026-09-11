import './node-gltf.mjs';
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {loadBundle,disposeScene} from '../components/t7/asset-loader.ts';
import {WalkEngine,initPhysics} from '../components/t7/walk-engine.ts';

globalThis.location={href:'https://t7.test/'};
const originalFetch=globalThis.fetch;
const manifest=JSON.parse(fs.readFileSync('public/models/manifest.json'));
let current=structuredClone(manifest),fault='',delivered=0;
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
globalThis.fetch=async(url,options={})=>{
 if(String(url).startsWith('blob:'))return originalFetch(url,options);
 if(options.signal?.aborted)throw new DOMException('Aborted','AbortError');
 const name=new URL(url,location.href).pathname.split('/').pop();
 if(name==='manifest.json')return new Response(JSON.stringify(current),{status:fault==='manifest-http'?503:200});
 if(fault==='download-http')return new Response('',{status:503});
 let bytes=fs.readFileSync('public/models/'+name);
 if(fault==='corruption'&&name===current.model)bytes=Buffer.concat([bytes,Buffer.from('invalid')]);
 if(fault==='collision-revision'&&name===current.colliders){const d=JSON.parse(bytes);d.revision='different';bytes=Buffer.from(JSON.stringify(d));current.hashes[name]=hash(bytes);}
 delivered+=bytes.length;return new Response(bytes);
};
const checks=[];
for(const [name,setup,expected] of [
 ['manifest unavailable',()=>{fault='manifest-http';},/obtener/],
 ['incomplete manifest',()=>{delete current.model;},/incompleto/],
 ['wrong units',()=>{current.units='cm';},/escala/],
 ['wrong eye height',()=>{current.eye_height_m=1.7;},/escala/],
 ['invalid asset path',()=>{current.model='../outside.glb';},/inválida/],
 ['failed download',()=>{fault='download-http';},/descargar/],
 ['corrupted model',()=>{fault='corruption';},/versiones distintas/],
 ['mismatched colliders',()=>{fault='collision-revision';const d=JSON.parse(fs.readFileSync('public/models/'+current.colliders));d.revision='different';current.hashes[current.colliders]=hash(Buffer.from(JSON.stringify(d)));},/colisiones/],
 ]){
 current=structuredClone(manifest);fault='';setup();
 await assert.rejects(()=>loadBundle('/models/manifest.json',new AbortController().signal),expected);
 checks.push({name,passed:true});
}
current=structuredClone(manifest);fault='';const abort=new AbortController();abort.abort();
await assert.rejects(()=>loadBundle('/models/manifest.json',abort.signal),{name:'AbortError'});checks.push({name:'cancelled download',passed:true});
delivered=0;const progress=[];const bundle=await loadBundle('/models/manifest.json',new AbortController().signal,label=>progress.push(label));
assert.equal(bundle.revision,manifest.revision);assert.equal(bundle.bytes,delivered);assert.ok(progress.some(p=>p.startsWith('Descargando')));assert.equal(progress.at(-1),'Preparando el recorrido…');
checks.push({name:'retry loads complete matching bundle with progress',passed:true});
await initPhysics();const engine=new WalkEngine(bundle.collision);engine.dispose();engine.dispose();engine.advance(1,{x:1,z:0});assert.ok(engine.disposed);disposeScene(bundle.scene);
checks.push({name:'releasing a scene safely stops pending frames',passed:true});
globalThis.fetch=originalFetch;
const report={revision:manifest.revision,checks,asset_bytes:delivered,scope:'Node structural loader with real compressed GLB and streamed responses; pixel rendering tested separately in browser.'};
fs.writeFileSync('../validation/e09/loader-check.json',JSON.stringify(report,null,2)+'\n');console.log(report);
