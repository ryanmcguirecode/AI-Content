import os 
from traceback import print_exc, format_exc

from ContentParameters import ContentParameters
from Music import Music
import generate_voiceover
import generate_text
import generate_image
import generate_video
from helper_functions import generate_content_name

class ContentGenerator:
    """ Generates all necesary content for video based on ContentParameters """
    
    def __init__(self, cp: ContentParameters, music: Music = None) -> str:
        self.content_parameters = cp
        self.prompt = cp.prompt
        self.music = music
        
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
        
        if self.content_parameters.text_content == "chat-gpt-generated":
            self.generate_chatgpt_text()
            self.get_paragraphs()
            self.paragraph_lengths = [len(par.split()) for par in self.paragraphs]
        else:
            print(self.content_parameters.text_content)
            raise Exception("Other text types not implemented yet.")
        
    def initialize_audio(self):
        """ Generate or retrive audio content of video """
        
        if "google-tts" in self.content_parameters.audio_content:
            self.voice = generate_voiceover.select_voice()
            self.generate_google_tts_voiceover()
        else:
            raise Exception("Other audio types not implemented yet.")
        
        if "music" in self.content_parameters.audio_content:
            assert self.music != None
    
    def initialize_visuals(self):
        """ Generate or retrive visual content of video """
        
        if self.content_parameters.visual_content == "dalle_paragraph_generated":
            self.generate_dalle_paragraph_images()
        else:
            raise Exception("Other visual types not implemented yet.")
    
    def generate_chatgpt_text(self) -> list[str]:
        """ Generate ChatGPT response based on prompt """
        
        print("Generating ChatGPT response based on prompt...")
        try:
            filepath = os.path.join(self.destination, "generated_text.txt")
            self.text = generate_text.generate(self.prompt, filepath)
        except:
            print("Error generating text:")
            print_exc()
            exit()
            
    def generate_google_tts_voiceover(self):
        """ Generate Google TTS voiceover and subtitle timestamps based on text """
        
        print("Generating Google TTS voiceover and timestamps...")
        try:
            voiceover_outpath = os.path.join(self.audio_path, "generated_voiceover.wav")
            timestamps_outpath = os.path.join(self.audio_path, "timestamps.json")
            generate_voiceover.generate(self.text, voiceover_outpath, timestamps_outpath, self.voice)
        except:
            print("Error generating voiceovers:")
            print_exc()
            exit()
            
    def generate_dalle_paragraph_images(self):
        """ Generate DALL-E images for each paragraph """
        
        print("Generating images for each paragraph...")
        try:
            self.images_directory = os.path.join(self.visuals_path, "images")
            os.mkdir(self.images_directory)
            for i, paragraph in enumerate(self.paragraphs):
                filepath = os.path.join(self.images_directory, "generated_image_" + str(i) + ".jpg")
                generate_image.generate(paragraph, filepath)
        except:
            print("Error generating DALL-E image")
            print_exc()
            exit()
            
    def generate_video(self):
        """ Generate final video based on all content """
        
        print("Generating final video...")
        try:
            if self.content_parameters.content_identifier == "generated-image-slideshow":
                generate_video.generate(self, self.content_parameters)
            else:
                raise Exception("Other video types not implemented yet.")
        except:
            print("Error generating DALL-E image")
            print_exc()
            exit()
            
    def get_paragraphs(self):
        """ Get paragraphs based on text """
        self.paragraphs = [par.strip() for par in self.text.split("\n") if par]
