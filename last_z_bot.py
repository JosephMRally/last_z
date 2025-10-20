"""
Copyright: (c) 2025 by Joseph Miguel<br/>
           NO WARRANTY, EXPRESS OR IMPLIED. AS-IS.  USE AT-YOUR-OWN-RISK.

           LICENCE TO USE - FREE with one condition:
           GIVE ME SOME CREDIT IF YOU USE IT TO PLAY THE GAME
           139 - T A C O    418 - BORG QUEEN 001 
"""
from abc import ABC, abstractmethod
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
import pygame
import os

class StrategyContext:

	def __init__(self):
		self.strategy = None
		self.last_action_timestamp = datetime.datetime.now()

	def pick_strategy(self, objs):
		if self.last_action_timestamp+datetime.timedelta(minutes = 10) < datetime.datetime.now():
			# reset state, something went wrong
			print("reset", str(datetime.datetime.now()))
			state_of_action = None
			self.last_action_timestamp = datetime.datetime.now()
			common.kill(device_id)
			self.strategy = None
			return

		if self.strategy == None:
			if LoadingStrategy.isReady(objs):
				self.strategy = LoadingStrategy()
			elif CompleteStrategy.isReady(objs):
				self.strategy = CompleteStrategy()
			elif HelpOthersStrategy.isReady(objs):
				self.strategy = HelpOthersStrategy()
			#elif BoomerStrategy.isReady(objs):
			#	self.strategy = BoomerStrategy()
			elif BuildStrategy.isReady(objs):
				self.strategy = BuildStrategy()

		if self.strategy != None:
			self.strategy.perform(objs)
			self.last_action_timestamp = datetime.datetime.now()
			if self.strategy.isComplete(objs):
				self.strategy = None

class SortingStrategy(ABC):
	@abstractmethod
	def isReady(self, objs):
		pass
	@abstractmethod
	def perform(self, objs):
		pass
	@abstractmethod
	def isComplete(self, objs):
		pass

class LoadingStrategy(ABC):
	def isReady(objs):
		return "loading" in objs or "last z icon" in objs

	def perform(self, objs):
		if "last z icon" in objs:
			print("last z icon")
			time.sleep(60 * 5)
			tap_this("last z icon")
		elif "loading" in objs:
			print("loading")
			self.complete = False
		elif "exit" in objs:
			tap_this("exit")
		elif "world" in objs:
			tap_this("world")
			self.complete = True

	def isComplete(self, objs):
		return 	self.complete

class CompleteStrategy(ABC):
	def isReady(objs):
		return "complete" in objs

	def perform(self, objs):
		print("complete")
		tap_this("complete")

	def isComplete(self, objs):
		return True

class HelpOthersStrategy(ABC):
	help_others_counter = 0

	def isReady(objs):
		return "help others" in objs

	def perform(self, objs):
		print("help others")
		tap_this("help others")
		HelpOthersStrategy.help_others_counter += 1
		print(f"help others {HelpOthersStrategy.help_others_counter} times")

	def isComplete(self, objs):
		return True

class BoomerStrategy(ABC):
	boomer_count = 0
	next_allowed_boomer_timestamp = datetime.datetime.now()

	def isReady(objs):
		# reset boomers if we have done to many
		if BoomerStrategy.boomer_count == 10:
			BoomerStrategy.next_allowed_boomer_timestamp = datetime.datetime.now() + datetime.timedelta(minutes = 1)
			boomer_count = 0
			return False

		return (BoomerStrategy.next_allowed_boomer_timestamp < datetime.datetime.now()
			and "headquarters" in objs 
			and "hero 1 sleeping" in objs 
			and "magnifying glass" in objs)

	def perform(self, objs):
		if "headquarters" in objs and "hero 1 sleeping" in objs and "magnifying glass" in objs:
			print("boomer starting")
			last_action_timestamp = datetime.datetime.now()
			tap_this("magnifying glass")
			state_of_action = "boomer starting"
		elif "boomer selected" in objs:
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

	def isComplete(self, objs):
		return False

class BuildStrategy(ABC):
	build_counter = 0

	def isReady(objs):
		return "ready to build" in objs

	def perform(self, objs):
		print("ready to build")
		if "ready to build" in objs and not hasattr(self, "state"):
			tap_this("ready to build")
			self.state = "ready to build"
		elif "upgrade" in objs and self.state == "ready to build":
			tap_this("upgrade")
			self.state = "upgrade"
		elif "go" in objs and self.state == "upgrade":
			tap_this("go")
			self.state = "complete"

	def isComplete(self, objs):
		return self.state == "complete"






pygame.init()

data_loc = "datasets/last_z"
yaml_loc = f"{data_loc}/data.yaml"

def find_directories_os(path):
    directories = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            directories.append(item)
    return directories
d = find_directories_os("./runs/detect/")
d = [int(x[5:]) for x in d if len(x)>5 and x.startswith("train")]
save_dir = f"./runs/detect/train{max(d)}"
model_loc = f"{save_dir}/weights/best.pt"

# load model
model = YOLO(model_loc)

# show all devices
print(common.get_device_list())

# load up the labels
with open(yaml_loc, 'r') as f:
	label = yaml.safe_load(f)['names']
print(label)

debug = True
device_id = "R9YT200S1PM"
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

ctx = StrategyContext()

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

	if debug:
		print("")
		print(datetime.datetime.now())
		#x = json.dumps(dict(objs))
		for k in objs.items():
			print(k)

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
