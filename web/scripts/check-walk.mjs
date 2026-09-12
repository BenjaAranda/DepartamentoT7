import fs from 'node:fs';
import assert from 'node:assert/strict';
import {WalkEngine,initPhysics,BODY_REST_Y} from '../components/t7/walk-engine.ts';
await initPhysics();
const data=JSON.parse(fs.readFileSync('public/models/departamento-t7.json'));
const engine=new WalkEngine(data);
// Fixture setup opens leaves before traversal; interaction sweeps are tested separately.
for(const door of engine.doors){engine.placeDoor(door,0,true);door.target=0;}
engine.world.step();
const step=.1,xmin=-.2,xmax=14.5,zmin=-6.8,zmax=1.5;
const nx=Math.floor((xmax-xmin)/step)+1,nz=Math.floor((zmax-zmin)/step)+1;
function graphFor(opening){
for(const door of engine.doors){const f=door.data.opening===opening||(process.argv.includes('--wardrobes-open')&&door.data.category==='wardrobe')?1:0;engine.placeDoor(door,f,true);door.target=f;}
engine.world.step();
const points=new Map();
for(let i=0;i<nx;i++)for(let j=0;j<nz;j++){
 const x=xmin+i*step,z=zmin+j*step;
 if(engine.isFree(x,z,BODY_REST_Y,.012)&&engine.hasFloor(x,z))points.set(i*nz+j,[x,z]);
}
function nearest(x,z,predicate=()=>true){
 let best,dist=Infinity;
 for(const [key,p] of points){const d=(p[0]-x)**2+(p[1]-z)**2;if(d<dist&&predicate(p)){best=key;dist=d}}
 assert.notEqual(best,undefined);return best;
}
function contains(p,poly){let inside=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){
 const a=poly[i],b=poly[j];if((a[1]>p[1])!==(b[1]>p[1])&&p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0])inside=!inside;
}return inside;}
const start=nearest(data.spawn[0],data.spawn[2]);
const queue=[start],parents=new Map([[start,null]]);
for(let k=0;k<queue.length;k++){
 const id=queue[k],i=Math.floor(id/nz),j=id%nz;
 for(const [a,b] of [[i-1,j],[i+1,j],[i,j-1],[i,j+1]]){
  const n=a*nz+b;if(a<0||b<0||a>=nx||b>=nz||!points.has(n)||parents.has(n))continue;
  parents.set(n,id);queue.push(n);
 }
}
return {points,parents,nearest,start,contains};
}
const routes=[];
const openings={D3:'O02',D1:'O03',D2:'O04',BATH:'O05',LOGIA:'O06',CORRIDOR:'O01'};
let reachableCells=0;
for(const room of data.rooms.filter(r=>!['SHAFT','CIRCULATION'].includes(r.id))){
 const {points,parents,nearest,contains}=graphFor(openings[room.id]);
 reachableCells=Math.max(reachableCells,parents.size);
 const ring=room.rings_xy_m.reduce((a,b)=>a.length>b.length?a:b);
 const center=[ring.reduce((s,p)=>s+p[0],0)/ring.length,-ring.reduce((s,p)=>s+p[1],0)/ring.length];
 const goal=nearest(...center,p=>room.rings_xy_m.some(poly=>contains([p[0],-p[1]],poly)));
 assert.ok(parents.has(goal),'Unreachable room: '+room.id);
 const path=[];for(let n=goal;n!==null;n=parents.get(n))path.push(points.get(n));path.reverse();
 routes.push({room:room.id,path});
}
const {points,parents,nearest}=graphFor('O01');
const corridor=nearest(13.5,data.spawn[2]);assert.ok(parents.has(corridor),'Common corridor unreachable');
const corridorPath=[];for(let n=corridor;n!==null;n=parents.get(n))corridorPath.push(points.get(n));routes.push({room:'CORRIDOR',path:corridorPath.reverse()});
{
 const {points,parents,nearest}=graphFor('O05');
 const bath=data.rooms.find(r=>r.id==='BATH').rings_xy_m.flat();
 const x=(Math.min(...bath.map(p=>p[0]))+Math.max(...bath.map(p=>p[0])))/2,z=-Math.min(...bath.map(p=>p[1]))-.38;
 const end=nearest(x,z);assert.ok(parents.has(end),'Shower unreachable');
 const path=[];for(let n=end;n!==null;n=parents.get(n))path.push(points.get(n));
 openings.SHOWER='O05';routes.push({room:'SHOWER',path:path.reverse()});
}
let minEye=Infinity,maxEye=-Infinity,frames=0;
function walk(path){
 for(const [x,z] of path){
  let reached=false;
  for(let i=0;i<90;i++){
   const p=engine.body.translation(),dx=x-p.x,dz=z-p.z,d=Math.hypot(dx,dz);
   if(d<.055){reached=true;break}
   engine.step({x:dx/d,z:dz/d});frames++;
   minEye=Math.min(minEye,engine.eye.y);maxEye=Math.max(maxEye,engine.eye.y);
   assert.ok(engine.eye.y>1.57&&engine.eye.y<1.63,'Fall or bad eye height');
  }
  assert.ok(reached,'Stuck on route near '+x+','+z+' at '+JSON.stringify(engine.eye));
 }
}
for(const route of routes){graphFor(openings[route.room]);assert.ok(engine.reset());walk(route.path);walk([...route.path].reverse());}
// A capsule in a leaf's future sweep must stop the leaf instead of being pushed.
const safety=new WalkEngine(data),door=safety.doors.find(d=>d.data.opening==='O01');
const before={...safety.body.translation()};safety.setDoor(door.data.id,true);
for(let i=0;i<90;i++)safety.step({x:0,z:0});
assert.ok(door.blocked&&door.fraction<.999,'Door must stop before player');
const playerDisplacement=Math.hypot(safety.body.translation().x-before.x,safety.body.translation().z-before.z);
assert.ok(playerDisplacement<.001,'Door pushed active player by '+playerDisplacement+' m');
safety.dispose();
const report={revision:data.revision,wardrobes_open:process.argv.includes('--wardrobes-open'),reachable_grid_cells:reachableCells,route_count:routes.length,round_trips_passed:routes.length,frames,minimum_eye_m:minEye,maximum_eye_m:maxEye,door_blocks_on_active_player:true,player_displacement_m:playerDisplacement,door_fraction_at_block:door.fraction,paths:routes};
const out=process.argv[2]||'../validation/e05';fs.mkdirSync(out,{recursive:true});fs.writeFileSync(out+'/walk-check.json',JSON.stringify(report,null,2)+'\n');
console.log({...report,paths:routes.map(r=>({room:r.room,waypoints:r.path.length}))});
engine.dispose();
