from abc import ABC, abstractmethod
import datetime
from .cmd_for_adb import tap_this

class HelpOthersStrategy(ABC):
	help_others_counter = 0

	def isReady(objs):
		return "help others" in objs

	def perform(self, objs):
		print("help others")
		tap_this(objs, "help others")
		HelpOthersStrategy.help_others_counter += 1
		print(f"help others {HelpOthersStrategy.help_others_counter} times")

	def isComplete(self, objs):
		return True

