from abc import ABC, abstractmethod
import datetime
from .cmd_for_adb import tap_this

class ExitStrategy(ABC):
	# this one should not be needed, something went wrong
	def isReady(objs):
		x = {k:v for k,v in objs.items() if not k.startswith("_")}
		return "exit" in x and len(x)==1

	def perform(self, objs):
		print("exit")
		tap_this(objs, "exit")

	def isComplete(self, objs):
		return True

