import RAPIER from '@dimforge/rapier3d-compat';
import type { CollisionData, DoorData } from './asset-loader.ts';

export const STEP = 1 / 60;
export const RADIUS = .22;
export const HALF_HEIGHT = .6;
export const BODY_REST_Y = RADIUS + HALF_HEIGHT + .01;
const IDENTITY = { x: 0, y: 0, z: 0, w: 1 };
let ready: Promise<void> | undefined;
export const initPhysics = () => ready ??= RAPIER.init();
type DoorState = { data: DoorData; body: RAPIER.RigidBody; collider: RAPIER.Collider; fraction: number; target: number; blocked: boolean };
export type WalkInput = { x: number; z: number; paused?: boolean };

export class WalkEngine {
  world: RAPIER.World;
  body: RAPIER.RigidBody;
  player: RAPIER.Collider;
  controller: RAPIER.KinematicCharacterController;
  doors: DoorState[] = [];
  labels = new Map<number, string>();
  floorHandles = new Set<number>();
  data: CollisionData;
  verticalVelocity = 0;
  accumulator = 0;
  elapsedSteps = 0;
  message = '';
  disposed = false;
  constructor(data: CollisionData) {
    this.data = data;
    this.world = new RAPIER.World({ x: 0, y: -9.81, z: 0 });
    this.world.timestep = STEP;
    for (const c of data.colliders) {
      const collider = this.world.createCollider(RAPIER.ColliderDesc.cuboid(c.size[0] / 2, c.size[1] / 2, c.size[2] / 2).setTranslation(...c.center));
      this.labels.set(collider.handle, c.id);
      const top=c.center[1]+c.size[1]/2;
      if(c.center[1]<0&&top>=-.1&&top<=.05&&c.size[1]<.4)this.floorHandles.add(collider.handle);
    }
    const spawn = data.spawn || [0, 1.6, 1.5];
    this.body = this.world.createRigidBody(RAPIER.RigidBodyDesc.kinematicPositionBased().setTranslation(spawn[0], BODY_REST_Y, spawn[2]));
    this.player = this.world.createCollider(RAPIER.ColliderDesc.capsule(HALF_HEIGHT, RADIUS), this.body);
    this.labels.set(this.player.handle, 'PLAYER');
    this.controller = this.world.createCharacterController(.01);
    this.controller.setNormalNudgeFactor(.01);
    this.controller.enableSnapToGround(.12);
    this.controller.setSlideEnabled(true);
    this.controller.setApplyImpulsesToDynamicBodies(false);
    for (const d of data.doors) {
      const body = this.world.createRigidBody(RAPIER.RigidBodyDesc.kinematicPositionBased());
      const collider = this.world.createCollider(RAPIER.ColliderDesc.cuboid(d.size[0] / 2, d.size[1] / 2, d.size[2] / 2), body);
      this.labels.set(collider.handle, d.id);
      const state: DoorState = { data: d, body, collider, fraction: 0, target: 0, blocked: false };
      this.doors.push(state);
      this.placeDoor(state, 0, true);
    }
    this.world.step();
    if (!this.isFree(spawn[0], spawn[2])) throw new Error('La posición inicial está ocupada.');
  }
  doorPose(d: DoorData, fraction: number) {
    const angle = (d.base_rotation_y || 0) + d.swing_radians * fraction;
    const [x, y, z] = d.center_local;
    return { angle, position: { x: d.pivot[0] + Math.cos(angle) * x + Math.sin(angle) * z, y: d.pivot[1] + y, z: d.pivot[2] - Math.sin(angle) * x + Math.cos(angle) * z }, rotation: { x: 0, y: Math.sin(angle / 2), z: 0, w: Math.cos(angle / 2) } };
  }
  placeDoor(door: DoorState, fraction: number, immediate = false) {
    const pose = this.doorPose(door.data, fraction);
    if (immediate) { door.body.setTranslation(pose.position, true); door.body.setRotation(pose.rotation, true); }
    else { door.body.setNextKinematicTranslation(pose.position); door.body.setNextKinematicRotation(pose.rotation); }
    door.fraction = fraction;
  }
  setDoor(id: string, opened: boolean) {
    const door = this.doors.find(d => d.data.id === id);
    if (!door) throw new Error('Puerta desconocida.');
    door.target = opened ? 1 : 0; door.blocked = false; this.message = '';
  }
  nearestDoor(maxDistance = 1.55) {
    const p = this.body.translation();
    return this.doors.map(door => ({ door, distance: Math.hypot(p.x - door.data.pivot[0], p.z - door.data.pivot[2]) }))
      .filter(q => {
        if(q.distance>maxDistance)return false;
        const target=q.door.body.translation(),dx=target.x-p.x,dz=target.z-p.z,length=Math.hypot(dx,dz);
        if(length<.01)return true;
        const hit=this.world.castRay(new RAPIER.Ray({x:p.x,y:1.1,z:p.z},{x:dx/length,y:0,z:dz/length}),length+.02,true,undefined,undefined,this.player);
        return !hit||hit.collider.handle===q.door.collider.handle;
      }).sort((a, b) => a.distance - b.distance)[0]?.door;
  }
  interact() {
    const door = this.nearestDoor();
    if (door) this.setDoor(door.data.id, door.target < .5);
  }
  isFree(x: number, z: number, y = BODY_REST_Y, horizontalMargin = 0) {
    return !this.world.intersectionWithShape({ x, y, z }, IDENTITY, new RAPIER.Capsule(HALF_HEIGHT-horizontalMargin, RADIUS+horizontalMargin), undefined, undefined, this.player);
  }
  hasFloor(x: number, z: number) {
    return !!this.world.castRay(new RAPIER.Ray({ x, y: .12, z }, { x: 0, y: -1, z: 0 }), .5, true, undefined, undefined, this.player);
  }
  reset() {
    const spawn = this.data.spawn || [0, 1.6, 1.5];
    if (!this.isFree(spawn[0], spawn[2])) { this.message = 'El acceso está ocupado. Aparta la puerta antes de volver.'; return false; }
    this.body.setTranslation({ x: spawn[0], y: BODY_REST_Y, z: spawn[2] }, true);
    this.body.setNextKinematicTranslation({ x: spawn[0], y: BODY_REST_Y, z: spawn[2] });
    this.verticalVelocity = 0; this.accumulator = 0; this.world.step(); return true;
  }
  step(input: WalkInput) {
    for (const door of this.doors) {
      if (Math.abs(door.target - door.fraction) < 1e-6) {door.body.setLinvel({x:0,y:0,z:0},true);door.body.setAngvel({x:0,y:0,z:0},true);continue;}
      // <= 1.72 degrees per fixed step bounds the continuous angular sweep.
      const next = door.fraction + Math.sign(door.target - door.fraction) * Math.min(Math.abs(door.target - door.fraction), STEP * 1.1);
      const pose = this.doorPose(door.data, next);
      const shape = new RAPIER.Cuboid(Math.max(.001, door.data.size[0] / 2 - .002), door.data.size[1] / 2 - .002, door.data.size[2] / 2 - .002);
      const hit = this.world.intersectionWithShape(pose.position, pose.rotation, shape, undefined, undefined, door.collider, undefined,
        collider => !this.labels.get(collider.handle)?.startsWith((door.data.opening || '__none') + '_'));
      // Stop before the controller's contact skin treats the leaf as a moving platform.
      const player=this.body.translation(),dx=player.x-pose.position.x,dz=player.z-pose.position.z;
      const localX=Math.cos(pose.angle)*dx-Math.sin(pose.angle)*dz,localZ=Math.sin(pose.angle)*dx+Math.cos(pose.angle)*dz;
      const gapX=Math.max(0,Math.abs(localX)-door.data.size[0]/2),gapZ=Math.max(0,Math.abs(localZ)-door.data.size[2]/2);
      // Two motion steps include the broad-phase contact cached by Rapier.
      const contactMargin=.02+2*STEP*1.1*Math.abs(door.data.swing_radians)*Math.hypot(door.data.size[0],door.data.size[2]);
      const nearPlayer=Math.hypot(gapX,gapZ)<RADIUS+contactMargin&&Math.abs(player.y-pose.position.y)<HALF_HEIGHT+RADIUS+door.data.size[1]/2;
      if (hit||nearPlayer) {
        door.target = door.fraction; door.blocked = true;
        door.body.setLinvel({x:0,y:0,z:0},true);door.body.setAngvel({x:0,y:0,z:0},true);
        this.message = 'Hay un obstáculo junto a la puerta.';
      } else this.placeDoor(door, next);
    }
    if (!input.paused) {
      const length = Math.hypot(input.x, input.z);
      const x = length > 1 ? input.x / length : input.x, z = length > 1 ? input.z / length : input.z;
      this.verticalVelocity = this.controller.computedGrounded() ? -.1 : Math.max(-10, this.verticalVelocity - 9.81 * STEP);
      this.controller.computeColliderMovement(this.player, { x: x * 1.6 * STEP, y: this.verticalVelocity * STEP, z: z * 1.6 * STEP });
      const move = this.controller.computedMovement(), p = this.body.translation();
      this.body.setNextKinematicTranslation({ x: p.x + move.x, y: p.y + move.y, z: p.z + move.z });
    }
    this.world.step(); this.elapsedSteps++;
  }
  advance(seconds: number, input: WalkInput) {
    if(this.disposed)return;
    this.accumulator += Math.min(Math.max(seconds, 0), .1);
    while (this.accumulator >= STEP) { this.step(input); this.accumulator -= STEP; }
  }
  get eye() {
    const p=this.body.translation();
    const floor=this.world.castRay(new RAPIER.Ray(p,{x:0,y:-1,z:0}),HALF_HEIGHT+RADIUS+.05,true,undefined,undefined,this.player,undefined,c=>this.floorHandles.has(c.handle));
    // The collision skin may nudge the capsule; the eye stays 1.60 m above its supporting floor.
    // Outside that small support range it follows the body, so a fall is never hidden.
    const supported=floor&&floor.timeOfImpact>=HALF_HEIGHT+RADIUS-.015;
    return {x:p.x,y:supported?p.y-floor.timeOfImpact+1.6:p.y+1.6-BODY_REST_Y,z:p.z};
  }
  dispose() { if(!this.disposed){this.disposed=true;this.world.free();} }
}
