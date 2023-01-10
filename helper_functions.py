import os
import pyautogui as p
from datetime import datetime
from time import sleep
from auto_user_functions import random_time

def generate_content_name(name: str) -> str:
    """ Generate unique name for content folder based on name and current time """
    
    return os.path.join(
        "generated_content", 
        name + "_" +  datetime.now().strftime("%m%d%Y_%H%M")
    )

def command_fn(hold_keys: list[str], press_keys: list[str]) -> None:
    """ Execute keyboard command functions """
    
    for key in hold_keys:
        p.keyDown(key)
        sleep(random_time(0, .3))
    sleep(random_time(.3, .3))
    for key in press_keys:
        p.press(key)
        sleep(random_time(0, .3))
    sleep(random_time(.3, .3))
    for key in hold_keys:
        p.keyUp(key)