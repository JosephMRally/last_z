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

data_loc = "datasets/last_z"
yaml_loc = f"{data_loc}/data.yaml"

save_dir = "/Users/large/Documents/code/python/ultralytics/runs/detect/train/"
model_loc = "yolo11n.pt"  # to start training from scratch
# model_loc = f"{save_dir}/weights/best.pt"


# delete the old model
shutil.rmtree("./runs/detect/train2", ignore_errors=True)

# load up the labels
with open(yaml_loc, 'r') as f:
	label = yaml.safe_load(f)['names']
print(label)

# Load a pretrained YOLO model (recommended for training)
model = YOLO(model_loc)

# Train the model using the dataset for 3 epochs
results = model.train(data=yaml_loc, epochs=1000, imgsz=1024, device="mps")  #, resume=True)
save_dir = str(results.save_dir)
model_loc = f"{save_dir}/weights/best.pt"

# Evaluate the model's performance on the validation set
results = model.val()
print()
print(results)
print(model_loc)


from roboflow import Roboflow
rf = Roboflow()
workspace = rf.workspace("lastz-u33ao")
print(workspace)
print(workspace.project_list)
project = workspace.project("last_z-afohb")
print(project)
version = project.version(6)
#dataset = version.download("yolov11")

project.version(6).deploy(model_type="yolov11", model_path=save_dir)

# roboflow upload_model -w lastz -p custom-object-detector-yolo11 -t yolov11 -n my-model-v1 -m ./runs/detect/train19
#workspace.deploy_model(project.
#    model_type="yolov11",  # Type of the model
#    model_path=save_dir,  # Path to model directory
#    project_ids=["custom-object-detector-yolo11"],  # List of project IDs
#    model_name=datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S_%f"),  # Name for the model (must have at least 1 letter, and accept numbers and dashes)
#    filename="weights/best.pt"  # Path to weights file (default)
#)
