from prompt import StoryPrompt
from Music import Music
from Video import Video

class ContentParameters:
    """ Stores all parameters for content generation """
    
    def __init__(self, name: str, story_prompt: StoryPrompt =None, 
                 music: Music =None, video: Video =None, art_style: str =None):
        
        self.name = name
        self.story_prompt = story_prompt
        self.music = music
        self.video = video
        self.art_style = art_style