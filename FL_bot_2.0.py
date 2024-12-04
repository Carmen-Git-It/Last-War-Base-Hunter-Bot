import os
import subprocess
import time
from datetime import datetime
from random import random

import PIL.Image
import cv2
import pytesseract as pt
import numpy as np
from PIL import Image

# POSITIONS (for 1280x720)
OPEN_GAME = (572, 257)

PROFILE = (53, 63)
SERVER = (514, 880)
APPLY = (358, 1095)

FL_TITLE = (145, 722)
STRAT_TITLE = (355, 722)
SEC_TITLE = (570, 722)
DEV_TITLE = (145, 980)
SCI_TITLE = (355, 980)
INT_TITLE = (570, 980)

# FL_TITLE_2 = (145, 722)
# STRAT_TITLE_2 = (355, 722)
# SEC_TITLE_2 = (570, 722)
# DEV_TITLE_2 = (145, 780)
# SCI_TITLE_2 = (355, 780)
# INT_TITLE_2  = (570, 780)

LIST = (621, 1080)
CLOSE = (664, 131)

LIST_SCROLL_START = (352, 428)
LIST_SCROLL_END = (352, 950)

ACCEPT = (540, 294)
DENY = (614, 294)

# DONT_SHOW_AGAIN = (380, 1050)
# CONFIRM_DENY = (721, 1215)

CLOSE_ADS = (623, 95)

# Other globals

connectionPort = 5555
deviceSerial = ""

template = Image.open("instruction_template.png")
template = np.asarray(template)
template = cv2.cvtColor(template, cv2.COLOR_RGB2BGR)

# Utils
def connect():
    global deviceSerial

    os.system(f"adb connect localhost:{connectionPort}")
    time.sleep(1)

    devices_string = os.popen("adb devices").read()
    devices_strings = devices_string.split("\n")
    print(devices_strings)
    if len(devices_string) > 1:
        deviceSerial = devices_strings[1].split("\t")[0]
        print("Connected to device: " + deviceSerial)
        if len(deviceSerial) == 0:
            deviceSerial = None
    else:
        deviceSerial = None
        print("Error: No devices connected")

def tap(x, y):
    x += random() * 10
    y += random() * 10
    os.system(f"adb -s {deviceSerial} shell input tap {x} {y}")
    time.sleep(2.5 + random())

def quick_tap(x, y):
    x += random() * 10
    y += random() * 10
    os.system(f"adb -s {deviceSerial} shell input tap {x} {y}")
    time.sleep(0.5 + random())

def long_tap(x, y, d):
    x += random() * 10
    y += random() * 10
    os.system(f"adb -s {deviceSerial} shell input swipe {x} {y} {x} {y} {d}")
    time.sleep(1 + random())

def swipe(x, y, xx, yy, d):
    x += random() * 10
    y += random() * 10
    os.system(f"adb -s {deviceSerial} shell input swipe {x} {y} {xx} {yy} {d}")
    time.sleep(0.5 + random())

# Logic

def close_game():
    # Go to home
    os.system(f"adb -s {deviceSerial} shell input keyevent KEYCODE_APP_SWITCH")
    time.sleep(2)
    swipe(140, 670, 712, 670, 300)
    time.sleep(2)
    os.system(f"adb -s {deviceSerial} shell input keyevent KEYCODE_HOME")
    time.sleep(2)

def restart_app():
    close_game()
    open_game()
    close_ads()
    open_title_screen()

def open_game():
    tap(OPEN_GAME[0], OPEN_GAME[1])
    time.sleep(30)

def close_ads():
    tap(CLOSE_ADS[0], CLOSE_ADS[1])
    tap(CLOSE_ADS[0], CLOSE_ADS[1])
    tap(CLOSE_ADS[0], CLOSE_ADS[1])

def open_title_screen():
    tap(PROFILE[0], PROFILE[1])
    tap(SERVER[0], SERVER[1])

def apply_to_fl():
    tap(FL_TITLE[0], FL_TITLE[1])
    tap(APPLY[0], APPLY[1])

def open_applicant_list():
    tap(LIST[0], LIST[1])

def close_list():
    tap(CLOSE[0], CLOSE[1])

