"""Blender T17/T18 proof: metric ruler, eye datum and hinged doorway."""
from pathlib import Path
import bpy
import json
import hashlib
import shutil
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[2]
data=json.loads((ROOT/'architecture/model/departamento-t7.json').read_text(encoding='utf-8'))
revision=data['revision']
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for col in list(bpy.data.collections):bpy.data.collections.remove(col)
collections={}
for name in ['Architecture','Equipment','Decoration','References','Collisions']:
    col=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(col);collections[name]=col
scene=bpy.context.scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1;scene.unit_settings.length_unit='METERS'
scene['revision']=revision;scene['eye_height_m']=1.6
def material(name,color):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    bsdf=m.node_tree.nodes.get('Principled BSDF');bsdf.inputs['Base Color'].default_value=(*color,1)
    bsdf.inputs['Roughness'].default_value=.7
    return m
mats={'wall':material('Chalk',(0.82,.85,.86)),'floor':material('Slate',(.23,.29,.34)),
      'door':material('Oak',(.43,.25,.12)),'metric':material('MetricOrange',(.98,.38,.05)),
      'eye':material('EyeBlue',(.02,.38,.66))}
colliders=[]
def box(name,pos,size,mat,col='Architecture',collision=True):
    bpy.ops.mesh.primitive_cube_add(size=1,location=pos)
    ob=bpy.context.object;ob.name=name;ob.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    for old in list(ob.users_collection):old.objects.unlink(ob)
    collections[col].objects.link(ob);ob.data.materials.append(mats[mat]);ob['id']=name;ob['revision']=revision
    if collision:
        colliders.append(dict(id=name,center=[pos[0],pos[2],-pos[1]],size=[size[0],size[2],size[1]],type='box'))
    return ob
box('ProofFloor',(0,0,-.1),(5,5,.2),'floor')
box('ProofWallLeft',(-1.225,0,1.2),(1.55,.2,2.4),'wall')
box('ProofWallRight',(1.225,0,1.2),(1.55,.2,2.4),'wall')
box('ProofLintel',(0,0,2.26),(.9,.2,.28),'wall')
pivot=bpy.data.objects.new('ProofDoorPivot',None);collections['Architecture'].objects.link(pivot);pivot.location=(-.425,0,0);pivot['revision']=revision
leaf=box('ProofDoor',(0,0,1.035),(.85,.035,2.07),'door',collision=False)
leaf.parent=pivot;leaf.location=(.425,0,1.035)
box('ProofRuler1m',(-1,-1.2,.03),(1,.05,.06),'metric','References',False)
box('ProofEyeDatum',(1,-1.2,1.6),(.4,.025,.01),'eye','References',False)
box('ProofEyePole',(1,-1.2,.8),(.015,.015,1.6),'eye','References',False)
for c in colliders:
    pos=c['center'];size=c['size']
    ob=box('COL_'+c['id'],(pos[0],-pos[2],pos[1]),(size[0],size[2],size[1]),'wall','Collisions',False)
    ob.hide_render=True;ob.hide_viewport=True;ob.display_type='WIRE'
camera_data=bpy.data.cameras.new('EyeCamera');camera=bpy.data.objects.new('EyeCamera',camera_data)
collections['References'].objects.link(camera);camera.location=(0,-2,1.6);camera.rotation_euler=(Vector((0,0,1.6))-camera.location).to_track_quat('-Z','Y').to_euler();scene.camera=camera
camera['eye_height_m']=1.6
for p in ['assets/interchange','assets/colliders','web/public/models','validation/e03']:(ROOT/p).mkdir(parents=True,exist_ok=True)
blend=ROOT/'blender/DepartamentoT7-prueba.blend';glb=ROOT/'assets/interchange/t7-prueba.glb'
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
bpy.ops.object.select_all(action='DESELECT')
for name in ['Architecture','References']:
    for ob in collections[name].objects:ob.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True,export_yup=True,export_extras=True,export_cameras=True)
collision_file=ROOT/'assets/colliders/t7-prueba.json'
collision_file.write_text(json.dumps(dict(revision=revision,units='m',axes='glTF +Y up',colliders=colliders,
    doors=[dict(id='ProofDoor',pivot=[-.425,0,0],size=[.85,2.07,.035],center_local=[.425,1.035,0],swing_radians=-1.5707963267948966)]),indent=2)+'\n',encoding='utf-8',newline='\n')
assert abs(bpy.data.objects['ProofRuler1m'].dimensions.x-1)<1e-6
assert abs(camera.location.z-1.6)<1e-6
assert all(abs(k-1)<1e-6 for ob in bpy.data.objects if ob.type=='MESH' for k in ob.scale)
manifest=dict(revision=revision,units='m',eye_height_m=1.6,model='t7-prueba.glb',colliders='t7-prueba.json',
              hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [blend,glb,collision_file]},blender_version=bpy.app.version_string)
for p in [glb,collision_file]:shutil.copyfile(p,ROOT/'web/public/models'/p.name)
(ROOT/'web/public/models/proof-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
(ROOT/'validation/e03/blender-check.json').write_text(json.dumps(dict(revision=revision,metric_scale=1,ruler_m=1,eye_z_m=camera.location.z,collections=list(collections),applied_mesh_scale=True,collider_count=len(colliders)),indent=2)+'\n',encoding='utf-8',newline='\n')
print('T7_EXCHANGE_PROOF_OK',revision)
