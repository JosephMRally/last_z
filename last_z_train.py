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
import last_z.cmd_for_adb as common
import time
import subprocess

data_loc = "datasets/last_z"
yaml_loc = f"{data_loc}/data.yaml"

# what pre-trained model should be continue training from
# adding/changing classes could require making a new model
save_dir = common.find_most_recent_model_directory()
if not save_dir:
    model_loc = "yolo11n.pt"  # to start training from scratch
else:
    model_loc = f"{save_dir}/weights/best.pt"
print(f"loading model at: {model_loc}")

# download latest version
cmd = [f"python last_z_download_dataset.py"]
process = subprocess.Popen(cmd, shell=True)
process.wait()

# load up the labels
with open(yaml_loc, 'r') as f:
	label = yaml.safe_load(f)['names']
print(label)

# Load a pretrained YOLO model (recommended for training)
model = YOLO(model_loc)

# Train the model using the dataset for 3 epochs
count=0
while True:
    try:
        results = model.train(data=yaml_loc, epochs=10000, imgsz=1024, device="mps", patience=100)
        save_dir = str(results.save_dir)
        model_loc = f"{save_dir}/weights/best.pt"
        exit(0)
    except:
        count += 1
        print(f"sleeping. # of retries: {count}")
        time.sleep(60)
        pass

# Evaluate the model's performance on the validation set
# results = model.val()
# print()
# print(results)
# print(model_loc)





# from roboflow import Roboflow
# rf = Roboflow()
# workspace = rf.workspace("lastz-u33ao")
# print(workspace)
# print(workspace.project_list)
# project = workspace.project("last_z-afohb")
# print(project)
# version = project.version(6)
# dataset = version.download("yolov11")

# project.version(6).deploy(model_type="yolov11", model_path=save_dir)

# roboflow upload_model -w lastz -p custom-object-detector-yolo11 -t yolov11 -n my-model-v1 -m ./runs/detect/train19
#workspace.deploy_model(project.
#    model_type="yolov11",  # Type of the model
#    model_path=save_dir,  # Path to model directory
#    project_ids=["custom-object-detector-yolo11"],  # List of project IDs
#    model_name=datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S_%f"),  # Name for the model (must have at least 1 letter, and accept numbers and dashes)
#    filename="weights/best.pt"  # Path to weights file (default)
#)
