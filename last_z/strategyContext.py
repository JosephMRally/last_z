import datetime

from .buildStrategy import BuildStrategy
from .cmd_for_adb import *
from .completeStrategy import CompleteStrategy
from .exitStrategy import ExitStrategy
from .helpOthersStrategy import HelpOthersStrategy
from .loadingStrategy import LoadingStrategy
from .lookAroundCityStrategy import LookAroundCityStrategy


class StrategyContext:
    def __init__(self):
        self.strategy = None
        self.last_action_timestamp = datetime.datetime.now()

    def pick_strategy(self, objs):
        # TODO: should this be moved to strategy?
        if self.last_action_timestamp + datetime.timedelta(minutes=10) < datetime.datetime.now():
            # reset state, something went wrong
            print("reset", str(datetime.datetime.now()))
            self.last_action_timestamp = datetime.datetime.now()
            kill(objs["_settings.device_id"])
            self.strategy = None
            return



        if self.strategy is None:
        	if "__current_view"

            # TODO: make this dynamic
            if LoadingStrategy.isReady(objs):
                self.strategy = LoadingStrategy()
            elif CompleteStrategy.isReady(objs):
                self.strategy = CompleteStrategy()
            elif ExitStrategy.isReady(objs):
                self.strategy = ExitStrategy()
            elif HelpOthersStrategy.isReady(objs):
                self.strategy = HelpOthersStrategy()
            # elif BoomerStrategy.isReady(objs):
            # self.strategy = BoomerStrategy()
            elif BuildStrategy.isReady(objs):
                self.strategy = BuildStrategy()
            # elif MilitaryStrategy.isReady(objs):
            # self.strategy = MilitaryStrategy()
            elif LookAroundCityStrategy.isReady(objs):
                self.strategy = LookAroundCityStrategy()

        if self.strategy is not None:
            print(f"strategy: {self.strategy}")
            self.strategy.perform(objs)
            if self.strategy.isComplete(objs):
                self.strategy = None
                self.last_action_timestamp = datetime.datetime.now()
