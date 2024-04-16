import unreal
import os, sys

from glob import glob
from pprint import pprint
from importlib import reload

RENDER_PATH = "E:/{PROJECT}/sequences/{PROJECT}/{SHOT}/UE/wip/{SHOT}_v{VERSION:03d}"

SHOTS = {
    "room": ["0010", "0020", "0030", "0040", "0050", "0060", "0070"],
    "stage": ["0110", "0120", "0130", "0140", "0150", "0170", "0200", "0202", "0204",
              "0230", "0240", "0250", "0260", "0270", "0280", "0290", "0300", "0310",
              "0320", "0330", "0340", "0350", "0360", "0370", "0380", "0390", "0400",
              "0410", "0420", "0430", "0440", "0450", "0460", "0470", "0480", "0490",
              "0500", "0510", "0520", "0530", "0540", "0550", "0560", "0570", "0580",
              "0590", "0600", "0602", "0604", "0606", "0608", "0610", "0620", "0630",
              "0640", "0650", "0660", "0670", "0680", "0690", "0700", "0710", "0715",
              "0720", "0730", "0735", "0740", "0770", "0780", "0790"],
    "westcoast": ["0010", "0020", "0030", "0040", "0050", "0060", "0065", "0070",
                  "0080", "0090"],
    "library": ["0100", "0110", "0120", "0130", "0140", "0150", "0160", "0170",
                "0180", "0190", "0200", "0210", "0220", "0230", "0240", "0250",
                "0260", "0270", "0280", "0290", "0300", "0310", "0320", "0330",
                "0340", "0350"]                
}

LEVEL = {
    "room": "/Game/Project/Level/Room.Room",
    "stage": "/Game/Project/Level/Stage.Stage",
    "library": "/Game/Project/Level/Library.Library",
    "westcoast": "/Game/Project/Level/westcoast.westcoast"
}

PRESET = {
    "room": "/Game/Project/Common/Render_Setting/SEQ_Render.SEQ_Render",
    "stage": "/Game/Project/Common/Render_Setting/SEQ_Render.SEQ_Render",
    "library": "/Game/Project/Common/Render_Setting/DnF45_Render.DnF45_Render",
    "westcoast": "/Game/Project/Common/Render_Setting/DnF45_Render.DnF45_Render"
}

def movie_queue_render(u_level_file, u_level_seq_file, u_preset_file, seq_name, output_path):

    subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
    queue = subsystem.get_queue()
    executor = unreal.MoviePipelinePIEExecutor()
    
    # config render job with movie pipeline config
    job = queue.allocate_new_job(unreal.MoviePipelineExecutorJob)
    job.job_name = seq_name
    job.map = unreal.SoftObjectPath(u_level_file)
    job.sequence = unreal.SoftObjectPath(u_level_seq_file)

    preset = unreal.EditorAssetLibrary.find_asset_data(u_preset_file).get_asset()
    
    seq_folder = "{sequence_name}"

    for setting in preset.get_user_settings():
        if type(setting) == unreal.MoviePipelineOutputSetting:
            setting.output_directory.set_editor_property("Path", output_path)

    job.set_configuration(preset)
    
    subsystem.render_queue_with_executor_instance(executor)

def execute_render(project, env, version=1):
    shot_list = SHOTS[env]
    level = LEVEL[env]
    render_setting = PRESET[env]
    asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()

    for shot in shot_list:

        shot_code = f"{project}_{shot}"
        asset_folder_path = f"/Game/Project/BP_Ani_Fx_Seq/{project}/{shot_code}"
        assets = asset_reg.get_assets_by_path(asset_folder_path)

        if assets:
            for asset in assets:
                if asset.asset_class_path.asset_name == "LevelSequence":
                    seq_path = f"{asset.package_path}/{asset.asset_name}.{asset.asset_name}"
                    con_project = project.upper()
                    con_shot_code = shot_code.upper()
                    out_path = RENDER_PATH.format(PROJECT=con_project, SHOT=con_shot_code, VERSION=version)                    
                    print(f"excute render {shot_code} at {out_path}")
                    movie_queue_render(level, seq_path, render_setting, asset.asset_name, out_path)



# execute_render("DnF", "stage", 3)
execute_render("DnF45", "library", 3)
print("finish scripts")