from abc import ABC, abstractmethod
import datetime
from .cmd_for_adb import tap_this
import time

class LoadingStrategy(ABC):
	def isReady(objs):
		return "loading" in objs or "last z icon" in objs

	def perform(self, objs):
		if "last z icon" in objs:
			print("last z icon")
			time.sleep(60 * 1)
			tap_this(objs, "last z icon")
			self.complete = False
		elif "loading" in objs:
			print("loading")
			self.complete = False
		elif "exit" in objs:
			tap_this(objs, "exit")
			self.complete = False
		else:
			self.complete = True

	def isComplete(self, objs):
		return 	self.complete

