"""Reproducible apartment geometry, colliders and inspection views from metric data."""
from pathlib import Path
import bpy
import json
import math
import hashlib
import shutil
from mathutils import Vector
from mathutils.geometry import tessellate_polygon

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'architecture/model/departamento-t7.json'
data=json.loads(SOURCE.read_text(encoding='utf-8'))
revision=hashlib.sha256((data['revision']+hashlib.sha256(Path(__file__).read_bytes()).hexdigest()).encode()).hexdigest()
v=data['height_assumptions']
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for col in list(bpy.data.collections):bpy.data.collections.remove(col)
cols={}
for name in ['Architecture','Carpentry','Equipment','Decoration','Context','Roofs','References','Collisions']:
    col=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(col);cols[name]=col
scene=bpy.context.scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1;scene.unit_settings.length_unit='METERS'
scene['revision']=revision;scene['architecture_revision']=data['revision'];scene['eye_height_m']=1.6
mats={}
for name,color in {'wall':(.83,.855,.85),'floor':(.56,.62,.64),'terrace':(.32,.35,.37),'oak':(.46,.26,.12),'frame':(.7,.74,.75),'metal':(.22,.26,.29),'glass':(.3,.58,.69),'context':(.24,.31,.36),'white':(.95,.96,.94)}.items():
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1)
    bsdf=m.node_tree.nodes.get('Principled BSDF');bsdf.inputs['Base Color'].default_value=(*color,1);bsdf.inputs['Roughness'].default_value=.72
    if name=='metal':bsdf.inputs['Metallic'].default_value=.7;bsdf.inputs['Roughness'].default_value=.27
    if name=='glass':bsdf.inputs['Transmission Weight'].default_value=.3;bsdf.inputs['Roughness'].default_value=.18
    mats[name]=m
objects=[];colliders=[];doors=[];wall_checks=[];opening_checks=[]
gltf=lambda p:[p[0],p[2],-p[1]]
def assign(ob,name,mat,col,source=None):
    ob.name=name
    for old in list(ob.users_collection):old.objects.unlink(ob)
    cols[col].objects.link(ob);ob.data.materials.append(mats[mat])
    ob['id']=name;ob['revision']=revision;ob['category']=col
    ob['inspection_hide']=col in ['Context','Roofs']
    if source:ob['source']=source
    objects.append(ob)
    return ob
def box(name,center,size,mat='wall',col='Architecture',collision=True,source=None):
    assert min(size)>0,(name,size)
    bpy.ops.mesh.primitive_cube_add(size=1,location=center)
    ob=assign(bpy.context.object,name,mat,col,source);ob.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if collision:colliders.append(dict(id=name,type='box',center=gltf(center),size=[size[0],size[2],size[1]],category=col))
    return ob
def prism(name,polygon,bottom,top,mat='floor',col='Architecture'):
    verts=[(x,y,z) for z in [bottom,top] for x,y in polygon];n=len(polygon)
    triangles=tessellate_polygon([[Vector((x,y,0)) for x,y in polygon]])
    index=lambda p:min(range(n),key=lambda i:(polygon[i][0]-p.x)**2+(polygon[i][1]-p.y)**2)
    faces=[]
    for tri in triangles:
        inds=[p if isinstance(p,int) else index(p) for p in tri];faces.extend([tuple(reversed(inds)),tuple(i+n for i in inds)])
    for i in range(n):j=(i+1)%n;faces.append((i,j,j+n,i+n))
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    ob=bpy.data.objects.new(name,mesh);cols[col].objects.link(ob);ob.data.materials.append(mats[mat])
    ob['id']=name;ob['revision']=revision;ob['category']=col;ob['inspection_hide']=col in ['Context','Roofs'];objects.append(ob)
    # Make all face normals consistent for either polygon winding.
    bpy.context.view_layer.objects.active=ob;ob.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT');ob.select_set(False)
    return ob
def bounds(poly):return min(p[0] for p in poly),min(p[1] for p in poly),max(p[0] for p in poly),max(p[1] for p in poly)
def rectbox(name,rect,z0,z1,mat='wall',col='Architecture',collision=True,source=None):
    l,b,r,t=rect
    return box(name,((l+r)/2,(b+t)/2,(z0+z1)/2),(r-l,t-b,z1-z0),mat,col,collision,source)
