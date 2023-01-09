import pyautogui as p
from time import sleep
from random import random

from auto_user_parameters import *
from auto_user_functions import *

# def login():
#     # Click login
#     p.moveTo(1175, 133, duration=random() + .4)
#     p.click()
#     sleep(random() * 3)

#     # Click login with google
#     p.moveTo(707, 502, duration=random() + .4)
#     p.click()
#     sleep(random() * 3)

#     # Click text field
#     p.moveTo(707, 502, duration=random() + .4)
#     p.click()
#     sleep(random() * 3)

#     # Type username
#     p.typewrite("story.forge.1")
#     sleep(random() * 3)

#     # Click next
#     p.moveTo(887, 719, duration=random() + .4)
#     p.click()
#     sleep(random() * 3)

#     # Click text field
#     p.moveTo(707, 502, duration=random() + .4)
#     p.click()
#     sleep(random() * 3)

#     # Type password
#     p.typewrite("zyxsiw-bapFo0-xignyc")
#     sleep(random() * 3)

#     # Click next
#     p.moveTo(887, 750, duration=random() + .4)
#     p.click()
#     sleep(random() + 10)

def select_file(filepath):
    """ Selects file at 'filepath' in file dialog using keyboard """
    
    p.typewrite("\\")
    sleep(3)
    for dir in filepath.split("/"):
        p.typewrite(dir + "/")
        sleep(random_time(1.5, 1))
    p.press('enter')
    sleep(random_time(3, 1))
    p.press("enter")
    
def type_caption(caption):
    """ Adds caption 'caption' and adds hashtags during video upload """
    
    for word in caption.split(" "):
        if "#" == word[0]:
            p.typewrite(word)
            sleep(random_time(2, .2))
            p.press("enter")
            sleep(random_time(.5, .1))
        else:
            p.typewrite(word + " ")
            sleep(random_time(.5, .1))
    p.press("backspace")
    
def launch_chrome(go_fullscreen=False):
    p.keyDown("command")
    p.press("space")
    sleep(1.5)
    p.keyUp("command")
    sleep(1)
    p.typewrite('chrome')
    sleep(2)
    p.hotkey('enter')
    sleep(8)

    if go_fullscreen:
        p.keyDown("command")
        p.keyDown("ctrl")
        p.press("f")
        sleep(1)
        p.keyUp("command")
        p.keyUp("ctrl")

def open_tiktok():
    """ Opens tiktok upload website """
    
    p.keyDown("command")
    sleep(.2)
    p.press("t")
    sleep(.2)
    p.keyUp("command")
    p.typewrite('https://www.tiktok.com/upload')
    p.press("enter")
    sleep(5)
    sleep(1)

def upload(filepath, caption):
    """ From tiktok.com/upload uploads video at 'filepath', 
        with caption 'caption' """
    
    # Click select file
    x, y = TT_SELECT_FILE_BUTTON
    move_and_click(x, y, random_time(.4, .5))
    sleep(random_time(1, 1))
    
    # Type file path and select
    select_file(filepath)

    # Wait for upload
    sleep(random_time(45, 10))
    
    # Click caption
    x, y = TT_CAPTION_BOX
    move_and_click(x, y, random_time(.4, .5))
    sleep(random_time(1, 2))
    
    # Clear preset caption
    for _ in range(15):
        p.press("backspace")
        sleep(random_time(.02, .02))
        
    # Type new caption
    type_caption(caption)
    sleep(random_time(3, 2))
    
    # Scroll down
    p.scroll(TT_SCROLL_TO_UPLOAD)
    sleep(random_time(.2, .2))
    
    # Click post
    x, y = TT_POST_BUTTON
    # move(x, y, random_time(.2, .2))
    move_and_click(x, y, random_time(.2, .2))
    
    # Wait for upload
    sleep(25)

# while True:
#     print(p.position())
#     sleep(5)