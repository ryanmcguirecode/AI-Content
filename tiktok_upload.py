def upload():
    
    # Click upload
    # p.moveTo(1052, 272, random() + .4)
    # p.click()
    # time.sleep(random() + 7)
    
    # Click select file
    p.moveTo(330, 673, random() + .4)
    p.click()
    time.sleep(1)
    
    # Type file path and select
    p.typewrite("\\")
    time.sleep(3)
    filename = '/Users/ryanmcguire/Desktop/AI_Content/generated_content/monkey_army_12222022_1846/final_video.mp4'
    for dir in filename.split("/"):
        p.typewrite(dir + "/")
        time.sleep(.2)
    time.sleep(random() + 3)
    p.press('enter')
    time.sleep(random() + 3)
    p.press("enter")
    
    # Wait for upload
    time.sleep(32 + random() * 6)
    
    # Click caption
    p.moveTo(809 + randint(-20, 20), 472, random() + .4)
    p.click()
    time.sleep(random() + 2)
    
    # Clear preset caption
    for _ in range(15):
        p.press("backspace")
        time.sleep(.1)
        
    # Type new caption
    message = "When monkeys take over the world #tiktok #fyp #monkeys"
    for word in message.split(" "):
        if "#" == word[0]:
            p.typewrite(word)
            time.sleep(2)
            p.press("enter")
            time.sleep(.5)
        else:
            p.typewrite(word + " ")
            time.sleep(.5)
    p.press("backspace")
    time.sleep(random() + 5)
    
    # Scroll down
    p.scroll(-15)
    time.sleep(.4 + random())
    
    # Click post
    p.moveTo(780 + randint(-10, 10), 454, random() + .4)
    p.click()
    time.sleep(15)