outline=data['floor_polygon_xy_m'];xmin,ymin,xmax,ymax=bounds(outline)
xnotch,ynotch=outline[4]
prism('T7Floor',outline,-v['floor_slab_thickness'],0)
for name,rect in [('FloorMain',(xmin,ynotch,xmax,ymax)),('FloorWet',(xnotch,ymin,xmax,ynotch))]:
    l,b,r,t=rect;colliders.append(dict(id=name,type='box',center=gltf(((l+r)/2,(b+t)/2,-.1)),size=[r-l,.2,t-b],category='Architecture'))
prism('T7Ceiling',outline,v['clear_height'],v['clear_height']+v['false_ceiling_thickness'],'white','Roofs')
prism('T7Slab',outline,v['slab_bottom'],v['storey_height'],'context','Roofs')
prism('ProvisionalTerrace',data['terrace']['polygon_xy_m'],-.23,-.03,'terrace')
for w in data['walls']:
    r=bounds(w['polygon_xy_m']);ob=rectbox(w['id'],r,0,w['height_m'],source=w['source'])
    actual=[ob.matrix_world@Vector(p) for p in ob.bound_box]
    # matrix_world is refreshed below before final comparisons.
    wall_checks.append(dict(id=w['id'],expected_rect_xy_m=list(r)))
door_by_opening={d['opening']:d for d in data['doors']}
for o in data['openings']:
    if o['kind']=='paso_abierto':continue
    rect=bounds(o['polygon_xy_m']);l,b,r,t=rect
    axis=o['axis'];span=r-l if axis=='h' else t-b;depth=t-b if axis=='h' else r-l
    head=v['door_rough_head'] if o['kind']=='puerta' or o['kind']=='celosia_probable' else v['bath_window_head'] if o['id']=='O10' else v['window_head']
    sill=0 if o['kind'] in ['puerta','celosia_probable'] else v['bath_window_sill'] if o['id']=='O10' else v['window_sill']
    if sill:rectbox(o['id']+'_Sill',rect,0,sill)
    rectbox(o['id']+'_Lintel',rect,head,v['slab_bottom'])
    frame=v['door_frame_width'];mid=((l+r)/2,(b+t)/2)
    # Coordinate along opening, across wall, and height. Shared by all frames.
    def trim(suffix,u,z,length,height,material='frame',thickness=None,collision=True):
        d=depth if thickness is None else thickness
        center=(l+u,mid[1],z) if axis=='h' else (mid[0],b+u,z)
        size=(length,d,height) if axis=='h' else (d,length,height)
        return box(o['id']+'_'+suffix,center,size,material,'Carpentry',collision)
    trim('JambA',frame/2,(sill+head)/2,frame,head-sill)
    trim('JambB',span-frame/2,(sill+head)/2,frame,head-sill)
    trim('Head',span/2,head-frame/2,span-2*frame,frame)
    if o['kind']=='puerta':
        source=door_by_opening[o['id']]
        vec=Vector(source['closed_tip_xy_m'])-Vector(source['hinge_xy_m']);vec.normalize()
        length=span-2*frame-.006
        hinge=Vector(source['hinge_xy_m'])
        if axis=='h':hinge.x=l+frame+.003 if vec.x>0 else r-frame-.003
        else:hinge.y=b+frame+.003 if vec.y>0 else t-frame-.003
        angle=math.atan2(vec.y,vec.x)
        pivot=bpy.data.objects.new(source['id']+'_Pivot',None);cols['Carpentry'].objects.link(pivot);pivot.location=(*hinge,0);pivot.rotation_euler.z=angle
        pivot['revision']=revision;pivot['id']=source['id'];pivot['door']=True
        leaf=box(source['id']+'_Leaf',(0,0,0),(length,v['door_leaf_thickness'],v['door_leaf_height']),'oak','Carpentry',False)
        leaf.parent=pivot;leaf.location=(length/2,0,v['door_leaf_height']/2+.008)
        for sign in [-1,1]:
            handle=box(source['id']+f'_Handle{sign}',(0,0,0),(.105,.02,.02),'metal','Carpentry',False)
            handle.parent=pivot;handle.location=(length-.10,sign*.04,1.0)
        doors.append(dict(id=source['id'],pivot_name=pivot.name,leaf_name=leaf.name,pivot=gltf((*hinge,0)),size=[length,v['door_leaf_height'],v['door_leaf_thickness']],center_local=[length/2,v['door_leaf_height']/2+.008,0],base_rotation_y=-angle,swing_radians=-math.radians(source['swing_deg']),opening=o['id'],clear_span_m=span-2*frame,source_hinge_xy_m=source['hinge_xy_m'],physical_hinge_xy_m=list(hinge),hinge_adjustment_m=(hinge-Vector(source['hinge_xy_m'])).length))
    elif o['kind']=='ventana':
        trim('Bottom',span/2,sill+frame/2,span-2*frame,frame)
        trim('Mullion',span/2,(sill+head)/2,frame,head-sill)
        trim('Glass',span/2,(sill+head)/2,span-2*frame,head-sill-2*frame,'glass',.014)
    else:
        count=int((head-sill)/.085)
        for i in range(count):trim(f'Louvre{i:02d}',span/2,sill+.04+i*.085,span-2*frame,.045,'frame',.04,False)
        # Conservative closed louvre boundary; it is not an invented exit.
        center=((l+r)/2,(b+t)/2,(sill+head)/2)
        colliders.append(dict(id=o['id']+'_Boundary',type='box',center=gltf(center),size=[r-l,head-sill,t-b],category='Carpentry'))
    opening_checks.append(dict(id=o['id'],rough_span_m=span,head_m=head,sill_m=sill,source=o['source']))
