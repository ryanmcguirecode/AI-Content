from prompt import StoryPrompt
from Music import Music
from Video import Video

class ContentParameters:
    """ Stores all parameters for content generation """
    
    def __init__(self, name: str, story_prompt: StoryPrompt =None, 
                 music: Music =None, video: Video =None, art_style: str =None,
                 end_time: float =0, image_gen_type: str = None, 
                 image_prompt: str ="random design"):
        
        self.name = name
        self.story_prompt = story_prompt
        self.music = music
        self.video = video
        self.art_style = art_style
        self.end_time = end_time
        self.image_gen_type = image_gen_type
        self.image_prompt = image_prompt