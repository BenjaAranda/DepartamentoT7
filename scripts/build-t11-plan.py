"""Generate the T11 metric register and evidence from authored native-pixel faces.

No Blender, runtime geometry, source editing, area fitting or guessed heights.
Run from any directory with the project's Python runtime (NumPy and Pillow).
"""
from pathlib import Path
from collections import defaultdict
import csv
import hashlib
import json
import math
import platform

import numpy as np
from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version

ROOT = Path(__file__).resolve().parents[1]
AUTHOR = ROOT / 'architecture/plan/t11-trazado.json'
OUT = ROOT / 'references/derived/t11-trazado'
OUT.mkdir(parents=True, exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text(encoding='utf-8'))
write = lambda p, v: p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
a = read(AUTHOR)
cal_path = ROOT / a['calibration']
cal = read(cal_path)
source = ROOT / a['source']
assert sha(source) == cal['source_image_sha256']
assert sha(cal_path) == 'c8a373f353b03cf51775398e48668c1cf3b9d215bf0c48c592bec8ba570a26ad'
pdf = ROOT.parent / 'Presentación Aprobación Proyecto Técnico 2.pdf'
assert sha(pdf) == cal['source_pdf_sha256']
reference_manifest = read(source.parent/'manifest.json')
reference_hashes = {}
for ref in reference_manifest['artifacts']+[reference_manifest['text_extraction']]:
    observed_hash = sha(source.parent/ref['file'])
    assert observed_hash == ref['sha256'], ref['file']
    reference_hashes[ref['file']] = observed_hash
native = Image.open(source).convert('RGB')
gray = np.array(native.convert('L'), dtype=float)
s = cal['scale']['m_per_px']
u0, v0 = cal['origin']['pixel_uv']
resolve = lambda x: a['coordinates'][x] if isinstance(x, str) else x
point = lambda p: [resolve(x) for x in p]
metric = lambda p: [(p[0]-u0)*s, (v0-p[1])*s]
rect = lambda r: [resolve(x) for x in r]
polygon = lambda r: [[r[0],r[1]], [r[2],r[1]], [r[2],r[3]], [r[0],r[3]]]
distance = lambda p,q: math.hypot(p[0]-q[0], p[1]-q[1])

walls = []
for w in a['walls']:
    r = rect(w['rect'])
    x0,y0,x1,y1 = r
    assert x1 > x0 and y1 > y0
    axis = [[x0,(y0+y1)/2],[x1,(y0+y1)/2]] if w['axis']=='h' else [[(x0+x1)/2,y0],[(x0+x1)/2,y1]]
    walls.append({**w, 'rect_px':r, 'polygon_px':polygon(r), 'polygon_xy_m':[metric(p) for p in polygon(r)],
                  'axis_px':axis, 'axis_xy_m':[metric(p) for p in axis],
                  'axis_length_m':distance(*axis)*s,
                  'traced_thickness_m':(y1-y0 if w['axis']=='h' else x1-x0)*s,
                  'nominal_thickness_m':w.get('nominal_m'), 'height_m':None,
                  'width_status':'inferida de caras del raster; nominal separado si existe',
                  'read_uncertainty_px':a['policy']['face_reading_px']})
wall_by_id = {w['id']:w for w in walls}
assert len(wall_by_id)==len(walls)

def overlap(r,t):
    return max(0,min(r[2],t[2])-max(r[0],t[0]))*max(0,min(r[3],t[3])-max(r[1],t[1]))

intersections = [(w['id'],q['id']) for i,w in enumerate(walls) for q in walls[i+1:] if overlap(w['rect_px'],q['rect_px']) > 1e-8]
assert not intersections, intersections

def contact_length(r,t):
    if abs(r[2]-t[0]) < 1e-8 or abs(r[0]-t[2]) < 1e-8:
        return max(0,min(r[3],t[3])-max(r[1],t[1]))
    if abs(r[3]-t[1]) < 1e-8 or abs(r[1]-t[3]) < 1e-8:
        return max(0,min(r[2],t[2])-max(r[0],t[0]))
    return 0

