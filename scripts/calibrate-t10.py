"""Calibrate one uniform metric transform, keeping independent checks separate."""
import csv
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'architecture/calibration'
OUT = ROOT / 'references/derived/t10-calibracion'
FONT = 'C:/Windows/Fonts/arial.ttf'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n',encoding='utf-8',newline='\n')


def probe(image, spec, algorithm):
    x0,y0,x1,y1 = spec['roi']
    if not (0<=x0<x1<=image.shape[1] and 0<=y0<y1<=image.shape[0]):
        raise ValueError('Probe outside the source frame')
    axis=spec['axis']
    profile=image[y0:y1,x0:x1].mean(axis=0 if axis=='u' else 1)
    peak=int(np.argmin(profile)); half=algorithm['profile_peak_half_width_px']
    lo=max(0,peak-half);hi=min(len(profile),peak+half+1)
    weights=np.maximum(0,algorithm['profile_darkness_threshold']-profile[lo:hi])
    if weights.sum()==0 or peak in {0,len(profile)-1}:
        raise ValueError('Probe lacks an isolated interior stroke peak')
    coordinate=float(np.dot(np.arange(lo,hi)+(x0 if axis=='u' else y0),weights)/weights.sum())
    point=[coordinate,spec['cross_coordinate']] if axis=='u' else [spec['cross_coordinate'],coordinate]
    return {'pixel':point,'coordinate':coordinate,'roi':spec['roi'],'axis':axis,'description':spec['description'],
            'profile_min':float(profile[peak]),'algorithm':'centroid below threshold, within one pixel of darkest profile sample'}


def fit_circle_pixels(image, spec, algorithm):
    cx,cy,r=spec['seed']
    # Limit computation to the observed image neighbourhood, not a metric model.
    x0=max(0,int(cx-r-5));x1=min(image.shape[1],int(cx+r+6))
    y0=max(0,int(cy-r-5));y1=min(image.shape[0],int(cy+r+6))
    yy,xx=np.mgrid[y0:y1,x0:x1];values=image[y0:y1,x0:x1]
    angle=np.degrees(np.arctan2(yy-cy,xx-cx))%360
    arcs=np.logical_or.reduce([(angle>=lo)&(angle<=hi) for lo,hi in spec['arcs_degrees']])
    mask=(abs(np.hypot(xx-cx,yy-cy)-r)<algorithm['circle_seed_band_px'])&(values<algorithm['circle_darkness_threshold'])&arcs
    points=np.column_stack((xx[mask],yy[mask]));intensity=values[mask]
    used=np.ones(len(points),dtype=bool)
    for iteration in range(algorithm['circle_iterations']+1):
        p=points[used].astype(float);weights=np.sqrt((255-intensity[used].astype(float))/255)
        if len(p)<50: raise ValueError('Not enough circle pixels')
        matrix=np.column_stack((2*p[:,0],2*p[:,1],np.ones(len(p))))
        solution=np.linalg.lstsq(matrix*weights[:,None],np.sum(p*p,axis=1)*weights,rcond=None)[0]
        center=solution[:2];radius=math.sqrt(solution[2]+np.dot(center,center))
        residual=np.linalg.norm(points-center,axis=1)-radius
        if iteration<algorithm['circle_iterations']:
            used=abs(residual)<algorithm['circle_trim_residual_px']
    # Independent x/y diameter diagnostics: do not impose equality of ellipse axes.
    z=(p-center)/radius
    conic=np.column_stack((z[:,0]**2,z[:,1]**2,z[:,0],z[:,1],np.ones(len(z))))
    _,_,vectors=np.linalg.svd(conic*weights[:,None],full_matrices=False)
    A,B,C,D,E=vectors[-1]
    if A<0:A,B,C,D,E=-A,-B,-C,-D,-E
    if B<=0:raise ValueError('Pixel fit did not yield an ellipse')
    local_center=np.array([-C/(2*A),-D/(2*B)])
    constant=C*C/(4*A)+D*D/(4*B)-E
    radii=radius*np.sqrt([constant/A,constant/B])
    ellipse_center=center+radius*local_center
    result={'id':spec['id'],'t09':spec['t09'],'label':spec['label'],'role':'check_circle','group':spec['id'],
            'seed_px':spec['seed'],'arcs_degrees':spec['arcs_degrees'],'candidate_pixels':len(points),'used_pixels':int(used.sum()),
            'circle_center_px':center.tolist(),'circle_diameter_px':float(radius*2),
            'circle_fit_rms_px':float(np.sqrt(np.mean(residual[used]**2))),
            'ellipse_center_px':ellipse_center.tolist(),'ellipse_diameters_px':(2*radii).tolist(),
            'note':'Dos diámetros de un mismo símbolo; comparten píxeles y no son dos fuentes independientes.'}
    return result,p


