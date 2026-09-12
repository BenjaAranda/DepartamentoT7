"""Import the canonical GLB, tag interactive pivots and configure a playable level."""
import unreal,json,shutil,hashlib,traceback,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'validation/e08';OUT.mkdir(parents=True,exist_ok=True)
try:
    data=json.loads((ROOT/'assets/colliders/departamento-t7.json').read_text(encoding='utf-8'))
    manifest=json.loads((ROOT/'web/public/models/manifest.json').read_text(encoding='utf-8'))
    assert data['revision']==manifest['revision']
    assert hashlib.sha256((ROOT/'assets/interchange/departamento-t7.glb').read_bytes()).hexdigest()==manifest['hashes']['departamento-t7.glb']
    levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem);actors_api=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    if unreal.EditorAssetLibrary.does_asset_exist('/Game/T7/Apartment'):
        # Regenerate only actors owned by this pipeline; preserve unrelated editor work.
        assert levels.load_level('/Game/T7/Apartment')
        owned=[a for a in actors_api.get_all_level_actors() if any(str(t).startswith('revision_') for t in a.tags) or a.get_actor_label() in ['T7_Runtime','Acceso_Visitante'] or isinstance(a,(unreal.PointLight,unreal.SkyLight,unreal.DirectionalLight,unreal.PostProcessVolume))]
        assert actors_api.destroy_actors(owned)
    else:
        assert levels.new_level('/Game/T7/Apartment')
    manager=unreal.InterchangeManager.get_interchange_manager_scripted();options=unreal.ImportAssetParameters();options.is_automated=True;options.replace_existing=True
    assert manager.import_scene('/Game/T7/Model',manager.create_source_data(str(ROOT/'assets/interchange/departamento-t7.glb')),options)
    actors=actors_api.get_all_level_actors();lookup={a.get_actor_label():a for a in actors}
    glb=(ROOT/'assets/interchange/departamento-t7.glb').read_bytes();document=json.loads(glb[20:20+struct.unpack_from('<I',glb,12)[0]])
    inspection_hidden={n['name'] for n in document['nodes'] if n.get('extras',{}).get('inspection_hide')}
    for actor in actors:
        label=actor.get_actor_label();actor.tags=[unreal.Name(label),unreal.Name('revision_'+data['revision'])]
        if label in inspection_hidden:actor.tags=list(actor.tags)+[unreal.Name('inspection_hide')]
        # Configure collisions/mobility in prepare-evidence.py after a saved reopen.
        # Interchange still has pending Chaos updates when this synchronous call returns.
    for door in data['doors']:assert door['pivot_name'] in lookup,door['pivot_name']
    source=json.loads((ROOT/'architecture/model/departamento-t7.json').read_text(encoding='utf-8'))
    checks=[]
    for wall in source['walls']:
        actor=lookup[wall['id']];origin,extent=actor.get_actor_bounds(False);poly=wall['polygon_xy_m']
        expected=[min(p[0] for p in poly)*100,-max(p[1] for p in poly)*100,max(p[0] for p in poly)*100,-min(p[1] for p in poly)*100]
        actual=[origin.x-extent.x,origin.y-extent.y,origin.x+extent.x,origin.y+extent.y]
        error=max(abs(a-b) for a,b in zip(actual,expected));assert error<.1,(wall['id'],error)
        checks.append(dict(id=wall['id'],maximum_error_cm=error))
    runtime=actors_api.spawn_actor_from_class(unreal.T7World,unreal.Vector());runtime.set_actor_label('T7_Runtime')
    x,y,z=data['spawn'];start=actors_api.spawn_actor_from_class(unreal.PlayerStart,unreal.Vector(x*100,z*100,84),unreal.Rotator(0,180,0));start.set_actor_label('Acceso_Visitante')
    for light in data['finishes']['lights']:
        x,y,z=light['position'];actor=actors_api.spawn_actor_from_class(unreal.PointLight,unreal.Vector(x*100,z*100,y*100));actor.set_actor_label('Light_'+light['id'])
        component=actor.point_light_component;component.set_mobility(unreal.ComponentMobility.MOVABLE);component.set_intensity(550);component.set_editor_property('source_radius',12);component.set_attenuation_radius(500);component.set_light_color(unreal.LinearColor(1,.88,.70,1));component.set_cast_shadows(True)
    sky=actors_api.spawn_actor_from_class(unreal.SkyLight,unreal.Vector(0,0,400));sky.light_component.set_mobility(unreal.ComponentMobility.MOVABLE);sky.light_component.set_intensity(.7)
    sun=actors_api.spawn_actor_from_class(unreal.DirectionalLight,unreal.Vector(0,0,1500),unreal.Rotator(-35,-60,0));sun.light_component.set_mobility(unreal.ComponentMobility.MOVABLE);sun.light_component.set_intensity(2)
    # Fixed exposure keeps all evidence comparable.
    pp=actors_api.spawn_actor_from_class(unreal.PostProcessVolume,unreal.Vector());pp.set_editor_property('unbound',True)
    settings=pp.get_editor_property('settings');settings.set_editor_property('override_auto_exposure_min_brightness',True);settings.set_editor_property('override_auto_exposure_max_brightness',True);settings.set_editor_property('auto_exposure_min_brightness',32);settings.set_editor_property('auto_exposure_max_brightness',32);pp.set_editor_property('settings',settings)
    folder=ROOT/'unreal/T7/Content/Data';folder.mkdir(exist_ok=True)
    shutil.copyfile(ROOT/'assets/colliders/departamento-t7.json',folder/'departamento-t7.json')
    shutil.copyfile(ROOT/'validation/e10/walk-check.json',folder/'routes.json')
    shutil.copyfile(ROOT/'validation/e10/wardrobes-open/walk-check.json',folder/'routes-open.json')
    shutil.copyfile(ROOT/'web/public/models/manifest.json',folder/'manifest.json')
    assert levels.save_current_level();unreal.EditorAssetLibrary.save_directory('/Game/T7',only_if_is_dirty=False,recursive=True)
    report=dict(revision=data['revision'],engine=unreal.SystemLibrary.get_engine_version(),model_sha256=manifest['hashes']['departamento-t7.glb'],wall_checks=checks,actors_imported=len(actors),doors=len(data['doors']),colliders=len(data['colliders']),units='cm',map='/Game/T7/Apartment')
    (OUT/'apartment-import.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');unreal.log('T7_APARTMENT_IMPORT_OK')
except Exception:
    (OUT/'apartment-error.txt').write_text(traceback.format_exc(),encoding='utf-8');raise
