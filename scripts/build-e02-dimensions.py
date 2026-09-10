"""Analytical floor accounting on the T11 arrangement; no rescaling or raster sum."""
from pathlib import Path
from collections import defaultdict
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'architecture/dimensions'
OUT.mkdir(exist_ok=True)
read = lambda f: json.loads((ROOT / f).read_text(encoding='utf-8'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
write = lambda p, d: p.write_text(json.dumps(d, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
plan = read('architecture/plan/t11-registro.json')
c = read('architecture/plan/t11-trazado.json')['coordinates']
cal = read('architecture/calibration/t10-calibracion.json')
s = cal['scale']['m_per_px']
u0, v0 = cal['origin']['pixel_uv']
xy = lambda p: [(p[0]-u0)*s, (v0-p[1])*s]
walls = [w['rect_px'] for w in plan['walls']]
openings = {o['id']:o['rect_px'] for o in plan['openings'] if o['rect_px']}
blocks = walls + list(openings.values())
outer = [[c['LX'],c['TOP']],[c['RX'],c['TOP']],[c['RX'],c['SOUTH_X']],
         [c['BATH_L'],c['SOUTH_X']],[c['BATH_L'],c['D1_BX']],[c['LX'],c['D1_BX']]]
terrace = [[c['LX'],c['D1_BX']],[c['BATH_L'],c['D1_BX']],
           [c['BATH_L'],c['SOUTH_X']],[c['LX'],c['SOUTH_X']]]
def area(poly):
    return abs(sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(poly,poly[1:]+poly[:1])))/2
def inside_rect(x,y,r): return r[0]<x<r[2] and r[1]<y<r[3]
def inside_outer(x,y):
    return c['LX']<x<c['RX'] and c['TOP']<y<c['SOUTH_X'] and (y<c['D1_BX'] or x>c['BATH_L'])
xs=sorted({x for r in blocks for x in (r[0],r[2])}|{1199.6})
ys=sorted({y for r in blocks for y in (r[1],r[3])}|{480})
free=set()
for i,(l,r) in enumerate(zip(xs,xs[1:])):
    for j,(t,b) in enumerate(zip(ys,ys[1:])):
        x,y=(l+r)/2,(t+b)/2
        if inside_outer(x,y) and not any(inside_rect(x,y,z) for z in blocks): free.add((i,j))
components=[]
while free:
    seed=min(free); free.remove(seed); stack=[seed]; comp=[]
    while stack:
        q=stack.pop();comp.append(q)
        for n in [(q[0]+1,q[1]),(q[0]-1,q[1]),(q[0],q[1]+1),(q[0],q[1]-1)]:
            if n in free: free.remove(n);stack.append(n)
    components.append(comp)
assert len(components)==7
room_names=['Dormitorio 3','Dormitorio 1','Espacio común','Dormitorio 2','Baño','Franja técnica','Logia']
room_ids=['D3','D1','COMMON','D2','BATH','SHAFT','LOGIA']
groups=defaultdict(list)
for name,comp in zip(room_ids,components):
    for i,j in comp:
        x,y=(xs[i]+xs[i+1])/2,(ys[j]+ys[j+1])/2
        label=name
        if name=='COMMON':
            label=('LIVING' if y<480 else 'DINING') if x>=1199.6 else ('CIRCULATION' if y<148.4 or x<824.3 else 'KITCHEN')
        groups[label].append((i,j))
def boundary(cells):
    edges=set()
    for i,j in cells:
        ps=[(xs[i],ys[j]),(xs[i+1],ys[j]),(xs[i+1],ys[j+1]),(xs[i],ys[j+1])]
        for p,q in zip(ps,ps[1:]+ps[:1]):
            if (q,p) in edges:edges.remove((q,p))
            else:edges.add((p,q))
    rings=[]
    while edges:
        p,q=min(edges);start=p;ring=[p];edges.remove((p,q))
        while q!=start:
            ring.append(q);n=[b for a,b in edges if a==q]
            assert len(n)==1,(q,n)
            edges.remove((q,n[0]));q=n[0]
        # Remove collinear grid vertices while preserving corners.
        ring=[p for k,p in enumerate(ring) if (ring[k-1][0]-p[0])*(ring[(k+1)%len(ring)][1]-p[1]) != (ring[k-1][1]-p[1])*(ring[(k+1)%len(ring)][0]-p[0])]
        rings.append(ring)
    return rings
regions=[]
for id,cells in groups.items():
    rects=[[xs[i],ys[j],xs[i+1],ys[j+1]] for i,j in cells]
    a=sum((r[2]-r[0])*(r[3]-r[1]) for r in rects)*s*s
    rings=boundary(cells)
    assert abs(sum(area(r) for r in rings)*s*s-a)<1e-8
    regions.append(dict(id=id,area_m2=a,rings_px=rings,rings_xy_m=[[xy(p) for p in r] for r in rings],
                        criterion='Caras interiores, sin umbrales; equipo y armarios no descontados. Límites comunes de uso sin tabiques.'))
gross=area(outer)*s*s
wall_area=sum((r[2]-r[0])*(r[3]-r[1])*s*s for r in walls)
opening_areas={k:(r[2]-r[0])*(r[3]-r[1])*s*s for k,r in openings.items()}
interior=sum(r['area_m2'] for r in regions if r['id']!='SHAFT')
shaft=next(r['area_m2'] for r in regions if r['id']=='SHAFT')
closure=wall_area+sum(opening_areas.values())+interior+shaft
assert abs(closure-gross)<1e-8,(closure,gross)
assert abs(gross-((c['RX']-c['LX'])*(c['D1_BX']-c['TOP'])+(c['RX']-c['BATH_L'])*(c['SOUTH_X']-c['D1_BX']))*s*s)<1e-8
thresholds=sum(v for k,v in opening_areas.items() if int(k[1:])<=6)
interval=[area(outer)*k*k for k in cal['scale']['sensitivity_interval_m_per_px']]
report=dict(task='T13',status='Cómputo reproducible terminado; equivalencia documental V03 pendiente',units='m²',
    source_sha256={f:sha(ROOT/f) for f in ['architecture/plan/t11-registro.json','architecture/calibration/t10-calibracion.json']},
    documentary=dict(header_edificado_m2=76.66,native_plan_label_m2=76.80,header_terrace_m2=0,user_interior_target_m2=76.66,
                     computation_boundary_documented=False,decision='Conservar escala T10; no equiparar edificada con útil. Consulta dimensional pendiente.'),
    outer=dict(polygon_px=outer,polygon_xy_m=[xy(p) for p in outer],area_m2=gross,top_face_provisional=True,delta_to_76_66_m2=gross-76.66,
               scale_sensitivity_m2=interval,criterion='Caras exteriores trazadas; no acredita perímetro de cómputo oficial ni ejes medianeros.'),
    useful=dict(room_sum_excluding_thresholds_m2=interior,door_thresholds_m2=thresholds,including_door_thresholds_m2=interior+thresholds,
                excludes=['muros','ventanas/celosía','franja técnica','terraza'],not_a_certified_regulatory_area=True),
    accounting=dict(walls_m2=wall_area,openings_m2=opening_areas,technical_void_m2=shaft,partition_residual_m2=closure-gross),regions=regions,
    terrace=dict(polygon_px=terrace,polygon_xy_m=[xy(p) for p in terrace],provisional_visual_area_m2=area(terrace)*s*s,
                 documented_boundary=False,criterion='Rectángulo de presentación en entrante, limitado provisionalmente por frente sur. No terraza documentada ni acceso nuevo.'),
    checks=dict(analytical_partition=True,independent_outer_formula=True,source_scale_unchanged=True,official_area_validated=False))
write(OUT/'t13-superficies.json',report)
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/arial.ttf',n)
image=Image.new('RGB',(1700,1110),'white');d=ImageDraw.Draw(image)
d.text((40,20),'T13 · Superficies separadas, sin deformar el plano',font=font(30),fill='#172b3a')
native=Image.open(ROOT/'references/derived/p20-t7/planta-nativa.png').convert('RGBA')
overlay=Image.new('RGBA',native.size);od=ImageDraw.Draw(overlay)
colors=['#2e83a4','#df974b','#658bd5','#dfab49','#77b5ac','#b882a9','#b7a47b','#4ca4b7','#738a9c','#a477be']
for region,color in zip(regions,colors):
    for ring in region['rings_px']: od.polygon([tuple(p) for p in ring],fill=color+'45',outline=color+'ff',width=2)
native=Image.alpha_composite(native,overlay);image.paste(native.convert('RGB'),(40,75))
d=ImageDraw.Draw(image)
d.text((40,920),f'Exterior trazado: {gross:.4f} m²  |  Interior entre caras sin umbrales: {interior:.4f} m²',font=font(25),fill='#172b3a')
d.text((40,960),f'Umbrales de puertas: {thresholds:.4f} m²  |  Franja técnica: {shaft:.4f} m²  |  Terraza provisional: {area(terrace)*s*s:.4f} m²',font=font(22),fill='#172b3a')
d.text((40,1000),'Documento: 76,66 m² EDIFICADO / rótulo 76,80 m². No son una comprobación de superficie útil.',font=font(23),fill='#8b392f')
d.text((40,1045),'Los colores de uso común no representan paredes. Borde superior y terraza conservan incertidumbre.',font=font(21),fill='#44515b')
dest=ROOT/'validation/e02';dest.mkdir(parents=True,exist_ok=True);image.save(dest/'superficies.png')
print(json.dumps({k:report[k] for k in ['outer','useful','accounting','checks']},ensure_ascii=False,indent=2))
