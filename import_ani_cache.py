import unreal
import os, sys

from glob import glob

PATH = "P:/DNF45/temp/test_abc"
UNREAL_PATH = "/Game/ani/ImportTest"

def _get_alembic_import_options(frame_start = -1, frame_end = -1):
    options = unreal.AbcImportSettings()
    # options.up_aixs = unreal.AlembicImportUp
    options.import_type = unreal.AlembicImportType.SKELETAL

    # options.sampling_settings.frame_start = frame_start
    # options.sampling_settings.frame_end = frame_end

    # Debug output.
    print(options.compression_settings)
    print(options.conversion_settings)
    print(options.geometry_cache_settings)
    print(options.material_settings)
    print(options.normal_generation_settings)
    print(options.sampling_settings)
    print(options.static_mesh_settings)

    return options

def import_alembic(abc_path, asset_path, asset_name, start=1, end=120):
    # Create an import task.
    import_task = unreal.AssetImportTask()

    # Set base properties on the task.
    import_task.filename = abc_path

    import_task.destination_path = asset_path
    import_task.destination_name = asset_name
    import_task.automated = True # Suppress UI.
    import_task.options = _get_alembic_import_options(frame_start = 1, frame_end = 120)
    

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_tools.import_asset_tasks([import_task])
    imported_asset = import_task.get_editor_property('imported_object_paths')

    if not imported_asset:
        unreal.log_warning('No assets were imported.')

# import_alembic("E:/Temp/testA.abc", "/Game/ani/ImportTest", "TestSphereA")
# import_alembic("E:/Temp/testB.abc", "/Game/ani/ImportTest", "TestSphereB")
# import_alembic("E:/Temp/testC.abc", "/Game/ani/ImportTest", "TestSphereC")




tars = [i.replace("\\", "/") for i in glob(f"{PATH}/*.txt") if "empty" not in i]

for tar in tars:

    file, _ext = os.path.splitext(tar)

    shot, s_f, e_f = file.split("_")[-3:]

    cache_file = f"{PATH}/DNF45_{shot}.abc"

    import_alembic(cache_file, UNREAL_PATH, f"{shot}_Book")

