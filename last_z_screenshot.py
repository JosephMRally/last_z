import cv2

from cmd_for_adb import *

data_loc = "datasets/last_z"
yaml_loc = f"{data_loc}/data.yaml"

# show all devices
print(get_device_list())

device_id = "R9YT200S1PM"
help_others_counter = 0

# first take a screenshot
path_and_filename = get_screenshot(device_id, "screenshots_train/screenshot_{n}.png")

# resize
img = cv2.imread(path_and_filename)
img_2 = cv2.resize(img, (1024, 1024))  # YOLO default image size is 640
cv2.imwrite(path_and_filename, img_2)
