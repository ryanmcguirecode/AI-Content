import pyautogui as p
from time import sleep
from random import random

def move(x, y, duration=.3):
    p.moveTo(x, y, duration=duration)
    
    
def move_and_click(x, y, duration=.3):
    move(x, y, duration=duration)
    p.click()
    
def random_time(min_time, random_multiplier):
    return min_time + random() * random_multiplier