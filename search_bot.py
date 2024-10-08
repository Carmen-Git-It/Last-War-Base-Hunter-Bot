import cv2
import pyautogui
import pyautogui as pg
import pytesseract as pt
import numpy as np
from PIL import Image
from enum import Enum
from fuzzywuzzy import fuzz, process
import time
from matplotlib import pyplot as plt

class Dir(Enum):
    UP = 1
    DOWN = 2

# calculate mean squared error (difference) between images
def mse(img1, img2):
    img1 = image_to_gray(img1)
    img2 = image_to_gray(img2)
    h, w = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff ** 2)
    mse_res = err / (float(h * w))
    return mse_res

def move_right():
    pg.moveTo(1685, 500)
    pg.dragRel(-200, 0, duration=0.2)

def move_left():
    pg.moveTo(1400, 500)
    pg.dragRel(200, 0, duration=0.2)

def move_up():
    pg.moveTo(1600, 300)
    pg.dragRel(0, 300, duration=0.2)

def move_down():
    pg.moveTo(1600, 700)
    pg.dragRel(0, -300, duration=0.20)

def screenshot():
    return np.asarray(pg.screenshot(region=(1385, 250, 425, 600)))

def image_to_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def position_bottom_left():
    # pyautogui.moveTo(1500, 600)
    # pyautogui.dragRel(0,100, duration=1)
    # for i in range(10):
    #     pyautogui.keyDown('-')
    #     pyautogui.keyUp('-')
    image = screenshot()
    done = False
    while not done:
        done = True
        move_down()
        move_left()
        old_image = image
        image = screenshot()
        if not at_bottom(image, old_image):
            done = False
        if not at_left(image, old_image):
            done = False

def set_zoom():
    pyautogui.moveTo(1500, 600)
    pyautogui.dragRel(0,100, duration=1)
    for i in range(20):
        pyautogui.keyDown('=')
        pyautogui.keyUp('=')
    pyautogui.keyDown('-')
    pyautogui.keyUp('-')

def match_name(name, names):
    names = [x for x in names if isinstance(x, str)]
    value = process.extractOne(name, names, scorer=fuzz.ratio)
    if value is not None:
        return value[1] > 90

# Starts in bottom left corner
def search(name, x_set, y_set, direction_set):
    image = screenshot()

    if not x_set and not y_set and not direction_set:
        x = 0
        y = 0

        position_bottom_left()

        set_zoom()

        move_right()

        x += 2

        direction = Dir.UP

    else:
        x = x_set
        y = y_set
        direction = direction_set

    found = False

    # start grid search bottom left, go to top, then right a bit, then down, then right again, etc.
    #TODO: implement grid search loops, done when hit right then bottom/top? Use a flag
    while not found:
        print(x, y)
        old_image = image
        names = []

        if direction == Dir.UP:
            move_up()
            y += 5
            image = screenshot()

        elif direction == Dir.DOWN:
            move_down()
            y -= 4.8
            image = screenshot()

        names = get_image_text(image)

        if match_name(name, names):
            return [x,y]

        #if direction == Dir.UP and at_top(image, old_image):
        if direction == Dir.UP and y >= 999:
            y = 999
            direction = Dir.DOWN
            old_image = image
            move_right()
            x += 2
            image = screenshot()
            names = get_image_text(image)
            if match_name(name, names):
                return [x,y]
            #end case
            #if at_right(image, old_image):
            if x >= 999:
                return None

        #elif direction == Dir.DOWN and at_bottom(image, old_image):
        elif direction == Dir.DOWN and y <= 0:
            y = 0
            direction = Dir.UP
            old_image = image
            move_right()
            x += 2
            image = screenshot()
            names = get_image_text(image)
            if match_name(name, names):
                return [x,y]
            #end case
            #if at_right(image, old_image):
            if x >= 999:
                return None

def at_bottom(image, old_image):
    h = image.shape[0] - int (image.shape[0] / 4)
    w = image.shape[1]
    old_bottom_image = old_image[h: image.shape[0]]
    new_bottom_image = image[h: image.shape[0]]

    return at_edge(new_bottom_image, old_bottom_image)

def at_left(image, old_image):
    h = image.shape[0]
    w = int (image.shape[1] / 5)
    old_left_image = old_image[0:h, 0:w]
    new_left_image = image[0:h, 0:w]

    return at_edge(new_left_image, old_left_image)

def at_right(image, old_image):
    h = image.shape[0]
    w = image.shape[1] - int (image.shape[1] / 5)
    old_right_image = old_image[0:h, w:image.shape[1]]
    new_right_image = image[0:h, w:image.shape[1]]

    return at_edge(new_right_image, old_right_image)

# Check if at top of screen
def at_top(image, old_image):
    #format [y:y+h, x:x+h]
    h = int (image.shape[0] / 4)
    w = image.shape[1]
    old_top_image = old_image[0: h]
    new_top_image = image[0: h]

    return at_edge(new_top_image, old_top_image)

# Check if at edge with difference
def at_edge(image, old_image):
    error = mse(image, old_image)
    return error == 0

def get_image_text(image):
    # Filter out shields
    lower = np.array([0, 10, 10])
    upper = np.array([255, 255, 255])

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    hsv = cv2.resize(hsv, (0, 0), fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

    mask = cv2.inRange(hsv, lower, upper)

    mask = cv2.bitwise_not(mask)

    mask = cv2.GaussianBlur(mask, (3, 3), 5)

    image = image_to_gray(image)

    # make big
    image = cv2.resize(image, (0,0), fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    image = cv2.GaussianBlur(image, (1, 1), 1)
    #sharpen
    #get white text black background

    image = cv2.bitwise_and(image, image, mask=mask)

    image = cv2.threshold(image, 170, 255, cv2.THRESH_BINARY)[1]

    # # Define structuring element
    # kernel = np.ones((1, 1), np.uint8)

    # #perform erosion
    # image = cv2.erode(image, kernel, iterations=1)
    #
    # # Perform dilation
    # image = cv2.dilate(image, kernel, iterations=1)

    image = cv2.bitwise_not(image, image)

    result = pt.image_to_string(image, config='--psm 6')
    result = result.replace("\x0c", "").replace("\\", "").replace("/", "")
    result = result.split("\n")

    return result

# Made redundant
# def mask_filter_only(image):
#     lower = np.array([0, 5, 5])
#     upper = np.array([255, 255, 255])
#
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#
#     hsv = cv2.resize(hsv, (0, 0), fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
#
#     mask = cv2.inRange(hsv, lower, upper)
#
#     mask = cv2.bitwise_not(mask)
#
#     mask = cv2.GaussianBlur(mask, (3, 3), 5)
#
#     result = pt.image_to_string(mask, config='--psm 6')

search_result = search("[Axu]TARGET", 582, 133, Dir.DOWN)
print(search_result)
