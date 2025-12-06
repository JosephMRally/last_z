"""
Copyright: (c) 2025 by Joseph Miguel<br/>
           NO WARRANTY, EXPRESS OR IMPLIED. AS-IS.  USE AT-YOUR-OWN-RISK.

           LICENSE TO USE - FREE with one condition:
           GIVE ME SOME CREDIT IF YOU USE IT TO PLAY THE GAME
           139 - T A C O    418 - BORG QUEEN 001
"""

import subprocess
import time
import os
import yaml
import multiprocessing as mp

import last_z.cmd_for_adb as common
from ultralytics import YOLO

def train_model(model, params, save_dir):
    results = model.train(**params)
    save_dir = str(results.save_dir)
    model_loc = f"{save_dir}/weights/best.pt"

if __name__ == '__main__':
    data_loc = "datasets/last_z"
    yaml_loc = f"{data_loc}/data.yaml"

    # what pre-trained model should be continue training from
    # adding/changing classes could require making a new model

    # download latest version
    cmd = ["python last_z_download_dataset.py"]
    process = subprocess.Popen(cmd, shell=True)
    process.wait()

    # Train the model using the dataset for n epochs
    count = 0
    max_duration = 60*60*4
    while True:
        try:
            save_dir = common.find_most_recent_model_directory()
        except:
            save_dir = None

        if not save_dir:
            save_dir = "./runs/detect/train"
            model_loc = "yolo11n.pt"  # to start training from scratch
            model = YOLO(model_loc)
            resume = False
            save_dir = None
        else:
            save_dir = "./runs/detect/train"
            model_loc = f"{save_dir}/weights/last.pt"
            model = YOLO(model_loc)
            resume = True

        try:
            params = {
                "data":yaml_loc, "epochs":2000, "imgsz":1024, "device":"mps", 
                "patience":200, "project":save_dir, "dropout":0.1, "batch":-1,
                "resume": resume
            }

            process = mp.Process(target=train_model, args=(model, params, save_dir))
            process.start()
            process.join(timeout=max_duration)

            if process.exitcode != 0:
                print(f"Worker process failed with exit code {process.exitcode}")
                raise RuntimeError(f"Worker process failed (exitcode {process.exitcode})")

            if process.is_alive():
                process.terminate()
                process.join()
                print('took too long')        

            exit(0)
        except Exception as e:
            count += 1
            print(e)
            print(f"sleeping. # of retries: {count}")

            time.sleep(10)
            pass



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
    # workspace.deploy_model(project.
    #    model_type="yolov11",  # Type of the model
    #    model_path=save_dir,  # Path to model directory
    #    project_ids=["custom-object-detector-yolo11"],  # List of project IDs
    #    model_name=datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S_%f"),  # Name for the model (must have at least 1 letter, and accept numbers and dashes)
    #    filename="weights/best.pt"  # Path to weights file (default)
    # )
