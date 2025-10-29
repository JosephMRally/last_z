import os
import subprocess
import datetime


def get_screenshot(device_id, path_and_filename = "screenshots/screenshot_{n}.png"):
    n = datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S_%f")
    path_and_filename = path_and_filename.format(**{"n":n})
    cmd = [f"adb -s {device_id} exec-out screencap -p > {path_and_filename}"]
    process = subprocess.Popen(cmd, shell=True)
    process.wait()
    return path_and_filename
# get_screenshot("R9YT200S1PM")

def get_device_list():
    cmd = "adb devices"
    output = subprocess.check_output(cmd, shell=True).decode('utf-8')
    devices = []
    for line in output.splitlines():
        if '\tdevice' in line:
            device_id = line.split('\t')[0]
            devices.append(device_id)
    return devices
# print(get_device_list())

# declaration of common methods
middle_of_xyxy = lambda xyxy : (xyxy[0]+(xyxy[2]-xyxy[0])/2, xyxy[1]+(xyxy[3]-xyxy[1])/2)
translate_to_display = lambda x,y: (1200/1024*x, 1920/1024*y)
def tap_this(objs, obj_dict_entry):
    a = objs[obj_dict_entry]
    a = a[0][0]
    x,y = middle_of_xyxy(a)
    x,y = translate_to_display(x,y)
    tap(objs["device_id"], x,y)

def tap(device_id, x, y):
    cmd = f"adb -s {device_id} shell input tap {x} {y}"
    print(cmd)
    subprocess.run(cmd, shell=True)

def swipe_direction(objs, direction):
    if direction == "left":
        xyxy = [[800, 500, 300, 500]]
    elif direction == "right":
        xyxy = [[300, 500, 800, 500]]
    elif direction == "down":
        xyxy = [[500, 300, 500, 800]]
    elif direction == "up":
        xyxy = [[500, 800, 500, 300]]
    swipe(objs, xyxy)

def swipe(objs, xyxy):
    device_id = objs['device_id']
    xyxy = xyxy[0]
    x1,y1,x2,y2 = xyxy
    cmd = f"adb -s {device_id} shell input touchscreen swipe {x1} {y1} {x2} {y2}"
    subprocess.run(cmd, shell=True)

def kill(device_id):
    cmd = f"adb -s {device_id} shell am force-stop com.readygo.barrel.gp"
    subprocess.run(cmd, shell=True)

def find_directories_os(path):
    directories = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            directories.append(item)
    return directories

def find_most_recent_model_directory():
    d = find_directories_os("./runs/detect/")
    d = [x.replace("train","") for x in d]
    if len(d)==0:
        return None
    d = [int(x) for x in d if x!=""]
    d = max(d) if len(d)>0 else ""
    print(d)
    return f"./runs/detect/train{d}"


