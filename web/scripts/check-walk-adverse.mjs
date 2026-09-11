import fs from 'node:fs';
import assert from 'node:assert/strict';
import {WalkEngine,initPhysics,BODY_REST_Y} from '../components/t7/walk-engine.ts';
await initPhysics();
const data=JSON.parse(fs.readFileSync('public/models/departamento-t7.json'));
const e=new WalkEngine(data);
function place(x,z){e.body.setTranslation({x,y:BODY_REST_Y,z},true);e.body.setNextKinematicTranslation({x,y:BODY_REST_Y,z});e.verticalVelocity=0;e.world.step();assert.ok(e.isFree(x,z));}
place(11.2,-2.5);
const doors=[];
for(const d of e.doors){
 e.setDoor(d.data.id,true);for(let i=0;i<70;i++)e.step({x:0,z:0,paused:true});
 assert.ok(d.fraction>.999,'Opening blocked by architecture: '+d.data.id+' fraction '+d.fraction);
 e.setDoor(d.data.id,false);for(let i=0;i<70;i++)e.step({x:0,z:0,paused:true});
 assert.ok(d.fraction<.001,'Closing blocked by architecture: '+d.data.id);
 doors.push(d.data.id);
}
function distance(input){place(11.2,-2.5);const p={...e.body.translation()};for(let i=0;i<15;i++)e.step(input);return Math.hypot(e.body.translation().x-p.x,e.body.translation().z-p.z);}
const straight=distance({x:0,z:1}),diagonal=distance({x:1,z:1});assert.ok(Math.abs(straight-diagonal)<.002);
// Furnished-scene fixtures start in clear floor space, away from the sofa and table.
place(10,-4.7);for(let i=0;i<120;i++)e.advance(.1,{x:0,z:-1});
const wall={...e.eye};assert.ok(wall.z> -4.94&&wall.z< -4.90&&Math.abs(wall.y-1.6)<.005);
place(3,-.7);for(let i=0;i<180;i++)e.step({x:0,z:1});
const window={...e.eye};assert.ok(window.z<-.22&&window.z>-.25&&Math.abs(window.y-1.6)<.005);
const pausedBefore={...e.eye};for(let i=0;i<240;i++)e.advance(.05,{x:1,z:1,paused:true});
assert.ok(Math.hypot(e.eye.x-pausedBefore.x,e.eye.z-pausedBefore.z)<1e-5);
assert.ok(e.reset());const reset={...e.eye};assert.ok(Math.hypot(reset.x-data.spawn[0],reset.z-data.spawn[2])<.001);
// Exact contact position observed during browser QA: retreat must work without reset.
const contact={x:3.016615629196167,y:.8299375176429747,z:-4.723948955535889};
e.body.setTranslation(contact,true);e.body.setNextKinematicTranslation(contact);e.world.step();
for(let i=0;i<180;i++)e.step({x:1,z:0});const retreat={...e.eye};assert.ok(retreat.x>7.5,'Cannot retreat from closed D3 door');
// The camera stabilizer must not conceal an unsupported fall.
e.body.setTranslation({x:30,y:.83,z:30},true);e.body.setNextKinematicTranslation({x:30,y:.83,z:30});e.world.step();
for(let i=0;i<60;i++)e.step({x:0,z:0});assert.ok(e.eye.y<0,'Unsupported camera must follow the falling capsule');
const report={revision:data.revision,all_doors_open_and_close:doors,straight_distance_m:straight,diagonal_distance_m:diagonal,low_fps_wall_stop:wall,window_stop:window,pause_no_drift:true,reset_valid:true,retreat_from_closed_door:retreat,unsupported_fall_is_not_hidden:true};
const out=process.argv[2]||'../validation/e05';fs.mkdirSync(out,{recursive:true});fs.writeFileSync(out+'/adverse-check.json',JSON.stringify(report,null,2)+'\n');console.log(report);e.dispose();
