import os
import csv
from constants import CONTENT_TYPE_PARAMETERS as CTP
from prompt import StoryPrompt

class ContentParameters:
    """ Stores all parameters for content generation """
    
    def __init__(self, name: str, story_prompt: StoryPrompt =None, music: str =None, art_style: str = None):
        
        self.name = name
        self.story_prompt = story_prompt
        self.music = music
        self.art_style = art_style
        # TODO: TEMPORARY
        self.bottom_video_path = "/Users/ryanmcguire/Desktop/AI_Content/content_resources/minecraft_parkour.mp4"