"""Prepare an isolated 10 mm wall edit without changing production assets."""
from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1]
PROBE=ROOT/'work/roundtrip-probe'
copies=['architecture/model/departamento-t7.json','architecture/furniture/layout.json','architecture/calibration/t10-calibracion.json','blender/scripts/build-apartment.py','blender/scripts/furnish.py','blender/scripts/finish.py']
for name in copies:
    destination=PROBE/name;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,destination)
source=json.loads((PROBE/copies[0]).read_text(encoding='utf-8'))
wall=next(w for w in source['walls'] if w['id']=='W01B')
before=[p[:] for p in wall['polygon_xy_m']]
for p in wall['polygon_xy_m']:p[0]+=.01
source['validation_probe']={'wall':'W01B','delta_x_m':.01,'production':False}
source['revision']=hashlib.sha256(json.dumps(source,sort_keys=True).encode()).hexdigest()
(PROBE/copies[0]).write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
project=PROBE/'unreal';project.mkdir(exist_ok=True)
(project/'T7Probe.uproject').write_text(json.dumps({'FileVersion':3,'EngineAssociation':'5.8','Plugins':[{'Name':n,'Enabled':True} for n in ['PythonScriptPlugin','EditorScriptingUtilities','Interchange','InterchangeEditor','InterchangeAssets']]},indent=2)+'\n',encoding='utf-8')
(PROBE/'validation/e09').mkdir(parents=True,exist_ok=True)
protected=['architecture/model/departamento-t7.json','blender/DepartamentoT7.blend','assets/interchange/departamento-t7.glb','assets/colliders/departamento-t7.json','web/public/models/manifest.json','web/public/models/departamento-t7-web.glb']
baseline={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in protected}
(PROBE/'baseline.json').write_text(json.dumps({'protected_hashes':baseline,'wall_before':before,'delta_x_m':.01},indent=2)+'\n',encoding='utf-8')
print('Isolated probe ready:',PROBE)