def main():
    spec_path=DATA/'t10-observaciones.json';spec=json.loads(spec_path.read_text(encoding='utf-8'))
    source_path=ROOT/spec['source']
    if sha(source_path)!=spec['source_sha256']:raise ValueError('Native plan changed')
    manifest=json.loads((ROOT/'references/derived/p20-t7/manifest.json').read_text(encoding='utf-8'))
    for artifact in manifest['artifacts']:
        if sha(ROOT/'references/derived/p20-t7'/artifact['file'])!=artifact['sha256']:raise ValueError('T07 reference changed')
    pdf=ROOT.parent/manifest['source']['filename']
    if sha(pdf)!=manifest['source']['sha256_before']:raise ValueError('PDF changed')
    inventory_path=ROOT/'architecture/measurements/t09-inventario.json'
    inventory=json.loads(inventory_path.read_text(encoding='utf-8'))
    previous_checks=json.loads((ROOT/'references/derived/t09-medidas/comprobacion.json').read_text(encoding='utf-8'))
    if sha(inventory_path)!=previous_checks['catalogue_sha256']:raise ValueError('T09 catalogue changed')
    if sha(ROOT/inventory['authored_source'])!=inventory['authored_source_sha256']:raise ValueError('T09 readings changed')
    t09={item['id']:item for item in inventory['items']}
    original=Image.open(source_path).convert('RGB');pixels=np.asarray(original.convert('L'))
    algorithm=spec['algorithm'];probes={key:probe(pixels,value,algorithm) for key,value in spec['probes'].items()}
    rows=[]
    for segment in spec['segments']:
        if segment['axis']!=probes[segment['a']]['axis'] or segment['axis']!=probes[segment['b']]['axis']:
            raise ValueError('Segment axes differ')
        expected=t09[segment['t09']]['length_m_if_unit_accepted']
        if expected is None or expected<=0:raise ValueError('No valid dimensional reading')
        length=abs(probes[segment['b']]['coordinate']-probes[segment['a']]['coordinate'])
        rows.append({**segment,'expected_m':expected,'length_px':length,'point_a_px':probes[segment['a']]['pixel'],'point_b_px':probes[segment['b']]['pixel'],
                     'unit_status':t09[segment['t09']]['unit_status']})
    fitting=[r for r in rows if r['role']=='fit']
    if {r['axis'] for r in fitting}!={'u','v'}:raise ValueError('Both axes are required')
    def fit(selected):
        return sum(r['length_px']*r['expected_m'] for r in selected)/sum(r['length_px']**2 for r in selected)
    scale=fit(fitting);scale_u=fit([r for r in fitting if r['axis']=='u']);scale_v=fit([r for r in fitting if r['axis']=='v'])
    circles=[];circle_points={}
    for circle in spec['circles']:
        result,points=fit_circle_pixels(pixels,circle,algorithm);circles.append(result);circle_points[result['id']]=points
        cx,cy=result['ellipse_center_px']
        for axis,diameter in zip(['u','v'],result['ellipse_diameters_px']):
            point_a=[cx-diameter/2,cy] if axis=='u' else [cx,cy-diameter/2]
            point_b=[cx+diameter/2,cy] if axis=='u' else [cx,cy+diameter/2]
            rows.append({'id':result['id']+'-'+axis.upper(),'role':'check_circle','axis':axis,'t09':result['t09'],'group':result['group'],
                         'label':result['label']+' / '+axis,'expected_m':t09[result['t09']]['length_m_if_unit_accepted'],
                         'length_px':diameter,'point_a_px':point_a,'point_b_px':point_b,'unit_status':'inferida','note':result['note']})
    limit=algorithm['metric_residual_target_m']
    for row in rows:
        row.update(measured_m=row['length_px']*scale,error_m=row['length_px']*scale-row['expected_m'])
        row['within_10mm']=abs(row['error_m'])<=limit
    fitting=[r for r in rows if r['role']=='fit'];checks=[r for r in rows if r['role']!='fit'];independent=[r for r in checks if r['role']!='check_shared']
    origin=[probes[spec['origin']['u_probe']]['coordinate'],probes[spec['origin']['v_probe']]['coordinate']]
    horizontal=math.degrees(math.atan2(probes['OV_RIGHT']['coordinate']-probes['OV_LEFT']['coordinate'],265-52.5))
    vertical=math.degrees(math.atan2(probes['OU_LOW']['coordinate']-probes['OU_HIGH']['coordinate'],607-295))
    alignment=max(abs(horizontal),abs(vertical))
    matrix=np.array([[scale,0,-scale*origin[0]],[0,-scale,scale*origin[1]],[0,0,1]])
    inverse=np.linalg.inv(matrix)
    def metric(p):return (matrix@np.array([*p,1.0]))[:2].tolist()
    samples=np.array([[0,0,1],[1535,812,1],[*origin,1],[*spec['landmarks'][0]['pixel'],1],[*spec['landmarks'][2]['pixel'],1]],dtype=float)
    metric_samples=(matrix@samples.T).T
    roundtrip=float(np.max(np.abs((inverse@metric_samples.T).T-samples)))
    if not np.allclose(metric(origin),[0,0],atol=1e-12):raise ValueError('Origin conversion failed')
    if not np.allclose(metric([origin[0]+1/scale,origin[1]]),[1,0],atol=1e-12):raise ValueError('X metric rule failed')
    if not np.allclose(metric([origin[0],origin[1]-1/scale]),[0,1],atol=1e-12):raise ValueError('Y metric rule failed')
    landmarks=[{**mark,'blender_xy_m':metric(mark['pixel'])} for mark in spec['landmarks']]
    by_id={mark['id']:mark['blender_xy_m'] for mark in landmarks}
    orientation_ok=by_id['REF-ACCESO'][0]>by_id['REF-LOGIA'][0]>by_id['REF-D3'][0] and by_id['REF-ACCESO'][1]>by_id['REF-LOGIA'][1]
    # Deterministic reading sensitivity, not a statistical confidence interval.
    spread=2*algorithm['endpoint_sensitivity_px']
    intervals=[(r['expected_m']/(r['length_px']+spread),r['expected_m']/(r['length_px']-spread)) for r in fitting]
    sensitivity=[max(v[0] for v in intervals),min(v[1] for v in intervals)]
    if not sensitivity[0]<=scale<=sensitivity[1]:raise ValueError('Reading sensitivity intervals are inconsistent')
    maximum=max(abs(r['error_m']) for r in checks)
    result={'task':'T10','revision':1,'status':'working_metric_calibration','source_pdf_sha256':sha(pdf),'source_image_sha256':sha(source_path),
            'observations_sha256':sha(spec_path),'t09_catalogue_sha256':sha(inventory_path),
            'runtime':{'python':sys.version.split()[0],'numpy':np.__version__,'pillow':pillow_version},
            'policy':{'uses_area_to_fit':False,'uses_furniture_dimensions':False,'nonuniform_scaling_applied':False,'architectural_validation_complete':False,
                      'local_units':'cm inferidos; coherentes con seis controles explícitos de 15 cm','scope':'Transformación de trabajo para levantar T11. No acredita dimensiones ausentes, área, alturas, cámara o modelo 3D.'},
            'scale':{'m_per_px':scale,'px_per_m':1/scale,'fit_method':'Least squares through origin: sum(pixel_span * nominal_m) / sum(pixel_span^2)',
                     'fit_ids':[r['id'] for r in fitting],'diagnostic_u_m_per_px':scale_u,'diagnostic_v_m_per_px':scale_v,
                     'diagnostic_axis_difference_percent':100*abs(scale_u-scale_v)/scale,
                     'sensitivity_interval_m_per_px':sensitivity,'sensitivity_assumption':'Cada extremo +/-1 px; intervalo de consistencia, no confianza estadística ni tolerancia constructiva.',
                     'metres_per_single_pixel':scale},
            'origin':{'pixel_uv':origin,'blender_xyz_m':[0,0,0],'definition':spec['origin']['label'],'reading_sensitivity_px':1},
            'axes':{**spec['axes'],'horizontal_deviation_deg':horizontal,'vertical_deviation_deg':vertical},
            'transforms':{'pixel_uv_to_blender_xy_homogeneous':matrix.tolist(),'blender_xy_to_pixel_uv_homogeneous':inverse.tolist(),
                          'formula_blender':'X=(u-u0)*s; Y=(v0-v)*s; Z=altura sobre piso terminado',
                          'formula_gltf':'Desde Blender: (X,Y,Z) -> (X,Z,-Y); una unidad = un metro',
                          'unreal':'Conversión de metros a centímetros y orientación a comprobar en T49; sin importación realizada en T10.'},
            'probes':probes,'observations':rows,'circles':circles,'not_used':spec['not_used'],'landmarks':landmarks,
            'specified_eye_height_m':spec['specified_eye_height_m'],'eye_height_verified_in_3d':False,
            'checks':{'fit_count':len(fitting),'check_segments':len([r for r in checks if r['role']!='check_circle']),
                      'check_circle_symbols':len(circles),'check_circle_diameters':len(circles)*2,
                      'max_fit_residual_m':max(abs(r['error_m']) for r in fitting),'max_check_residual_m':maximum,
                      'max_fit_independent_check_residual_m':max(abs(r['error_m']) for r in independent),
                      'all_selected_checks_within_10mm':all(r['within_10mm'] for r in checks),
                      'axis_alignment_within_target':alignment<=algorithm['axis_alignment_target_deg'],'orientation_landmarks_pass':orientation_ok,'roundtrip_max_error_px':roundtrip}}
    OUT.mkdir(parents=True,exist_ok=True)
    save_json(DATA/'t10-calibracion.json',result)
    with (OUT/'residuos.tsv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.writer(stream,delimiter='\t',lineterminator='\n');writer.writerow(['id','rol','eje','referencia_T09','nominal_m','longitud_px','convertida_m','residuo_mm','dentro_10mm','grupo'])
        for r in rows:writer.writerow([r['id'],r['role'],r['axis'],r['t09'],r['expected_m'],f"{r['length_px']:.6f}",f"{r['measured_m']:.6f}",f"{r['error_m']*1000:.3f}",r['within_10mm'],r['group']])
    report=['# Residuos de calibración T10','','Resultados numéricos de lecturas del raster. Los decimales sirven para reproducir el cálculo; no implican precisión constructiva.','',
            '| ID | Función | Referencia | Nominal (m) | Leído (px) | Convertido (m) | Residuo (mm) | ≤ 10 mm |','|---|---|---|---:|---:|---:|---:|---|']
    roles={'fit':'Ajuste','check':'Control fuera del ajuste','check_shared':'Control con marca compartida','check_circle':'Diámetro de control'}
    for r in rows:report.append(f"| {r['id']} | {roles[r['role']]} | {r['t09']} | {r['expected_m']:.3f} | {r['length_px']:.3f} | {r['measured_m']:.6f} | {r['error_m']*1000:+.3f} | {'Sí' if r['within_10mm'] else 'No'} |")
    report += ['',f"Escala uniforme: **{scale:.10f} m/px**, equivalente a **{1/scale:.4f} px/m**. El máximo residuo de control es **{maximum*1000:.3f} mm**.",
               '', 'Los controles que comparten marcas, alineaciones o el mismo círculo no se consideran fuentes estadísticamente independientes. Las tres cotas de ajuste se mantienen separadas de los controles; no se reajusta con estos últimos.',
               '',f"Sensibilidad a ±1 px por extremo de ajuste: [{sensitivity[0]:.10f}, {sensitivity[1]:.10f}] m/px. No es un intervalo de confianza ni una validación de todas las dimensiones de la vivienda.",'']
    (DATA/'RESIDUOS_T10.md').write_text('\n'.join(report),encoding='utf-8',newline='\n')
    render_evidence(original,result,spec,circle_points)
    evidence=[{'file':name,'sha256':sha(OUT/name)} for name in ['planta-calibrada.png','detalle-cadenas.png','controles-circulos.png','residuos.tsv']]
    summary={'task':'T10','source_pdf_unchanged':True,'t07_references_unchanged':True,'t09_catalogue_and_readings_unchanged':True,
             **result['checks'],'scale_m_per_px':scale,'scale_px_per_m':1/scale,'origin_pixel':origin,
             'scale_axis_difference_percent':result['scale']['diagnostic_axis_difference_percent'],'uses_area_to_fit':False,
             'architecture_final_validation':False,'catalogue_sha256':sha(DATA/'t10-calibracion.json'),'evidence':evidence,
             'font_sha256':sha(Path(FONT))}
    save_json(OUT/'comprobacion.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    if not (summary['all_selected_checks_within_10mm'] and summary['axis_alignment_within_target'] and orientation_ok and roundtrip<1e-9):
        raise ValueError('Calibration needs review; do not mark T10 complete')


def render_evidence(original,result,spec,circle_points):
    blue='#006ca8';green='#14794d';orange='#bd5100';dark='#172535'
    fonts={size:ImageFont.truetype(FONT,size) for size in [16,18,20,24,30]}
    def label(draw,xy,text,color=dark,size=18):
        box=draw.textbbox(xy,text,font=fonts[size]);draw.rectangle((box[0]-3,box[1]-2,box[2]+3,box[3]+2),fill='white');draw.text(xy,text,font=fonts[size],fill=color)
    def segment(draw,row,offset=(0,0),zoom=1,origin=(0,0)):
        def pt(p):return (offset[0]+(p[0]-origin[0])*zoom,offset[1]+(p[1]-origin[1])*zoom)
        a=pt(row['point_a_px']);b=pt(row['point_b_px']);color=blue if row['role']=='fit' else green
        draw.line([a,b],fill=color,width=2)
        for x,y in [a,b]:draw.ellipse((x-3,y-3,x+3,y+3),fill='white',outline=color,width=2)
    canvas=Image.new('RGB',(2000,1040),'#f4f7fb');draw=ImageDraw.Draw(canvas)
    draw.text((28,20),'T10 | Origen, ejes y escala de trabajo',font=fonts[30],fill=dark)
    draw.text((28,59),'Una escala uniforme. Controles fuera del ajuste. Sin usar la superficie para calibrar.',font=fonts[20],fill=dark)
    offset=(28,105);canvas.paste(original,offset);draw=ImageDraw.Draw(canvas)
    for row in result['observations']:
        if row['role']!='check_circle':segment(draw,row,offset)
    for circle in result['circles']:
        cx,cy=circle['ellipse_center_px'];rx,ry=np.array(circle['ellipse_diameters_px'])/2
        draw.ellipse((offset[0]+cx-rx,offset[1]+cy-ry,offset[0]+cx+rx,offset[1]+cy+ry),outline=green,width=2)
    ox=offset[0]+result['origin']['pixel_uv'][0];oy=offset[1]+result['origin']['pixel_uv'][1];rule=1/result['scale']['m_per_px']
    draw.ellipse((ox-5,oy-5,ox+5,oy+5),fill=orange)
    draw.line((ox,oy,ox+rule,oy),fill=orange,width=3);draw.polygon([(ox+rule,oy),(ox+rule-9,oy-5),(ox+rule-9,oy+5)],fill=orange)
    draw.line((ox,oy,ox,oy-rule),fill=orange,width=3);draw.polygon([(ox,oy-rule),(ox-5,oy-rule+9),(ox+5,oy-rule+9)],fill=orange)
    label(draw,(ox+rule+8,oy-9),'+X / 1 m',orange);label(draw,(ox+10,oy-rule-12),'+Y / 1 m',orange);label(draw,(ox+8,oy+12),'Origen D1',orange)
    for mark in result['landmarks']:
        u,v=mark['pixel'];x=offset[0]+u;y=offset[1]+v
        draw.line((x-5,y,x+5,y),fill=orange,width=2);draw.line((x,y-5,x,y+5),fill=orange,width=2)
        short={'REF-ACCESO':'Acceso','REF-D3':'D3','REF-LOGIA':'Logia'}[mark['id']]
        label(draw,(x-45,y+12),short,orange,16)
    sx=1590;y=120
    notes=[('Escala uniforme',24,dark),(f"{result['scale']['px_per_m']:.4f} px = 1 m",24,blue),
           (f"{result['scale']['m_per_px']:.10f} m/px",20,blue),('',20,dark),('Azul: 3 cotas de ajuste',20,blue),
           ('Verde: cadenas, espesores',20,green),('y 4 círculos de control',20,green),('',20,dark),('Máximo residuo de control',20,dark),
           (f"{result['checks']['max_check_residual_m']*1000:.3f} mm",24,green),('en las muestras seleccionadas',18,dark),('',20,dark),('Origen nativo (u, v)',20,dark),
           (f"({result['origin']['pixel_uv'][0]:.3f}, {result['origin']['pixel_uv'][1]:.3f})",20,dark),('X derecha / Y arriba / Z altura',18,dark),('Norte geográfico sin determinar',18,dark),('',20,dark),
           ('Precisión limitada por el raster',20,orange),('1 píxel ≈ 8,5 mm con esta escala',18,dark),('La sensibilidad se informa aparte.',18,dark),('',20,dark),('No valida superficie, alturas,',18,dark),('vanos ni una cámara 3D existente.',18,dark)]
    for text,size,color in notes:draw.text((sx,y),text,font=fonts[size],fill=color);y+=31
    draw.text((28,958),'Los círculos verdes son símbolos de maniobra de la referencia; no forman muros ni colliders.',font=fonts[20],fill=dark)
    draw.text((28,992),'Fuente: planta nativa de p20. Los marcadores de orientación no son puntos de inicio del recorrido.',font=fonts[18],fill=dark)
    canvas.save(OUT/'planta-calibrada.png')

    detail=Image.new('RGB',(1640,980),'#f4f7fb');d=ImageDraw.Draw(detail)
    d.text((24,18),'T10 | Marcas de las cadenas de cotas',font=fonts[30],fill=dark)
    d.text((24,59),'Azul: ajuste. Verde: control. Las marcas proceden del trazo, no de la caja del texto.',font=fonts[20],fill=dark)
    panels=[('Baño: 90 para ajuste; 40 comparte una marca',(826,223,1024,266),(24,140),3.8,['CAL-FH01','CAL-CH01']),
            ('Baño: 80 y 70, marcas fuera del ajuste',(826,438,1024,522),(24,465),3.8,['CAL-CH02','CAL-CH03']),
            ('Logia: ajuste 137.5 y 50; control 90',(1029,597,1215,719),(845,140),3.8,['CAL-FH02','CAL-FV01','CAL-CH04'])]
    for title,box,where,zoom,ids in panels:
        d.text((where[0],where[1]-33),title,font=fonts[20],fill=dark)
        crop=original.crop(box).resize((round((box[2]-box[0])*zoom),round((box[3]-box[1])*zoom)),Image.Resampling.NEAREST)
        detail.paste(crop,where);d=ImageDraw.Draw(detail)
        for row in result['observations']:
            if row['id'] in ids:segment(d,row,where,zoom,box[:2])
    d.text((845,680),'137.5 y 90 tienen extremos diferentes.',font=fonts[20],fill=dark)
    d.text((845,719),'El extremo derecho de 90 está sobre la',font=fonts[20],fill=dark)
    d.text((845,750),'línea discontinua, junto al marco.',font=fonts[20],fill=dark)
    d.text((24,873),'Unidades locales: cm inferidos, coherentes con las menciones explícitas de 15 cm.',font=fonts[20],fill=dark)
    d.text((24,914),'Las posiciones subpíxel reproducen la lectura; no aumentan la precisión del documento original.',font=fonts[20],fill=dark)
    detail.save(OUT/'detalle-cadenas.png')

    cc=Image.new('RGB',(1020,1230),'#f4f7fb');d=ImageDraw.Draw(cc)
    d.text((24,16),'T10 | Cuatro círculos fuera del ajuste',font=fonts[30],fill=dark)
    d.text((24,61),'Sectores verdes: píxeles usados. Azul: elipse de comprobación.',font=fonts[18],fill=dark)
    for i,circle in enumerate(result['circles']):
        cx,cy=circle['ellipse_center_px'];box=(int(cx-101),int(cy-101),int(cx+101),int(cy+101));box=(max(0,box[0]),max(0,box[1]),box[2],box[3])
        x=24+(i%2)*500;y=147+(i//2)*522;zoom=2
        crop=original.crop(box).resize(((box[2]-box[0])*zoom,(box[3]-box[1])*zoom),Image.Resampling.NEAREST);cc.paste(crop,(x,y));d=ImageDraw.Draw(cc)
        for u,v in circle_points[circle['id']]:
            xx=x+(u-box[0])*zoom;yy=y+(v-box[1])*zoom;d.rectangle((xx,yy,xx+1,yy+1),fill=green)
        rx,ry=np.array(circle['ellipse_diameters_px'])/2;d.ellipse((x+(cx-rx-box[0])*zoom,y+(cy-ry-box[1])*zoom,x+(cx+rx-box[0])*zoom,y+(cy+ry-box[1])*zoom),outline=blue,width=1)
        d.text((x,y-33),circle['id']+' | '+circle['label'],font=fonts[20],fill=dark)
        diam=np.array(circle['ellipse_diameters_px'])*result['scale']['m_per_px']
        d.text((x,y+415),f"Horizontal {diam[0]:.4f} m / vertical {diam[1]:.4f} m",font=fonts[18],fill=dark)
        d.text((x,y+444),'Nominal 1,50 m; diámetros correlacionados.',font=fonts[18],fill=dark)
    d.text((24,1191),'La elipse se mide por separado en ambos ejes; no deforma el plano.',font=fonts[18],fill=dark)
    cc.save(OUT/'controles-circulos.png')


if __name__=='__main__':
    main()
