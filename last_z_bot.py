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
has_gas = True

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

    # determine which view is being shown
    if "world" in objs and "hero" in objs and "magnifying glass":
    	objs["__current_view"] = "headquarters"
    elif "headquarters" in objs and "hero" in objs and "magnifying glass":
    	objs["__current_view"] = "world"
    elif "label - requirements" in objs and "upgrade" in objs:
    	objs["__current_view"] = "build"
    elif "label - get more" in objs and "replenish all" in objs:
    	objs["__current_view"] = "build"
    elif "label - warehouse" in objs:
    	objs["__current_view"] = "warehouse"
    elif "label - bounty mission" in objs:
    	objs["__current_view"] = "bounty mission"
    elif "label - hospital" in objs:
    	objs["__current_view"] = "hospital"
    elif "last z icon" in objs or "loading" in objs:
    	objs["__current_view"] = "loading"

    print("")
    print(datetime.datetime.now())
    ke = list(objs.keys())
    ke.sort()
    for k in ke:
        print(k, objs[k])

    ctx.pick_strategy(objs)

    """

	elif "attack" in objs:
		print("under attack")
		pygame.mixer.music.load("alarm_sound.mp3") 
		pygame.mixer.music.play(loops=0)		
	elif "medic" in objs:
		print("medic")
		tap_this("medic")
	elif "exit" in objs and len(objs)==1:
		print("objs")
		tap_this("exit")	


	elif state_of_action == None and "complete" in objs:
		print("complete")
		tap_this("complete")
		last_action_timestamp = datetime.datetime.now()
	"""

    """
	elif state_of_action == None and "ready to build" in objs:
		print("ready to build")
		tap_this("ready to build")
		last_action_timestamp = datetime.datetime.now()
	"""

    """
	elif state_of_action == None and "wanted" in objs:
		print("wanted")
		tap_this("wanted")
		last_action_timestamp = datetime.datetime.now()
	"""

    """
	elif state_of_action == None and "radar" in objs:
		print("radar")
		tap_this("radar")
		last_action_timestamp = datetime.datetime.now()
	"""

    """
	elif state_of_action == None and "event calendar" in objs:
		print("event calendar")
		tap_this("event calendar")
		last_action_timestamp = datetime.datetime.now()
	"""

    time.sleep(4)
