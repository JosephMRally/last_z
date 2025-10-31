import datetime
from abc import ABC

from .cmd_for_adb import tap_this


class BoomerStrategy(ABC):
    boomer_count = 0
    next_allowed_boomer_timestamp = datetime.datetime.now()

    def isReady(objs):
        # reset boomers if we have done to many
        if BoomerStrategy.boomer_count == 10:
            BoomerStrategy.next_allowed_boomer_timestamp = datetime.datetime.now() + datetime.timedelta(minutes=1)
            return False

        return (
            BoomerStrategy.next_allowed_boomer_timestamp < datetime.datetime.now()
            and "headquarters" in objs
            and "hero 1 sleeping" in objs
            and "magnifying glass" in objs
        )

    def perform(self, objs):
        if "headquarters" in objs and "hero 1 sleeping" in objs and "magnifying glass" in objs:
            print("boomer starting")
            datetime.datetime.now()
            tap_this("magnifying glass")
        elif "boomer selected" in objs:
            print("boomer selected: ", end="")
            tap_this("boomer selected")
        elif "search" in objs:
            print("boomer search: ", end="")
            tap_this("search")
        elif "team up" in objs:
            print("boomer team up: ", end="")
            tap_this("team up")
        elif "march" in objs:
            print("boomer march: ", end="")
            tap_this("march")
            boomer_counter += 1
        elif "no gas" in objs:
            print("no gas")
            has_gas = False
        elif "hero 1 sleeping" in objs:
            print("boomer completed")
            datetime.datetime.now()
        elif not has_gas and "headquarters" not in objs:
            objs["corner"] = [[[0, 0, 0, 0]]]
            tap_this("corner")

    def isComplete(self, objs):
        return False