# Four-storey local context; upper masses have no copied T7 interior.
cwidth=data['context']['provisional']['common_corridor_clear_width_m']
rectbox('CommonCorridor',(xmax,ymin,xmax+cwidth,ymax+1.5),-.2,0,'floor','Context')
rectbox('NeighbourNorth',(xmin,ymax,xmax,ymax+6),0,10.8,'context','Context')
rectbox('NeighbourEast',(xmax+cwidth,ymin,xmax+cwidth+5,ymax+1.5),0,10.8,'context','Context')
for floor in range(1,4):
    z=floor*v['storey_height'];prism(f'UpperT6Mass{floor+1}',outline,z,z+2.5,'context','Context')
    prism(f'UpperSlab{floor+1}',outline,z+2.5,z+2.7,'frame','Context')
rectbox('CorridorEndSouth',(xmax,ymin-.12,xmax+cwidth,ymin),0,2.7,'context','Context')
rectbox('CorridorEndNorth',(xmax,ymax+1.5,xmax+cwidth,ymax+1.62),0,2.7,'context','Context')
# Ceiling and terrace edge colliders remain when inspection meshes are hidden.
for name,rect,z0,z1 in [('CeilingMain',(xmin,ynotch,xmax,ymax),2.4,2.5),('CeilingWet',(xnotch,ymin,xmax,ynotch),2.4,2.5),('TerraceFloor',(xmin,ymin,xnotch,ynotch),-.23,-.03)]:
    l,b,r,t=rect;colliders.append(dict(id=name,type='box',center=gltf(((l+r)/2,(b+t)/2,(z0+z1)/2)),size=[r-l,z1-z0,t-b],category='Roofs'))
for name,rect in [('TerraceSouth',(xmin,ymin-.05,xnotch,ymin)),('TerraceWest',(xmin-.05,ymin,xmin,ynotch))]:
    l,b,r,t=rect;colliders.append(dict(id=name,type='box',center=gltf(((l+r)/2,(b+t)/2,.6)),size=[r-l,1.2,t-b],category='Boundary'))
for c in colliders:
    center=c['center'];size=c['size']
    ob=box('COL_'+c['id'],(center[0],-center[2],center[1]),(size[0],size[2],size[1]),col='Collisions',collision=False)
    ob.hide_render=True;ob.hide_viewport=True;ob.display_type='WIRE'
bpy.context.view_layer.update()
for check in wall_checks:
    ob=bpy.data.objects[check['id']];verts=[ob.matrix_world@Vector(p) for p in ob.bound_box]
    actual=[min(p.x for p in verts),min(p.y for p in verts),max(p.x for p in verts),max(p.y for p in verts)]
    check['actual_rect_xy_m']=actual;check['max_error_m']=max(abs(a-b) for a,b in zip(actual,check['expected_rect_xy_m']))
    assert check['max_error_m']<1e-5
