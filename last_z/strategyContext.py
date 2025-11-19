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
        label_builder = "label - builder" # is this still used?
        upgrade = "upgrade"
        complete_rss = "complete - rss"
        rss_chest = "rss chest"
        build_icon_can = "build icon - can"
        under_attack = "under_attack"
        label_idle_rewards = "label - idle rewards"
        collect = "collect"
        free_gas = "free gas"
        join = "join"
        complete_build = "complete - build"
        congratulations = "congratulations"
        collect = "collect"
        medic = "medic"
        military = "military"
        ec_icon = "ec - icon"
        truck_icon = "truck - icon"
        radar = "radar background image"
        world = "world"
        complete_military = "complete - military"
        request_help = "help - request"
        help_others = "help others"
        ec_army_expansion = "event calendar - army expansion"
        ec_icon = "ec - icon"
        label_requirements = "label - requirements"
        headquarters = "headquarters"
        magnifying_glass = "magnifying glass"
        lab_icon = "lab icon"
        radar_icon = "radar - icon"
        exit = "exit"
        skull = "skull"
        vip_icon = "vip - icon"
        label_get_more = "label - get more"
        replenish_all = "replenish all"
        label_replenish_all = "label - replenish all"
        confirm = "confirm"
        radar_label = "radar - label"
        radar_help_alliance = "radar - help alliance"


        x = lambda key: key in objs
        l = lambda: len([x for x in objs if not x.startswith("_")])
        def occurances(predicate)->[]:
            q = self.prior
            q = list(q)
            q = q[::-1]
            results = []
            for item in q:
                if predicate(item):
                    results.append(item)
            return results
        def occurances_within_seconds(predicate, seconds)->[]:
            tc = lambda x: predicate(x) & ((x["_timestamp"] + datetime.timedelta(seconds=seconds)) > datetime.datetime.now())
            x = occurances(tc)
            return x
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

        # always reset after 10 hours
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

        if x(world):
            c.append(headquarters)
        if x(headquarters):
            c.append(world)
        if x(label_idle_rewards):
            c.append(label_idle_rewards)
        if x(congratulations):
            c.append("acknowledge")
        if x(label_builder):
            c.append(label_builder)
        if x(label_requirements):
            c.append(label_requirements)
        if x(label_get_more):
            c.append(label_get_more)
        if x(label_replenish_all):
            c.append(label_replenish_all)
        
        if x("loading") or x("last z icon"):
            c.append("loading")
        if x("military - warrior level"):
            c.append("military")
        if x("label - hospital"):
            c.append("hospital")
        if x("todays loot count"):
            c.append(truck)
        if x(ec_army_expansion):
            c.append(ec_army_expansion)
        if x(radar_label):
            c.append(radar_label)
        if x("boomer selected"): # TODO: this is incomplete
            c.append(magnifying_glass)
        if x("my truck"): # TODO: this needs to be better
            c.append("truck")
        if x("dice") and x("go"):
            c.append("truck - dice choose")
        if x("vip - claim"):
            c.append("vip")
        if x(exit) and len(c)==0: # unknown view
            c.append(exit)
        if x("back") and len(c)==0: # unknown view
            c.append("back")


        # strategy
        """
        if x(under_attack):
            if x("hero busy") and not x("return"):
                tap_this("hero busy")
            elif x("return"):
                tap_this("return")
            return
        """
        if headquarters in c:
            if x(complete_rss):
                b = lambda item: item["_action"]==complete_rss
                a = occurances_within_seconds(b, 60*60*1)
                if len(a)<5:
                    objs["_action"] = complete_rss
                    tap_this(complete_rss)
                    return
            if x(rss_chest):
                b = lambda item: item["_action"]==rss_chest
                a = occurances_within_seconds(b, 60*60*4)
                if len(a)==0:
                    tap_this(rss_chest)
                    return
            if x(complete_build):
                tap_this(complete_build)
                return
            if x(build_icon_can):
                b = lambda item: item["_action"] == build_icon_can
                a = occurances_within_seconds(b, 60*10)
                if len(a)==0:
                    tap_this(build_icon_can)
                    return
            if x(upgrade):
                b = lambda item: item["_action"] == upgrade
                a = occurances_within_seconds(b, 60)
                if len(a)==0:
                    tap_this(upgrade)
                    return
            if x(military):
                b = lambda item: item["_action"] == military
                a = occurances_within_seconds(b, 60*10)
                if len(a)==0:
                    tap_this(military)
                    return
            if x(complete_military):
                tap_this(complete_military)
                return                
            if x(help_others):
                b = lambda item: item["_action"] == help_others
                a = occurances_within_seconds(b, 60*1)
                if len(a)==0:
                    tap_this(help_others)
                    return
            if x(free_gas):
                tap_this(free_gas)
                return
            if x(medic):
                tap_this(medic)
                return
            """
            if x(radar_icon):
                tap_this(radar_icon)
                return
            """
            """
            if x(skull):
                tap_this(skull)
                return
            """
            """
            if x(ec_icon):
                b = lambda item: item["_action"] == ec_icon
                a = occurances_within_seconds(b, 60*60*1)
                if len(a)==0:
                    tap_this(ec_icon)
                    return
            """
            if x(join):
                tap_this(join)
                return
            if x(request_help):
                tap_this(request_help)
                return
            """
            if x(vip_icon):
                b = lambda item: item["_action"] == vip_icon
                a = occurances_within_seconds(b, 60*60*12)
                tap_this(vip_icon)
                return
            """
        if world in c:
            if x(magnifying_glass):
                b = lambda item: item["_action"] == magnifying_glass
                a = occurances_within_seconds(b, 60*1)
                if len(a)==0:
                    tap_this(magnifying_glass)
                    return
            if x("team up"):
                tap_this("team up")
                return
            if x("march"):
                tap_this("march")
                return
            """
            if x(radar_icon):
                tap_this(radar_icon)
                return
            """
        """
        if headquarters in c or world in c:
            b = lambda item: item["_action"] != None and item["_action"] not in ['left', 'right', 'up', 'down']
            a = occurances_within_seconds(b, 60*10)
            if len(a)==0:
                if headquarters in c:
                    tap_this(world)
                else:
                    tap_this(headquarters)
                return
        """
        if label_idle_rewards in c:
            if x(collect):
                tap_this(collect)
                return
            if x(exit):
                tap_this(exit)
                return
        if "acknowledge" in c:
            if x(collect):
                tap_this(collect)
                return
            if x(congratulations):
                tap_this(congratulations)
                return
        if label_builder in c:
            #if x("finish now"): # TODO: put back on next trained model
            #    tap_this("finish now")
            #    return
            if x("build"):
                tap_this("build")
                return
            if x(exit):
                tap_this(exit)
                return
        if label_requirements in c:
            b = lambda item: item["_action"] == upgrade
            a = occurances_within_seconds(b, 60*1)
            print(a)
            if len(a)<=1: # TODO: set this back to zero and change to upgrade button
                if x(upgrade):
                    tap_this(upgrade)
                    return
            elif x(exit):
                tap_this(exit)
                return
        if label_get_more in c:
            b = lambda item: item["_action"] == replenish_all
            a = occurances_within_seconds(b, 60*1)
            if len(a)==0:
                if x(replenish_all):
                    tap_this(replenish_all)
                    return
            elif x(exit):
                tap_this(exit)
        if label_replenish_all in c:
            b = lambda item: item["_action"] == confirm
            a = occurances_within_seconds(b, 60*1)
            if len(a)==0:
                if x(label_replenish_all):
                    tap_this(confirm)
                    return
        
        if "loading" in c:
            if x("last z icon"):
                time.sleep(60*10)
                tap_this("last z icon")
            elif x("loading"):
                pass
        if "military" in c:
            b = lambda item: item["_action"] == military
            m = occurances_within_seconds(b, 60)
            b = lambda item: item["_action"] == "train"
            t = occurances_within_seconds(b, 60)
            if (m and len(m)>0) and not t and x("train"):
                tap_this("train")
            elif x("back"):
                tap_this("back")
        if "hospital" in c:
            if x("heal"):
                tap_this("heal")
            elif x("back"):
                tap_this("back")
        """
        if ec_hero_initiative in c:
            if x(ec_hero_initiative):
                tap_this(ec_hero_initiative)
            elif x("back"):
                tap_this("back")
        """
        if exit in c:
            tap_this(exit)
            return
        if "back" in c:
            tap_this("back")
            return
        if len(c)==0 and "headquarters" in c:
            b = lambda item: item["_action"] in ['left', 'right', 'up', 'down']
            a = occurances_within_seconds(b, 60*1)
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

        if magnifying_glass in c:
            if x("boomer"):
                tap_this("boomer")
            elif x("boomer selected"):
                tap_this("search")

        if "truck" in c:
            b = lambda item: item["_action"] == "my truck"
            m = occurances_within_seconds(b, 60*60*1)
            b = lambda item: item["_action"] == "truck - add"
            n = occurances_within_seconds(b, 60*60*1)
            if x("my truck") and len(m)==0:
                tap_this("my truck")
                return
            elif x("truck - add") and len(n)<3:
                tap_this("truck - add")
                return
        if "truck - dice choose" in c:
            if x("dice") and not x("asdf"):
                tap_this("dice")
                return
            if x(confirm):
                tap_this(confirm)
                return
        if "vip" in c:
            if x("vip - claim"):
                tap_this("vip - claim")
                return
            elif x("back"):
                tap_this("back")
                return
        if radar_label in c:
            b = lambda item: item["_action"] == "radar - laurasadditional items"
            a = occurances_within_seconds(b, 60*60*1)
            if len(a)==0 and x("radar - laurasadditional items"):
                tap_this("radar - laurasadditional items")
                return
            b = lambda item: item["_action"] == radar_help_alliance
            a = occurances_within_seconds(b, 60*60*1)
            if len(a)==0 and x(radar_help_alliance):
                tap_this(radar_help_alliance)
                return