contacts = [{'walls':[w['id'],q['id']], 'shared_edge_length_m':contact_length(w['rect_px'],q['rect_px'])*s}
            for i,w in enumerate(walls) for q in walls[i+1:] if contact_length(w['rect_px'],q['rect_px']) > 0]
for jog in a['jogs']:
    reached = {jog['walls'][0]}
    while True:
        grown = reached | {i for c in contacts if set(c['walls']) & reached for i in c['walls'] if i in jog['walls']}
        if grown == reached: break
        reached = grown
    assert reached == set(jog['walls']), jog

openings = []
for o in a['openings']:
    if 'rect' in o:
        r = rect(o['rect'])
        x0,y0,x1,y1 = r
        p,q = ([[x0,(y0+y1)/2],[x1,(y0+y1)/2]] if o['axis']=='h' else [[(x0+x1)/2,y0],[(x0+x1)/2,y1]])
        assert not any(overlap(r,w['rect_px']) > 1e-8 for w in walls), o['id']
        assert all(contact_length(r,wall_by_id[i]['rect_px'])>0 for i in o['supports']), o['id']
    else:
        r = None
        p,q = [point(v) for v in o['line']]
        for t in np.linspace(.01,.99,99):
            x,y = np.array(p)*(1-t)+np.array(q)*t
            assert not any(w['rect_px'][0]<x<w['rect_px'][2] and w['rect_px'][1]<y<w['rect_px'][3] for w in walls)
    openings.append({**o,'rect_px':r,'span_px':[p,q], 'span_xy_m':[metric(p),metric(q)],
                     'traced_span_m':distance(p,q)*s,'finished_clear_width_m':None,
                     'sill_m':None,'lintel_m':None,'source_width_dimension':None})
opening_by_id = {o['id']:o for o in openings}

def leaf_record(d):
    hinge = d['hinge_px']
    r = d['leaf_span_px']
    closed = [hinge[i]+r*d['closed_uv'][i] for i in (0,1)]
    opened = [hinge[i]+r*d['open_uv'][i] for i in (0,1)]
    cv = [d['closed_uv'][0],-d['closed_uv'][1]]
    ov = [d['open_uv'][0],-d['open_uv'][1]]
    angle = math.degrees(math.atan2(cv[0]*ov[1]-cv[1]*ov[0],cv[0]*ov[0]+cv[1]*ov[1]))
    assert abs(angle)==90
    return {**d,'hinge_xy_m':metric(hinge),'leaf_span_m':r*s,'closed_tip_px':closed,'open_tip_px':opened,
            'closed_tip_xy_m':metric(closed),'open_tip_xy_m':metric(opened),
            'blender_swing_degrees':angle,'swing_axis':'Blender +Z, visto desde arriba',
            'leaf_thickness_m':None,'hinge_height_m':None,'graphic_uncertainty_px':2}

doors = [leaf_record(d) for d in a['doors']]
furniture = [leaf_record(d) for d in a['furniture_leaves']]
for d in doors:
    o = opening_by_id[d['opening']]
    assert o['kind']=='puerta'
    assert distance(d['open_tip_px'],d['graphic_leaf_open_tip_px']) < 1e-8
    # Hinges are placed on the frame offset, not automatically on the wall axis.
    r = o['rect_px']; p = d['hinge_px']
    jamb = r[1] if d['hinge_side']=='superior' else (r[2] if d['hinge_side']=='derecha' else r[0])
    assert abs(p[1 if o['axis']=='v' else 0]-jamb) <= 6
    assert d['leaf_span_m'] <= o['traced_span_m']+2*s
assert {d['opening'] for d in doors} == {o['id'] for o in openings if o['kind']=='puerta'}

