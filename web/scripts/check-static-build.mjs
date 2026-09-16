import assert from 'node:assert/strict';
import {readFileSync, readdirSync, statSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {resolve, relative} from 'node:path';
const root=fileURLToPath(new URL('../dist-static/',import.meta.url));
const base=process.env.T7_BASE_PATH||'/DepartamentoT7/';
const html=readFileSync(resolve(root,'index.html'),'utf8');
assert(html.includes(`<base href="${base}"`),'Missing repository base path');
assert(html.includes('Content-Security-Policy'),'Missing CSP');
assert(html.includes("script-src 'self' 'wasm-unsafe-eval'"),'Scripts must stay same-origin');
assert(!html.includes("'unsafe-eval'"),'JavaScript eval must not be allowed');
for(const match of html.matchAll(/(?:src|href)="([^"]+)"/g)){
 assert(match[1].startsWith(base),'URL escapes deployment prefix: '+match[1]);
 if(match[1]!==base)assert(statSync(resolve(root,match[1].slice(base.length))).isFile());
}
const manifest=JSON.parse(readFileSync(resolve(root,'models/manifest.json')));
const collision=JSON.parse(readFileSync(resolve(root,'models',manifest.colliders)));
assert.equal(manifest.revision,collision.revision);
assert.equal(manifest.eye_height_m,1.6);
for(const file of [manifest.model,manifest.colliders]){
 const bytes=readFileSync(resolve(root,'models',file));
 assert.equal(createHash('sha256').update(bytes).digest('hex'),manifest.hashes[file]);
 if(file.endsWith('.glb'))assert.equal(bytes.subarray(0,4).toString(),'glTF','Git LFS pointer instead of model');
}
const allowed=new Set(['index.html','.nojekyll','favicon.svg','reference/planta-t7.png','models/manifest.json',`models/${manifest.model}`,`models/${manifest.colliders}`]);
const files=[];
function visit(dir){for(const name of readdirSync(dir)){const path=resolve(dir,name);if(statSync(path).isDirectory())visit(path);else{const rel=relative(root,path).replaceAll('\\','/');assert(allowed.has(rel)||/^assets\/[\w.-]+\.(js|css|wasm|woff2)$/.test(rel),'Unexpected public file: '+rel);assert(statSync(path).size<25*1024*1024);files.push(rel);}}}
visit(root);
console.log(JSON.stringify({passed:true,revision:manifest.revision,base,files:files.length,model_hash_verified:true,no_private_or_server_files:true},null,2));
