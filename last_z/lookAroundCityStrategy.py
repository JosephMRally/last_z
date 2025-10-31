import random
from abc import ABC

from .cmd_for_adb import *


class LookAroundCityStrategy(ABC):
    def isReady(objs):
        return "world" in objs and "build icon - can" in objs

    def __init__(self):
        self.direction = random.choice(range(0, 4))

    def perform(self, objs):
        print(f"direction: {self.direction}")

        if self.direction == 0:
            swipe_direction(objs, "left")
        elif self.direction == 1:
            swipe_direction(objs, "up")
        elif self.direction == 2:
            swipe_direction(objs, "right")
        elif self.direction == 3:
            swipe_direction(objs, "down")

    def isComplete(self, objs):
        return True
