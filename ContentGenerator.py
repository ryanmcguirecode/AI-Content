import os 

from ContentParameters import ContentParameters
from helper_functions import generate_content_name
from constants import WORDS_PER_PICTURE as WPP

class ContentGenerator:
    """ Generates all necesary content for video based on ContentParameters
        Paent class for all content generators """
    
    def __init__(self, cp: ContentParameters) -> str:
    
        self.content_parameters = cp
        
        self.destination = generate_content_name(cp.name)
        os.mkdir(self.destination)
        self.audio_path = os.path.join(self.destination, "audio_content")
        os.mkdir(self.audio_path)
        self.visuals_path = os.path.join(self.destination, "visual_content")
        os.mkdir(self.visuals_path)

        self.initialize_text()
        self.initialize_audio()
        self.initialize_visuals()
        self.generate_video()
    
    def initialize_text(self):
        """ Generate or retrive text content of video """
        raise NotImplementedError("Abstract method in ConentGenerator interface")
        
    def initialize_audio(self):
        """ Generate or retrieve audio content of video """
        raise NotImplementedError("Abstract method in ConentGenerator interface")
    
    def initialize_visuals(self):
        """ Generate or retrive visual content of video """
        raise NotImplementedError("Abstract method in ConentGenerator interface")
            
    def generate_video(self):
        """ Generate final video based on all content """
        raise NotImplementedError("Abstract method in ConentGenerator interface")
            
    def get_paragraphs(self):
        """ Get paragraphs based on text """
        
        self.paragraphs = [[]]
        for word in self.text.split():
            if len(self.paragraphs[-1]) >= WPP:
                self.paragraphs.append([])
            self.paragraphs[-1].append(word)
        
        self.paragraphs = [" ".join(par).strip() for par in self.paragraphs]
