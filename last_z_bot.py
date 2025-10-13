import datetime
import time
from collections import defaultdict

import cv2

import cmd_for_adb as common
from ultralytics import YOLO

data_loc = "datasets/last_z"
yaml_loc = f"{data_loc}/data.yaml"

save_dir = "/Users/large/Documents/code/python/ultralytics/runs/detect/train2"
model_loc = f"{save_dir}/weights/best.pt"

# load model
model = YOLO(model_loc)

# show all devices
print(common.get_device_list())

debug = True
device_id = "R9YT200S1PM"
help_others_counter = 0
boomer_counter = 0
state_of_action = None
last_action_timestamp = datetime.datetime.now()


def middle_of_xyxy(xyxy):
    return (xyxy[0] + (xyxy[2] - xyxy[0]) / 2, xyxy[1] + (xyxy[3] - xyxy[1]) / 2)


def translate_to_display(x, y):
    return (1200 / 1024 * x, 1920 / 1024 * y)


device_id = "R9YT200S1PM"
has_gas = True


def tap_this(obj_dict_entry):
    a = objs[obj_dict_entry]
    a = a[0][0]
    x, y = middle_of_xyxy(a)
    x, y = translate_to_display(x, y)
    common.tap(device_id, x, y)


while True:
    # first take a screenshot
    path_and_filename = common.get_screenshot(device_id, "screenshots/screenshot.png")

    # resize
    img = cv2.imread(path_and_filename)
    img_2 = cv2.resize(img, (1024, 1024))  # YOLO default image size is 640
    cv2.imwrite(path_and_filename, img_2)

    # Perform object detection on an image using the model
    results = model.predict(path_and_filename, show=debug, show_boxes=True, verbose=False, imgsz=1024, conf=0.50)

    # extract the results
    objs = defaultdict(list)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy.tolist()
            c = int(box.cls)
            c_name = model.names[c]
            objs[c_name].append(b)
    objs = dict(objs)

    # print(objs)
    # r = redis.Redis()
    # r.set("vision", json.dumps(dict(objs)))

    if debug:
        print("")
        print(datetime.datetime.now(), state_of_action)
        # x = json.dumps(dict(objs))
        for k in objs.items():
            print(k)

    if has_gas and last_action_timestamp + datetime.timedelta(minutes=3) < datetime.datetime.now():
        # reset state if something went wrong
        print("reset", str(datetime.datetime.now()))
        state_of_action = None
        last_action_timestamp = datetime.datetime.now()
        common.kill(device_id)

    elif state_of_action is None and "help others" in objs:
        print("help others")
        tap_this("help others")
        help_others_counter += 1
        last_action_timestamp = datetime.datetime.now()
        print("help others", help_others_counter, str(datetime.datetime.now()))

    elif "last z icon" in objs:
        tap_this("last z icon")
    elif "loading" in objs and state_of_action != "loading":
        print("loading")
        last_action_timestamp = datetime.datetime.now()
        state_of_action = "loading"
    elif state_of_action == "loading" and "exit" in objs:
        tap_this("exit")
    elif state_of_action == "loading" and "world" in objs:
        tap_this("world")
        state_of_action = None

    elif (
        has_gas
        and state_of_action is None
        and "headquarters" in objs
        and "hero 1 sleeping" in objs
        and "magnifying glass" in objs
    ):
        print("boomer starting")
        last_action_timestamp = datetime.datetime.now()
        tap_this("magnifying glass")
        state_of_action = "boomer starting"
    elif state_of_action is not None and state_of_action.startswith("boomer"):
        if "boomer selected" in objs:
            print("boomer selected: ", end="")
            tap_this("boomer selected")
            state_of_action = "boomer selected"
        elif "search" in objs:
            print("boomer search: ", end="")
            tap_this("search")
            state_of_action = "boomer search"
        elif "team up" in objs:
            print("boomer team up: ", end="")
            tap_this("team up")
            state_of_action = "boomer team up"
        elif "march" in objs:
            print("boomer march: ", end="")
            tap_this("march")
            state_of_action = "boomer marching"
            boomer_counter += 1
        elif "no gas" in objs:
            print("no gas")
            has_gas = False
            state_of_action = None
        elif "hero 1 sleeping" in objs:
            print("boomer completed")
            last_action_timestamp = datetime.datetime.now()
            state_of_action = None
    elif not has_gas:
        tap_this("headquarters")

    # time.sleep(2 + random.randrange(0, 100)/10)
    time.sleep(4)