# Union boundary from exact shared coordinates, without filling doors/windows.
# Every cell is analytical, not a pixel mask. Interior seams cancel.
xs = sorted({r for w in walls for r in (w['rect_px'][0],w['rect_px'][2])})
ys = sorted({r for w in walls for r in (w['rect_px'][1],w['rect_px'][3])})
edges = set()
for x0,x1 in zip(xs,xs[1:]):
    for y0,y1 in zip(ys,ys[1:]):
        x,y = (x0+x1)/2,(y0+y1)/2
        if not any(w['rect_px'][0]<x<w['rect_px'][2] and w['rect_px'][1]<y<w['rect_px'][3] for w in walls): continue
        ps = [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
        for p,q in zip(ps,ps[1:]+ps[:1]):
            if (q,p) in edges: edges.remove((q,p))
            else: edges.add((p,q))
outgoing = defaultdict(list)
for p,q in edges: outgoing[p].append(q)
assert all(len(v)==1 for v in outgoing.values()), 'Point-only contact in wall union'
rings = []
while edges:
    start = min(edges)[0]; p = start; ring = []
    while True:
        ring.append(p); q = outgoing[p][0]; edges.remove((p,q)); p = q
        if p == start: break
    simple = []
    for i,p in enumerate(ring):
        before,after = ring[i-1],ring[(i+1)%len(ring)]
        cross = (p[0]-before[0])*(after[1]-p[1])-(p[1]-before[1])*(after[0]-p[0])
        if cross != 0: simple.append(p)
    rings.append(simple)
corners = []
boundary = []
for ri,ring in enumerate(rings,1):
    ids = []
    for i,p in enumerate(ring):
        before,after = ring[i-1],ring[(i+1)%len(ring)]
        turn = (p[0]-before[0])*(after[1]-p[1])-(p[1]-before[1])*(after[0]-p[0])
        owners = [w['id'] for w in walls if w['rect_px'][0]<=p[0]<=w['rect_px'][2] and w['rect_px'][1]<=p[1]<=w['rect_px'][3]]
        cid = f'C{len(corners)+1:03d}';ids.append(cid)
        corners.append({'id':cid,'ring':ri,'pixel_uv':p,'blender_xy_m':metric(p),'walls':owners,
                        'turn_relative_to_material':'convexo' if turn>0 else 'entrante'})
    boundary.append({'id':f'B{ri:02d}','corner_ids':ids,'closed':True,
                     'points_px':ring,'points_xy_m':[metric(p) for p in ring]})

# Independent pixel evidence for a selected set of faces, not construction tolerances.
face_checks = []
for f in a['face_checks']:
    x0,y0,x1,y1 = f['roi']
    prof = gray[y0:y1,x0:x1].mean(axis=0 if f['axis']=='u' else 1)
    pos = np.arange(len(prof))+(x0 if f['axis']=='u' else y0)
    peak = int(np.argmin(prof))
    weights = np.maximum(0,220-prof)*(abs(np.arange(len(prof))-peak)<=1)
    observed = float(np.sum(pos*weights)/np.sum(weights))
    residual = resolve(f['key'])-observed
    face_checks.append({**f,'observed_coordinate_px':observed,'traced_coordinate_px':resolve(f['key']),
                        'residual_px':residual,'residual_m':residual*s})
assert max(abs(f['residual_px']) for f in face_checks) <= 1

with (ROOT/'architecture/classification/t08-trazos.tsv').open(encoding='utf-8',newline='') as h:
    classification = list(csv.DictReader(h,delimiter='\t'))
known_ids = {c['id'] for c in classification}
wall_sources = {i for w in walls for i in w['t08']}
assert wall_sources == {c['id'] for c in classification if c['familia']=='muros'}
assert {o['t08'] for o in openings} == {c['id'] for c in classification if c['familia']=='vanos'}
assert {d['t08'] for d in doors+furniture} == {c['id'] for c in classification if c['familia']=='hojas'}
assert not (set(a['excluded_as_walls']) & wall_sources)
assert set(a['excluded_as_walls']) <= known_ids

register = {'task':'T11','revision':a['revision'],'status':a['policy']['status'],
            'source_image_sha256':sha(source),'source_pdf_sha256':sha(pdf),'author_sha256':sha(AUTHOR),
            'calibration_sha256':sha(cal_path),'calibration_path':a['calibration'],
            'units':'metros; coordenadas pixel conservadas como observaciones',
            'policy':a['policy'],'walls':walls,'openings':openings,'doors':doors,
            'furniture_leaves':furniture,'contacts':contacts,'corners':corners,'boundary_rings':boundary,
            'jogs':a['jogs'],'resolutions':a['resolutions'],'face_checks':face_checks}
reg_path = ROOT / 'architecture/plan/t11-registro.json'
write(reg_path,register)

def tsv(path,fields,rows):
    with path.open('w',encoding='utf-8',newline='') as h:
        wr = csv.DictWriter(h,fields,delimiter='\t',lineterminator='\n');wr.writeheader();wr.writerows(rows)
tsv(OUT/'muros.tsv',['id','nombre','eje_m','espesor_trazado_m','espesor_nominal_m','t08','t09'],
    [{'id':w['id'],'nombre':w['name'],'eje_m':f"{w['axis_length_m']:.6f}",
      'espesor_trazado_m':f"{w['traced_thickness_m']:.6f}",'espesor_nominal_m':w['nominal_thickness_m'],
      't08':','.join(w['t08']),'t09':','.join(w['t09']) or '—'} for w in walls])
tsv(OUT/'vanos.tsv',['id','nombre','tipo','ancho_trazado_m','soportes','apertura'],
    [{'id':o['id'],'nombre':o['name'],'tipo':o['kind'],'ancho_trazado_m':f"{o['traced_span_m']:.6f}",
      'soportes':','.join(o['supports']),'apertura':o.get('operation','Ver puerta P'+o['id'][1:])} for o in openings])
tsv(OUT/'puertas.tsv',['id','vano','hoja_grafica_m','bisagra_X_m','bisagra_Y_m','soporte','lado','giro_Blender_grados','abre_hacia'],
    [{'id':d['id'],'vano':d['opening'],'hoja_grafica_m':f"{d['leaf_span_m']:.6f}",
      'bisagra_X_m':f"{d['hinge_xy_m'][0]:.6f}",'bisagra_Y_m':f"{d['hinge_xy_m'][1]:.6f}",
      'soporte':d['hinge_support'],'lado':d['hinge_side'],'giro_Blender_grados':d['blender_swing_degrees'],
      'abre_hacia':d['opens_to']} for d in doors])
tsv(OUT/'esquinas.tsv',['id','anillo','u_px','v_px','X_m','Y_m','tipo','panos'],
    [{'id':c['id'],'anillo':c['ring'],'u_px':c['pixel_uv'][0],'v_px':c['pixel_uv'][1],
      'X_m':c['blender_xy_m'][0],'Y_m':c['blender_xy_m'][1],'tipo':c['turn_relative_to_material'],
      'panos':','.join(c['walls'])} for c in corners])
tsv(OUT/'control-caras.tsv',['coordenada','trazado_px','leido_px','residuo_px','residuo_m','roi'],
    [{'coordenada':f['key'],'trazado_px':f['traced_coordinate_px'],'leido_px':f['observed_coordinate_px'],
      'residuo_px':f['residual_px'],'residuo_m':f['residual_m'],'roi':json.dumps(f['roi'])} for f in face_checks])

lines = ['# Registro T11: muros y aperturas','',
         'Generado desde `t11-trazado.json` mediante `scripts/build-t11-plan.py`. Todas las longitudes de las tablas son lecturas métricas de trabajo, no cotas nominales ni precisión de fabricación. El JSON conserva píxeles, metros, caras, ejes, fuentes, contactos y límites.',
         '', '## Paños', '', '| ID | Paño | Longitud de eje (m) | Espesor leído (m) | Nominal documentado (m) |',
         '|---|---|---:|---:|---:|']
for w in walls:
    nominal = '—' if w['nominal_thickness_m'] is None else f"{w['nominal_thickness_m']:.3f}"
    lines.append(f"| {w['id']} | {w['name']} | {w['axis_length_m']:.3f} | {w['traced_thickness_m']:.3f} | {nominal} |")
lines += ['', 'Las longitudes de eje terminan en la sección del paño, sin prolongarse hasta ejes de otro muro. Los encuentros se describen con sus caras compartidas, no sumando estas longitudes como cotas de recinto.',
          '', '## Vanos y paso abierto', '', '| ID | Ubicación | Tramo entre soportes (m) | Tipo |', '|---|---|---:|---|']
for o in openings:lines.append(f"| {o['id']} | {o['name']} | {o['traced_span_m']:.3f} | {o['kind']} |")
lines += ['', 'O13 es una línea de paso libre de referencia, sin muro ni marco. O11 tiene jambas parcialmente ocultas por equipos y celosía probable por la isométrica. Antepechos, dinteles y funcionamiento de ventanas siguen pendientes.',
          '', '## Puertas de recinto', '', '| Puerta / vano | Hoja gráfica (m) | Bisagra en el plano | Soporte | Giro Blender +Z | Abre hacia |', '|---|---:|---|---|---:|---|']
for d in doors:lines.append(f"| {d['id']} / {d['opening']} | {d['leaf_span_m']:.3f} | {d['hinge_side']} | {d['hinge_support']} | {d['blender_swing_degrees']:+.0f}° | {d['opens_to']} |")
lines += ['', 'La posición cerrada se deriva del pivote, el radio gráfico y el sentido observado. No define todavía holguras de herrajes. En P06 la hoja gráfica supera el tramo entre soportes en 1 px (8,46 mm); ambos se conservan como observaciones del símbolo, dentro de la sensibilidad de lectura de 2 px, y requieren ajuste de carpintería en T22 antes de generar una hoja física. No se autoriza una hoja que penetre su marco.',
          '', '## Hojas de mobiliario', '', '| ID | Propietario | Hoja gráfica (m) | Situación |', '|---|---|---:|---|']
for d in furniture:lines.append(f"| {d['id']} | {d['owner']} | {d['leaf_span_m']:.3f} | {d['status']} |")
lines += ['', 'Las cinco hojas visibles se registran para explicar los nueve grupos de símbolos T08 junto con las seis puertas de recinto. No son once accesos de habitaciones. Los tres armarios finales tendrán dos hojas según el usuario; D3 requiere adaptar el diseño en T37.',
          '', '## Esquinas y retranqueos', '',
          f"La unión de los paños produce {len(corners)} vértices de borde en {len(boundary)} anillos cerrados. Incluye esquinas entrantes, convexas y remates de jambas; no equivale al número de esquinas de recintos. Las uniones internas entre paños se eliminan del borde. Los IDs, las coordenadas y los paños relacionados están en [esquinas.tsv](../../references/derived/t11-trazado/esquinas.tsv) y el registro JSON.", '',
          '| Grupo | Encuentro | Paños conectados |', '|---|---|---|']
for j in a['jogs']:lines.append(f"| {j['id']} | {j['name']} | {', '.join(j['walls'])} |")
lines += ['', '## Resoluciones y continuidad', '']
for r in a['resolutions']:lines.append(f"- **{r['source']}**: {r['result']} Estado: {r['status']}. Sigue en {r['next']}.")
(ROOT/'architecture/plan/REGISTRO_T11.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')

FONT = Path('C:/Windows/Fonts/arial.ttf')
BOLD = Path('C:/Windows/Fonts/arialbd.ttf')
font = lambda n,b=False: ImageFont.truetype(str(BOLD if b else FONT),n)
INK = '#19324a';BLUE = '#006baa';ORANGE = '#d25611';TEAL = '#008e87'

def label(draw,xy,text,size=16,color=INK):
    box = draw.textbbox(xy,text,font=font(size,True));draw.rectangle((box[0]-3,box[1]-2,box[2]+3,box[3]+2),fill='white')
    draw.text(xy,text,font=font(size,True),fill=color)

def draw_leaf(draw,d,transform,color=ORANGE,width=2):
    h,c,o = [transform(d[k]) for k in ('hinge_px','closed_tip_px','open_tip_px')]
    draw.line((h,o),fill=color,width=width)
    for t0 in np.arange(0,1,.12):
        t1 = min(t0+.065,1);draw.line((tuple(np.array(h)*(1-t0)+np.array(c)*t0),tuple(np.array(h)*(1-t1)+np.array(c)*t1)),fill=TEAL,width=width)
    ca = math.atan2(d['closed_uv'][1],d['closed_uv'][0]);delta = -math.radians(d['blender_swing_degrees'])
    pts = [transform([d['hinge_px'][0]+d['leaf_span_px']*math.cos(ca+t*delta),d['hinge_px'][1]+d['leaf_span_px']*math.sin(ca+t*delta)]) for t in np.linspace(0,1,45)]
    draw.line(pts,fill=color,width=max(1,width-1));draw.ellipse((h[0]-4,h[1]-4,h[0]+4,h[1]+4),fill=color)

def header(im,title,subtitle):
    d = ImageDraw.Draw(im);d.text((32,22),title,font=font(30,True),fill=INK)
    d.text((32,64),subtitle,font=font(18),fill=INK)

sheet = Image.new('RGB',(2000,1120),'white')
header(sheet,'T11 · Muros, vanos y giros','Levantamiento 2D sobre planta nativa · una escala T10 · alturas y superficie pendientes')
offset = (32,124);sheet.paste(native,offset)
overlay = Image.new('RGBA',sheet.size);dr = ImageDraw.Draw(overlay)
tr = lambda p:(p[0]+offset[0],p[1]+offset[1])
for w in walls:
    dr.polygon([tr(p) for p in w['polygon_px']],fill=(0,107,170,80),outline=(0,107,170,230),width=1)
for o in openings:
    dr.line([tr(p) for p in o['span_px']],fill=(0,142,135,255),width=4)
for d in doors:draw_leaf(dr,d,tr,ORANGE,2)
sheet = Image.alpha_composite(sheet.convert('RGBA'),overlay).convert('RGB');dr = ImageDraw.Draw(sheet)
positions = {'O01':(1460,72),'O02':(367,54),'O03':(400,178),'O04':(739,125),'O05':(862,125),'O06':(1116,575),
             'O07':(30,177),'O08':(359,653),'O09':(635,653),'O10':(882,805),'O11':(1090,805),'O12':(1332,805),'O13':(1210,90)}
for o in openings:label(dr,tr(positions[o['id']]),o['id'],17,TEAL)
for xy,name in [((130,345),'D1'),((610,352),'D2'),((136,65),'D3'),((857,541),'BAÑO'),((1097,370),'COCINA'),((1280,159),'ESTAR'),((1300,587),'COMEDOR'),((1105,741),'LOGIA')]:
    label(dr,tr(xy),name,20)
label(dr,(260,871),'TERRAZA · sin contorno exterior acreditado',18)
sx = 1600;dr.text((sx,126),'Registro de vanos',font=font(23,True),fill=INK)
for i,o in enumerate(openings):
    y = 171+i*48
    dr.text((sx,y),f"{o['id']}  {o['name']}",font=font(17,True),fill=INK)
    dr.text((sx,y+22),f"Tramo: {o['traced_span_m']:.3f} m".replace('.',','),font=font(16),fill=TEAL)
for i,t in enumerate(['Azul: caras de 40 paños','Verde: vano / paso abierto','Naranja: hoja, pivote y giro','Verde discontinuo: hoja cerrada','Dimensiones leídas del raster.','No son anchos libres terminados.']):
    dr.text((sx,830+i*27),t,font=font(17),fill=INK)
dr.text((32,990),'Caras registradas por tramos reales; se conservan los cambios de espesor y los retranqueos.',font=font(21),fill=INK)
dr.text((32,1027),'No se crean tabiques sobre mobiliario, tramas, ducha o arcos. Las ventanas conservan su vano, con antepechos por definir.',font=font(18),fill=INK)
dr.text((32,1060),'El borde exterior superior está recortado. 76,66 / 76,80 m² se resolverá en T13 sin deformar esta planta.',font=font(18),fill=INK)
sheet.save(OUT/'planta-muros-vanos.png')

sheet = Image.new('RGB',(1740,1190),'white')
header(sheet,'T11 · Las seis puertas de recinto','Pivote naranja · hoja abierta naranja · cerrada discontinua verde · giros vistos desde arriba')
crops = [(1380,0,1536,158),(228,0,378,150),(352,178,502,328),(693,129,842,279),(802,26,951,176),(1075,578,1225,728)]
for i,(d,b) in enumerate(zip(doors,crops)):
    col,row = i%3,i//3;x,y = 30+col*575,113+row*520
    dr = ImageDraw.Draw(sheet);dr.rounded_rectangle((x,y,x+550,y+497),12,outline='#d4dfe7',width=2)
    o = opening_by_id[d['opening']]
    dr.text((x+15,y+12),f"{d['id']} · {o['name']}",font=font(22,True),fill=INK)
    k = min(510/(b[2]-b[0]),340/(b[3]-b[1]));size=(round((b[2]-b[0])*k),round((b[3]-b[1])*k))
    left,top = x+(550-size[0])//2,y+48
    sheet.paste(native.crop(b).resize(size), (left,top))
    tr2 = lambda p:(left+(p[0]-b[0])*k,top+(p[1]-b[1])*k)
    dr = ImageDraw.Draw(sheet);draw_leaf(dr,d,tr2,ORANGE,3)
    dr.text((x+15,y+394),f"Hueco {o['traced_span_m']:.3f} m · hoja gráfica {d['leaf_span_m']:.3f} m".replace('.',','),font=font(19,True),fill=INK)
    dr.text((x+15,y+426),f"Bisagra {d['hinge_side']} · giro {d['blender_swing_degrees']:+.0f}° en Blender",font=font(18),fill=INK)
    dr.text((x+15,y+456),f"Abre: {d['opens_to']}",font=font(16),fill=INK)
dr.text((32,1160),'Anchos inferidos, sin cotas nominales de puerta. El marco y su paso útil se definirán en T22; no se ha probado el barrido físico.',font=font(17),fill=INK)
sheet.save(OUT/'puertas-y-bisagras.png')

sheet = Image.new('RGB',(1680,1190),'white')
header(sheet,'T11 · Remates y lectura de carpinterías','Detalle de referencia · trazos de arquitectura en azul · símbolos de mueble y equipos preservados')
details = [
    ('Nicho D3: dos paños y saliente de jamba',(215,111,385,285),['W12B','W12C','W13A','W13B'],['La hoja pequeña abre hacia D3 desde el oeste.','Es mueble; el armario final tendrá dos hojas en T37.']),
    ('Cocina–estar: cambio de espesor y retorno',(1176,382,1228,631),['W18A','W18B','W18C','W18D'],['El paño grueso continúa en un tabique delgado.','La jamba de logia tiene un retorno propio.']),
    ('Baño–logia: retranqueo y volumen técnico',(982,514,1107,800),['W16A','W16B','W19A','W19B','W19C','W20A','W20B','W08B'],['Se registran bordes; la X interior no es pared.','La función y las alturas se revisarán en T12/T14.']),
    ('Frente de logia: celosía probable',(1028,758,1225,805),['W08B','W09A','W18D','W20B'],['Planta parcialmente tapada por equipamiento.','La isométrica muestra lamas; apertura sin confirmar.'])]
for i,(title,b,ids,notes) in enumerate(details):
    x,y = 30+(i%2)*830,112+(i//2)*520
    dr=ImageDraw.Draw(sheet);dr.rounded_rectangle((x,y,x+800,y+493),12,outline='#d4dfe7',width=2)
    dr.text((x+15,y+12),title,font=font(21,True),fill=INK)
    if i==3:
        k=3.7;size=(round((b[2]-b[0])*k),round((b[3]-b[1])*k));left,top=x+25,y+55
    else:
        k=min(750/(b[2]-b[0]),340/(b[3]-b[1]));size=(round((b[2]-b[0])*k),round((b[3]-b[1])*k));left,top=x+(800-size[0])//2,y+49
    crop=native.crop(b).resize(size).convert('RGBA');layer=Image.new('RGBA',crop.size);ld=ImageDraw.Draw(layer)
    for wid in ids:
        pp=[((p[0]-b[0])*k,(p[1]-b[1])*k) for p in wall_by_id[wid]['polygon_px']]
        ld.polygon(pp,fill=(0,107,170,55),outline=(0,107,170,255),width=2)
    crop=Image.alpha_composite(crop,layer).convert('RGB');sheet.paste(crop,(left,top))
    if i==3:
        iso=Image.open(ROOT/'references/derived/p20-t7/isometrica-nativa.jpg')
        ic=iso.crop((135,336,256,490)).resize((151,192));sheet.paste(ic,(x+65,y+225))
        dr=ImageDraw.Draw(sheet);dr.text((x+244,y+270),'Isométrica original de p20',font=font(19,True),fill=INK)
        dr.text((x+244,y+302),'Sin introducir una puerta exterior supuesta.',font=font(18),fill=INK)
    dr=ImageDraw.Draw(sheet)
    for j,t in enumerate(notes):dr.text((x+15,y+427+j*29),t,font=font(18),fill=INK)
ImageDraw.Draw(sheet).text((32,1160),'Los detalles documentan T11. No acreditan alturas, superficies, mobiliario final ni un recorrido con colisiones.',font=font(18),fill=INK)
sheet.save(OUT/'remates-y-logia.png')

report = {'task':'T11','runtime':{'python':platform.python_version(),'numpy':np.__version__,'pillow':pillow_version},
          'source_image_sha256':sha(source),'source_pdf_sha256':sha(pdf),'calibration_sha256':sha(cal_path),
          'author_sha256':sha(AUTHOR),'register_sha256':sha(reg_path),'font_sha256':sha(FONT),
          'reference_hashes':reference_hashes,
          'checks':{'wall_groups_covered':len(wall_sources),'wall_segments':len(walls),'openings':len(openings),
                    'room_doors':len(doors),'furniture_source_leaves':len(furniture),'jogs_connected':len(a['jogs']),
                    'wall_contacts':len(contacts),'boundary_rings':len(boundary),'boundary_corners':len(corners),
                    'positive_wall_overlaps':len(intersections),'openings_obstructed_by_wall_footprints':0,
                    'selected_face_checks':len(face_checks),'max_selected_face_residual_px':max(abs(f['residual_px']) for f in face_checks),
                    'all_door_pivots_located':True,'all_source_leaf_symbols_accounted_for':True,
                    'source_unchanged':True,'uniform_T10_transform':True},
          'not_tested':['área del departamento','alturas','barrido físico de hojas y marcos','colisiones 3D','mobiliario final','recorrido','Blender/GLB/Unreal','sitio publicado'],
          'files':{p.name:sha(p) for p in sorted(OUT.iterdir()) if p.suffix in ('.png','.tsv')}}
write(OUT/'comprobacion.json',report)
print(json.dumps(report['checks'],ensure_ascii=False,indent=2))
