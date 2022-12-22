import os 
from datetime import datetime
from traceback import print_exc, format_exc
import generate_voiceover
import generate_text
import generate_image

class ContentGenerator:
    def __init__(self, prompt: str, name: str) -> str:
        self.prompt = prompt
        self.destination = os.path.join("generated_content", name + "_" +  datetime.now().strftime("%m%d%Y_%H%M"))
        os.mkdir(self.destination)

        self.paragraphs = self.generate_text()
        self.paragraph_lengths = [len(par.split()) for par in self.paragraphs]
        self.generate_visuals()
        self.voice = generate_voiceover.select_voice()
        self.generate_audio()
    
    def generate_text(self) -> list[str]:
        print("Generating response based on prompt...")
        try:
            filepath = os.path.join(self.destination, "generated_text.txt")
            self.text = generate_text.generate(self.prompt, filepath)
            return [par.strip() for par in self.text.split("\n") if par]
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
        print("Generating voiceover and timestamps...")
        try:
            voiceover_outpath = os.path.join(self.destination, "generated_voiceover.wav")
            timestamps_outpath = os.path.join(self.destination, "timestamps.json")
            generate_voiceover.generate(self.text, voiceover_outpath, timestamps_outpath, self.voice)
        except:
            print("Error generating voiceovers:")
            print_exc()
            exit()

class ContentGeneratorTest:
    def __init__(self, prompt: str, name: str) -> str:
        self.prompt = prompt
        self.destination = "generated_content/fable_education_12222022_1147"
        # os.mkdir(self.destination)

        self.paragraphs = self.generate_text()
        self.paragraph_lengths = [len(par.split(" ")) for par in self.paragraphs]
        self.generate_visuals()
        self.voice = generate_voiceover.select_voice()
        self.generate_audio()
    
    def generate_text(self) -> list[str]:
        print("Generating response based on prompt...")
        try:
            filepath = os.path.join(self.destination, "generated_text.txt")
            with open(os.path.join(self.destination, "generated_text.txt"), "r") as f:
                self.text = f.read()
            return [par.strip() for par in self.text.split("\n") if par]
        except:
            print("Error generating text:")
            print_exc()
            exit()

    def generate_visuals(self):
        print("Generating images for each paragraph...")
        try:
            self.images_directory = os.path.join(self.destination, "images")
            # os.mkdir(self.images_directory)
            # for i, paragraph in enumerate(self.paragraphs):
            #     filepath = os.path.join(self.images_directory, "generated_image_" + str(i) + ".jpg")
            #     generate_image.generate(paragraph, filepath)
        except:
            print("Error generating images:")
            print_exc()
            exit()
    
    def generate_audio(self):
        print("Generating voiceover and timestamps...")
        try:
            voiceover_outpath = os.path.join(self.destination, "generated_voiceover.wav")
            timestamps_outpath = os.path.join(self.destination, "timestamps.json")
            # generate_voiceover.generate(self.text, voiceover_outpath, timestamps_outpath, self.voice)
        except:
            print("Error generating voiceovers:")
            print_exc()
            exit()