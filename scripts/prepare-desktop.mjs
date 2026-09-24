import {cpSync,existsSync,mkdirSync,readFileSync,rmSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {resolve, sep} from 'node:path';

const root=fileURLToPath(new URL('../',import.meta.url));
const web=resolve(root,'web');
const source=resolve(web,'dist-static');
const launcher=resolve(root,'launcher');
const target=resolve(launcher,'cmd/departamentot7/site');
if(!existsSync(resolve(source,'index.html')))throw Error('Build web/ with T7_BASE_PATH=/ first');
const html=readFileSync(resolve(source,'index.html'),'utf8');
if(!html.includes('<base href="/"'))throw Error('The desktop site needs T7_BASE_PATH=/');
execFileSync(process.execPath,[resolve(web,'scripts/check-static-build.mjs')],{cwd:web,env:{...process.env,T7_BASE_PATH:'/'},stdio:'inherit'});
if(!target.startsWith(launcher+sep)||!target.endsWith(sep+'site'))throw Error('Unsafe generated-site path');
rmSync(target,{recursive:true,force:true});
mkdirSync(target,{recursive:true});
cpSync(source,target,{recursive:true});
console.log('Prepared embedded desktop site');
