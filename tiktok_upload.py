import pyautogui as p
from time import sleep

from auto_user_parameters import *
from auto_user_functions import *
from helper_functions import command_fn


def get_f_coords(text):
    command_fn(["command"], ["f"])
    p.typewrite(text)
    sleep(random_time(2.5, 1))
    
    im = p.screenshot()
    w, h = p.size()
    for x in range(w * 2):
        for y in range(h * 2):
            if im.getpixel((x, y)) == FIND_COLOR:
                return (x // 2, y // 2)
    return (-1, -1)

def is_logged_out():
    im = p.screenshot()
    x, y = TT_LOG_IN_BUTTON
    if im.getpixel((x * 2, y * 2)) == TT_LOG_IN_BUTTON_COLOR:
        return True
    return False

def login(username):
    x, y = TT_LOG_IN_BUTTON
    move_and_click(x, y, random_time(.4, .5))
    sleep(random_time(2, 5))
    
    x, y = TT_CONTINUE_WITH_GOOGLE
    move_and_click(x, y, random_time(.4, .5))
    sleep(random_time(6, 4))
    
    x, y = get_f_coords(username)
    if (x, y) == (-1, -1):
        raise Exception("Not logged in to user " + username)
    move_and_click(x, y, random_time(.4, 1))
    sleep(random_time(12, 6))
    
def is_fullscreen():
    im = p.screenshot()
    for i in range(len(CHROME_FULLSCREEN_TEST)):
        x, y = CHROME_FULLSCREEN_TEST[i]
        if not im.getpixel((x * 2, y * 2)) == CHROME_FULLSCREEN_TEST_COLORS[i]:
            return False
    return True

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
    
def launch_chrome():
    command_fn(["command"], ["space"])
    sleep(1)
    p.typewrite('chrome')
    sleep(2)
    p.hotkey('enter')
    sleep(8)

def open_tiktok():
    """ Opens tiktok upload website """
    
    command_fn(["command"], ["l", "a"])
    p.press("backspace")
    p.typewrite('https://www.tiktok.com/')
    p.press("enter")
    sleep(random_time(5, 2))
    
    if not is_fullscreen():
        command_fn(["command", "ctrl"], ["f"])

def auto_upload(filepath, caption):
    """ From tiktok.com/upload uploads video at 'filepath', 
        with caption 'caption' """
    
    # Click upload
    x, y = TT_UPLOAD_BUTTON
    move_and_click(x, y, random_time(.4, .5))
    sleep(random_time(8, 4))
    
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

def log_out():
    x, y = TT_PROFILE_ICON
    move(x, y, random_time(.2, .4))
    sleep(random_time(.1, .2))
    x, y = TT_LOG_OUT_BUTTON
    move_and_click(x, y, random_time(.2, .4))

def upload(username, filepath, caption):
    launch_chrome()
    sleep(random_time(4, 2))
    open_tiktok()
    sleep(random_time(2, 1))
    if is_logged_out():
        login(username)
        sleep(random_time(10, 5))
    sleep(random_time(1, 3))
    auto_upload(filepath, caption)


# while True:
#     print(p.position())
#     sleep(3)