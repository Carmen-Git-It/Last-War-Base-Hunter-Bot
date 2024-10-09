import time
import csv

import pyautogui as pg

APP_DRAWER = (1905, 1023)
CLOSE_APP = (1842, 198)
OPEN_APP = (1779, 215)

KIM_POS = (1805, 170)

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
CLOSE_LIST = (1846, 135)
# TODO:
ACCEPT = (1742, 264)
ACCEPT_OFFSET = (1742, 237)
DENY = (1803, 260)

def close_app():
    pg.mouseDown(APP_DRAWER)
    pg.mouseUp(APP_DRAWER)

    time.sleep(4)

    pg.mouseDown(CLOSE_APP)
    pg.mouseUp(CLOSE_APP)

    time.sleep(4)

def open_app():
    pg.mouseDown(OPEN_APP)
    pg.mouseUp(OPEN_APP)

    time.sleep(40)

    pg.mouseDown(KIM_POS)
    pg.mouseUp(KIM_POS)

    time.sleep(4)

def go_to_titles():
    # Avatar
    pg.mouseDown(AVATAR_POS)
    pg.mouseUp(AVATAR_POS)

    time.sleep(1)

    # Server
    pg.mouseDown(SERVER_POS)
    pg.mouseUp(SERVER_POS)

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

    #TODO: Intelligently detect high demand

    if high_demand:
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

    pg.mouseDown(ACCEPT)
    pg.mouseUp(ACCEPT)
    time.sleep(1)

    pg.mouseDown(CLOSE_LIST)
    pg.mouseUp(CLOSE_LIST)
    time.sleep(1)

    pg.mouseDown(CLOSE_LIST)
    pg.mouseUp(CLOSE_LIST)
    time.sleep(1)

def accept_loop():
    # print("loop")

    # Strategy
    pg.mouseDown(STRATEGY)
    pg.mouseUp(STRATEGY)
    time.sleep(1)

    accept_top_applicant(False)

    # Security
    pg.mouseDown(SECURITY)
    pg.mouseUp(SECURITY)
    time.sleep(1)

    accept_top_applicant(False)

    high_demand = True

    # Development
    pg.mouseDown(DEVELOPMENT)
    pg.mouseUp(DEVELOPMENT)
    time.sleep(1)

    accept_top_applicant(True)

    high_demand = True

    # SCIENCE
    pg.mouseDown(SCIENCE)
    pg.mouseUp(SCIENCE)
    time.sleep(1)

    accept_top_applicant(True)

    high_demand = False

    # INTERIOR
    pg.mouseDown(INTERIOR)
    pg.mouseUp(INTERIOR)
    time.sleep(1)

    accept_top_applicant(False)

pg.FAILSAFE = False
blacklist = []

use_blacklist = False

if use_blacklist:
    with open('blacklist.txt', newline='') as csvfile:
        bl_reader = csv.reader(csvfile, delimiter=',')
        print("Reading blacklist file...")
        for row in bl_reader:
            blacklist.append(row)
            print(', '.join(row))

# TODO: integrate blacklist

time.sleep(10)

pg.mouseDown(1613, 910)
pg.mouseUp(1613, 910)

time.sleep(10)

start_time = time.time()

while True:
    if time.time() - start_time > 3600:
        close_app()
        open_app()
        start_time = time.time()
    else:
        accept_loop()
        time.sleep(5)
