import os
import subprocess
import datetime

def get_screenshot(device_id):
    n = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path_and_filename = f"screenshots/screenshot_{n}.png"
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
    subprocess.run(cmd, shell=True)

def swipe(device_id, direction):
    cmd = f"adb -s {device_id} shell input touchscreen swipe 300 1000 300 500"
    subprocess.run(cmd, shell=True)
# swipe("R9YT200S1PM", "up")
