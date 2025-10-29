from abc import ABC, abstractmethod
import datetime
from .cmd_for_adb import tap_this

class ExitStrategy(ABC):
	# this one should not be needed, something went wrong
	def isReady(objs):
		return "exit" in objs and len(objs)==1

	def perform(self, objs):
		print("exit")
		tap_this("exit")

	def isComplete(self, objs):
		return True

