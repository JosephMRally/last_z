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

def tap(device_id, x, y):
    cmd = f"adb -s {device_id} shell input tap {x} {y}"
    print(cmd)
    subprocess.run(cmd, shell=True)

def swipe(device_id, direction):
    cmd = f"adb -s {device_id} shell input touchscreen swipe 300 1000 300 500"
    subprocess.run(cmd, shell=True)
# swipe("R9YT200S1PM", "up")

def kill(device_id):
    cmd = f"adb -s {device_id} shell am force-stop com.readygo.barrel.gp"
    subprocess.run(cmd, shell=True)
# kill()

def find_directories_os(path):
    directories = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            directories.append(item)
    return directories

def find_most_recent_model_directory():
    d = find_directories_os("./runs/detect/")
    d = [int(x[5:]) for x in d if len(x)>5 and x.startswith("train")]
    return f"./runs/detect/train{max(d)}"


