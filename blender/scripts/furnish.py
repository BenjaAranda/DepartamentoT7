"""Parametric furniture: editable metric inventory, render meshes and shared colliders."""
import bpy, math
from mathutils import Vector

def build(items, box, assign, mats, cols, doors, colliders, revision):
    inventory=[]
    palette={'linen':(.73,.75,.69),'sage':(.26,.37,.31),'fabric':(.40,.49,.47),'navy':(.045,.10,.14),'stone':(.78,.77,.71),'black':(.018,.027,.033),'ceramic':(.89,.9,.86),'brass':(.42,.28,.10),'sheet':(.91,.87,.77)}
    for name,color in palette.items():
        m=bpy.data.materials.new(name);m.diffuse_color=(*color,1)
        bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=.8
        if name in ['brass']:bs.inputs['Metallic'].default_value=.75;bs.inputs['Roughness'].default_value=.28
        if name=='ceramic':bs.inputs['Roughness'].default_value=.22
        mats[name]=m
    for item in items:
        ident=item['id'];w,d=item['size'];cx,cy=item['center'];angle=math.radians(item.get('rotation',0));co,si=math.cos(angle),math.sin(angle)
        names=[]
        def point(p):x,y,z=p;return (cx+co*x-si*y,cy+si*x+co*y,z)
        def part(suffix,p,size,mat='oak',collision=True,bevel=0):
            # Orthogonal assemblies permit exact axis-aligned box proxies.
            ob=box(ident+'_'+suffix,point(p),(abs(co)*size[0]+abs(si)*size[1],abs(si)*size[0]+abs(co)*size[1],size[2]),mat,'Equipment',collision)
            ob['assembly']=ident;ob['room']=item['room'];names.append(ob.name)
            if bevel:
                mod=ob.modifiers.new('Soft edges','BEVEL');mod.width=bevel;mod.segments=3
                bpy.context.view_layer.objects.active=ob;bpy.ops.object.modifier_apply(modifier=mod.name)
                for face in ob.data.polygons:face.use_smooth=True
                mod=ob.modifiers.new('Weighted normals','WEIGHTED_NORMAL');bpy.ops.object.modifier_apply(modifier=mod.name)
            return ob
        def legset(zheight,spread=.07):
            for ix in [-1,1]:
                for iy in [-1,1]:part(f'Leg{ix}{iy}',(ix*(w/2-spread),iy*(d/2-spread),zheight/2),(.035,.035,zheight),'oak')
        def faucet(z,back_y,width=.03):
            part('TapPost',(0,back_y,z+.13),(width,width,.26),'metal',False,.009)
            part('TapSpout',(0,back_y-.07,z+.25),(width,.16,width),'metal',False,.009)
        def bowl(z,width,depth,mat='ceramic'):
            # Open basin, four rounded rims and recessed bottom, no solid lid.
            for sign in [-1,1]:
                part(f'BasinSide{sign}',(sign*(width/2-.025),0,z-.07),(.05,depth,.15),mat,True,.018)
                part(f'BasinRim{sign}',(0,sign*(depth/2-.025),z-.07),(width-.10,.05,.15),mat,True,.018)
            part('BasinBottom',(0,0,z-.145),(width-.05,depth-.05,.025),mat,True,.015)
            part('Drain',(0,0,z-.13),(.05,.05,.004),'metal',False,.015)
        kind=item['type']
        if kind=='bed':
            part('Base',(0,0,.22),(w,d,.25),'oak',True,.025)
            part('Mattress',(0,-.01,.44),(w-.035,d-.08,.22),'sheet',True,.075)
            part('Duvet',(0,-.30,.57),(w-.045,d-.70,.10),'linen',False,.055)
            part('Throw',(0,-d/2+.25,.627),(w-.04,.43,.025),'sage',False,.012)
            part('Headboard',(0,d/2-.025,.45),(w,.05,.9),'oak',True,.02)
            n=2 if item['double'] else 1
            for i in range(n):part(f'Pillow{i}',((i-(n-1)/2)*(w/n),d/2-.36,.605),(w/n-.12,.40,.13),'sheet',False,.06)
        elif kind=='nightstand':
            part('Body',(0,0,.31),(w,d,.40),'oak',True,.014)
            part('Drawer',(0,-d/2-.002,.36),(w-.04,.016,.19),'linen',False,.008)
            part('Handle',(0,-d/2-.021,.36),(.12,.023,.015),'brass',False)
            legset(.12)
        elif kind=='wardrobe':
            h=2.20
            part('Back',(0,d/2-.012,h/2),(w,.024,h),'linen')
            for sign in [-1,1]:part(f'Jamb{sign}',(sign*(w/2-.018),0,h/2),(.036,d,h),'wall')
            part('Plinth',(0,0,.055),(w,d,.11),'wall')
            part('Crown',(0,0,h-.035),(w+.012,d+.012,.07),'wall')
            part('Shelf',(0,0,.48),(w-.072,d-.02,.022),'linen')
            part('Rail',(0,0,1.87),(w-.072,.025,.025),'metal',False)
            leaf_width=(w-.080)/2
            for i,sign in enumerate([-1,1]):
                leafid=ident+f'_Door{i+1}';hp=point((sign*(w/2-.038),-d/2+.012,0));alpha=angle+(0 if sign==-1 else math.pi)
                pivot=bpy.data.objects.new(leafid+'_Pivot',None);cols['Equipment'].objects.link(pivot);pivot.location=hp;pivot.rotation_euler.z=alpha
                pivot['id']=leafid;pivot['revision']=revision;pivot['assembly']=ident;pivot['door']=True
                leaf=box(leafid+'_Leaf',(0,0,0),(leaf_width,.022,2.015),'linen','Equipment',False)
                leaf.parent=pivot;leaf.location=(leaf_width/2,0,1.1575);leaf['assembly']=ident;leaf['room']=item['room'];names.append(leaf.name)
                handle=box(leafid+'_Handle',(0,0,0),(.014,.034,.20),'brass','Equipment',False)
                handle.parent=pivot;handle.location=(leaf_width-.06,sign*.026,1.12);handle['assembly']=ident;names.append(handle.name)
                doors.append(dict(id=leafid,pivot_name=pivot.name,leaf_name=leaf.name,pivot=[hp[0],hp[2],-hp[1]],size=[leaf_width,2.015,.022],center_local=[leaf_width/2,1.1575,0],base_rotation_y=alpha,swing_radians=sign*math.pi/2,opening=ident,label=f'Armario dormitorio {item["room"][-1]} · hoja {i+1}',category='wardrobe'))
        elif kind in ['wall_tv','console_tv']:
            height=1.36 if kind=='wall_tv' else 1.16
            if kind=='console_tv':
                part('Cabinet',(0,0,.31),(w,d,.46),'oak',True,.012)
                for sign in [-1,1]:part(f'Front{sign}',(sign*w/4,-d/2-.004,.31),(w/2-.012,.016,.38),'linen',False)
                part('Stand',(0,0,.64),(.04,.04,.18),'black',False)
            width=1.03 if kind=='wall_tv' else 1.07
            part('Bezel',(0,-d/2+.01,height),(width,.035,.61),'black',True,.016)
            part('Screen',(0,-d/2-.009,height),(width-.024,.003,.584),'navy',False,.008)
        elif kind=='basin':
            bowl(.82,w,d);faucet(.82,d/2-.055)
            part('Trap',(0,d/2-.10,.56),(.06,.06,.28),'metal',False,.015)
        elif kind=='toilet':
            part('Pedestal',(0,-.035,.20),(.24,.43,.40),'ceramic',True,.08)
            part('Bowl',(0,-.07,.40),(w,.48,.18),'ceramic',True,.13)
            part('Seat',(0,-.09,.49),(w-.005,.43,.035),'white',True,.11)
            part('Cistern',(0,d/2-.07,.65),(w,.14,.40),'ceramic',True,.035)
            part('Flush',(0,d/2-.065,.855),(.05,.025,.008),'metal',False)
            for sign in [-1,1]:
                part(f'Grab{sign}',(sign*.39,-.01,.76),(.032,.65,.032),'metal',True,.015)
                part(f'GrabMount{sign}',(sign*.39,d/2-.05,.67),(.04,.04,.20),'metal',False,.015)
        elif kind=='shower':
            part('FlushFloor',(0,0,.002),(w,d,.004),'stone',False)
            part('LinearDrain',(0,-d/2+.09,.006),(w-.18,.045,.005),'metal',False)
            part('Mixer',(w/2-.05,.07,1.05),(.04,.18,.035),'metal',False,.013)
            part('Riser',(w/2-.04,.07,1.58),(.026,.026,1.10),'metal',False,.011)
            part('ShowerHead',(w/2-.14,.07,2.11),(.24,.20,.025),'metal',False,.014)
            part('WallGrab',(-w/2+.04,0,.76),(.035,.65,.035),'metal',True,.014)
            part('FoldedSeat',(-w/2+.055,.02,.60),(.065,.43,.38),'linen',True,.025)
        elif kind in ['counter','kitchen_sink','cooker','upper_cabinet']:
            z=.43 if kind=='kitchen_sink' else .48 if kind!='upper_cabinet' else 1.79;h=.62 if kind in ['upper_cabinet','kitchen_sink'] else .72
            part('Body',(0,0,z),(w,d,h),'sage',True,.009)
            part('Plinth',(0,.03,.07),(w-.03,d-.09,.14),'black') if kind!='upper_cabinet' else None
            for sign in [-1,1]:
                part(f'Front{sign}',(sign*w/4,-d/2-.007,z),(w/2-.013,.022,h-.035),'sage',False,.004)
                part(f'Pull{sign}',(sign*w/4,-d/2-.027,z+h/2-.08),(.12,.025,.012),'brass',False)
            if kind not in ['upper_cabinet','kitchen_sink']:part('Worktop',(0,0,.87),(w+.008,d+.02,.045),'stone',True,.008)
            if kind=='kitchen_sink':
                # Cabinet below; opening above modeled by the basin instead of a lid.
                bowl(.9,w-.04,d-.06,'metal');faucet(.9,d/2-.07)
            if kind=='cooker':
                part('OvenWindow',(0,-d/2-.021,.48),(w-.10,.009,.30),'black',False,.014)
                part('OvenPull',(0,-d/2-.055,.685),(w-.13,.03,.022),'metal',False)
                part('Hob',(0,0,.899),(w-.045,d-.045,.015),'black',False,.009)
                for ix in [-1,1]:
                    for iy in [-1,1]:
                        part(f'Burner{ix}{iy}',(ix*.125,iy*.13,.912),(.16,.16,.008),'metal',False,.07)
                part('Hood',(0,.04,1.78),(w,.44,.13),'metal',True,.022)
                part('Flue',(0,d/2-.11,2.05),(.22,.21,.42),'metal',True)
        elif kind=='fridge':
            part('Body',(0,0,1.02),(w,d,2.04),'metal',True,.018)
            for suffix,z,h in [('Freezer',.39,.70),('Door',1.39,1.24)]:
                part(suffix,(0,-d/2-.006,z),(w-.016,.027,h),'white',False,.012)
                part(suffix+'Pull',(-w/2+.06,-d/2-.035,z),(.025,.035,.26),'metal',False,.008)
        elif kind=='sofa':
            legset(.14)
            part('Base',(0,0,.29),(w,d,.28),'fabric',True,.065)
            part('Back',(0,d/2-.10,.64),(w,.20,.55),'fabric',True,.08)
            for sign in [-1,1]:
                part(f'Arm{sign}',(sign*(w/2-.075),-.015,.49),(.15,d-.08,.40),'fabric',True,.06)
                part(f'Seat{sign}',(sign*(w-.30)/4,-.08,.48),((w-.33)/2,d-.27,.15),'linen',False,.055)
                part(f'BackCushion{sign}',(sign*(w-.30)/4,.20,.71),((w-.33)/2,.13,.38),'linen',False,.06)
        elif kind=='table':
            part('Top',(0,0,.755),(w,d,.045),'oak',True,.025);legset(.735,.10)
        elif kind=='chair':
            legset(.43,.055);part('Seat',(0,0,.46),(w,d,.065),'linen',True,.04)
            part('Back',(0,d/2-.025,.72),(w,.045,.49),'oak',True,.04)
        elif kind=='washer':
            part('Body',(0,0,.43),(w,d,.86),'white',True,.02)
            part('Control',(0,-d/2-.003,.77),(w-.035,.012,.11),'metal',False)
            part('Porthole',(0,-d/2-.022,.41),(.40,.035,.40),'black',False,.18)
            part('Glass',(0,-d/2-.044,.41),(.29,.018,.29),'navy',False,.13)
            part('Knob',(-.16,-d/2-.025,.775),(.05,.025,.05),'white',False,.022)
        elif kind=='laundry_sink':
            bowl(.88,w,d);faucet(.88,d/2-.07)
            for sign in [-1,1]:part(f'Leg{sign}',(sign*(w/2-.05),0,.36),(.035,.035,.72),'metal')
        else:raise ValueError(kind)
        inventory.append({**item,'mesh_names':names,'forward_xy': [si,-co]})
    bpy.context.view_layer.update()
    for record in inventory:
        verts=[bpy.data.objects[n].matrix_world@Vector(p) for n in record['mesh_names'] for p in bpy.data.objects[n].bound_box]
        record['actual_bounds_xyz_m']=[[min(p[i] for p in verts) for i in range(3)],[max(p[i] for p in verts) for i in range(3)]]
    return inventory
