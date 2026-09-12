"""Verify a disposable changed revision inside a separate Unreal project."""
import unreal,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];PROBE=ROOT/'work/roundtrip-probe'
baseline=json.loads((PROBE/'baseline.json').read_text())
data=json.loads((PROBE/'assets/colliders/departamento-t7.json').read_text())
levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem);assert levels.new_level('/Game/Probe')
manager=unreal.InterchangeManager.get_interchange_manager_scripted();options=unreal.ImportAssetParameters();options.is_automated=True
assert manager.import_scene('/Game/ProbeModel',manager.create_source_data(str(PROBE/'assets/interchange/departamento-t7.glb')),options)
actor=next(a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors() if a.get_actor_label()=='W01B')
center,extent=actor.get_actor_bounds(False)
collider=next(c for c in data['colliders'] if c['id']=='W01B')
old_center=sum(p[0] for p in baseline['wall_before'])/len(baseline['wall_before'])
assert abs(center.x/100-collider['center'][0])<1e-5
assert abs(collider['center'][0]-old_center-.01)<1e-8
for path,digest in baseline['protected_hashes'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
web=json.loads((PROBE/'validation/e09/web-glb-check.json').read_text())
assert web['revision']==data['revision'] and web['all_hashes_match']
report=dict(probe_revision=data['revision'],production_unchanged=True,controlled_wall='W01B',expected_delta_m=.01,collider_delta_m=collider['center'][0]-old_center,unreal_delta_cm=center.x-old_center*100,unreal_vs_collider_error_cm=abs(center.x-collider['center'][0]*100),web_meshes_checked=web['compressed_meshes'],web_pivots_checked=web['pivots_preserved'],scope='Isolated full Blender build, compressed GLB loader/bounds validation and actual Unreal import; production files unchanged.')
(ROOT/'validation/e09/revision-probe.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
unreal.log('T7_REVISION_PROBE_OK')
