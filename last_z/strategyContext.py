import datetime
import random

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
            objs["_action"] = obj_dict_entry
            common_kill(objs)

        self.prior.append(objs)

        # TODO: should this be moved to strategy?
        if self.last_action_timestamp + datetime.timedelta(minutes=60) < datetime.datetime.now():
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
        if x("exit") and len(c)==0:
            c.append("exit")
        if x("back") and len(c)==0:
            c.append("back")

        # we don't know this view
        if len(c) == 0:
            return None

        # strategy
        if "headquarters" in c:
            if x(complete_rss):
                b = lambda item: item["_action"]==complete_rss
                a = find_last_occurance_within_seconds(b, 60*10)
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
            if x(build_icon_can) and not x("build icon - cannot"):
                b = lambda item: item["_action"]==build_icon_can
                a = find_last_occurance_within_seconds(b, 60)
                if not a:
                    tap_this(build_icon_can)
                    return
            if x("complete - build"):
                tap_this("complete - build")
                return
            if x(upgrade):
                b = lambda item: item["_action"] in [build_icon_can, "build", "upgrade"]
                a = find_last_occurance_within_seconds(b, 60)
                print(a)
                if a and len(a)>0:
                    tap_this(upgrade)
                    return
            if x(attack):
                tap_this(attack)
                return
            if x("free gas"):
                tap_this("free gas")
                return
            b = lambda item: item["_action"]=="look around"
            a = find_last_occurance_within_seconds(b, 60)
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
        if label_idle_rewards in c:
            if x(collect):
                tap_this(collect)
                return
        if "acknowledge" in c:
            if x("collect"):
                tap_this("collect")
                return
            if x("congratulations"):
                tap_this("congratulations")
                return
        if "builder" in c:
            if x("build"):
                tap_this("build")
                return
        if "requirements" in c and x(upgrade):
            if x(upgrade):
                tap_this(upgrade)
                return
        if "loading" in c:
            if x("last z icon"):
                tap_this("last z icon")
            elif x("loading"):
                pass
        if "exit" in c:
            tap_this("exit")
            return
        if "back" in c:
            tap_this("back")
            return




        """

        if self.strategy is None:
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

        """

    """

    elif "attack" in objs:
        print("under attack")
        pygame.mixer.music.load("alarm_sound.mp3") 
        pygame.mixer.music.play(loops=0)        
    elif "medic" in objs:
        print("medic")
        tap_this("medic")
    elif "exit" in objs and len(objs)==1:
        print("objs")
        tap_this("exit")    


    elif state_of_action == None and "complete" in objs:
        print("complete")
        tap_this("complete")
        last_action_timestamp = datetime.datetime.now()
    """

    """
    elif state_of_action == None and "ready to build" in objs:
        print("ready to build")
        tap_this("ready to build")
        last_action_timestamp = datetime.datetime.now()
    """

    """
    elif state_of_action == None and "wanted" in objs:
        print("wanted")
        tap_this("wanted")
        last_action_timestamp = datetime.datetime.now()
    """

    """
    elif state_of_action == None and "radar" in objs:
        print("radar")
        tap_this("radar")
        last_action_timestamp = datetime.datetime.now()
    """

    """
    elif state_of_action == None and "event calendar" in objs:
        print("event calendar")
        tap_this("event calendar")
        last_action_timestamp = datetime.datetime.now()
    """

