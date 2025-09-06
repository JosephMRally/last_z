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

data_loc = "datasets/last_z"
yaml_loc = f"{data_loc}/data.yaml"

save_dir = "/Users/large/Documents/code/python/ultralytics/runs/detect/train39"
model_loc = f"{save_dir}/weights/best.pt"

# load model
model = YOLO(model_loc)

# show all devices
print(get_device_list())

device_id = "R9YT200S1PM"

while True:
	# first take a screenshot
	path_and_filename = get_screenshot(device_id)

	# resize
	img = cv2.imread(path_and_filename)
	img_2 = cv2.resize(img, (640, 640)) # YOLO default image size is 640
	cv2.imwrite(path_and_filename, img_2)

	# Perform object detection on an image using the model
	results = model.predict(path_and_filename, 
		show=False, show_boxes=True, verbose=False, 
		imgsz=640, conf=0.01)

	# clear the terminal
	# cmd = [f"clear"]
	# process = subprocess.Popen(cmd, shell=True)
	# process.wait()

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

	if "help others" in objs:
		help_others = objs["help others"]
		help_others = help_others[0][0]
		x,y = help_others[0]+(help_others[2]-help_others[0]), help_others[1]+(help_others[3]-help_others[1])
		x = 1200/640*x
		y = 1900/640*y
		print(help_others)
		tap("R9YT200S1PM", x,y)

	time.sleep(60*5)


