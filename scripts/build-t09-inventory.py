"""Validate T09 readings and build a non-geometric, illustrated inventory."""
import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from decimal import Decimal
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'architecture/measurements'
OUTPUT = ROOT / 'references/derived/t09-medidas'
REFERENCE = ROOT / 'references/derived/p20-t7'


def sha(content):
    return hashlib.sha256(content).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def lines(text, face, width):
    result, current = [], ''
    for word in text.split():
        candidate = (current + ' ' + word).strip()
        if current and face.getlength(candidate) > width:
            result.append(current)
            current = word
        else:
            current = candidate
    return result + [current]


def main(font_path):
    manifest = json.loads((REFERENCE / 'manifest.json').read_text(encoding='utf-8'))
    for artifact in manifest['artifacts']:
        if sha((REFERENCE / artifact['file']).read_bytes()) != artifact['sha256']:
            raise ValueError('Referencia T07 modificada: ' + artifact['file'])
    pdf = ROOT.parent / manifest['source']['filename']
    pdf_hash = sha(pdf.read_bytes())
    if pdf_hash != manifest['source']['sha256_before']:
        raise ValueError('El PDF fuente cambió.')
    reader = PdfReader(pdf)
    source_images = {
        'p20_planta': Image.open(REFERENCE / 'planta-nativa.png').convert('RGB'),
        'p20_pagina': Image.open(REFERENCE / 'pagina-20-contexto.png').convert('RGB'),
    }
    source_info = {
        'p20_planta': {'page':20,'object':196,'frame_unit':'px','frame_size':[1536,813], 'raster_factor':1, 'reference':'references/derived/p20-t7/planta-nativa.png'},
        'p20_pagina': {'page':20,'object':None,'frame_unit':'PDF_pt_top_left','frame_size':[960,540], 'raster_factor':3, 'reference':'references/derived/p20-t7/pagina-20-contexto.png'},
    }
    for key, page, object_id in [('p23_obj210',23,210),('p24_obj222',24,222)]:
        embedded = next(im for im in reader.pages[page-1].images if im.indirect_reference.idnum == object_id)
        source_images[key] = embedded.image.convert('RGB')
        source_info[key] = {'page':page,'object':object_id,'frame_unit':'px','frame_size':list(embedded.image.size),'raster_factor':1,
                            'embedded_stream_sha256':sha(embedded.indirect_reference.get_object().get_data()),'reference':'PDF original, imagen embebida'}
    for key, im in source_images.items():
        source_info[key]['decoded_rgb_sha256'] = sha(im.tobytes())

    review_path = DATA / 't09-revision-pdf.json'
    review = json.loads(review_path.read_text(encoding='utf-8'))
    reviewed = [page for group in review['page_groups'] for page in group['pages']]
    if sorted(reviewed) != list(range(1, len(reader.pages)+1)):
        raise ValueError('La revisión no cubre las páginas del PDF exactamente una vez.')
    t08 = json.loads((ROOT/'architecture/classification/t08-clasificacion.json').read_text(encoding='utf-8'))
    known_ids = {item['id'] for item in t08['items']}
    items, ids = [], set()
    with (DATA/'t09-inventario.tsv').open(encoding='utf-8',newline='') as stream:
        for row in csv.DictReader(stream,delimiter='\t'):
            if row['id'] in ids:
                raise ValueError('ID duplicado: '+row['id'])
            ids.add(row['id'])
            box = [float(row[k]) for k in ['x0','y0','x1','y1']]
            source = source_info[row['fuente']]
            w,h = source['frame_size']
            if not (0 <= box[0] < box[2] <= w and 0 <= box[1] < box[3] <= h):
                raise ValueError('Recorte fuera de referencia: '+row['id'])
            if row['confianza_lectura'] not in {'alta','media','baja'}:
                raise ValueError('Confianza desconocida: '+row['id'])
            refs = row['t08_ids'].split(';') if row['t08_ids'] else []
            if not set(refs) <= known_ids:
                raise ValueError('Referencia T08 desconocida: '+row['id'])
            numeric = float(Decimal(row['valor'])) if row['valor'] else None
            unit = row['unidad_visible'] or row['unidad_propuesta'] or None
            unit_status = 'documentada' if row['unidad_visible'] else ('inferida' if unit else 'no_aplica_o_no_legible')
            converted = None
            if numeric is not None and unit in {'cm','mm'}:
                converted = float(Decimal(row['valor']) / (100 if unit=='cm' else 1000))
            if row['tipo']=='codigo' and (numeric is not None or unit is not None):
                raise ValueError('Un código se ha convertido en medida: '+row['id'])
            if row['tipo']=='cota' and unit_status != 'inferida':
                raise ValueError('Se atribuyó una unidad impresa no documentada a la cota: '+row['id'])
            item = {'id':row['id'],'kind':row['tipo'],'source':row['fuente'],'bbox':box,'literal':row['literal'],
                    'value_as_read':numeric,'unit_visible':row['unidad_visible'] or None,'unit_proposed':row['unidad_propuesta'] or None,
                    'unit_status':unit_status,'length_m_if_unit_accepted':converted,'reading_confidence':row['confianza_lectura'],
                    'location':row['ubicacion'],'t08_ids':refs,'use':row['uso'],'note':row['nota'],
                    'reading_crop_transform':{'mirror_horizontal':row['espejo_lectura']=='true','rotate_ccw_degrees':int(row['rotacion_lectura'])},
                    'model_geometry_allowed':False}
            items.append(item)
    OUTPUT.mkdir(parents=True,exist_ok=True)
    data = {'task':'T09','revision':1,'source_pdf_sha256':pdf_hash,'authored_source':'architecture/measurements/t09-inventario.tsv',
            'authored_source_sha256':sha((DATA/'t09-inventario.tsv').read_bytes()),'pdf_review_sha256':sha(review_path.read_bytes()),
            'sources':source_info,'policy':{'coordinates_are_reading_locators':True,'metric_transform':None,'model_geometry_allowed':False,
            'conversion_note':'La conversión numérica es condicional a la unidad y no fija escala ni geometría. Las cotas locales usan cm inferidos; los códigos F no se convierten en longitudes.'},'items':items}
    write_json(DATA/'t09-inventario.json',data)

    title_font, body_font, small_font = [ImageFont.truetype(str(font_path),size) for size in [26,18,15]]
    sheets = [
        ('cotas-y-espesores.png','T09 | Cotas locales y espesores explícitos',{'cota','espesor'}),
        ('codigos-tabiques.png','T09 | Códigos de paños: espesor por documentar',{'codigo'}),
        ('superficies-y-complementos.png','T09 | Superficies declaradas y referencias complementarias',{'superficie','complementaria'}),
    ]
    outputs=[]
    for filename,title,kinds in sheets:
        records=[item for item in items if item['kind'] in kinds]
        cw,ch,margin,header=440,250,24,114
        canvas=Image.new('RGB',(cw*3+margin*2,header+math.ceil(len(records)/3)*ch+margin),'#f4f7fb')
        draw=ImageDraw.Draw(canvas)
        draw.text((margin,20),title,font=title_font,fill='#172535')
        draw.text((margin,60),'Recortes ampliados para leer; no añaden resolución ni fijan una escala métrica.',font=body_font,fill='#43576c')
        draw.text((margin,84),'La confianza es de lectura. El inventario conserva ubicación, fuente y unidad documentada o inferida.',font=small_font,fill='#43576c')
        for i,item in enumerate(records):
            x=margin+(i%3)*cw;y=header+(i//3)*ch
            draw.rounded_rectangle((x,y,x+cw-16,y+ch-16),radius=9,fill='white',outline='#ccd6df')
            draw.text((x+12,y+10),item['id']+' | '+item['reading_confidence'],font=body_font,fill='#075a95')
            for j,line in enumerate(lines(item['location'],small_font,cw-42)[:2]):
                draw.text((x+12,y+39+j*18),line,font=small_font,fill='#43576c')
            factor=source_info[item['source']]['raster_factor']
            box=tuple(round(v*factor) for v in item['bbox'])
            crop=source_images[item['source']].crop(box)
            trans=item['reading_crop_transform']
            if trans['mirror_horizontal']:
                crop=ImageOps.mirror(crop)
            crop=crop.rotate(trans['rotate_ccw_degrees'],expand=True,fillcolor='white')
            scale=min(5,(cw-42)/crop.width,90/crop.height)
            crop=crop.resize((max(1,round(crop.width*scale)),max(1,round(crop.height*scale))),Image.Resampling.NEAREST)
            canvas.paste(crop,(x+12,y+82))
            label=item['literal']
            for j,line in enumerate(lines(label,body_font,cw-42)[:2]):
                draw.text((x+12,y+179+j*20),line,font=body_font,fill='#172535')
            if item['kind']=='complementaria':
                suffix='Referencia genérica; no atribuida al T7'
            elif item['kind']=='codigo':
                suffix='Código de tipo; espesor sin documentar'
            else:
                suffix=(item['unit_visible'] or item['unit_proposed'] or 'sin unidad')+' | '+item['unit_status']
            draw.text((x+12,y+218),suffix,font=small_font,fill='#43576c')
        canvas.save(OUTPUT/filename)
        outputs.append({'file':filename,'records':len(records),'size_px':list(canvas.size),'sha256':sha((OUTPUT/filename).read_bytes())})
    checks={'task':'T09','records':len(items),'unique_ids':len(ids),'kinds':dict(Counter(i['kind'] for i in items)),
            'reading_confidence':dict(Counter(i['reading_confidence'] for i in items)),
            'pdf_pages_reviewed':len(reviewed),'source_pdf_unchanged':True,'t07_references_unchanged':True,
            'all_locators_in_source_bounds':True,'t08_links_valid':True,'all_records_blocked_for_geometry':True,
            'local_dimension_units':'cm inferidos, no confirmados por rótulo general',
            'catalogue_sha256':sha((DATA/'t09-inventario.json').read_bytes()),
            'evidence_font':{'filename':font_path.name,'sha256':sha(font_path.read_bytes())},'evidence_sheets':outputs}
    write_json(OUTPUT/'comprobacion.json',checks)
    print(json.dumps(checks,ensure_ascii=False,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font',type=Path,default=Path('C:/Windows/Fonts/arial.ttf'),help='Fuente TrueType con caracteres españoles y símbolo de diámetro.')
    args=parser.parse_args()
    main(args.font)
