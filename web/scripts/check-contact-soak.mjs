import fs from 'node:fs';
import assert from 'node:assert/strict';
import {WalkEngine,initPhysics} from '../components/t7/walk-engine.ts';
await initPhysics();
const data=JSON.parse(fs.readFileSync('public/models/departamento-t7.json'));
const engine=new WalkEngine(data),trips=[];
for(let trip=0;trip<40;trip++){
 for(let frame=0;frame<360+trip%3;frame++)engine.step({x:-1,z:0});
 const contact={...engine.body.translation()};
 for(let frame=0;frame<360;frame++)engine.step({x:1,z:0});
 const end={...engine.body.translation()};
 trips.push({trip,contact,end});
 assert.ok(end.x>12,'Repeated contact cannot retreat: '+JSON.stringify(trips.at(-1)));
 assert.ok(Math.abs(engine.eye.y-1.6)<.005);
}
const report={revision:data.revision,round_trips:trips.length,contact_recoveries:engine.contactRecoveries,passed:true,trips};
fs.mkdirSync('../validation/e10',{recursive:true});fs.writeFileSync('../validation/e10/contact-soak.json',JSON.stringify(report,null,2)+'\n');
console.log({round_trips:trips.length,passed:true});engine.dispose();
