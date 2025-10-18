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

data_loc = "datasets/last_z"
yaml_loc = f"{data_loc}/data.yaml"

save_dir = "/Users/large/Documents/code/python/ultralytics/runs/detect/"
model_loc = f"{save_dir}/weights/best.pt"
model_loc = "yolo11n.pt"

# https://roboflow.github.io/roboflow-python/core/project/#roboflow.core.project.Project.list_versions
from roboflow import Roboflow
rf = Roboflow()
workspace = rf.workspace("lastz-u33ao")
project = workspace.project("last_z-afohb")
project_versions = project.get_version_information()
project_versions = {x['id']: x for x in project_versions}
project_versions = {k.split("/")[-1]: v for k,v in project_versions.items()}
latest_version = max(project_versions.keys())
print(latest_version)
version = project.version(latest_version)
dataset = version.download("yolov11")
