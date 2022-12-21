import os 
from datetime import datetime
from traceback import print_exc, format_exc
import generate_voiceover
import generate_text
import generate_image

class ContentGenerator:
    def __init__(self, topic: str) -> str:
        self.topic = topic
        self.destination = os.path.join("generated_content", "fable_" + topic + "_" +  datetime.now().strftime("%m%d%Y_%H%M"))
        os.mkdir(self.destination)

        self.paragraphs = self.generate_story()
        self.generate_visuals()
        # self.music = self.generate_music()
    
    def generate_story(self) -> list[str]:
        print("Generating fable about " + self.topic + "...")
        try:
            filepath = os.path.join(self.destination, "generated_text.txt")
            text = generate_text.generate('write a short fable about ' + self.topic, filepath)
            return [par.strip() for par in text.split("\n") if par]
        except:
            print("Error generating text:")
            print_exc()
            exit()

    def generate_visuals(self):
        print("Generating images for each paragraph...")
        try:
            self.images_directory = os.path.join(self.destination, "images")
            os.mkdir(self.images_directory)
            for i, paragraph in enumerate(self.paragraphs):
                filepath = os.path.join(self.images_directory, "generated_image_" + str(i) + ".jpg")
                generate_image.generate(paragraph, filepath)
        except:
            print("Error generating images:")
            print_exc()
            exit()
    
    def generate_audio(self):
        print("Generating voiceovers for each paragraph...")
        try:
            self.voiceovers_directory = os.path.join(self.destination, "voiceovers")
            os.mkdir(self.voiceovers_directory)
            for i, paragraph in enumerate(self.paragraphs):
                filepath = os.path.join(self.voiceovers_directory, "generated_voiceover_" + str(i) + ".wav")
                generate_voiceover.generate(paragraph, filepath)
        except:
            print("Error generating voiceovers:")
            print_exc()
            exit()

    # def get_music(self) -> str:
    #     return os.path.listdir("music")[0]
    
