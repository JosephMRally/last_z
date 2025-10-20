"""
Copyright: (c) 2025 by Joseph Miguel<br/>
           NO WARRANTY, EXPRESS OR IMPLIED. AS-IS.  USE AT-YOUR-OWN-RISK.

           LICENCE TO USE - FREE with one condition:
           GIVE ME SOME CREDIT IF YOU USE IT TO PLAY THE GAME
           139 - T A C O    418 - BORG QUEEN 001 
"""
from ultralytics import YOLO
import yaml
import datetime
import os
import shutil
from roboflow import Roboflow

data_loc = "datasets/last_z"
yaml_loc = f"{data_loc}/data.yaml"

# what pre-trained model should be continue training from
# adding/changing classes could require making a new model
save_dir = common.find_most_recent_model_directory()
# model_loc = "yolo11n.pt"  # to start training from scratch
model_loc = f"{save_dir}/weights/best.pt"

# https://roboflow.github.io/roboflow-python/core/project/#roboflow.core.project.Project.list_versions
rf = Roboflow()
workspace = rf.workspace("lastz-u33ao")
project = workspace.project("last_z-afohb")
project_versions = project.get_version_information()
project_versions = {x['id']: x for x in project_versions}
project_versions = {k.split("/")[-1]: v for k,v in project_versions.items()}
print(project_versions)
# latest_version = max(project_versions.keys())
# version = project.version(latest_version)
# project.version(latest_version).deploy(model_type="yolov11", model_path=save_dir)
model_name=datetime.datetime.now().strftime("z--%Y-%m-%d--%H-%M-%S")
workspace.deploy_model(model_type="yolov11", model_path=save_dir, model_name=model_name, project_ids=["last_z-afohb"])
