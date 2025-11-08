import datetime
import random
import time

from .cmd_for_adb import tap_this as common_tap_this
from .cmd_for_adb import swipe_direction as common_swipe_direction
from .cmd_for_adb import kill as common_kill

from .buildStrategy import BuildStrategy
from .completeStrategy import CompleteStrategy
from .exitStrategy import ExitStrategy
from .helpOthersStrategy import HelpOthersStrategy
from .loadingStrategy import LoadingStrategy
from .lookAroundCityStrategy import LookAroundCityStrategy
from collections import deque
from functools import partial
import pygame

class StrategyContext:

    def __init__(self):
        self.strategy = None
        self.last_action_timestamp = datetime.datetime.now()
        self.prior = deque(maxlen=1000)

    def pick_strategy(self, objs):
        cv = "_current_view"
        label_builder = "label - builder"
        upgrade = "upgrade"
        complete_rss = "complete - rss"
        rss_chest = "rss chest"
        build_icon_can = "build icon - can"
        attack = "attack"
        label_idle_rewards = "idle rewards"
        collect = "collect"
        free_gas = "free gas"
        join = "join"
        complete_build = "complete - build"
        congratulations = "congratulations"
        collect = "collect"
        medic = "medic"
        military = "military"

        x = lambda key: key in objs
        l = lambda: len([x for x in objs if not x.startswith("_")])
        def find_last_occurance(predicate):
            q = self.prior
            q = list(q)
            q = q[::-1]
            for item in q:
                if predicate(item):
                    return item
            return None
        def find_last_occurance_within_seconds(predicate, seconds):
            x = find_last_occurance(predicate)
            if x == None:
                return None
            y = (x["_timestamp"] + datetime.timedelta(seconds=seconds)) > datetime.datetime.now()
            if y:
                return x
            else:
                return None
        def tap_this(obj_dict_entry):
            objs["_action"] = obj_dict_entry
            common_tap_this(objs, obj_dict_entry)
        def swipe_direction(direction):
            objs["_action"] = direction
            common_swipe_direction(objs, direction)
        def kill(objs):
            device_id = objs["_settings.device_id"]
            objs["_action"] = "kill"
            common_kill(objs)

        self.prior.append(objs)

        # TODO: should this be moved to strategy?
        if self.last_action_timestamp + datetime.timedelta(minutes=60*10) < datetime.datetime.now():
            # reset state, something went wrong
            print("reset", str(datetime.datetime.now()))
            self.last_action_timestamp = datetime.datetime.now()
            kill(objs)
            self.strategy = None
            return

        # determine which view is being shown
        objs[cv] = []
        c = objs[cv]
        objs["_action"] = None

        if x("world"):
            c.append("headquarters")
        if x(label_idle_rewards):
            c.append(label_idle_rewards)
        if x("congratulations"):
            c.append("acknowledge")
        if x(label_builder):
            c.append("builder")
        if x("label - requirements"):
            c.append("requirements")
        if x("loading") or x("last z icon"):
            c.append("loading")
        if x("train") and x("back") and x("finish now"):
            c.append("military")
        if x("exit") and len(c)==0: # unknown view
            c.append("exit")
        if x("back") and len(c)==0: # unknown view
            c.append("back")

        # strategy
        if x(attack):
            tap_this(attack)
            pygame.mixer.music.load("alarm_sound.mp3") 
            pygame.mixer.music.play(loops=0)   
            return
        if "headquarters" in c:
            if x(complete_rss):
                b = lambda item: item["_action"]==complete_rss
                a = find_last_occurance_within_seconds(b, 60*60*.5)
                if not a:
                    objs["_action"] = complete_rss
                    tap_this(complete_rss)
                    return
            if x(rss_chest):
                b = lambda item: item["_action"]==rss_chest
                a = find_last_occurance_within_seconds(b, 60*60*4)
                if not a:
                    tap_this(rss_chest)
                    return
            if x(complete_build):
                tap_this(complete_build)
                return
            if x(build_icon_can) and not x("build icon - cannot"):
                b = lambda item: item["_action"]==build_icon_can
                a = find_last_occurance_within_seconds(b, 60*10)
                if not a:
                    tap_this(build_icon_can)
                    return
            if x(upgrade):
                b = lambda item: item["_action"] in [build_icon_can, "build", "upgrade"]
                a = find_last_occurance_within_seconds(b, 60)
                if a and len(a)>0:
                    tap_this(upgrade)
                    return
            if x(military):
                b = lambda item: item["_action"] == military
                a = find_last_occurance_within_seconds(b, 60*10)
                if not a:
                    tap_this(military)
                    return
            if x("help others"):
                b = lambda item: item["_action"] == "help others"
                a = find_last_occurance_within_seconds(b, 60*1)
                if not a:
                    tap_this("help others")
                    return
            if x(free_gas):
                tap_this(free_gas)
                return
            if x(medic):
                tap_this(medic)
                return
            if x(join):
                tap_this(join)
                return
        if label_idle_rewards in c:
            if x(collect):
                tap_this(collect)
                return
        if "acknowledge" in c:
            if x(collect):
                tap_this(collect)
                return
            if x(congratulations):
                tap_this(congratulations)
                return
        if "builder" in c:
            if x("finish now"):
                tap_this("finish now")
                return
            if x("build"):
                tap_this("build")
                return
            if x("exit"):
                tap_this("exit")
                return
        if "requirements" in c and x(upgrade):
            if x(upgrade):
                tap_this(upgrade)
                return
        if "loading" in c:
            if x("last z icon"):
                time.sleep(60*10)
                tap_this("last z icon")
            elif x("loading"):
                pass
        if "military" in c:
            b = lambda item: item["_action"] == military
            m = find_last_occurance_within_seconds(b, 10)
            b = lambda item: item["_action"] == "train"
            t = find_last_occurance_within_seconds(b, 10)
            if (m and len(m)>0) and not t and x("train"):
                tap_this("train")
            elif x("back"):
                tap_this("back")
        if "exit" in c:
            tap_this("exit")
            return
        if "back" in c:
            tap_this("back")
            return
        if len(c)==0 and x("hero"):
            b = lambda item: item["_action"] in ['left', 'right', 'up', 'down']
            a = find_last_occurance_within_seconds(b, 60*2)
            if not a:
                rnd = random.choice(range(0, 4))
                if rnd == 0:
                    swipe_direction("left")
                elif rnd == 1:
                    swipe_direction("up")
                elif rnd == 2:
                    swipe_direction("right")
                elif rnd == 3:
                    swipe_direction("down")
                return

