"""
Copyright: (c) 2025 by Joseph Miguel<br/>
           NO WARRANTY, EXPRESS OR IMPLIED. AS-IS.  USE AT-YOUR-OWN-RISK.

           LICENSE TO USE - FREE with one condition:
           GIVE ME SOME CREDIT IF YOU USE IT TO PLAY THE GAME
           139 - T A C O    418 - BORG QUEEN 001
"""

# import redis
import datetime
import time
from collections import defaultdict

import cv2
import pygame

import last_z.cmd_for_adb as common
from last_z.strategyContext import StrategyContext
from ultralytics import YOLO

pygame.init()

# find the most recent model
save_dir = common.find_most_recent_model_directory()
model_loc = f"{save_dir}/weights/best.pt"
print(save_dir)

# load model
model = YOLO(model_loc)

# show all devices
print(common.get_device_list())

# setup config values
device_id = "R9YT200S1PM"
debug = False
# has_gas = True

# strategy design pattern
ctx = StrategyContext()

# infinite loop
while True:
    # first take a screenshot
    path_and_filename = common.get_screenshot(device_id, "screenshots/screenshot.png")

    # resize
    img = cv2.imread(path_and_filename)
    img_2 = cv2.resize(img, (1024, 1024))  # YOLO default image size is 640
    cv2.imwrite(path_and_filename, img_2)

    # Perform object detection on an image using the model
    results = model.predict(path_and_filename, show=debug, show_boxes=True, verbose=False, imgsz=1024, conf=0.80)

    # extract the results
    objs = defaultdict(list)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy.tolist()
            b = [[int(a) for a in x] for x in b]  # xyxy convert to int
            c = int(box.cls)
            c_name = model.names[c]
            objs[c_name].append(b)
    objs = dict(objs)
    objs["_settings.device_id"] = device_id
    objs["_timestamp"] = datetime.datetime.now()

    ctx.pick_strategy(objs)

    with open("log.txt", "a") as f:
        print("")
        f.write("\n\n")
        print(datetime.datetime.now())
        ke = list(objs.keys())
        ke.sort()
        for k in ke:
            print(k, objs[k])
            f.write(f"{k}: {objs[k]}\n")

        time.sleep(4)
