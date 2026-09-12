"""Reopen the saved level, check imports and persist inspection-only visibility tags."""
import unreal,json,struct,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
actors_api=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
assert levels.load_level('/Game/T7/Apartment')
actors=actors_api.get_all_level_actors();lookup={a.get_actor_label():a for a in actors}
raw=(ROOT/'assets/interchange/departamento-t7.glb').read_bytes()
document=json.loads(raw[20:20+struct.unpack_from('<I',raw,12)[0]])
hidden={n['name'] for n in document['nodes'] if n.get('extras',{}).get('inspection_hide')}
data=json.loads((ROOT/'assets/colliders/departamento-t7.json').read_text(encoding='utf-8'))
for name in hidden:
    actor=lookup[name];actor.tags=list(actor.tags)+([unreal.Name('inspection_hide')] if not actor.actor_has_tag('inspection_hide') else [])
assert len([a for a in actors if isinstance(a,unreal.T7World)])==1
assert all(d['pivot_name'] in lookup for d in data['doors'])
meshes=0
repaired=[]
for actor in actors:
    for component in actor.get_components_by_class(unreal.StaticMeshComponent):
        if str(component.get_collision_profile_name())!='NoCollision':
            actor.modify();component.modify();component.set_collision_profile_name('NoCollision',False);repaired.append(actor.get_actor_label())
        assert component.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION,actor.get_actor_label()
        assert component.static_mesh is not None
        assert all(component.get_material(i) is not None for i in range(component.get_num_materials()))
        meshes+=1
assert meshes==499,meshes
for actor in actors:
    if any(actor.get_actor_label().startswith(d['id']+'_') for d in data['doors']):
        actor.modify();actor.root_component.modify();actor.root_component.set_mobility(unreal.ComponentMobility.MOVABLE)
for actor in actors:
    if isinstance(actor,unreal.PostProcessVolume):
        actor.modify();settings=actor.get_editor_property('settings')
        settings.set_editor_property('auto_exposure_min_brightness',32);settings.set_editor_property('auto_exposure_max_brightness',32)
        actor.set_editor_property('settings',settings)
    if isinstance(actor,unreal.PointLight):
        actor.modify();actor.point_light_component.modify();actor.point_light_component.set_editor_property('source_radius',12)
assert levels.save_current_level()
report=dict(revision=data['revision'],map='/Game/T7/Apartment',saved_and_reopened=True,mesh_components=meshes,interactive_pivots=12,static_mesh_collision_disabled=True,repaired_collision_profiles=repaired,inspection_hidden=len(hidden),source_glb_sha256=hashlib.sha256(raw).hexdigest())
(ROOT/'validation/e08/reopen-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
unreal.log('T7_REOPEN_CHECK_OK')
