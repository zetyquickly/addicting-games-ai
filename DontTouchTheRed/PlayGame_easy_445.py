#!/hdd/anaconda2/envs/games_ai/bin/python

# if "Xlib.error.DisplayConnectionError" use "xhost +" on linux

import shutil
import os
import keyboard
import mss
import cv2
import numpy
from time import time, sleep
import pyautogui
from random import randint
import math

pyautogui.PAUSE = 0.0

print("Press 's' to start")
print("Press 'q' to quit")
keyboard.wait('s')

try:
    shutil.rmtree("./screenshots")
except FileNotFoundError:
    pass
os.mkdir("./screenshots")

# setup mss and get the full size of your monitor
sct = mss.mss()
mon = sct.monitors[0]

frame_id = 0
# decide where is the region of interest
for idx in range(3,0,-1):
    roi = {
        "left": 0, 
        "top": int(mon["height"] * (idx * 0.2)), 
        "width": int(mon["width"] / 2), 
        "height": int(mon["height"] * 0.23)
    }

    green_button = cv2.imread('green_button.png')
    offset_x = int(green_button.shape[0] / 2)
    offset_y = int(green_button.shape[1] / 2)

    roi_crop = numpy.array(sct.grab(roi))[:,:,:3]
    result = cv2.matchTemplate(roi_crop, green_button, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    print(max_val, max_loc)

    button_center = (max_loc[0] + offset_y, max_loc[1] + offset_x)
    roi_crop = cv2.circle(roi_crop.astype(float), button_center, 20, (255, 0, 0), 2)
    cv2.imwrite(f"./screenshots/{frame_id:03}.jpg", roi_crop)

    abs_x_roi = roi["left"] + button_center[0]
    abs_y_roi = roi["top"] + button_center[1]
    pyautogui.click(x=abs_x_roi, y=abs_y_roi)
    frame_id += 1

second_roi = {
    "left": 0, 
    "top": int(mon["height"] * 0.2), 
    "width": int(mon["width"] / 2), 
    "height": int(mon["height"] * 0.06)
}

btn = cv2.imread('center.png')
offset_y = int(btn.shape[0])
offset_x = int(btn.shape[1] / 2)


thresh = 0.9
frame_list = []
btn_cnt = 1
while True:
    frame_id += 1
    second_roi_crop = numpy.array(sct.grab(second_roi))[:,:,:3]
    result = cv2.matchTemplate(second_roi_crop, btn, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    speed = math.floor(math.log(frame_id)**2.4)
    # print(frame_id, max_val, max_loc, speed)
    frame_list.append(max_loc[0])
    if max_val > thresh:
        button_center = (max_loc[0] + offset_x, max_loc[1] + offset_y)
        # second_roi_crop = cv2.circle(second_roi_crop.astype(float), button_center, 20, (255, 0, 0), 2)
        # cv2.imwrite(f"./screenshots/{frame_id:03}.jpg", second_roi_crop)

        abs_x_sec = second_roi["left"] + button_center[0]
        abs_y_sec = second_roi["top"] + button_center[1] + speed
        pyautogui.click(x=abs_x_sec, y=abs_y_sec)
        btn_cnt += 1

    if keyboard.is_pressed('q'):
        break

import numpy as np
np.save("arr.npy", np.array(frame_list))