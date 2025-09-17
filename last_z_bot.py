from ultralytics import YOLO
import yaml
import time
from cmd_for_adb import *
import cv2
import subprocess
from ultralytics.utils.plotting import Annotator
import numpy as np
from collections import defaultdict
import redis
import json
import datetime

data_loc = "datasets/last_z"
yaml_loc = f"{data_loc}/data.yaml"

save_dir = "/Users/large/Documents/code/python/ultralytics/runs/detect/train3"
model_loc = f"{save_dir}/weights/best.pt"

# load model
model = YOLO(model_loc)

# show all devices
print(get_device_list())

device_id = "R9YT200S1PM"
debug = False
help_others_counter = 0
boomer_counter = 0
state_of_action = None
state_of_action_start_time = None
middle_of_xyxy = lambda xyxy : (xyxy[0]+(xyxy[2]-xyxy[0])/2, xyxy[1]+(xyxy[3]-xyxy[1])/2)
translate_to_display = lambda x,y: (1200/1024*x, 1920/1024*y)


while True:
	# first take a screenshot
	path_and_filename = get_screenshot(device_id, "screenshots/screenshot.png")

	# resize
	img = cv2.imread(path_and_filename)
	img_2 = cv2.resize(img, (1024, 1024)) # YOLO default image size is 640
	cv2.imwrite(path_and_filename, img_2)

	# Perform object detection on an image using the model
	results = model.predict(path_and_filename, 
		show=debug, show_boxes=True, verbose=False, 
		imgsz=1024, conf=0.20)

	# extract the results
	objs = defaultdict(list)
	for r in results:
		boxes = r.boxes
		for box in boxes:
			b = box.xyxy.tolist()
			c = int(box.cls)
			c_name = model.names[c]
			objs[c_name].append(b)
	objs = dict(objs)


	# print(objs)
	# r = redis.Redis()
	# r.set("vision", json.dumps(dict(objs)))

	if debug:
		print("")
		print(json.dumps(dict(objs)))

	if state_of_action != None and state_of_action_start_time+datetime.timedelta(minutes = 3) < datetime.datetime.now():
		# reset state if something went wrong
		print("reset", str(datetime.datetime.now()))
		state_of_action = None
		state_of_action_start_time = None

	elif state_of_action == None and "help others" in objs:
		print("help others")
		help_others = objs["help others"]
		help_others = help_others[0][0]
		x,y = middle_of_xyxy(help_others)
		x,y = translate_to_display(x,y)
		tap("R9YT200S1PM", x,y)
		help_others_counter += 1
		print(help_others_counter, str(datetime.datetime.now()))

	elif state_of_action == None and "headquarters" in objs and "hero 1 sleeping" in objs and "magnifying glass" in objs:
		print("starting boomer")
		magnifying_glass = objs["magnifying glass"]
		magnifying_glass = magnifying_glass[0][0]
		x,y = middle_of_xyxy(magnifying_glass)
		x,y = translate_to_display(x,y)
		state_of_action = "boomer"
		tap("R9YT200S1PM", x,y)
		state_of_action_start_time = datetime.datetime.now()
	elif state_of_action == "boomer" and "boomer selected" in objs:
		print("boomer selected: ", end="")
		boomer_selected = objs["boomer selected"]
		boomer_selected = boomer_selected[0][0]
		x,y = middle_of_xyxy(boomer_selected)
		x,y = translate_to_display(x,y)
		state_of_action_start_time = datetime.datetime.now()
		state_of_action = "boomer selected"
		tap("R9YT200S1PM", x,y)
	elif (state_of_action == "boomer" or state_of_action == "boomer selected") and "search" in objs:
		print("boomer search: ", end="")
		search = objs["search"]
		search = search[0][0]
		x,y = middle_of_xyxy(search)
		x,y = translate_to_display(x,y)
		state_of_action = "boomer search"
		state_of_action_start_time = datetime.datetime.now()
		tap("R9YT200S1PM", x,y)
	elif state_of_action == "boomer search" and "team up" in objs:
		print("boomer team up: ", end="")
		team_up = objs["team up"]
		team_up = team_up[0][0]
		x,y = middle_of_xyxy(team_up)
		x,y = translate_to_display(x,y)
		state_of_action = "boomer team up"
		state_of_action_start_time = datetime.datetime.now()
		tap("R9YT200S1PM", x,y)
	elif state_of_action == "boomer team up" and "march" in objs:
		print("boomer march: ", end="")
		march = objs["march"]
		march = march[0][0]
		x,y = middle_of_xyxy(march)
		x,y = translate_to_display(x,y)
		tap("R9YT200S1PM", x,y)
		state_of_action = "boomer marching"
		state_of_action_start_time = datetime.datetime.now()
		boomer_counter += 1
	elif state_of_action == "boomer marching" and "hero 1 sleeping" in objs:
		print("boomer completed")
		state_of_action = None
		state_of_action_start_time = None

	time.sleep(2)


