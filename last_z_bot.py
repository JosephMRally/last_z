"""
Copyright: (c) 2025 by Joseph Miguel
           NO WARRANTY, EXPRESS OR IMPLIED.  USE AT-YOUR-OWN-RISK.
           LICENCE, GIVE ME SOME CREDIT IF YOU USE IT PLAYING THE GAME
           T A C O - BORG QUEEN 001 
"""
from ultralytics import YOLO
import yaml
import time
import cmd_for_adb as common
import cv2
import subprocess
from ultralytics.utils.plotting import Annotator
import numpy as np
from collections import defaultdict
import redis
import json
import datetime
import random

data_loc = "datasets/last_z"
yaml_loc = f"{data_loc}/data.yaml"

save_dir = "/Users/large/Documents/code/python/ultralytics/runs/detect/train2"
model_loc = f"{save_dir}/weights/best.pt"

# load model
model = YOLO(model_loc)

# show all devices
print(common.get_device_list())

debug = False
device_id = "R9YT200S1PM"
help_others_counter = 0
boomer_counter = 0
state_of_action = None
last_action_timestamp = datetime.datetime.now()
middle_of_xyxy = lambda xyxy : (xyxy[0]+(xyxy[2]-xyxy[0])/2, xyxy[1]+(xyxy[3]-xyxy[1])/2)
translate_to_display = lambda x,y: (1200/1024*x, 1920/1024*y)
device_id = "R9YT200S1PM"
has_gas = True

def tap_this(obj_dict_entry):
	a = objs[obj_dict_entry]
	a = a[0][0]
	x,y = middle_of_xyxy(a)
	x,y = translate_to_display(x,y)
	common.tap(device_id, x,y)

while True:
	# first take a screenshot
	path_and_filename = common.get_screenshot(device_id, "screenshots/screenshot.png")

	# resize
	img = cv2.imread(path_and_filename)
	img_2 = cv2.resize(img, (1024, 1024)) # YOLO default image size is 640
	cv2.imwrite(path_and_filename, img_2)

	# Perform object detection on an image using the model
	results = model.predict(path_and_filename, 
		show=debug, show_boxes=True, verbose=False, 
		imgsz=1024, conf=0.50)

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


	print(objs)
	# r = redis.Redis()
	# r.set("vision", json.dumps(dict(objs)))

	if debug:
		print("")
		print(datetime.datetime.now(), state_of_action)
		#x = json.dumps(dict(objs))
		for k in objs.items():
			print(k)

	if has_gas and last_action_timestamp+datetime.timedelta(minutes = 3) < datetime.datetime.now():
		# reset state if something went wrong
		print("reset", str(datetime.datetime.now()))
		state_of_action = None
		last_action_timestamp = datetime.datetime.now()
		common.kill(device_id)

	elif state_of_action == None and "help others" in objs:
		print("help others")
		tap_this("help others")
		help_others_counter += 1
		last_action_timestamp = datetime.datetime.now()
		print("help others", help_others_counter, str(datetime.datetime.now()))

	elif "last z icon" in objs:
		tap_this("last z icon")
	elif "loading" in objs and state_of_action != "loading":
		print("loading")
		last_action_timestamp = datetime.datetime.now()
		state_of_action = "loading"
	elif state_of_action == "loading" and "exit" in objs:
		tap_this("exit")
	elif state_of_action == "loading" and "world" in objs:
		tap_this("world")
		state_of_action = None

	elif has_gas and state_of_action == None and "headquarters" in objs and "hero 1 sleeping" in objs and "magnifying glass" in objs:
		print("boomer starting")
		last_action_timestamp = datetime.datetime.now()
		tap_this("magnifying glass")
		state_of_action = "boomer starting"
	elif state_of_action != None and state_of_action.startswith("boomer"):
		if "boomer selected" in objs:
			print("boomer selected: ", end="")
			tap_this("boomer selected")
			state_of_action = "boomer selected"
		elif "search" in objs:
			print("boomer search: ", end="")
			tap_this("search")
			state_of_action = "boomer search"
		elif "team up" in objs:
			print("boomer team up: ", end="")
			tap_this("team up")
			state_of_action = "boomer team up"
		elif "march" in objs:
			print("boomer march: ", end="")
			tap_this("march")
			state_of_action = "boomer marching"
			boomer_counter += 1
		elif "no gas" in objs:
			print("no gas")
			has_gas = False
			state_of_action = None
		elif "hero 1 sleeping" in objs:
			print("boomer completed")
			last_action_timestamp = datetime.datetime.now()
			state_of_action = None
	elif not has_gas and "headquarters" not in objs:
		objs["corner"] = [[[0, 0, 0, 0]]]
		tap_this("corner")

	#time.sleep(2 + random.randrange(0, 100)/10)
	time.sleep(4)