def scroll_up_list():
    swipe(LIST_SCROLL_START[0], LIST_SCROLL_START[1], LIST_SCROLL_END[0], LIST_SCROLL_END[1], 500)
    swipe(LIST_SCROLL_START[0], LIST_SCROLL_START[1], LIST_SCROLL_END[0], LIST_SCROLL_END[1], 500)
    swipe(LIST_SCROLL_START[0], LIST_SCROLL_START[1], LIST_SCROLL_END[0], LIST_SCROLL_END[1], 500)
    swipe(LIST_SCROLL_START[0], LIST_SCROLL_START[1], LIST_SCROLL_END[0], LIST_SCROLL_END[1], 500)
    swipe(LIST_SCROLL_START[0], LIST_SCROLL_START[1], LIST_SCROLL_END[0], LIST_SCROLL_END[1], 500)
    swipe(LIST_SCROLL_START[0], LIST_SCROLL_START[1], LIST_SCROLL_END[0], LIST_SCROLL_END[1], 500)
    swipe(LIST_SCROLL_START[0], LIST_SCROLL_START[1], LIST_SCROLL_END[0], LIST_SCROLL_END[1], 500)
    swipe(LIST_SCROLL_START[0], LIST_SCROLL_START[1], LIST_SCROLL_END[0], LIST_SCROLL_END[1], 500)
    swipe(LIST_SCROLL_START[0], LIST_SCROLL_START[1], LIST_SCROLL_END[0], LIST_SCROLL_END[1], 500)
    time.sleep(1)

def accept_top_applicant():
    scroll_up_list()
    quick_tap(ACCEPT[0], ACCEPT[1])
    quick_tap(ACCEPT[0], ACCEPT[1])
    quick_tap(ACCEPT[0], ACCEPT[1])
    quick_tap(ACCEPT[0], ACCEPT[1])
    quick_tap(ACCEPT[0], ACCEPT[1])

def on_instruction_screen():
    global template
    os.system(f"adb -s {deviceSerial} exec-out screencap -p > test.png")
    time.sleep(0.2)
    image = Image.open("test.png")
    image = image.crop((238, 211, 480, 276))
    image = np.asarray(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # image = image[238: 480, 211: 276]
    difference = cv2.subtract(template, image)
    b, g, r = cv2.split(difference)
    if cv2.countNonZero(b) < 30 and cv2.countNonZero(g) < 30 and cv2.countNonZero(r) < 30:
        print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S" + ": " +"On instruction screen"))
        return True
    return False

def loop(title_y_offset):
    if on_instruction_screen():
        close_list()

    # Secretary of Strategy
    tap(STRAT_TITLE[0], STRAT_TITLE[1] + title_y_offset)
    open_applicant_list()
    accept_top_applicant()
    if on_instruction_screen():
        close_list()
    else:
        close_list()
        close_list()

    if on_instruction_screen():
        close_list()

    # Secretary of Security
    tap(SEC_TITLE[0], SEC_TITLE[1] + title_y_offset)
    open_applicant_list()
    accept_top_applicant()
    if on_instruction_screen():
        close_list()
    else:
        close_list()
        close_list()

    if on_instruction_screen():
        close_list()

    # Secretary of Development
    tap(DEV_TITLE[0], DEV_TITLE[1] + title_y_offset)
    open_applicant_list()
    accept_top_applicant()
    if on_instruction_screen():
        close_list()
    else:
        close_list()
        close_list()

    if on_instruction_screen():
        close_list()

    # Secretary of Science
    tap(SCI_TITLE[0], SCI_TITLE[1] + title_y_offset)
    open_applicant_list()
    accept_top_applicant()
    if on_instruction_screen():
        close_list()
    else:
        close_list()
        close_list()

    if on_instruction_screen():
        close_list()

    # Secretary of Interior
    tap(INT_TITLE[0], INT_TITLE[1] + title_y_offset)
    open_applicant_list()
    accept_top_applicant()
    close_list()
    close_list()

connect()

# IMPORTANT: Set before starting
extra_titles = False

last_time = time.time()

while True:
    loop(0 if extra_titles else -200)
    if time.time() - last_time > 3600:
        restart_app()