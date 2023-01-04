import os
import csv
from constants import CONTENT_TYPE_PARAMETERS as CTP
from prompt import StoryPrompt

class ContentParameters:
    """ Stores all parameters for content generation """
    
    def __init__(self, name: str, content_identifier: str, story_prompt: StoryPrompt =None, music: str =None, art_style: str = None):
        
        self.name = name
        self.content_identifier = content_identifier
        self.story_prompt = story_prompt
        self.music = music
        self.art_style = art_style
        # TEMPORARY
        self.bottom_video_path = "/Users/ryanmcguire/Desktop/AI_Content/content_resources/minecraft_parkour.mp4"

        with open(os.path.join("content_settings", "parameters.csv"), "r") as f:
            reader = csv.reader(f)
            content_identifier_index = CTP.index("content_identifier")
            rows = [row for row in reader if row[content_identifier_index] == content_identifier]
            if len(rows) != 1:
                raise Exception("Invalid content identifier")
            for i, parameter in enumerate(CTP):
                exec("self." + parameter + " = '" + rows[0][i] + "'")