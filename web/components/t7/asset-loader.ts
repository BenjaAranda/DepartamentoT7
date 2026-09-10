import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import type { Group } from 'three';
export type BoxCollider = { id: string; center: [number, number, number]; size: [number, number, number]; type: 'box' };
export type CollisionData = { revision: string; units: string; colliders: BoxCollider[]; doors: { id: string; pivot: number[]; size: number[]; center_local: number[]; swing_radians: number }[] };
export type AssetBundle = { revision: string; scene: Group; collision: CollisionData; eyeHeight: number };
type Manifest = { revision: string; units: string; eye_height_m: number; model: string; colliders: string; hashes: Record<string, string> };
const digest = async (buffer: ArrayBuffer) => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', buffer)), n => n.toString(16).padStart(2, '0')).join('');
export async function loadBundle(manifestUrl: string, signal: AbortSignal): Promise<AssetBundle> {
  const response = await fetch(manifestUrl, { signal, cache: 'no-cache' });
  if (!response.ok) throw new Error('No se pudo obtener la versión del modelo.');
  const manifest = await response.json() as Manifest;
  if (!manifest || typeof manifest.revision !== 'string' || !manifest.hashes || typeof manifest.model !== 'string' || typeof manifest.colliders !== 'string') throw new Error('El manifiesto del modelo está incompleto.');
  if (manifest.units !== 'm' || manifest.eye_height_m !== 1.6) throw new Error('La escala del modelo no coincide con la esperada.');
  const base = new URL('.', new URL(manifestUrl, location.href));
  const files = await Promise.all([manifest.model, manifest.colliders].map(async (name: string) => {
    if (!/^[a-zA-Z0-9_.-]+$/.test(name)) throw new Error('Referencia de archivo inválida.');
    const fetched = await fetch(new URL(name, base), { signal });
    if (!fetched.ok) throw new Error('No se pudo descargar el departamento.');
    const bytes = await fetched.arrayBuffer();
    if (await digest(bytes) !== manifest.hashes[name]) throw new Error('Los archivos pertenecen a versiones distintas. Vuelve a cargar.');
    return bytes;
  }));
  const collision: CollisionData = JSON.parse(new TextDecoder().decode(files[1]));
  if (collision.revision !== manifest.revision || collision.units !== 'm') throw new Error('Las colisiones no corresponden al modelo.');
  const gltf = await new GLTFLoader().parseAsync(files[0], base.href);
  gltf.scene.traverse(object => {
    if (object.userData.revision && object.userData.revision !== manifest.revision) throw new Error('La geometría tiene una revisión diferente.');
    object.castShadow = true; object.receiveShadow = true;
  });
  if (signal.aborted) throw new DOMException('Aborted', 'AbortError');
  return { revision: manifest.revision, scene: gltf.scene, collision, eyeHeight: manifest.eye_height_m };
}
