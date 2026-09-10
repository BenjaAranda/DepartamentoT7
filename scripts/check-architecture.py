"""Compare generated Blender wall bounds against registered native-plan coordinates."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
read=lambda p:json.loads((R/p).read_text(encoding='utf-8'))
report=read('validation/e04/geometry-check.json')
cal=read('architecture/calibration/t10-calibracion.json')
adjust=read('architecture/dimensions/t13-criterio-aproximado.json')
s=adjust['m_per_native_pixel'];u0,v0=cal['origin']['pixel_uv']
native=Image.open(R/'references/derived/p20-t7/planta-nativa.png').convert('RGBA')
overlay=Image.new('RGBA',native.size);d=ImageDraw.Draw(overlay)
errors=[]
for wall in report['walls']:
    l,b,r,t=wall['actual_rect_xy_m']
    rect=(l/s+u0,v0-t/s,r/s+u0,v0-b/s)
    d.rectangle(rect,fill=(0,122,178,65),outline=(0,80,164,230),width=2)
    errors.append(wall['max_error_m'])
composite=Image.alpha_composite(native,overlay).convert('RGB')
canvas=Image.new('RGB',(1636,1030),'white');canvas.paste(composite,(50,100));d=ImageDraw.Draw(canvas)
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/arial.ttf',n)
d.text((50,25),'E04 · Muros de Blender sobre la planta original',font=font(29),fill='#173548')
d.text((50,65),'Contornos proyectados desde las mallas; transformación XY uniforme registrada en T13.',font=font(20),fill='#405968')
d.text((50,940),f'40 paños · Desviación de generación máxima: {max(errors)*1000:.4f} mm · Contorno: {report["area_m2"]:.2f} m²',font=font(23),fill='#173548')
d.text((50,980),'La coincidencia gráfica no mejora la precisión del raster: control dimensional máximo de 12,073 mm.',font=font(21),fill='#8b4938')
canvas.save(R/'validation/e04/superposicion.png')
assert max(errors)<1e-5
assert abs(report['area_m2']-76.66)<=.5
assert report['context_storeys']==4 and len(report['doors'])==6
checks=dict(revision=report['revision'],generated_wall_bounds_match=True,maximum_generated_error_m=max(errors),
    area_within_user_tolerance=True,physical_eye_height_m=report['eye_m'],graphical_source_error_limit_m=adjust['max_control_error_m'],
    nominal_10mm_source_goal_met=adjust['checks']['controls_within_10mm'],upper_context_storeys=3,
    max_hinge_adjustment_m=max(d['hinge_adjustment_m'] for d in report['doors']),
    scope='40 wall bodies compared; opening geometry detailed in geometry-check.json. Furniture and physical routes follow in E05/E06.')
(R/'validation/e04/orthographic-check.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(checks,indent=2))
