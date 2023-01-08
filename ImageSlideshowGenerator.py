import os 
from traceback import print_exc
from moviepy.editor import CompositeAudioClip, CompositeVideoClip, concatenate_videoclips
from moviepy.video.fx.all import scroll

from ContentGenerator import ContentGenerator
from ContentParameters import ContentParameters
import generate_voiceover
import generate_text
import generate_image
from generate_video import generate_voiceover_audiofileclip, get_timestamps, \
    generate_music_audiofileclip, generate_image_imageclips, generate_subtitle_textclips, \
    resize_video, save_video

class ImageSlideshowGenerator(ContentGenerator):
    def __init__(self, cp: ContentParameters) -> str:
        super().__init__(cp)
    
    def initialize_text(self):
        """ Generate ChatGPT response based on prompt """
        
        print("Generating ChatGPT response based on prompt...")
        try:
            filepath = os.path.join(self.destination, "generated_text.txt")
            self.text = generate_text.generate(self.content_parameters.story_prompt.text, filepath)
        except:
            print("Error generating text:")
            print_exc()
            exit()
            
        self.get_paragraphs()
        self.paragraph_lengths = [len(par.split()) for par in self.paragraphs]
        
    def initialize_audio(self):
        """ Generate Google TTS voiceover and timestamps """
        
        self.voice = generate_voiceover.select_voice()
        print("Generating Google TTS voiceover and timestamps...")
        try:
            voiceover_outpath = os.path.join(self.audio_path, "generated_voiceover.wav")
            timestamps_outpath = os.path.join(self.audio_path, "timestamps.json")
            generate_voiceover.generate(self.text, voiceover_outpath, timestamps_outpath, self.voice)
        except:
            print("Error generating voiceovers:")
            print_exc()
            exit()
    
    def initialize_visuals(self):
        """ Generate and save DALL-E images for each paragraph """

        print("Generating DALL-E images for each paragraph...")
        try:
            self.images_directory = os.path.join(self.visuals_path, "images")
            os.mkdir(self.images_directory)
            for i, paragraph in enumerate(self.paragraphs):
                filepath = os.path.join(self.images_directory, "generated_image_" + str(i) + ".jpg")
                image_prompt = self.content_parameters.story_prompt.generate_image_prompt(
                    paragraph, self.content_parameters.art_style
                )
                # image_prompt = self.content_parameters.story_prompt.generate_image_prompt(
                #     "", self.content_parameters.art_style
                # )
                generate_image.generate(image_prompt, filepath)
        except:
            print("Error generating DALL-E image")
            print_exc()
            exit()
            
    def generate_video(self):
        """ Generate and save final video based on all content """
        
        print("Generating final video...")
        
        self.voiceover = generate_voiceover_audiofileclip(self, self.content_parameters)
        self.timestamps = get_timestamps(self, self.content_parameters)
        
        self.content_parameters.music.music_duration = self.voiceover.duration
        music_audio = generate_music_audiofileclip(self, self.content_parameters)
        full_audio = CompositeAudioClip([self.voiceover, music_audio])
        
        image_clips = generate_image_imageclips(self, self.content_parameters)
        image_clips = [scroll(clip, w=608, h=1080, x_speed=((1080 - 608) / clip.duration)) for clip in image_clips]
        text_clips = generate_subtitle_textclips(self, self.content_parameters)

        full_image_video = concatenate_videoclips(image_clips)
        full_image_video = resize_video(full_image_video)
        full_text_clips = concatenate_videoclips(text_clips).set_pos(("center", 1320))
        
        self.final_video = CompositeVideoClip([full_image_video, full_text_clips]).set_audio(full_audio)
        video_outpath = os.path.join(self.destination, "final_video.mp4")
        save_video(self.final_video, video_outpath)
        
        print("Final video saved to " + video_outpath)