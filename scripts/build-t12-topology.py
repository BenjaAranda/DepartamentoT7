"""T12: source-grounded wet-core interpretation and bounded 2D topology checks.

Reads T11 faces without changing them. Does not generate areas, heights, colliders
or a navigable model. All metric coordinates derive from T10, never a second fit.
"""
from pathlib import Path
from collections import deque
import csv
import hashlib
import json
import math
import platform
import re

import numpy as np
from PIL import Image, ImageDraw, ImageFont, __version__ as PIL_VERSION
from pypdf import PdfReader, __version__ as PDF_VERSION

ROOT = Path(__file__).resolve().parents[1]
AUTHOR = ROOT/'architecture/topology/t12-interpretacion.json'
OUT = ROOT/'references/derived/t12-bano-logia'
OUT.mkdir(parents=True, exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text(encoding='utf-8'))
def write(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')

a = read(AUTHOR)
paths = {k:ROOT/v for k,v in a['sources'].items() if isinstance(v,str) and k!='secondary_scope'}
reg = read(paths['walls'])
definitions = read(paths['coordinate_definitions'])
cal = read(paths['calibration'])
assert sha(paths['walls']) == '72693862f4e05123c422cea84d369002e34810adb64ac1df4807b6164599b535'
assert sha(paths['coordinate_definitions']) == reg['author_sha256']
assert sha(paths['calibration']) == reg['calibration_sha256']
pdf = ROOT.parent/'Presentación Aprobación Proyecto Técnico 2.pdf'
assert sha(pdf) == reg['source_pdf_sha256']
manifest = read(paths['plan'].parent/'manifest.json')
for record in manifest['artifacts']+[manifest['text_extraction']]:
    assert sha(paths['plan'].parent/record['file']) == record['sha256']
source_hashes = {k:sha(p) for k,p in paths.items()}
source_hashes['pdf'] = sha(pdf)

coord = lambda x: definitions['coordinates'][x] if isinstance(x,str) else x
pt = lambda p:[coord(x) for x in p]
rect = lambda r:[coord(x) for x in r]
s = cal['scale']['m_per_px'];u0,v0 = cal['origin']['pixel_uv']
metric = lambda p:[(p[0]-u0)*s,(v0-p[1])*s]
wall_by_id = {w['id']:w for w in reg['walls']}
walls = [w['rect_px'] for w in reg['walls']]
openings = {o['id']:o for o in reg['openings']}

def rect_overlap(r,t):
    return max(0,min(r[2],t[2])-max(r[0],t[0]))*max(0,min(r[3],t[3])-max(r[1],t[1]))

def inside_rect(p,r,epsilon=0):
    return r[0]-epsilon<=p[0]<=r[2]+epsilon and r[1]-epsilon<=p[1]<=r[3]+epsilon

def point_in_polygon(p, poly):
    inside = False
    for q,r in zip(poly,poly[1:]+poly[:1]):
        if (q[1]>p[1]) != (r[1]>p[1]):
            x = q[0]+(p[1]-q[1])*(r[0]-q[0])/(r[1]-q[1])
            if p[0]<x: inside = not inside
    return inside

def segment_hits_rect(p,q,r):
    """Liang-Barsky on a slightly inset rectangle: boundary contact is not intrusion."""
    bounds = [r[0]+1e-7,r[1]+1e-7,r[2]-1e-7,r[3]-1e-7]
    low,high = 0.,1.
    for axis in (0,1):
        delta = q[axis]-p[axis]
        if abs(delta)<1e-12:
            if p[axis]<bounds[axis] or p[axis]>bounds[axis+2]:return False
        else:
            t0,t1 = sorted([(bounds[axis]-p[axis])/delta,(bounds[axis+2]-p[axis])/delta])
            low,high = max(low,t0),min(high,t1)
            if low>high:return False
    return True

regions = []
for rr in a['regions']:
    poly = [pt(p) for p in rr['polygon_refs']]
    bands = [rect(b) for b in rr['interior_bands']]
    assert all(x0<x1 and y0<y1 for x0,y0,x1,y1 in bands)
    assert all(not rect_overlap(b,w) for b in bands for w in walls), rr['id']
    assert all(not rect_overlap(b,c) for i,b in enumerate(bands) for c in bands[i+1:])
    # Connected bands share a positive-width edge, not just one point.
    seen = {0};todo = deque([0])
    while todo:
        i = todo.popleft();b = bands[i]
        for j,c in enumerate(bands):
            if j in seen:continue
            horizontal = (b[3]==c[1] or b[1]==c[3]) and min(b[2],c[2])>max(b[0],c[0])
            vertical = (b[2]==c[0] or b[0]==c[2]) and min(b[3],c[3])>max(b[1],c[1])
            if horizontal or vertical:seen.add(j);todo.append(j)
    assert len(seen)==len(bands)
    # Exact coordinate-cell comparison of polygon and the independent band decomposition.
    xs=sorted({p[0] for p in poly}|{b[k] for b in bands for k in (0,2)})
    ys=sorted({p[1] for p in poly}|{b[k] for b in bands for k in (1,3)})
    for x0,x1 in zip(xs,xs[1:]):
        for y0,y1 in zip(ys,ys[1:]):
            p=[(x0+x1)/2,(y0+y1)/2]
            assert point_in_polygon(p,poly)==any(inside_rect(p,b) for b in bands)
    # Every perimeter segment must be supported by the named wall face or a named opening.
    # Door/window segments close only this analytical contour, never the physical geometry.
    providers=[wall_by_id[i]['rect_px'] for i in rr['walls']]+[openings[i]['rect_px'] for i in rr['access_openings']+rr['non_access_openings']]
    perimeter_samples=0
    for p,q in zip(poly,poly[1:]+poly[:1]):
        for t in np.linspace(0,1,51):
            sample=(np.array(p)*(1-t)+np.array(q)*t).tolist()
            assert any(inside_rect(sample,b,1e-7) for b in providers),(rr['id'],sample)
            perimeter_samples+=1
    for oi in rr['access_openings']:
        r=openings[oi]['rect_px']
        assert any(abs(r[3]-b[1])<1e-8 and min(r[2],b[2])>max(r[0],b[0]) for b in bands)
    regions.append({**rr,'polygon_px':poly,'polygon_xy_m':[metric(p) for p in poly],'bands_px':bands,
                    'length_y_m':(max(p[1] for p in poly)-min(p[1] for p in poly))*s,
                    'band_widths_m':[(b[2]-b[0])*s for b in bands],
                    'connected_2d':True,'perimeter_samples_supported':perimeter_samples,
                    'computed_area_m2':None})
region_by_id={r['id']:r for r in regions}
assert all(not rect_overlap(b,c) for i,r in enumerate(regions) for t in regions[i+1:] for b in r['bands_px'] for c in t['bands_px'])

zones=[]
for z in a['zones']:
    zone={**z,'geometry_role':'observacion funcional, no collider ni huella final de equipo'}
    if 'ellipse_from_calibration' in z:
        e=next(c for c in cal['circles'] if c['id']==z['ellipse_from_calibration'])
        center=e['ellipse_center_px'];diam=e['ellipse_diameters_px'];radii=[d/2 for d in diam]
        zone.update(center_px=center,diameters_px=diam,center_xy_m=metric(center),diameters_m=[d*s for d in diam])
        for w in walls:
            nearest=[min(max(center[i],w[i]),w[i+2]) for i in (0,1)]
            assert sum(((nearest[i]-center[i])/radii[i])**2 for i in (0,1)) >= 1, 'Giro intersects wall footprint'
    else:
        r=rect(z.get('rect_refs',z.get('rect_px')))
        zone.update(rect_px=r,diagonal_xy_m=[metric(r[:2]),metric(r[2:])],span_m=[(r[2]-r[0])*s,(r[3]-r[1])*s])
        # Rectangles locate equipment and use zones; they are never treated as solids.
        assert all(any(inside_rect(p,b,1e-7) for b in region_by_id[z['region']]['bands_px']) for p in [r[:2],r[2:],[r[0],r[3]],[r[2],r[1]]]),z['id']
        if 'nominal_dimensions_m' in z:
            zone['dimension_residuals_m']=[None if n is None else zone['span_m'][i]-n for i,n in enumerate(z['nominal_dimensions_m'])]
    zones.append(zone)
zone_by_id={z['id']:z for z in zones}

guides=[]
for g in a['topological_guides']:
    p=g['points_px'];segments=list(zip(p,p[1:]))
    assert all(not segment_hits_rect(start,end,w) for start,end in segments for w in walls),g['id']
    assert any(segment_hits_rect(start,end,openings[g['opening']]['rect_px']) for start,end in segments)
    for zi in g['crosses_zones']:
        assert any(segment_hits_rect(start,end,zone_by_id[zi]['rect_px']) for start,end in segments),zi
    guides.append({**g,'points_xy_m':[metric(q) for q in p],'wall_intersections':0})

# The shared vertical extent is protected by the bath-side and loggia-side walls.
bath=region_by_id['R-BANO'];loggia=region_by_id['R-LOGIA']
shared_y=[max(min(p[1] for p in r['polygon_px']) for r in (bath,loggia)),
          min(max(p[1] for p in r['polygon_px']) for r in (bath,loggia))]
assert shared_y[0]<shared_y[1]
for wi in ['W20A','W20B']:
    w=wall_by_id[wi]['rect_px'];assert w[1]<=shared_y[0] and w[3]>=shared_y[1]
assert set(bath['access_openings']).isdisjoint(loggia['access_openings'])
assert all(e['via'] in region_by_id[e['to']]['access_openings'] for e in a['adjacency'])
assert all(e['from']!='R-BANO' or e['to']!='R-LOGIA' for e in a['adjacency'])
assert zone_by_id['SH01']['rect_px'][1] > zone_by_id['EQ03']['rect_px'][3]
assert zone_by_id['SH01']['rect_px'][3] == coord('SOUTH_I')
assert zone_by_id['UA02']['rect_px'][3] == zone_by_id['SH01']['rect_px'][1]

reader=PdfReader(pdf)
terms=['lavadora','lavadero','shaft','sanitario','baño','logia']
text_hits=[]
for i,p in enumerate(reader.pages,1):
    text=p.extract_text() or ''
    matched=[t for t in terms if t in text.lower()]
    if matched:text_hits.append({'page':i,'terms':matched,'text':text})
secondary_images={}
secondary_provenance=[]
for page_number,obj in [(22,204),(23,210)]:
    im=next(v for v in reader.pages[page_number-1].images if v.indirect_reference.idnum==obj)
    image=im.image.convert('RGB');secondary_images[page_number]=image
    secondary_provenance.append({'page':page_number,'pdf_image_object':obj,'size_px':list(image.size),
                                 'decoded_rgb_sha256':hashlib.sha256(image.tobytes()).hexdigest(),
                                 'scope':a['sources']['secondary_scope']})

checks={'regions_connected':len(regions),'bathroom_continuous_bands':len(bath['bands_px']),
        'bathroom_has_one_access':bath['access_openings']==['O05'],
        'loggia_has_one_access':loggia['access_openings']==['O06'],
        'no_direct_bath_loggia_access':True,'separating_walls_cover_shared_length':True,
        'shower_at_far_end':True,'shower_front_continuous_with_use_zone':True,
        'giro_ellipse_does_not_intersect_wall_footprints':True,'guide_wall_intersections':0,
        'guides_cross_expected_portals':True,'functional_zones':len(zones),
        'new_walls_created':0,'existing_wall_coordinates_changed':False,
        'source_files_unchanged':True,'area_computed':False,'physical_walkthrough_tested':False}
result={'task':'T12','revision':a['revision'],'status':a['status'],'author_sha256':sha(AUTHOR),
        'source_sha256':source_hashes,'units':'metros; observaciones en pixeles nativos conservadas',
        'policy':a['policy'],'regions':regions,'zones':zones,'guides':guides,
        'adjacency':a['adjacency'],'forbidden_adjacency':a['forbidden_adjacency'],
        'secondary_provenance':secondary_provenance,'pdf_text_search':{'pages_reviewed':42,'hits':text_hits,'limits':'Busqueda de texto extraible, no OCR exhaustivo de rotulos embebidos.'},
        'checks':checks,'pending':a['pending']}
result_path=ROOT/'architecture/topology/t12-topologia.json';write(result_path,result)

with (OUT/'lectura-funcional.tsv').open('w',encoding='utf-8',newline='') as h:
    fields=['id','elemento','recinto','clase','confianza','interpretacion','decision','continuacion']
    wr=csv.DictWriter(h,fields,delimiter='\t',lineterminator='\n');wr.writeheader()
    wr.writerows({'id':z['id'],'elemento':z['name'],'recinto':z['region'],'clase':z['type'],'confianza':z['confidence'],
                 'interpretacion':z['interpretation'],'decision':z['decision'],'continuacion':z['next']} for z in zones)

FONT=Path('C:/Windows/Fonts/arial.ttf');BOLD=Path('C:/Windows/Fonts/arialbd.ttf')
font=lambda n,b=False:ImageFont.truetype(str(BOLD if b else FONT),n)
INK='#19324a';BLUE='#126f9e';TEAL='#007e79';ORANGE='#ad520c'
native=Image.open(paths['plan']).convert('RGB');iso=Image.open(paths['isometric']).convert('RGB')
def wrap(draw,text,xy,width,size=19,color=INK,bold=False):
    line='';y=xy[1]
    for word in text.split():
        attempt=(line+' '+word).strip()
        if draw.textlength(attempt,font=font(size,bold))>width and line:
            draw.text((xy[0],y),line,font=font(size,bold),fill=color);y+=size+7;line=word
        else:line=attempt
    if line:draw.text((xy[0],y),line,font=font(size,bold),fill=color);y+=size+7
    return y
def tag(draw,xy,text,color=INK,size=18):
    box=draw.textbbox(xy,text,font=font(size,True));draw.rectangle((box[0]-3,box[1]-2,box[2]+3,box[3]+2),fill='white')
    draw.text(xy,text,font=font(size,True),fill=color)
def title(sheet,heading,sub):
    d=ImageDraw.Draw(sheet);d.text((30,22),heading,font=font(31,True),fill=INK)
    d.text((30,67),sub,font=font(19),fill=INK)

sheet=Image.new('RGB',(1800,1220),'white')
title(sheet,'T12 · Baño continuo y logia separada','Planta e isométrica de p20 · comprobación de distribución · sin añadir tabiques ni cambiar T11')
b=(800,125,1230,807);k=1.4;left,top=35,139
sheet.paste(native.crop(b).resize((602,955)),(left,top))
tr=lambda p:(left+(p[0]-b[0])*k,top+(p[1]-b[1])*k)
layer=Image.new('RGBA',sheet.size);d=ImageDraw.Draw(layer)
colors={'R-BANO':(0,128,125,48),'R-LOGIA':(221,135,40,50),'R-TECNICO':(60,75,90,70)}
for r in regions:d.polygon([tr(p) for p in r['polygon_px']],fill=colors[r['id']],outline=colors[r['id']][:3]+(230,),width=2)
for w in reg['walls']:
    if w['rect_px'][2]>=b[0] and w['rect_px'][0]<=b[2] and w['rect_px'][3]>=b[1]:
        # Clip to the source viewport before painting any wall.
        clipped=[max(w['rect_px'][0],b[0]),max(w['rect_px'][1],b[1]),min(w['rect_px'][2],b[2]),min(w['rect_px'][3],b[3])]
        if clipped[0]<clipped[2] and clipped[1]<clipped[3]:d.rectangle((*tr(clipped[:2]),*tr(clipped[2:])),fill=(18,111,158,95))
for g in guides:
    ps=[tr(p) for p in g['points_px']];d.line(ps,fill=(0,115,99,255),width=4)
    x,y=ps[-1];d.polygon([(x,y),(x-6,y-13),(x+6,y-13)],fill=(0,115,99,255))
sheet=Image.alpha_composite(sheet.convert('RGBA'),layer).convert('RGB');d=ImageDraw.Draw(sheet)
for p,name in [([845,165],'BAÑO'),([1100,735],'LOGIA'),([945,719],'DUCHA'),([850,140],'O05'),([1130,580],'O06')]:tag(d,tr(p),name,TEAL,17)
for zid,loc in [('EQ01',[947,187]),('EQ02',[970,286]),('EQ03',[960,461]),('UA01',[918,367]),('UA02',[906,611]),('SV01',[1009,640])]:tag(d,tr(loc),zid,INK,15)

# This is a crop of the actual reference, never a rendering of an invented model.
ic=(135,217,540,539);icrop=iso.crop(ic).resize((1013,805));sheet.paste(icrop,(708,130))
d=ImageDraw.Draw(sheet);tag(d,(718,137),'Isométrica original · continuidad longitudinal',INK,20)
for line,y in [(['Un baño, una entrada por O05, ducha al fondo.'],952),
               (['Logia por O06 desde cocina; sin paso lateral desde baño.'],986),
               (['La franja técnica y sus bordes se conservan separados.'],1020)]:
    d.text((707,y),line[0],font=font(23,True),fill=INK)
d.text((35,1127),'Verde: baño y guías sin anchura · ocre: logia · gris: espacio técnico · azul: paños T11',font=font(21),fill=INK)
d.text((35,1161),'Las guías comprueban continuidad 2D. No certifican el paso de una persona, silla de ruedas o cápsula con muebles.',font=font(19),fill=INK)
sheet.save(OUT/'bano-logia-continuidad.png')

sheet=Image.new('RGB',(1800,1230),'white')
title(sheet,'T12 · Equipos y áreas de uso del baño','Los rectángulos localizan símbolos. No son huellas físicas finales, muros ni colliders.')
cards=[
 ('EQ01','Equipo de cabecera',(930,149,1020,246),['Caja con panel posterior en isométrica: lavadora superior probable.','Sin rótulo confirmatorio; la lavadora final se ubicará en logia.']),
 ('EQ02','Lavamanos',(954,243,1023,330),['Cubeta curva con grifería, reconocible en ambas vistas.','El apoyo y la altura se definirán al equipar el baño.']),
 ('EQ03','Inodoro y apoyos',(908,409,1022,531),['Taza, estanque y barras; reserva de transferencia a la izquierda.','No construir paredes sobre barras ni líneas de cota.']),
 ('UA01','Achurado central',(853,308,1021,429),['Reserva de uso; cifras 120 × 80 coherentes con su dibujo.','No es otro plato de ducha ni un tabique transversal.']),
 ('UA02','Reserva antes de la ducha',(846,552,1008,678),['Área anterior a ducha; la cifra 90 es coherente con su longitud.','Su frente y fondo mantienen la circulación del baño.']),
 ('SH01','Ducha al fondo',(844,661,1008,789),['Líneas de escurrimiento y desagüe en el extremo del recinto.','El trazo frontal no justifica una pared, mampara o escalón.'])]
for i,(zid,name,b,notes) in enumerate(cards):
    x,y=25+(i%3)*592,116+(i//3)*540;d=ImageDraw.Draw(sheet)
    d.rounded_rectangle((x,y,x+565,y+518),12,outline='#d3dfe5',width=2)
    d.text((x+15,y+13),f'{zid} · {name}',font=font(22,True),fill=INK)
    kk=min(505/(b[2]-b[0]),315/(b[3]-b[1]));sz=(round((b[2]-b[0])*kk),round((b[3]-b[1])*kk))
    xx,yy=x+(565-sz[0])//2,y+52;sheet.paste(native.crop(b).resize(sz),(xx,yy))
    if zid=='EQ01':
        # Small isometric inset shows the separate box and its rear control panel.
        inset=iso.crop((430,277,505,356)).resize((112,118));sheet.paste(inset,(x+428,y+241))
    d=ImageDraw.Draw(sheet);ny=y+385
    for text in notes:ny=wrap(d,text,(x+15,ny),535,18)+6
d.text((30,1200),'Las áreas de uso se reservan para la etapa de mobiliario; no se declara cumplimiento normativo ni se fijan alturas.',font=font(19),fill=INK)
sheet.save(OUT/'simbolos-del-bano.png')

sheet=Image.new('RGB',(1800,1160),'white')
title(sheet,'T12 · Logia y volumen técnico','Interpretación de servicio · funciones probables identificadas · referencias genéricas sin transferir dimensiones')
b=(989,589,1221,805);sheet.paste(native.crop(b).resize((650,605)),(35,136))
d=ImageDraw.Draw(sheet)
for text,y in [('LG01: lavadero reconocible.',778),('LG02: símbolo doble de servicio sin identidad confirmada.',817),('SV01: la X interior no son paredes diagonales.',856)]:
    wrap(d,text,(35,y),660,21)
wrap(d,'El acceso pertenece a cocina. La apertura de la celosía y las instalaciones concretas siguen pendientes.',(35,922),650,21)

# Generic construction reference, explicitly distinct from the T7 plan.
p22=secondary_images[22];p23=secondary_images[23]
piece22=p22.crop((610,865,985,1260)).resize((375,395))
piece23=p23.copy();piece23.thumbnail((480,535))
sheet.paste(piece22,(752,173));sheet.paste(piece23,(1260,173))
d=ImageDraw.Draw(sheet)
d.text((752,126),'p22 · Ejemplo Galaxy DS49',font=font(22,True),fill=INK)
wrap(d,'Shaft exterior y celosía de logia rotulados en el ejemplo constructivo.',(752,596),440,20)
d.text((1260,600),'p23 · Ejemplo de instalaciones',font=font(20,True),fill=INK)
wrap(d,'Canalizaciones y cámara técnica: contexto de función, no plano de instalaciones del T7.',(1260,641),480,20)
wrap(d,'En el T7 se conserva la franja y sus bordes. No se asignan diámetros, registros ni altura a partir de estos ejemplos.',(752,927),990,22)
d.text((30,1095),'La lavadora final responde al requisito del usuario y se encajará en logia en T42, conservando puerta y circulación.',font=font(20),fill=INK)
sheet.save(OUT/'logia-y-servicio.png')

report={'task':'T12','source_sha256':source_hashes,'author_sha256':sha(AUTHOR),
        'result_sha256':sha(result_path),'checks':checks,
        'runtime':{'python':platform.python_version(),'numpy':np.__version__,'pillow':PIL_VERSION,'pypdf':PDF_VERSION},
        'font_sha256':sha(FONT),'secondary_images':secondary_provenance,
        'files':{p.name:sha(p) for p in sorted(OUT.iterdir()) if p.suffix in ('.png','.tsv')},
        'limits':['sin áreas computadas','sin dimensiones verticales','sin verificación de acceso físico','sin modelo 3D o colisiones','sin publicación']}
for k,p in paths.items():assert sha(p)==source_hashes[k]
write(OUT/'comprobacion.json',report)
print(json.dumps({'checks':checks,'bathroom_length_m':bath['length_y_m'],'bathroom_widths_m':bath['band_widths_m']},ensure_ascii=False,indent=2))
