from abc import ABC, abstractmethod
import datetime
from .cmd_for_adb import *

class CompleteStrategy(ABC):
	complete_count = 0
	next_allowed_complete_timestamp = datetime.datetime.now()

	def isReady(objs):
		# collect at least once every 1 hours
		if CompleteStrategy.next_allowed_complete_timestamp + datetime.timedelta(hours = .25) < datetime.datetime.now():
			CompleteStrategy.next_allowed_complete_timestamp = datetime.datetime.now()
			return False

		# congrats page
		if "congratulations" in objs:
			return True

		if "complete - rss" in objs and "world" in objs and CompleteStrategy.complete_count < 10:
			return True
		if "complete - rss" in objs and 'build icon - can' in objs:
			return True

		if "complete - build" in objs:
			return True

		if "rss chest" in objs:
			return True

		return False

	def __init__(self):
		self.completed = False

	def perform(self, objs):
		if "complete - rss" in objs:
			print(f"complete - rss: {CompleteStrategy.complete_count}")
			tap_this(objs, "complete - rss")
		elif "complete - build" in objs:
			print(f"complete - build: {CompleteStrategy.complete_count}")
			tap_this(objs, "complete - build")
		elif "congratulations" in objs:
			print(f"congratulations: {CompleteStrategy.complete_count}")
			tap_this(objs, "congratulations")
		elif "rss chest" in objs:
			print(f"rss chest: {CompleteStrategy.complete_count}")
			tap_this(objs, "rss chest")
		elif "collect" in objs and "idle rewards" in objs:
			print(f"collect: {CompleteStrategy.complete_count}")
			tap_this(objs, "collect")
		elif "hero" in objs and "world" in objs:
			self.completed = True


		CompleteStrategy.complete_count += 1

	def isComplete(self, objs):
		return self.completed

	def reset():
		CompleteStrategy.next_allowed_complete_timestamp = datetime.datetime.now()

