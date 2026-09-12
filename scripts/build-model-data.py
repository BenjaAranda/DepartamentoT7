"""T16: one metric contract, derived from the audited plan rather than web coordinates."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
read=lambda f:json.loads((ROOT/f).read_text(encoding='utf-8'))
sha=lambda f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
sources=['architecture/plan/t11-registro.json','architecture/dimensions/t13-superficies.json','architecture/dimensions/t14-alturas.json','architecture/dimensions/t15-contexto.json']
p,a,h,c=map(read,sources)
adjust=read('architecture/dimensions/t13-criterio-aproximado.json')
factor=adjust['xy_factor']
project=lambda points:[[x*factor,y*factor] for x,y in points]
sources.append('architecture/dimensions/t13-criterio-aproximado.json')
cal=read('architecture/calibration/t10-calibracion.json')
u0,v0=cal['origin']['pixel_uv'];scale=cal['scale']['m_per_px']*factor
def opening_polygon(o):
    if not o.get('rect_px'): return None
    l,t,r,b=o['rect_px']
    return [[(u-u0)*scale,(v0-v)*scale] for u,v in [[l,t],[r,t],[r,b],[l,b]]]
v={k:d['value_m'] for k,d in h['values'].items()}
data=dict(schema_version=1,project='DepartamentoT7',units='m',axes='Blender XYZ: right, plan-up, elevation',
          eye_height_m=1.6,sources={f:sha(f) for f in sources},height_assumptions=v,context=c,
          calibration_adjustment=adjust,floor_polygon_xy_m=project(a['outer']['polygon_xy_m']),
          terrace={**a['terrace'],'polygon_xy_m':project(a['terrace']['polygon_xy_m']),'provisional_visual_area_m2':a['terrace']['provisional_visual_area_m2']*factor**2},
          area={k:value*factor**2 if k.endswith('_m2') else value for k,value in a['useful'].items()},area_validation=adjust['checks'],
          rooms=[dict(id=r['id'],rings_xy_m=[project(ring) for ring in r['rings_xy_m']],area_m2=r['area_m2']*factor**2,source='T13/T11') for r in a['regions']],
          walls=[dict(id=w['id'],polygon_xy_m=project(w['polygon_xy_m']),height_m=v['slab_bottom'],source='T11/'+w['id'],height_source='T14/slab_bottom') for w in p['walls']],
          openings=[dict(id=o['id'],name=o['name'],kind=o['kind'],axis=o['axis'],span_xy_m=project(o['span_xy_m']),polygon_xy_m=opening_polygon(o),width_m=o['traced_span_m']*factor,source='T11/'+o['id']) for o in p['openings']],
          doors=[dict(id=d['id'],opening=d['opening'],hinge_xy_m=project([d['hinge_xy_m']])[0],closed_tip_xy_m=project([d['closed_tip_xy_m']])[0],swing_deg=d['blender_swing_degrees'],source='T11/'+d['id']) for d in p['doors']])
adjustments_path='architecture/model/door-adjustments.json'
adjustments=read(adjustments_path)
data['sources'][adjustments_path]=sha(adjustments_path)
for door in data['doors']:
    if door['id'] in adjustments['doors']:
        door.update(adjustments['doors'][door['id']])
        door['adjustment_source']=adjustments_path
data['revision']=hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()
dest=ROOT/'architecture/model';dest.mkdir(exist_ok=True)
(dest/'departamento-t7.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
ids=[o['id'] for key in ['rooms','walls','openings','doors'] for o in data[key]]
assert len(ids)==len(set(ids))
assert len(data['walls'])==40 and len(data['openings'])==13 and len(data['doors'])==6
print(json.dumps(dict(revision=data['revision'],walls=40,openings=13,doors=6,rooms=len(data['rooms']),metres=True)))
