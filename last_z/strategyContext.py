from abc import ABC, abstractmethod
import datetime
import time
from .loadingStrategy import LoadingStrategy
from .completeStrategy import CompleteStrategy
from .exitStrategy import ExitStrategy
from .helpOthersStrategy import HelpOthersStrategy
from .buildStrategy import BuildStrategy
from .lookAroundCityStrategy import LookAroundCityStrategy
from .cmd_for_adb import *

class StrategyContext:

	def __init__(self):
		self.strategy = None
		self.last_action_timestamp = datetime.datetime.now()

	def pick_strategy(self, objs):
		# TODO: should this be moved to strategy?
		if self.last_action_timestamp+datetime.timedelta(minutes = 10) < datetime.datetime.now():
			# reset state, something went wrong
			print("reset", str(datetime.datetime.now()))
			self.last_action_timestamp = datetime.datetime.now()
			kill(objs["device_id"])
			self.strategy = None
			return

		if self.strategy == None:
			# TODO: make this dynamic
			if LoadingStrategy.isReady(objs):
				self.strategy = LoadingStrategy()
			elif CompleteStrategy.isReady(objs):
				self.strategy = CompleteStrategy()
			elif ExitStrategy.isReady(objs):
				self.strategy = ExitStrategy()
			elif HelpOthersStrategy.isReady(objs):
				self.strategy = HelpOthersStrategy()
			#elif BoomerStrategy.isReady(objs):
			#	self.strategy = BoomerStrategy()
			elif BuildStrategy.isReady(objs):
				self.strategy = BuildStrategy()
			#elif MilitaryStrategy.isReady(objs):
			#	self.strategy = MilitaryStrategy()	
			elif LookAroundCityStrategy.isReady(objs):
				self.strategy = LookAroundCityStrategy()

		if self.strategy != None:	
			print(f"strategy: {self.strategy}")
			self.strategy.perform(objs)
			if self.strategy.isComplete(objs):
				self.strategy = None
				self.last_action_timestamp = datetime.datetime.now()