area=lambda ps:abs(sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(ps,ps[1:]+ps[:1])))/2
assert abs(area(outline)-77.1)<1e-8
assert len(doors)==6 and len(wall_checks)==40 and len(opening_checks)==12
def camera(name,location,target,ortho=17):
    cd=bpy.data.cameras.new(name);cd.type='ORTHO';cd.ortho_scale=ortho
    ob=bpy.data.objects.new(name,cd);cols['References'].objects.link(ob);ob.location=location;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();return ob
center=Vector(((xmin+xmax)/2,(ymin+ymax)/2,0))
cam_a=camera('IsometricA',center+Vector((-15,-15,15)),center,19.5)
cam_b=camera('IsometricB',center+Vector((15,15,15)),center,19.5)
scale=data['calibration_adjustment']['m_per_native_pixel']
cal=json.loads((ROOT/'architecture/calibration/t10-calibracion.json').read_text(encoding='utf-8'));u0,v0=cal['origin']['pixel_uv']
cam_top=camera('OrthographicPlan',((768-u0)*scale,(v0-406.5)*scale,30),((768-u0)*scale,(v0-406.5)*scale,0),1536*scale)
cam_top.rotation_euler=(0,0,0)
cd=bpy.data.cameras.new('WalkEye');eye=bpy.data.objects.new('WalkEye',cd);cols['References'].objects.link(eye)
entry=next(d for d in doors if d['opening']=='O01');eye.location=(xmax-.6,-entry['pivot'][2]-.4,1.6);eye['eye_height_m']=1.6
eye.rotation_euler=(Vector((eye.location.x-1,eye.location.y,1.6))-eye.location).to_track_quat('-Z','Y').to_euler()
scene.camera=cam_a
for p in ['validation/e04','assets/interchange','assets/colliders','web/public/models']:(ROOT/p).mkdir(parents=True,exist_ok=True)
blend=ROOT/'blender/DepartamentoT7.blend';glb=ROOT/'assets/interchange/departamento-t7.glb';cf=ROOT/'assets/colliders/departamento-t7.json'
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
bpy.ops.object.select_all(action='DESELECT')
for name in ['Architecture','Carpentry','Equipment','Decoration','Context','Roofs']:
    for ob in cols[name].objects:ob.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True,export_yup=True,export_extras=True)
payload=dict(revision=revision,architecture_revision=data['revision'],units='m',colliders=colliders,doors=doors,eye_height_m=1.6,spawn=gltf(tuple(eye.location)),rooms=data['rooms'],area_m2=area(outline),useful_area_m2=data['area']['including_door_thresholds_m2'])
cf.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
manifest=dict(revision=revision,architecture_revision=data['revision'],units='m',eye_height_m=1.6,model=glb.name,colliders=cf.name,hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [blend,glb,cf]},blender_version=bpy.app.version_string)
for p in [glb,cf]:shutil.copyfile(p,ROOT/'web/public/models'/p.name)
(ROOT/'web/public/models/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
report=dict(revision=revision,walls=wall_checks,openings=opening_checks,doors=doors,area_m2=area(outline),area_delta_m2=area(outline)-76.66,eye_m=eye.location.z,context_storeys=4,orthographic_camera_scale_m=cam_top.data.ortho_scale,collider_count=len(colliders),metric_source=SOURCE.relative_to(ROOT).as_posix())
(ROOT/'validation/e04/geometry-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
# Inspection views hide only roofs and opaque context; saved source retains them.
for name in ['Context','Roofs']:cols[name].hide_render=True
scene.render.engine='BLENDER_WORKBENCH';scene.display.shading.light='STUDIO';scene.display.shading.color_type='MATERIAL';scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True
scene.display.shading.background_type='WORLD';scene.world.color=(.82,.87,.91)
scene.render.image_settings.file_format='PNG';scene.render.resolution_percentage=100
for name,cam,size in [('isometrica-a',cam_a,(1600,1100)),('isometrica-b',cam_b,(1600,1100)),('ortografica',cam_top,(1536,813))]:
    scene.camera=cam;scene.render.resolution_x,scene.render.resolution_y=size;scene.render.filepath=str(ROOT/'validation/e04'/f'{name}.png');bpy.ops.render.render(write_still=True)
print('T7_ARCHITECTURE_OK',revision,len(objects),len(colliders))
