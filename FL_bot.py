import time
import csv

import PIL.Image
import cv2
import pyautogui as pg
import pytesseract as pt
import numpy as np
from fuzzywuzzy import fuzz, process

APP_DRAWER = (1905, 1023)
CLOSE_APP = (1815, 225)
OPEN_APP = (1779, 215)

KIM_POS = (1800, 162)
AD_POS = (1819, 107)

AVATAR_POS = (1366,77)
SERVER_POS = (1733, 722)
FL_POS = (1433, 508)
STRATEGY = (1597, 508)
SECURITY = (1772, 508)
DEVELOPMENT = (1433, 721)
SCIENCE = (1597, 721)
INTERIOR = (1772, 721)
LIST = (1810, 885)
APPLY = (1602, 891)
NAME_PLATE_TOPLEFT = (1458, 231)
NAME_PLATE_TOPRIGHT = (1768, 231)
NAME_PLATE_BOTLEFT = (1458, 269)
NAME_PLATE_BOT_RIGHT = (1762, 269)
CLOSE_LIST = (1840, 135)
# TODO:
ACCEPT = (1742, 264)
ACCEPT_OFFSET = (1742, 237)
DENY = (1803, 260)

# LOST OR GAINED TITLES
ALT_FL = (1430, 594)
ALT_STRATEGY = (1603, 594)
ALT_SECURITY = (1765, 594)
ALT_DEVELOPMENT = (1425, 792)
ALT_SCIENCE = (1602, 792)
ALT_INTERIOR = (1771, 792)

ALLIANCE_TOPLEFT = (1456,239)
ALLIANCE_TOPRIGHT = (1528, 239)
ALLIANCE_BOTLEFT = (1456, 262)
ALLIANCE_BOTRIGHT = (1528, 262)

MILITARY_COMMANDER = (1506, 216)
ADMINISTRATIVE_COMMANDER = (1691, 217)

def close_app():
    pg.mouseDown(APP_DRAWER)
    pg.mouseUp(APP_DRAWER)

    time.sleep(8)

    pg.mouseDown(CLOSE_APP)
    pg.mouseUp(CLOSE_APP)

    time.sleep(8)

def open_app():
    pg.mouseDown(OPEN_APP)
    pg.mouseUp(OPEN_APP)

    time.sleep(60)

    pg.mouseDown(AD_POS)
    pg.mouseUp(AD_POS)

    time.sleep(8)

    pg.mouseDown(KIM_POS)
    pg.mouseUp(KIM_POS)

    time.sleep(8)

    pg.mouseDown(KIM_POS)
    pg.mouseUp(KIM_POS)

    time.sleep(8)

    pg.mouseDown(KIM_POS)
    pg.mouseUp(KIM_POS)

    time.sleep(8)

    pg.mouseDown(AD_POS)
    pg.mouseUp(AD_POS)

    time.sleep(8)

def go_to_titles():
    # Avatar
    pg.mouseDown(AVATAR_POS)
    pg.mouseUp(AVATAR_POS)

    time.sleep(3)

    # Server
    pg.mouseDown(SERVER_POS)
    pg.mouseUp(SERVER_POS)

    time.sleep(3)

    pg.moveTo(1610, 710)
    pg.dragRel(0, -300, duration=1)

    time.sleep(2)

def apply_fl():
    # FL
    pg.mouseDown(FL_POS)
    pg.mouseUp(FL_POS)

    # Apply
    pg.mouseDown(APPLY)
    pg.mouseUp(APPLY)

def accept_top_applicant(high_demand):
    print("Accept top apps")
    pg.mouseDown(LIST)
    pg.mouseUp(LIST)
    time.sleep(1)

    if high_demand == True:

        pg.moveTo(1588, 246)
        pg.dragRel(0, 500, duration=0.5)

        pg.moveTo(1588, 246)
        pg.dragRel(0, 500, duration=0.5)

        pg.moveTo(1588, 246)
        pg.dragRel(0, 500, duration=0.5)

        pg.moveTo(1588, 246)
        pg.dragRel(0, 500, duration=0.5)

        pg.moveTo(1588, 246)
        pg.dragRel(0, 500, duration=0.5)

        pg.moveTo(1588, 246)
        pg.dragRel(0, 500, duration=0.5)

        pg.moveTo(1588, 246)
        pg.dragRel(0, 500, duration=0.5)

        time.sleep(0.5)

    # Get image of their alliance tag
    image = np.asarray(pg.screenshot(region=(1456, 239, 85, 23)))
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_gray = cv2.copyMakeBorder(image_gray, 40, 40, 60, 60, cv2.BORDER_REPLICATE)
    image = cv2.threshold(image_gray, 55, 255, cv2.THRESH_BINARY)[1]
    image = cv2.resize(image, (0, 0), fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)

    # Comment this out in prod
    # image = PIL.Image.fromarray(image)
    # image.show()

    result = pt.image_to_string(image, config='--psm 6')
    result = result.replace("\x0c", "").replace("\\", "").replace("/", "")
    result = result.split("\n")
    print(result)


    if result[0] and result[0] == "[Nova]":
        print("Detected Nova, reject.")
    #else:

    #TODO: in prod, reject or accept in if/else

    pg.mouseDown(ACCEPT)
    pg.mouseUp(ACCEPT)
    time.sleep(1)

    pg.mouseDown(CLOSE_LIST)
    pg.mouseUp(CLOSE_LIST)
    time.sleep(1)

    pg.mouseDown(CLOSE_LIST)
    pg.mouseUp(CLOSE_LIST)
    time.sleep(1)

def accept_loop(extra_titles):
    # print("loop")

    strat = STRATEGY
    sec = SECURITY
    dev = DEVELOPMENT
    sci = SCIENCE
    inter = INTERIOR

    if extra_titles:
        strat = ALT_STRATEGY
        sec = ALT_SECURITY
        dev = ALT_DEVELOPMENT
        sci = ALT_SCIENCE
        inter = ALT_INTERIOR

    # Strategy
    pg.mouseDown(strat)
    pg.mouseUp(strat)
    time.sleep(1)

    accept_top_applicant(True)

    # Security
    pg.mouseDown(sec)
    pg.mouseUp(sec)
    time.sleep(1)

    accept_top_applicant(True)

    # Development
    pg.mouseDown(dev)
    pg.mouseUp(dev)
    time.sleep(1)

    accept_top_applicant(True)

    # SCIENCE
    pg.mouseDown(sci)
    pg.mouseUp(sci)
    time.sleep(1)

    accept_top_applicant(True)

    # INTERIOR
    pg.mouseDown(inter)
    pg.mouseUp(inter)
    time.sleep(1)

    accept_top_applicant(True)

pg.FAILSAFE = False
blacklist = []

use_blacklist = False

# TODO: REMOVE TEST

if use_blacklist:
    with open('blacklist.txt', newline='') as csvfile:
        bl_reader = csv.reader(csvfile, delimiter=',')
        print("Reading blacklist file...")
        for row in bl_reader:
            blacklist.append(row)
            print(', '.join(row))

time.sleep(10)

start_time = time.time()

while True:
    if time.time() - start_time > 3600:
        close_app()
        open_app()
        go_to_titles()
        start_time = time.time()
    else:
        # image = pg.screenshot(allScreens=True)
        # image.show()
        #TODO: CHANGE THIS EVERY SATURDAY
        accept_loop(extra_titles=True)
        time.sleep(5)

