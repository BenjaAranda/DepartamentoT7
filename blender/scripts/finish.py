"""Deterministic PBR textures, metre-based UVs and decoration with collision proxies."""
import bpy, math
import numpy as np
from mathutils import Vector

def build(root,data,box,prism,assign,mats,cols,colliders,revision):
    palette={'sand':(.57,.45,.29),'leaf':(.11,.25,.12),'leaf_light':(.24,.36,.15),'clay':(.48,.22,.13),'art_blue':(.08,.23,.29),'art_cream':(.87,.78,.59),'rug':(.58,.55,.44),'lamp':(.90,.83,.64),'mirror':(.50,.59,.63),'paper':(.86,.83,.70)}
    for name,color in palette.items():
        m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=.83
        if name=='lamp':bs.inputs['Emission Color'].default_value=(*color,1);bs.inputs['Emission Strength'].default_value=1.4
        if name=='mirror':bs.inputs['Metallic'].default_value=.95;bs.inputs['Roughness'].default_value=.09
        mats[name]=m
    texture_dir=root/'blender/textures';texture_dir.mkdir(exist_ok=True)
    n=512;yy,xx=np.mgrid[0:n,0:n]/n;rng=np.random.default_rng(71020)
    # Repeat unit 1.2 m: eight 15-cm planks, staggered 60-cm ends.
    row=np.floor(yy*8);grain=.024*np.sin(xx*220+np.sin(yy*130)*2)+.012*np.sin(xx*780)+rng.normal(0,.007,(n,n))
    board=(np.sin(row*31)*.035)+grain
    joints=(np.mod(yy*8,1)<.018)|(np.mod(xx*2+np.mod(row,2)*.5,1)<.0035)
    oak=np.clip(np.array([.69,.56,.40])[None,None,:]+board[:,:,None],0,1);oak[joints]*=.73
    grout=(np.mod(xx*4,1)<.010)|(np.mod(yy*4,1)<.010)
    tiles=np.clip(np.array([.73,.74,.71])[None,None,:]+rng.normal(0,.007,(n,n,1)),0,1);tiles[grout]=[.55,.57,.55]
    textures={}
    for name,pixels in [('OakPlanks',oak),('Porcelain',tiles)]:
        im=bpy.data.images.new(name,width=n,height=n,alpha=False)
        rgba=np.ones((n,n,4),dtype=np.float32);rgba[:,:,:3]=pixels;im.pixels.foreach_set(rgba.ravel());im.filepath_raw=str(texture_dir/(name+'.png'));im.file_format='PNG';im.save();im.pack()
        textures[name]=im
    for name,tex in [('floor','OakPlanks'),('oak','OakPlanks')]:
        m=mats[name];node=m.node_tree.nodes.new('ShaderNodeTexImage');node.image=textures[tex];m.node_tree.links.new(node.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs['Base Color']);m.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.64
    m=bpy.data.materials.new('porcelain');m.diffuse_color=(.73,.74,.71,1);bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.73
    node=m.node_tree.nodes.new('ShaderNodeTexImage');node.image=textures['Porcelain'];m.node_tree.links.new(node.outputs['Color'],bs.inputs['Base Color']);mats['porcelain']=m
    for room in data['rooms']:
        if room['id'] in ['BATH','KITCHEN','LOGIA']:
            for i,ring in enumerate(room['rings_xy_m']):prism('Finish_'+room['id']+str(i),ring,.0005,.0025,'porcelain')
    decoration=[]
    def deco(name,center,size,mat='sand',collision=False,bevel=0):
        ob=box(name,center,size,mat,'Decoration',collision);decoration.append(name)
        if bevel:
            mod=ob.modifiers.new('Soft edge','BEVEL');mod.width=bevel;mod.segments=3;bpy.context.view_layer.objects.active=ob;bpy.ops.object.modifier_apply(modifier=mod.name)
        return ob
    def ellipsoid(name,p,scale,mat):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=1,location=p);ob=assign(bpy.context.object,name,mat,'Decoration');ob.scale=scale
        bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        for face in ob.data.polygons:face.use_smooth=True
        decoration.append(ob.name);return ob
    def cylinder(name,p,radius,depth,mat):
        bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=radius,depth=depth,location=p);ob=assign(bpy.context.object,name,mat,'Decoration');decoration.append(ob.name);return ob
    def plant(name,p,small=False):
        x,y,z=p;s=.32 if small else 1
        cylinder(name+'_Pot',(x,y,z+.16*s),.15*s,.32*s,'clay')
        cylinder(name+'_Soil',(x,y,z+.322*s),.132*s,.012*s,'oak')
        for i in range(7):
            a=i*2.399;h=(.45+(i%3)*.17)*s;px=x+math.cos(a)*.105*s;py=y+math.sin(a)*.105*s
            deco(name+f'_Stem{i}',(px,py,z+.33*s+h/2),(.014*s,.014*s,h),'leaf',False)
            ob=ellipsoid(name+f'_Leaf{i}',(px,py,z+.32*s+h),(.07*s,.18*s,.055*s),'leaf' if i%2 else 'leaf_light');ob.rotation_euler.z=a
        if not small:colliders.append(dict(id=name+'_Proxy',type='box',center=[x,z+.59,-y],size=[.56,1.18,.56],category='Decoration'))
    plant('Living_Plant',(12.16,1.58,0))
    plant('D1_TablePlant',(.26,2.33,.52),True)
    plant('Kitchen_Herb',(8.68,1.73,.895),True)
    # Thin rugs have no raised thresholds; furniture and walls remain authoritative.
    for name,p,size in [('Living_Rug',(11.10,3.03,.004),(1.70,2.15,.008)),('D1_Rug',(2.58,1.13,.004),(.80,1.68,.008)),('D2_Rug',(5.52,1.20,.004),(.73,1.72,.008)),('D3_Rug',(1.40,4.04,.004),(.50,1.35,.008))]:
        deco(name,p,size,'rug',False,.003)
        for edge in [-1,1]:deco(name+f'_Border{edge}',(p[0]+edge*(size[0]/2-.045),p[1],.009),(.02,size[1]-.08,.002),'sand')
    # Art is geometric, authored here, with no third-party image dependencies.
    for name,x,y,z,w,h,axis in [('Art_D1',.026,1.20,1.55,.88,.55,'x'),('Art_D2',5.65,.026,1.45,.66,.50,'y'),('Art_D3',.55,5.126,1.52,.68,.50,'y'),('Art_Living',12.515,3.03,1.61,1.05,.62,'x')]:
        dims=(.035,w,h) if axis=='x' else (w,.035,h)
        deco(name+'_Frame',(x,y,z),dims,'oak')
        # Put canvas on both faces so the intended interior side is visible.
        for sign in [-1,1]:
            p=(x+sign*.019,y,z) if axis=='x' else (x,y+sign*.019,z)
            size=(.003,w-.05,h-.05) if axis=='x' else (w-.05,.003,h-.05)
            deco(name+f'_Canvas{sign}',p,size,'art_cream')
            p=(p[0]+sign*.003,p[1]-.10,p[2]-.06) if axis=='x' else (p[0]-.10,p[1]+sign*.003,p[2]-.06)
            deco(name+f'_Landscape{sign}',p,(.003,w*.47,h*.37) if axis=='x' else (w*.47,.003,h*.37),'art_blue')
    deco('Bath_MirrorFrame',(8.305,2.88,1.40),(.03,.57,.76),'oak')
    deco('Bath_Mirror',(8.286,2.88,1.40),(.006,.53,.72),'mirror')
    # Cushions rest on the sofa; they do not add floor obstacles.
    for i,y in enumerate([2.43,3.60]):ellipsoid(f'Living_Pillow{i}',(12.13,y,.65),(.12,.21,.21),'sage' if i else 'sand')
    # Bedside lights and a standing lamp.
    for name,x,y,z in [('D1_Lamp',.26,.215,.52),('D2_Lamp',5.33,.32,.52),('D3_Lamp',1.29,4.87,.52),('Living_Lamp',10.55,1.88,0)]:
        floor=z==0;height=1.48 if floor else .33;radius=.20 if floor else .10
        cylinder(name+'_Base',(x,y,z+.018),radius*.7,.035,'metal');deco(name+'_Stem',(x,y,z+height/2),(.018,.018,height),'brass')
        cylinder(name+'_Shade',(x,y,z+height),radius,.26 if floor else .18,'lamp')
        if floor:colliders.append(dict(id=name+'_Proxy',type='box',center=[x,.80,-y],size=[.40,1.60,.40],category='Decoration'))
    # Books, folded towels and kitchen accessories remain on supporting furniture.
    for i in range(3):deco(f'Living_Book{i}',(10.23,2.71,.555+i*.027),(.24,.16,.025),['art_blue','paper','clay'][i])
    deco('Bath_TowelRail',(6.785,2.65,1.10),(.035,.50,.025),'metal')
    deco('Bath_Towel',(6.81,2.65,.93),(.018,.37,.33),'linen')
    cylinder('Kitchen_Jar',(8.66,2.18,1.015),.065,.24,'ceramic')
    cylinder('Dining_Vase',(11.3,-.30,.87),.07,.18,'clay')
    lights=[('D1',2.05,1.65),('D2',5.5,2.2),('D3',1.25,4.5),('HallWest',3.6,4.64),('HallCenter',6.1,4.64),('HallEast',8.9,4.65),('Living',11.2,3.25),('Dining',11.25,-.25),('Kitchen',9.4,2.15),('Bath',7.5,2.65),('Shower',7.5,-.55),('Loggia',9.5,-.55)]
    for name,x,y in lights:
        ob=cylinder('CeilingLight_'+name,(x,y,2.365),.16,.055,'lamp');ob['inspection_hide']=True
        ld=bpy.data.lights.new('Light_'+name,'AREA');ld.energy=65;ld.color=(1,.88,.70);ld.shape='DISK';ld.size=.55
        lo=bpy.data.objects.new('Light_'+name,ld);cols['References'].objects.link(lo);lo.location=(x,y,2.30)
    # All UV coordinates derive from metric vertex positions (1.2-m repeat).
    bpy.context.view_layer.update()
    for ob in list(cols['Architecture'].objects)+list(cols['Carpentry'].objects)+list(cols['Equipment'].objects):
        if ob.type!='MESH':continue
        uv=ob.data.uv_layers.active or ob.data.uv_layers.new(name='MetricUV')
        for face in ob.data.polygons:
            normal=ob.matrix_world.to_3x3()@face.normal;axis=max(range(3),key=lambda i:abs(normal[i]));axes=[i for i in range(3) if i!=axis]
            for index in face.loop_indices:
                p=ob.matrix_world@ob.data.vertices[ob.data.loops[index].vertex_index].co;uv.data[index].uv=(p[axes[0]]/1.2,p[axes[1]]/1.2)
    return dict(decorations=decoration,lights=[dict(id=n,position=[x,2.30,-y]) for n,x,y in lights],texture_repeat_m=1.2,textures=[(texture_dir/(n+'.png')).relative_to(root).as_posix() for n in textures])
