from abc import ABC, abstractmethod
import datetime
from .cmd_for_adb import tap_this
from .completeStrategy import CompleteStrategy

class BuildStrategy(ABC):
	build_counter = 0

	def isReady(objs):
		res = 'build icon - can' in objs and "ready to build" in objs
		if res:
			CompleteStrategy.reset() # TODO: mediator design pattern
		return res

	def __init__(self):
		self.strategy_start_time = datetime.datetime.now()
		self.state = ""

	def perform(self, objs):
		print("building")
		if self.strategy_start_time + datetime.timedelta(minutes=1) < datetime.datetime.now():
			print("ran out of time")
			if "exit" in objs:
				tap_this(objs, "exit")
			else:
				self.state = "complete"
		else:
			if 'build icon - can' in objs and "ready to build" in objs and "upgrade" not in objs:
				# adjust where to tap, it's not on the middle of the icon
				import random
				xyxy = random.sample(objs['ready to build'], 1)
				a = xyxy[0][0]
				xyxy = [a[0]+20, a[1]-20, a[2]+20, a[3]-20]
				objs['ready to build'] = [[xyxy]]
				print(objs['ready to build'])
				tap_this(objs, "ready to build")
				self.state = "building"
			if self.state == "building":
				if "upgrade" in objs:
					tap_this(objs, "upgrade")
				if "confirm" in objs:
					tap_this(objs, "confirm")
					self.state = "complete"
				elif "replenish all" in objs:
					tap_this(objs, "replenish all")

	def isComplete(self, objs):
		return hasattr(self, "state") and self.state == "complete"

