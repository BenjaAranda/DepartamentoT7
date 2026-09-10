"""Run inside Unreal Editor 5.8; imports the unchanged metric GLB fixture."""
import unreal, json, traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
out=ROOT/'validation/e08';out.mkdir(parents=True,exist_ok=True)
try:
    levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    assert levels.new_level('/Game/Validation/MetricProof')
    manager=unreal.InterchangeManager.get_interchange_manager_scripted()
    source=manager.create_source_data(str(ROOT/'assets/interchange/t7-prueba.glb'))
    options=unreal.ImportAssetParameters();options.is_automated=True
    assert manager.import_scene('/Game/Validation/Proof',source,options)
    actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
    results=[]
    for actor in actors:
        origin,extent=actor.get_actor_bounds(False)
        results.append(dict(label=actor.get_actor_label(),class_name=actor.get_class().get_name(),location=list(actor.get_actor_location().to_tuple()),bounds_origin=list(origin.to_tuple()),bounds_extent=list(extent.to_tuple())))
    assert levels.save_current_level()
    unreal.EditorAssetLibrary.save_directory('/Game/Validation',only_if_is_dirty=False,recursive=True)
    (out/'proof-import.json').write_text(json.dumps(dict(engine=unreal.SystemLibrary.get_engine_version(),actors=results),indent=2)+'\n',encoding='utf-8')
    unreal.log('T7_PROOF_IMPORT_OK')
except Exception:
    (out/'proof-error.txt').write_text(traceback.format_exc(),encoding='utf-8');raise
