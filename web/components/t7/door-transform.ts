import { Quaternion, Vector3, type Object3D } from 'three';

const up = new Vector3(0, 1, 0);
const target = new Quaternion();

/** Replace the whole local rotation: a glTF half-turn may decompose to X/Z Euler turns. */
export function applyDoorAngle(pivot: Object3D, angle: number): boolean {
  target.setFromAxisAngle(up, angle);
  if (Math.abs(pivot.quaternion.dot(target)) > 1 - 1e-12) return false;
  pivot.quaternion.copy(target);
  return true;
}
